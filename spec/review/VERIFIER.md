# Verifier's brief

You help the coordinator of a review of the Warp specification. One scope was read by its reviewers, and you do steps 5 to 8 of [the review](README.md) for that scope, as a draft the coordinator judges: verify each finding, merge findings with one root, propose a verdict for each row, and answer the criteria for the scope. Change nothing in any repository. Write only your ledger.

## What you read

The coordinator names, for your scope:

- the reviewers' reports;
- the lines a run printed: for every case of the scope, run beforehand, and for each probe the reviewers wrote;
- the specification at the commit read, and `review/record/`, whose rejected lines stand;
- where your ledger goes.

Read a spec at the sentence a finding cites, and further only as far as you need. Read nothing else.

## How to verify

- **Re-derive, do not repeat.** Rebuild each critical and major finding's reasoning from the spec text and its resources yourself. A reviewer's words are a claim.
- **Behaviour comes from a printed line.** A claim about what the work does holds only where a line a run printed shows it. Where none does, say so. Comments, notes and an implementation's source are claims, never evidence of what is right.
- **A probe that answered otherwise is a question.** Either the spec says what the probe expected, and the work is wrong against it, or the probe expected what the spec does not say. Say which, with the sentence.
- **A minor finding is verified by reading.**
- **Merge** findings with one root into one row, and keep every id.

## How to propose a verdict

- **adopt**: fix it now, and say whether every existing case keeps its answer (a supplement) or one moves (a supersession).
- **defer**: record it and fix it when that spec is next touched.
- **reject**: no change, with the reason. A finding that does not hold, one that would change an accepted rule without showing the rule's own reason fails, one that only prefers another design, and one a decision below settles.
- **owner**: two designs both meet every criterion, and the specification does not choose. Give a concrete example and what each design answers for it.

Decisions already made, which settle a finding without the owner:

1. What the base language decides, its stack, memory, stopping a run and Unicode's tables among it, Warp sets no limit on and makes no promise about (criterion A3).
2. A defect of the build is a build that accepts what every run refuses. Where some run uses the thing without refusing, a run refusal is not a defect.
3. The IR holds declarations, not inference: what a document does not write is the default its WARP names, checks are made against what is declared, and a claim of a contract is declared, never discovered from a type's shape (criterion A2).
4. The IR holds what a front end cannot write in place, and a second way to write what a front end could write the first way is the front end's (criterion A1).
5. A check that asks again what an earlier stage already proved is not added, except at a security boundary (the reviewer's brief).
6. "Nothing uses this" is never a reason to remove a rule (the reviewer's brief).
7. A rule is written as the form whole, not against the one input that raised it ([the specification](../README.md), *How a rule is written*).
8. An empty Motivation in an accepted WARP is a text to write: the row is adopt and the scope's verdict is revise ([the criteria](CRITERIA.md), A).

## What you write

```
# Ledger <scope>

| row | ids | crit | spec | claim | sev | by | verdict | fix kind | reason |
```

- `by` is how you verified it: a run (name the line), the text (re-derived), or reading (a minor finding).
- `claim` is one sentence, and `reason` one or two, with the spec sentence where it decides.

Then `## Owner` (for each owner row the subject, the example, what each design answers, and every noun defined), `## Criteria` (every criterion, yes, no or unchecked, with the evidence), `## Verdict`, and `## Not verified`.
