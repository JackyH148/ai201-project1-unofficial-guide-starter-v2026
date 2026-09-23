# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
One of my questions is about a topic only two documents mention, so I expect that one to be hard.

---

## 2. Every answer names a source

**Why this target:**
`build_prompt` labels every chunk `[from {source}]`, so the filename is always
in front of the model, and `GROUNDING_INSTRUCTION` requires naming it. The
mechanism is already there — five of five is the right bar because a missing
citation isn't a near miss, it's an untraceable answer. What would have to go
wrong: the model answering from training data instead of the documents, or
dropping the citation under the instruction's two-or-three-sentence brevity
rule, which is where I'd expect it to give first.

---

## 3. The relevance gate stops out-of-corpus questions

**Why this target:**
When I set the cutoff in Milestone 4 the two groups separated cleanly: my
in-scope questions scored 0.4194 to 0.5425 and the five OUT_OF_SCOPE questions
scored 0.8246 to 0.9340, a gap of 0.28. Against questions that far away I'd
expect 5 of 5, but the gap is an artifact of picking questions from an
unrelated domain. Campus-shaped questions the corpus doesn't cover land much
closer — "is Halden Hall a good option if you are vegetarian" came in at
0.614, only 0.014 above my cutoff. 4 of 5 leaves room for one question that is
off-topic in content but campus-flavoured in vocabulary.

---

## 4. No chunk is shorter than 200 characters

Every chunk my chunker produces is at least 200 characters long.

**Why this target:**
The starter's fixed-window chunker produced a 2-character chunk on one
document — the leftover tail of a document that didn't divide evenly into
800-character windows. A fragment that short can't answer anything, and it
still competes for a slot in the top 5. 200 rather than 50 because the
shortest useful unit in my corpus is a single post paragraph, and those run
150 to 300 characters.

---

## 5. If it gets corrected one somethind and find out its right, I want it to add this example to its knowledge base

I want the AI to be self learning. Since AI is not expected
     to get everything right, I want it to at least be better
     than it was before and realize its own mistake and fix it.


**Why this target:**
I want the AI to learn from its mistake so that when it is asked the same thing again, it will answer correctly


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
