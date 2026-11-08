# 2026-11-08 series

Commit `f02e81a6`. Scope WARP-2, WARP-3, WARP-4, WARP-5, WARP-6, WARP-7. Verdict: revise.

| criterion | answer | evidence |
|---|---|---|
| A1 | yes | each Motivation names what no front end or second implementation could settle alone |
| A2 | yes | every refusal reads the document or the value's form |
| A3 | yes | no stack, memory or stop limit; the budget is the document's own size |
| A4 | yes | one key order, one sameness, one tag table, one grammar |
| B0 | yes | `spec-series lint` |
| B1 | no | abd-1 to abd-4 |
| B2 | no | WARP-30 `dictionary` and WARP-80 `setting` restate WARP-3; WARP-6 restated WARP-5's budget as the bytes that remain |
| B3 | no | abd-5 |
| B4 | yes | encoding refusals at `load`; a key holding a procedure at `run`, where the build cannot see it |
| B5 | no | abd-6, abd-7 |
| B6 | unchecked | no second runtime |
| B7 | yes | tables for kinds and tags, a grammar for the text |
| C1 | no | c-7, c-10 |
| C2 | no | c-1, c-2, c-3, c-6 |
| C3 | no | c-4, c-5, c-8, c-9 |
| C4 | yes | WARP-42, WARP-47, WARP-49, WARP-77, WARP-93 cases meet these rules |
| C5 | yes | 101 of 101 scope cases HELD |
| D1 | yes | no draft in scope |
| D2 | yes | nothing in scope supersedes or is superseded |
| E1 | no | majors open |
| E2 | yes | nothing marked **Open.** |
| E3 | yes | abd-1 settled by an owner decision, below |

- abd-1, B1, WARP-4: which Unicode version's grapheme and normalization tables apply is not said. reject: what the base language decides, Unicode's tables among it, Warp sets no promise on; WARP-4 says so in a Note.
- abd-5, B3, WARP-7: a name that reads back bare has a second spelling in backticks, where a second spelling of a string or a number refuses. defer: no reason is stated for the difference; settle it, by a refusal or a Note giving the reason, when the text's spellings are next decided.
- draft-96-5, B4, WARP-3 `a-path-writing-a-key-of-a-struct-holding-a-procedure-refuses`: a struct claimed `Hashable` whose field is a procedure type refuses at the run, though the build sees that every value of it holds a procedure. Raised by the dry-run review of a draft that carried the case. reject: a claim is declared and asks nothing of the fields, and the claim is used without refusing wherever no value of the struct is written as a key, under a type parameter bounded by `Hashable` or in a dictionary that stays empty, so not every run refuses, and the run is the stage that sees a key.
