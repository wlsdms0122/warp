# Reviewing the specification

How a WARP is reviewed before it is accepted, and how the accepted series is audited. What decides acceptance is [the acceptance criteria](CRITERIA.md). A run has one coordinator and several reviewers. The coordinator follows this page and hands each reviewer a pack, one file `spec-series pack` writes from this repository: [the reviewer's brief](REVIEWER.md), the criteria it answers, its scope and what was run beforehand. A workflow runner (Forge, or anything that can start agents and hand them a file) can coordinate, so the review travels with the language it reviews.

## Modes

| mode | what is reviewed | when |
|---|---|---|
| `draft` | one WARP whose status is `draft`, with the changes it makes in accepted WARPs and the places in the live set it reaches | before it is accepted |
| `change` | a diff to accepted WARPs | before a supplement or a superseding WARP is merged |
| `series` | the live set, split into scopes | after a release, or when the owner asks |

The input of a run is the mode, the WARPs or the diff, and the commit of this repository it reads.

## Scopes

A reviewer reads one scope, and a scope is small enough to read whole: one WARP for `draft`, the WARPs a diff touches for `change`, and a run of neighbouring WARPs for `series`. A WARP outside the scope is read only at the sentence the scope links to, and the pack holds that section. For `series`, the coordinator cuts the live set into scopes of related titles, in reading order, from the live set at the commit.

What a reviewer pays for is its reading. `spec/README.md`, WARP-1, the brief and the criteria are read by every reviewer, so a scope is as large as one reading holds, about ten WARPs, rather than many small scopes that each pay that again. A scope goes to two reviewers, one answering every criterion but C and the other C, only where its cases are too many to read beside its text.

## The coordinator

1. Run `spec-series lint` on this repository. A run starts from a specification it passes, since what it checks needs no reviewer.
2. Run beforehand what a tool decides, so that no reviewer spends its reading on it. For `draft`, the diff of `spec/` from where the draft branched gives the changes it makes in accepted WARPs, `spec-series lint --as <WARP>` prints each link the acceptance would leave pointing at a superseded WARP, and `spec-series impact <WARP>` prints the places in the live set the draft reaches, which the pack also holds. Run every case of the scope on the reference runtime pinned at this commit, each WARP's cases in a folder named for the WARP, and keep the line printed for each. For `change`, run the whole suite before and after the diff and compare the two: an answer that moved makes the change a supersession, not a supplement.
3. Start the record with `spec-series record <mode> <WARP>...`. It names the commit and refuses while `spec/` has changes not committed, since then no commit is what the run reads.
4. Write one pack per reviewer with `spec-series pack <mode> <WARP>... --criteria <groups> --report <file> --probes <folder> --attach spec/WARP-1/SPEC.md --attach <lines of step 2>`, and start each reviewer with its pack and nothing else. Every reviewer of every run is briefed in the same words, from this repository.
5. Run the probes the reviewers wrote, each a `.test.warpt` file, the way step 2 ran the cases. Then verify every critical and major finding before it reaches the ledger: re-derive the reasoning from the WARP text and the cases, not from the reviewer's words, and confirm a finding about behaviour by the line a run printed. A minor finding is verified by reading.
6. Merge findings with one root into one row.
7. Judge each row: **adopt** (fix it now), **defer** (record it and fix it when that WARP is next touched), **reject** (no change, with the reason), or **owner** (a real design fork). A finding an accepted rule already settles is the coordinator's to judge. An owner row goes to the owner as a question: the layer, the subject, a concrete document and what it answers, and every noun defined.
8. Write the ledger, the run's working table: one row per finding, with id, criterion, WARP, claim, severity, evidence, verdict, reason, and for an adopted row whether the fix is a supplement or a superseding WARP. Then answer every criterion for the whole run, yes, no or unchecked, with the evidence. A criterion two reviewers answered differently is settled by the coordinator running it.
9. Give the run's verdict, accept, revise or reject, as CRITERIA.md defines them. For `draft`, the verdict is what the owner reads to decide, and accepting also needs the reference runtime built against the WARP and its cases passing (criterion C5).
10. Fixes run after the owner has read the ledger, one layer at a time: the WARP and its cases first, then each implementation. A draft the owner accepts is accepted with `spec-series accept <WARP>`, which refuses while `spec-series lint --as <WARP>` finds anything, and which writes `Superseded-By` into each WARP it supersedes.
11. Fill in the record: the verdict, the criteria table, and under it one line for each finding judged defer, reject or owner, with its id, criterion, WARP, claim, verdict and reason. An adopted finding is not recorded, since its fix is in the text and the history. A deferred line is deleted when its fix lands, and an owner line when the answer is in the text. A rejected line stays, so the same finding is not raised again unless its reason fails. The ledger is not kept.

Where a run has many scopes, the coordinator may hand steps 5 to 8 of each scope to a verifier, briefed by [the verifier's brief](VERIFIER.md) with that scope's reports, the lines its cases and probes printed, and where its ledger goes. The coordinator then judges every reject and owner row itself, merges the scopes' ledgers into the run's, and keeps its own notes where no reviewer reads.

A round ends when what is left is wording and maintainability. Critical and major findings start another round on the fixes alone, and only where a fix could reach further than its own lines.
