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
| 1. Retrieved chunk contains the answer | 4 of 5 | 2/5 | 2/5 | 2/5 | MISSED |
| 2. Every answer names a source | 5 of 5 | 3/5 | 3/5 | 3/5 | MISSED |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. No chunk shorter than 200 characters | 0 of 88 under 200 | 4/88 under | 4/88 under | 4/88 under | MISSED |
| 5. Adds corrected examples to its knowledge base | learns from a correction | not measurable | not measurable | not measurable | MISSED |

Source log: `results/run_2026-09-29_2325_before.md`, produced by
`run_eval.py::main`. An earlier pass one minute before
(`results/run_2026-09-29_2324_before.md`, no changes in between) gives the
same counts for every criterion.

`scorer.py::judge` marked all 15 runs `fail`. That verdict is not used above.
My `expects` values in `questions.py` are answer *types* ("place", "item",
"method") rather than answer text, so an exact substring match can never
succeed. The counts above come from reading each answer and each retrieved
chunk by hand.

Criteria 1, 3 and 4 are deterministic: retrieval, the gate and the chunker
give the same result every run, so one number goes in all three columns.
Criterion 2 depends on the generated text, but it came out the same in all
three runs.

### Criterion 1 — retrieved chunks contain the answer (2/5)

Output of `python app.py retrieve "<question>"` (`app.py::cmd_retrieve`,
which calls `store.py::search` with top-k 5). Retrieval is deterministic, so
this is what all three runs saw.

**Hit — bread:**

```
Question: which dining hall bakes its own bread

#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.5425     dining_halden_hall.txt           Halden Hall  I lived here my sophomore year. Wait ti...
2   0.5626     dining_pellew_dining_hall_followup.txt Re: Pellew Dining Hall  Adding to what people have s...
3   0.5711     dining_pellew_dining_hall.txt    Pellew Dining Hall  Second-year here. Wait times: 12...
4   0.6434     dining_north_kitchen.txt         North Kitchen  Second-year here. Wait times: none, i...
5   0.6505     dining_halden_hall_followup.txt  Re: Halden Hall  Adding to what people have said abo...

Gate: best distance 0.542 is under the 0.6 cutoff
```

The full text of rank 1, `dining_halden_hall.txt`, which contains the answer:

```
Halden Hall

I lived here my sophomore year. Wait times: rarely more than 8 minutes, even at noon. The thing worth going for is soup rotation, and the bread is baked on site. The thing to know is that closes at 7:00pm, which catches people out.

Hours are 7:30am to 7:00pm weekdays, closed Sundays. Costs one meal swipe, or $10.00 cash.
```

**Hit — Verrill Street Grill:**

```
Question: what is worth ordering at Verrill Street Grill

#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.4623     dining_verrill_street_grill_followup.txt Re: Verrill Street Grill  Adding to what people have...
2   0.4636     dining_verrill_street_grill.txt  Verrill Street Grill  I'm a junior and I've done thi...
3   0.6606     admin_parking_permits.txt        On the parking permits  Student permits for the west...
4   0.6620     dining_north_kitchen.txt         North Kitchen  Second-year here. Wait times: none, i...
5   0.6946     dining_the_atrium.txt            The Atrium  Transferred in last year, so take this w...

Gate: best distance 0.462 is under the 0.6 cutoff
```

The full text of rank 2, `dining_verrill_street_grill.txt`, which contains the answer:

```
Verrill Street Grill

I'm a junior and I've done this twice now. Wait times: up to 30 minutes on Friday evenings, otherwise under 10. The thing worth going for is the burger, which is the only late-night hot food on campus. The thing to know is that one register, so the queue is a single line no matter how busy.

Hours are 11:00am to 1:00am daily during term. Costs declining balance, or cash after 11:00pm.
```

**Miss — supermarket.** No file in the corpus mentions a supermarket or
groceries (`grep -ril "supermarket\|grocer" corpora/` returns nothing):

```
Question: how do you get to the nearest supermarket near campus

#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.5428     dining_verrill_street_grill.txt  Verrill Street Grill  I'm a junior and I've done thi...
2   0.5676     dining_kestrel_commons.txt       Kestrel Commons  I'm a junior and I've done this twi...
3   0.5804     transit_walking.txt              Walking times across campus  Rough numbers, measured...
4   0.5964     dining_the_ridgeway_cafe.txt     The Ridgeway Café  Second-year here. Wait times: 10 ...
5   0.6065     dining_the_ridgeway_cafe_followup.txt Re: The Ridgeway Café  Adding to what people have sa...

Gate: best distance 0.543 is under the 0.6 cutoff
```

**Miss — best food.** The chunks give one highlight per hall, but none ranks
one hall as best:

