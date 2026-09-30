"""
Scoring a run.

`run_eval.py` calls `judge(question, expects, answer, results)` once per run and
prints pass/fail from what comes back. "Correct" here means the thing you wrote
in `questions.py` as `expects` actually showed up in the answer.
"""

import re


def _normalize(text) -> str:
    """Lowercase and collapse runs of whitespace, so line wrapping can't fail a match."""
    return re.sub(r"\s+", " ", str(text or "")).strip().lower()


def judge(question, expects, answer, results) -> bool:
    """True when the answer contains what the question said to expect.

    question: the question that was asked (unused — kept for the eval's signature)
    expects:  the word or phrase a correct answer should contain
    answer:   what the model wrote
    results:  the retrieved chunks behind that answer

    An empty `expects` returns False: with nothing to look for there is no
    evidence the run passed.
    """
    needle = _normalize(expects)
    if not needle:
        return False

    return needle in _normalize(answer)


def retrival_hits(expects, results) -> bool:
    """True when at least one retrieved chunk contains `expects`.

    Says whether retrieval put the right material in front of the model, which
    is a different question from whether the model used it. A failing `judge`
    with a passing `retrival_hits` means the generation step lost the answer;
    both failing points at retrieval.
    """
    needle = _normalize(expects)
    if not needle:
        return False

    return any(needle in _normalize(chunk.text) for chunk in results)
