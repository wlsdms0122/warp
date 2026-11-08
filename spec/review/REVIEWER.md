# Reviewer's brief

You review part of the Warp specification. This brief opens your pack, and the pack holds everything you read: where you write, the criteria you answer, how the specification works, WARP-1, the record lines on your scope, the scope whole with its cases, the sections it links to outside the scope, and the lines the coordinator ran beforehand. Read the scope whole, judge it against the criteria, and report. Beyond the pack, search only the specification at the commit it names, for a sentence or a case outside your scope; read nothing else, the coordinator's notes and other reviewers' reports included. Change nothing in any repository.

## What Warp is, for judging

- **A language kit, not a language.** Front ends bring the syntax, and the IR gives them what they cannot write themselves. Criterion A is this sentence made testable.
- **A runtime knows facts about the program, not what values mean.** What can be known by reading the document is the runtime's to judge. What a value means is the vocabulary's.
- **The value model is a transport model.** A value is what crosses between a host and a program: null, booleans, numbers, strings, lists, dictionaries, named structs. Nothing holds a reference.
- **Portability is the measure.** A second runtime in another language follows these WARPs and passes the same cases.

## How the series works

- A WARP is `draft` or `accepted`, and it is superseded when an accepted WARP names it under `Supersedes`. A superseded WARP says so under `Superseded-By`.
- A change that leaves every existing case's answer as it was is a supplement, made in place. A change that alters any answer is a new WARP that supersedes the old one whole.
- The cases are the statements as data. A rule no case holds is a rule nobody can measure.
- What `spec-series lint` checks, and what the pack says was run beforehand, is not yours to find again.

## How to judge

Go through every criterion in your pack. For each one, answer yes or no, with evidence. Every no is a finding.

- **Behaviour comes from running, not reading.** Notes, case notes and implementation comments are claims. What a runtime does is shown by a line a run printed. Where you need a run the pack does not hold, write a probe where the pack says, one `.test.warpt` file each, and say which finding waits on it. Leave a criterion unchecked rather than yes where nothing was run.
- **What is right comes from WARP text.** Cite `WARP-N` and the sentence.
- **Accepted rules stand.** A finding that would change an accepted rule must show that the rule's own reason fails, with a concrete document. Preferring another design is not a finding.
- **Rejected findings stay rejected.** A finding a line in `spec/review/record/` rejected is raised again only by showing that the line's reason fails.
- **Lack of use is no reason.** "Nothing uses this" or "no front end writes this" never justifies removing a rule. Judge by role: should a language kit at this boundary have it?
- **No re-checking what is already proven.** A check that asks again what an earlier stage already proved is not a defense. Recommend one only at a security boundary.
- **A fork is the owner's.** Where two designs both meet every criterion and the specification does not choose, recommend `owner` and say what each answers.

## Report

First, the criteria table for your scope:

```
criterion   yes | no | unchecked
evidence    WARP-N sentence, case name, or printed line
```

Then one entry per finding:

```
id          <scope>-<n>
criterion   the one it fails
WARP        WARP-N, the sentence or case
claim       one sentence
severity    critical (a conforming implementation may do harm, or the series contradicts itself) | major (two implementations may answer differently, or a rule no case holds) | minor (wording, a term, a link)
evidence    the WARP text, the case, the document and what it answered
fix         what would change, which layers, and whether it is a supplement or a superseding WARP
leave       what leaving it costs
recommend   adopt | defer | reject | owner, and why
```

End with your verdict for the scope: accept, revise or reject, as the criteria define them. Also say what you read and what you did not reach.