```
Question: which dining area has the best food on campus

#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.4589     dining_verrill_street_grill.txt  Verrill Street Grill  I'm a junior and I've done thi...
2   0.4904     money_jobs.txt                   On-campus work  Library and dining jobs post in the ...
3   0.5466     dining_halden_hall.txt           Halden Hall  I lived here my sophomore year. Wait ti...
4   0.5510     housing_tamsin_court.txt         Tamsin Court — what it's actually like  I lived here...
5   0.5677     dining_the_ridgeway_cafe.txt     The Ridgeway Café  Second-year here. Wait times: 10 ...

Gate: best distance 0.459 is under the 0.6 cutoff
```

**Miss — hackathon.** No file in the corpus mentions a hackathon:

```
Question: when does the campus host a annual hackathon

#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.6552     admin_wifi_and_accounts.txt      On the wifi and accounts  Your student account gives...
2   0.6699     housing_aldridge_hall.txt        Aldridge Hall — what it's actually like  I lived her...
3   0.6767     transit_walking.txt              Walking times across campus  Rough numbers, measured...
4   0.6811     dining_verrill_street_grill.txt  Verrill Street Grill  I'm a junior and I've done thi...
5   0.6814     transit_shuttle.txt              The campus shuttle  Runs a loop every 20 minutes fro...

Gate: best distance 0.655 is over the 0.6 cutoff — refusing
```

### Criterion 2 — every answer names a source (3/5 each run)

Answers from `generate.py::answer_from_chunks`, run 1:

```
which dining hall bakes its own bread
Halden Hall bakes its bread on site.

Source: dining_halden_hall.txt
```

```
what is worth ordering at Verrill Street Grill
The burger is worth going for at Verrill Street Grill, as it is the only late-night hot food on campus.

Source: `dining_verrill_street_grill.txt`
```

```
which dining area has the best food on campus
The provided documents do not state which dining area has the best food on campus.

Source: dining_verrill_street_grill.txt, dining_halden_hall.txt, dining_the_ridgeway_cafe.txt
```

The two misses are both refusals, and they came from different stages:

```
how do you get to the nearest supermarket near campus   (passed the gate, 0.5428 — model refused)
I do not have enough information to answer this question.
```

```
when does the campus host a annual hackathon   (refused by the gate, 0.6552)
I don't have enough information about that.
```

### Criterion 3 — gate stops out-of-corpus questions (5/5)

From `run_eval.py::check_out_of_scope`, cutoff 0.6:

| Out-of-scope question | Best distance | Gate |
|---|---|---|
| What is the capital of Mongolia? | 0.825 | refused |
| How do I change the oil in a diesel engine? | 0.934 | refused |
| Who won the 1994 World Cup? | 0.886 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.844 | refused |
| How do I write a for loop in Rust? | 0.896 | refused |

### Criterion 4 — no chunk shorter than 200 characters (4 of 88 under)

`chunker.py::split_documents` produces 88 chunks, and four are under 200
characters: 178, 186, 191 and 194. Output of
`python app.py chunks --from-doc <file>` (`app.py::cmd_chunks`) for each:

```
======================================================================
Chunk 1  |  source: course_hist_118_exams.txt#0  |  produced by: chunker.py::split_documents
======================================================================
HIST 118 Modern World History — assessment

No exams; two essays and a final project. Not curved.

The essay rubric is posted in week 2 and it's followed exactly — read it early.

======================================================================
Chunk 1  |  source: course_math_220_exams.txt#0  |  produced by: chunker.py::split_documents
======================================================================
MATH 220 Linear Algebra — assessment

Two midterms and a cumulative final. Curved to a b- median.

The problem sets are the course; the lectures make sense afterwards rather than during.

======================================================================
Chunk 1  |  source: course_biol_160_exams.txt#0  |  produced by: chunker.py::split_documents
======================================================================
BIOL 160 Cell Biology — assessment

Four unit tests and a cumulative final. Not curved.

The unit tests come fast, roughly every three weeks; falling behind once is very hard to recover from.

======================================================================
Chunk 1  |  source: course_phys_130_exams.txt#0  |  produced by: chunker.py::split_documents
======================================================================
PHYS 130 Mechanics — assessment

Three midterms, no final, plus a lab practical. Not curved, but the lowest midterm is dropped.

The lab practical is worth 20% and almost nobody prepares for it.
```

Each short chunk is the whole of its source document (`#0` and nothing after
it), so these four files are shorter than 200 characters from the start.

### Criterion 5 — learns from corrections (not measurable)

