"""
Stage 2 of the pipeline: splitting documents into chunks.

Milestone 3: `split_documents` now splits on paragraph breaks instead of a
fixed character window. Rationale in that function's docstring.
"""

import re
from dataclasses import dataclass

import config
from ingest import Document

TARGET_SIZE = 700   # stop packing paragraphs past this
HARD_MAX = 900      # blunt-cut anything still longer
MIN_SIZE = 120      # a fragment this short always joins the chunk before it


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split on paragraph breaks, packing up to TARGET_SIZE.

    A blank line is where the author signalled a thought ended, so that is the
    boundary; the character counts only decide when to stop packing (700) and
    when to cut inside an oversized paragraph (900). No overlap: cuts land on
    blank lines, so no sentence is severed and overlap would only duplicate
    text. Short paragraphs are absorbed into the chunk before them, which is
    what prevents the 2-character tail `fallback_split` leaves behind.
    """
    chunks: list[Chunk] = []
    for doc in documents:
        pieces: list[str] = []
        for para in re.split(r"\n\s*\n", doc.text):
            para = para.strip()
            if not para:
                continue
            limit = TARGET_SIZE if len(para) >= MIN_SIZE else HARD_MAX
            if pieces and len(pieces[-1]) + len(para) + 2 <= limit:
                pieces[-1] += "\n\n" + para
            else:
                pieces.append(para)
        cut = [p[i : i + HARD_MAX] for p in pieces for i in range(0, len(p), HARD_MAX)]
        for index, text in enumerate(cut):
            chunks.append(
                Chunk(
                    text=text,
                    source=doc.source,
                    index=index,
                    produced_by="chunker.py::split_documents",
                )
            )
    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))