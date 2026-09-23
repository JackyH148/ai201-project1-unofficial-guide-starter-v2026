# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->

## What This Does

This answers questions from an unofficial student guide to a university, built
as a retrieval-augmented pipeline over the `CORPUS_NAME` corpus — N short
posts written first-person by students, covering dining halls, residence halls
and their laundry rooms, courses and their workloads, campus transit, and
administrative topics like add/drop deadlines and meal plan changes. Many
topics appear as a pair: an original post and a follow-up that adds to or
corrects it.

Ask a question and it embeds it, retrieves the five most similar chunks, and
refuses if the closest one is further than 0.60 away. If it passes that gate,
the retrieved text is sent to the model with an instruction to answer only
from those documents and name the file each claim came from.

It handles specific factual questions — "which dining hall bakes its own
bread", "how do Halden Hall and Pellew compare on wait times" — and refuses
two different kinds of question it can't answer: off-topic ones, which the
gate catches on distance, and on-topic ones the posts simply don't cover,
which the model catches when the retrieved text doesn't contain the fact.

## Chunking Strategy

**Chunk size:**317 because it is the average characters in the documents and the context in each document should be the same throughout the document
**Overlap:** 120 (unchanged)


My chunker splits on paragraph breaks, not on a character count. The character
numbers are secondary: 700 decides when to stop packing paragraphs into a
chunk, 900 is the only point at which I cut inside a paragraph, and 120 is the
floor below which a fragment gets merged into the chunk before it.

Why: these documents are short student posts with a consistent shape — a
header line, then two or three paragraphs. A blank line is where the author
finished a thought, so that is the boundary worth respecting. The starter's
800-character window never fired on most posts and sliced arbitrarily through
the ones it did.

Overlap is zero because cuts land on blank lines, so no sentence is severed.
Overlap exists to rescue context across a mid-sentence cut; with a paragraph
boundary there is nothing to rescue, and it would only duplicate text and make
near-identical chunks compete in retrieval.

The 120 floor came from a problem I saw in the starter: on one document it
produced a 2-character chunk, the leftover tail of a document that didn't
divide evenly into 800-character windows. A fragment that short carries no
retrievable meaning.

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `` — produced by: ``

```
======================================================================
Chunk 1  |  source: admin_add_drop_deadline.txt#0  |  produced by: chunker.py::split_documents
======================================================================
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.

```

**Chunk 2** — source: `` — produced by: ``

```
======================================================================
Chunk 2  |  source: course_biol_160.txt#0  |  produced by: chunker.py::split_documents
======================================================================
BIOL 160 Cell Biology

I lived here my sophomore year. Format is lecture three times a week with a weekly lab. Assessment: four unit tests and a cumulative final. Not curved.

Expect 9 to 11 hours a week, the heaviest first-year course by reputation.

The one piece of advice: the unit tests come fast, roughly every three weeks; falling behind once is very hard to recover from.

```

**Chunk 3** — source: `` — produced by: ``

```
======================================================================
Chunk 3  |  source: course_hist_118_workload.txt#0  |  produced by: chunker.py::split_documents
======================================================================
Workload for HIST 118 Modern World History

People keep asking so: a lot of reading, about 120 pages a week, but no problem sets. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.

```

**Chunk 4** — source: `` — produced by: ``

```
======================================================================
Chunk 4  |  source: dining_pellew_dining_hall_followup.txt#0  |  produced by: chunker.py::split_documents
======================================================================
Re: Pellew Dining Hall

Adding to what people have said about Pellew Dining Hall. The wait figure of 12 to 18 minutes at peak matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely.

Also worth saying: the furthest hall from anywhere, next to the athletics centre. Nobody tells you this at orientation.

```

**Chunk 5** — source: `` — produced by: ``

```
======================================================================
Chunk 5  |  source: housing_innisfree_hall.txt#0  |  produced by: chunker.py::split_documents
======================================================================
Innisfree Hall — what it's actually like

Transferred in last year, so take this with a grain of salt. Built 1991, renovated 2022. Rooms are doubles arranged as pairs sharing one bathroom between two rooms.

The good: the shared-bathroom-between-two-rooms arrangement is the best compromise on campus.

The bad: no air conditioning, which matters for the first three weeks of September.

Laundry costs $1.75 wash, $1.75 dry, app-based. On noise: moderate; the building is L-shaped and the short wing is much quieter.

For each one, ask: could someone answer a question using only this,
without reading what came before or after?
```

## Sample Answer

**Question:** how do Halden Hall and Pellew Dining Hall compare on wait times

**Answer:**

```
  (best distance 0.259, cutoff 0.6)

Halden Hall has wait times that are rarely more than 8 minutes, even at noon
(*dining_halden_hall.txt*). In contrast, Pellew Dining Hall has wait times of
12 to 18 minutes at peak hours (*dining_pellew_dining_hall.txt*).

Sources retrieved: dining_halden_hall.txt, dining_halden_hall_followup.txt,
dining_kestrel_commons_followup.txt, dining_pellew_dining_hall.txt,
dining_pellew_dining_hall_followup.txt

1 model calls this session, 763 tokens (698 in, 65 out)
```