The pipeline has no path that writes back to the corpus or the index:
`app.py ask` only reads. No test can be run against this criterion as it is
written.

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer (4 of 5) | MISSED | 2 of 5 on every run: only the bread and Verrill Street Grill questions retrieved a chunk that contains the answer. The supermarket and hackathon facts are not in the corpus at all, and no chunk says which hall is "best". Not close — two short of the target. |
| 2 | Every answer names a source (5 of 5) | MISSED | 3 of 5 on every run. The two refusals (supermarket, hackathon) name no file. I counted refusals as answers because the criterion says "every answer" and I didn't exclude refusals when I wrote it. Reading it generously to get 5 of 5 would be changing the target after seeing the result. |
| 3 | Gate stops out-of-corpus questions (4 of 5) | MET | 5 of 5 refused. The closest was 0.825, far above the 0.6 cutoff, so this isn't a borderline pass. As I said in criteria.md, that gap exists because these questions are from unrelated domains, so this target was easy to clear. |
| 4 | No chunk shorter than 200 characters | MISSED | 4 of 88 chunks are under 200 (178, 186, 191, 194). The target said "every chunk", so one short chunk is a miss, and even the one closest to the line (194) is still under 200. |
| 5 | Adds corrected examples to its knowledge base | MISSED | The system has no way to take a correction or write to the corpus or index, so it can't do what the criterion asks. The criterion also can't be measured as written — there's no count or observable test in it — so I've revised it in `criteria.md` (the original stays). The revised version is also MISSED, because the correction step it describes hasn't been tried. |

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

### The pattern: criteria 1 and 2 fail on the same three questions

Every miss in criteria 1 and 2 comes from a question whose answer isn't in
the corpus: supermarket, hackathon and "best food". When the answer did exist
(bread, Verrill Street Grill), retrieval found it in the top 2 and the model
cited the right file in 6 of 6 runs. That makes it one problem, not five:
**three of my five test questions ask for something my corpus doesn't
contain.** Two of them then fail criterion 2 too, because both of the ways my
pipeline refuses say nothing about sources.

### Criterion 1 — stage: loading (the corpus), not retrieval

- **Supermarket and hackathon.** The loaded documents contain neither fact.
  `grep -ril "supermarket\|grocer\|hackathon" corpora/` returns nothing across
  all the files `ingest.py::load_documents` reads. Retrieval returned the
  nearest neighbours it had (dining halls, `transit_walking.txt`, the
  shuttle), and no chunk could contain an answer that was never loaded.
- **Best food.** The dining documents each give one highlight ("The thing
  worth going for is…") but none compares halls, so there's no "best" to
  retrieve. The question asks for an opinion across documents that no single
  document holds.

Embedding has a part in it but didn't cause the miss. Distance measures
topic, not whether the answer is there: the supermarket question scored
0.5428 and the bread question 0.5425. They're almost identical, but only one
has an answer. The embedding also matches on surface words: "best food on
campus" pulled `money_jobs.txt` at rank 2 because it mentions dining jobs,
and "Verrill Street Grill" pulled `admin_parking_permits.txt` because it
mentions parking on Verrill Street. That fills top-k slots with noise, but
both questions that had an answer still got it.

The root cause is in how I wrote the questions: I didn't check the corpus
before writing three of them. Criterion 1 measures retrieval, but it only
works as a test when every question has an answer to retrieve.

### Criterion 2 — stage: generation (supermarket) and the gate (hackathon)

The two misses fail in two different places:

- **Supermarket — generation.** It passed the gate (0.5428 < 0.6), so it
  reached the model. `GROUNDING_INSTRUCTION` in `generate.py` has two rules
  that pull against each other: "If the documents don't cover the question,
  say you don't have enough information" and "Name the document your answer
  came from". When the model refuses, there's no document the answer "came
  from", so it follows the first rule and drops the second. All three runs
  did this: "I do not have enough information to answer this question."
- **Hackathon — the gate, before generation.** It scored 0.6552, over the
  cutoff, so `gate.py` returned the fixed string `REFUSAL = "I don't have
  enough information about that."` The model was never called. That string
  is hard-coded and has nowhere to put a filename, so a gate refusal can
  never pass criterion 2.

"Best food" shows the model can cite files when it refuses. It said the
documents don't rank halls and still listed the three files it looked at. So
a refusal with no source isn't unavoidable: it's the model resolving an
unclear instruction one way on some questions and another way on others.

### Criterion 4 — stage: loading (short source documents), then chunking

The four short chunks are four whole documents. The raw files are 183, 189,
194 and 197 bytes on disk (`course_hist_118_exams.txt`,
`course_math_220_exams.txt`, `course_biol_160_exams.txt`,
`course_phys_130_exams.txt`), and each comes out as a single chunk (`#0`) of
178–194 characters once `ingest.py::clean_text` strips whitespace.

`chunker.py::split_documents` can't make them longer, because it chunks one
document at a time: `pieces` resets at the start of each `for doc in
documents` loop, so a short document is never merged with its neighbour.
The 120-character `MIN_SIZE` only merges short *paragraphs* inside a
document. The other five `*_exams.txt` files are 209–242 bytes, just over
the line. So this isn't a chunker bug. The target assumed every document is
at least 200 characters, and nine of these files sit right around that
length.

Each short file has siblings about the same course (`course_hist_118.txt`,
`course_hist_118_workload.txt`), so the material a short chunk needs does
exist, just in a separate document.

### Criterion 5 — no stage

No stage failed, because no stage does this. Nothing in the pipeline takes
a correction or writes to the corpus or the index. The revised criterion in
`criteria.md` describes something you'd do by hand (add a correction
document, re-index), and it hasn't been tried yet.

## The Improvement

**What I changed:** One line of `GROUNDING_INSTRUCTION` in `generate.py`,
the citation rule:

```
before: - Name the document your answer came from, using the filename given in each excerpt.
after:  - Name the document your answer came from, using the filename given in each excerpt. If you don't have enough information, still name the documents you checked.
```

Nothing else changed: same corpus, chunker, index, top-k 5 and cutoff 0.6.

**Why I picked it:** My criterion 2 diagnosis found that the model drops the
citation when it refuses, because the refusal rule and the citation rule
pull against each other and nothing says which one wins. This line settles
it.

Before the run I expected at most 4/5: the hackathon refusal comes from the
gate's hard-coded string before the model is called, so a prompt change
can't reach it.

### Run Log — After

Source log: `results/run_2026-09-29_2345_after.md`, produced by
`run_eval.py::main`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 2/5 | 2/5 | 2/5 | MISSED |
| 2. Every answer names a source | 5 of 5 | 4/5 | 4/5 | 4/5 | MISSED |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. No chunk shorter than 200 characters | 0 of 88 under 200 | 4/88 under | 4/88 under | 4/88 under | MISSED |
| 5. Adds corrected examples to its knowledge base | learns from a correction | not measurable | not measurable | not measurable | MISSED |

### Before and after, side by side

| Criterion | Target | Before (runs 1/2/3) | After (runs 1/2/3) | Change |
|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 2/5 · 2/5 · 2/5 | 2/5 · 2/5 · 2/5 | none (retrieval untouched) |
| 2. Every answer names a source | 5 of 5 | 3/5 · 3/5 · 3/5 | 4/5 · 4/5 · 4/5 | **+1, on every run** |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | none (gate untouched) |
| 4. No chunk under 200 characters | 0 under | 4/88 under | 4/88 under | none (chunker untouched) |
| 5. Learns from corrections | — | not measurable | not measurable | none |

Real output for the one criterion that moved: the supermarket question,
`generate.py::answer_from_chunks`, run 1.

Before (`results/run_2026-09-29_2325_before.md`):

```
I do not have enough information to answer this question.
```

After (`results/run_2026-09-29_2345_after.md`):

```
I don't have enough information to answer your question. 

Documents checked: `dining_verrill_street_grill.txt`, `dining_kestrel_commons.txt`, `transit_walking.txt`, `dining_the_ridgeway_cafe.txt`, and `dining_the_ridgeway_cafe_followup.txt`.
```

The hackathon miss is unchanged in all three runs, as expected. It never
reaches the model:

```
when does the campus host a annual hackathon   (refused by the gate, 0.6552)
I don't have enough information about that.
```

Criteria 1, 3 and 4 get the same output as the before run, because
retrieval, the gate and the chunker didn't change (see the Run Log — Before
output above).

**Did it help?**

Yes, for what it targeted: criterion 2 went from 3/5 to 4/5 on all three
runs, and the supermarket refusal now names its documents every time. It is
still MISSED, because 4 of 5 isn't 5 of 5, and the remaining miss is at the
gate, which this change can't reach.

It also made citations worse in a way criterion 2 doesn't measure. The model
now lists every file it checked on *successful* answers too, and in some runs
it mixes the file the answer came from with files that had nothing to do
with it. Before, the Verrill Street Grill answer cited only
`dining_verrill_street_grill.txt`. After, run 3 reads:

```
The burger is worth going for at Verrill Street Grill, as it is the only late-night hot food on campus. 

Sources checked: `dining_verrill_street_grill.txt`, `dining_verrill_street_grill_followup.txt`, `dining_north_kitchen.txt`, `dining_the_atrium.txt`, and `admin_parking_permits.txt`.
```

Here the real source is listed alongside `admin_parking_permits.txt` with
nothing to tell them apart. A reader can no longer tell which file the claim
came from, which is the thing a citation is for. Criterion 2 only asks
whether a source is named, so it scores this as a pass. My rewording asked
for "documents you checked" only when there isn't enough information, but
the model applied it to every answer.

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