Both source documents use an identical "Wait times:" template and appeared in
the same retrieval window, so this question tested whether the answer would
blend them. Each figure stayed attached to the correct hall, and each claim
cites the file it came from.

```
```

**My relevance cutoff:**

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

| Question | In corpus? | Best distance |
|---|---|---|
|  |  |  |

**Cutoff: 0.60** (kept the starter default — see justification below)

### In-scope questions

| question | best distance | gate |
|---|---|---|
| where on campus can you get real espresso | 0.4194 | pass |
| what is worth ordering at Verrill Street Grill | 0.4623 | pass |
| which dining area has the best food on campus | 0.4881 | pass |
| which dining hall bakes its own bread | 0.5425 | pass |
| when does the campus host an annual hackathon | 0.6552 | refuse |

Answerable range: 0.4194 – 0.5425

### Out-of-scope questions

| question | best distance | gate |
|---|---|---|
| What is the capital of Mongolia? | 0.8246 | refuse |
| What is the recommended dosage of ibuprofen for a headache? | 0.8442 | refuse |
| Who won the 1994 World Cup? | 0.8859 | refuse |
| How do I write a for loop in Rust? | 0.8960 | refuse |
| How do I change the oil in a diesel engine? | 0.9340 | refuse |

Range: 0.8246 – 0.9340. **5 of 5 refused** (criterion 3 target: 4 of 5).

### Why 0.60

The gap runs from 0.5425 to 0.8246 — 0.28 wide. The midpoint would be 0.68,
but the hackathon question sits at 0.6552, inside the gap. It is phrased like
an in-scope question and retrieves campus documents, but the corpus contains
no events content, so it has no answer. A cutoff of 0.68 would pass it to the
model; 0.60 refuses it at the gate for zero cost.

At 0.60 the margins are near-symmetric: the closest passing question clears by
0.0575, the closest refusal clears by 0.0552.

Verified: `python app.py ask "What is the capital of Mongolia?"` returned
"I don't have enough information about that" and reported **0 model calls** —
the gate refused before reaching the model, as intended.

### What the distances do and don't measure

Distance measures topical similarity, not whether the answer is present.
Two observations from the retrieved chunks:

- "where on campus can you get real espresso" returned
  `housing_old_brewhouse.txt` at rank 2 (0.5343), ahead of several dining
  documents. "Brewhouse" is lexical overlap with coffee, not a place to get
  espresso.
- Every out-of-scope question retrieved its nearest topical relative:
  Mongolia and the 1994 World Cup both pulled `course_hist_118`, the Rust
  question pulled writing and history courses. The embedding always returns
  its closest neighbour — the gate, not retrieval, is what makes refusal
  possible.

The hackathon question is the clearest case: retrieval behaved correctly and
returned campus documents, and the question was still unanswerable. A cutoff
can catch a wrong topic; it cannot detect a missing fact.

Note on top-k: `dining_halden_hall.txt` ranked 1 (0.5425) but its follow-up
`dining_halden_hall_followup.txt` ranked 5 (0.6505), with three unrelated
dining halls in between. Posts and their follow-ups do not rank adjacently,
so k=5 barely captures both halves of one topic — a question whose answer
sits only in a follow-up could fall outside the window.

## How I Used AI


**1.** I asked Claude to write a replacement for `split_documents`, telling it
my documents were short first-person student posts with a header line and two
or three paragraphs. It came back with a paragraph-boundary splitter — right
idea — but with four helper functions at module level, and with runt-merging
that only absorbed a short trailing paragraph if the result stayed under the
700-character target. That meant a document ending in a two-character line
after a long paragraph still emitted a two-character chunk, the exact starter
bug I was replacing. I nested the helpers inside `split_documents` because my
brief wanted the strategy in one function, and changed the merge rule so
fragments below the 120 floor merge up to the 900 hard maximum instead:

    limit = TARGET_SIZE if len(para) >= MIN_SIZE else HARD_MAX

**2.** I asked Claude whether `GROUNDING_INSTRUCTION` was strict enough for my
corpus. It proposed three additions: attribute claims to the student who made
them, never combine details from two documents into one claim, and report both
sides when a post and its follow-up disagree. The blending rule looked like the
important one, since five near-identical dining documents with identical "Wait
times:" lines show up in a single retrieval window. I tested it before adding
anything — asked "how do Halden Hall and Pellew Dining Hall compare on wait
times" with both documents retrieved — and the unmodified instruction kept both
figures attached to the correct hall with the correct filename. I dropped the
blending and disagreement rules and kept only the attribution one, which my
probe answers did violate by reporting one student's wait time as fact.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
# ai201-project1-unofficial-guide-starter-v2026
