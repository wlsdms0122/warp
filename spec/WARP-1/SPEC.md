# WARP-1: Conformance

Status: accepted

## Summary

Conformance cases are data: one file asks one question of a subject and says what should happen. The rules decide how a case is written and what a runner does with one, so that an implementation in another language runs the same cases and finds out the same things. Each case belongs to the conformance directory of the one WARP it measures, and no two cases share a name.

## Motivation

Warp has more than one implementation in view. A golden byte layout described in prose and kept as a test inside each implementation is a test of that implementation, and it says nothing to another.

## Rules

How a case is written, and what a runner does with one. An implementation that passes every case is not thereby correct, and one that fails a case is thereby wrong.

The rules the WARPs state, as cases that run: each WARP's `conformance/`. Which cases belong to which rules is written where the rules are: each case sits in the `conformance/` of the one WARP it measures, and no two cases anywhere share a name. Data rather than code, so an implementation written in another language runs the same cases and finds out the same things.

### What a case is

One file, one question: a subject, what to ask it with, and what should happen.

    test        int. The case format this file is written for
    name        what the case is called
    note        why it exists. The rule it holds an implementation to
    program     a document; a case expecting `answers` or `refuses` starts
                a run from its `public` procedure spelled `entry`
    bytes       a document's bytes, in the binary encoding
    text        a document's, an interface's or a case's text, in the text
                encoding; a string, or bytes where the question is whether
                they are text at all
    object      an object, written as data
    document    bytes. The identity the runner reads the object under, where
                it is not the one the object writes; only an object case
                writes it
    arguments   what the entry procedure is given, if anything, as data
    vocabulary  the procedures the runner brings, if any
    documents   documents laid beside the program, if any, each written as
                a document is; only a program case writes them
    expect      answers <value>   it runs and returns this
                reads <value>     it reads as that value
                spells <value>    it reads as that value, and writing that
                                  value gives exactly it
                builds <object>   building the program's own document writes
                                  exactly this object
                refuses <stage>   it is refused, at load, build or run

**A case carries exactly one of `program`, `bytes`, `text` and `object`,** and which one it carries decides what it may expect and, with that, the keys it writes. A case carrying two would be two cases sharing one expectation. Beside `test`, `name`, `note` and `expect`, a case writes only the keys its subject and its expectation read:

| subject | expect | keys it may write |
|---|---|---|
| `program` | `answers` or `refuses` | `arguments`, `vocabulary`, `documents` |
| `program` | `builds` | `vocabulary`, no procedure of which writes `answers`, and `documents` |
| `object` | `answers` or `refuses` | `arguments`, `document` |
| `bytes` | `spells` or `refuses` | none |
| `text` | `reads`, `spells` or `refuses` | none |

Any other key, a misspelled one included, and any other expectation **refuse** as a case.

A case carrying a **program** is the ordinary kind: it is read, built and run, and it expects `answers` or `refuses`. It may instead expect `builds`: the program's own document, compiled against the standard vocabulary, the documents beside it and whatever the case asked the runner to bring, writes exactly this object, as a value, under [what an object holds](../WARP-85/SPEC.md). That is the writer's half of the object format, the way `spells` is the writer's half of an encoding. Nothing runs, which is why it hands no `arguments` and brings no `answers`.

A case carrying an **object** asks the reader's half: the object is read, linked with the standard vocabulary and run from `entry`, and it expects `answers` or `refuses`. It brings no `vocabulary`, since what it leans on is already written inside it. It is read under the identity it writes for its document, or under `document` where the case writes one, which is how a case asks whether an object kept under one document is refused when handed back under another. An object refused where it is read refuses at `load`; one refused where it is laid beside the vocabulary, at `build`.

A case carrying **bytes** or **text** asks about an encoding rather than about a program. `spells <value>` is both directions at once: reading gives the value, *and* writing the value gives exactly those bytes or that text, which is what holds a writer to one spelling. A writer that agrees with no reader and a reader that agrees with no writer each satisfy half of it, and half of it is what leaves one document with two spellings. `reads <value>` is the reading half alone. `refuses "load"` is the other direction: it is not a document, and reading is the only stage it reaches, so no other stage may be written beside it. Nothing runs and nothing is brought, so a case carrying either writes no key beside its subject.

A case carrying **bytes** expects `spells` or `refuses`. The bytes are the **binary** encoding, which is the one a document travels in and the one that is canonical: a non-canonical byte spelling is refused, which leaves no bytes that read one way, so a bytes case writing `reads` **refuses** as a case.

A case carrying **text** expects `reads`, `spells` or `refuses`. A text has many layouts of one value, since layout is free on the way in: a text in the writer's layout expects `spells`, and a case saying `reads` of one **refuses** as a case. A text case is read by one reader on both sides, so a reader taking a spelling for the wrong value would agree with itself; every scalar and every name a text case reads therefore appears in some bytes case, which is where a spelling is pinned. A container's structure is not a spelling and is not pinned. What the text encoding must read at all is asked of every case in passing, since a case is a text and a runner reads it before it can ask anything at all.

A case is **not a document**. It is written in the same text, under [a case, in the text](../WARP-44/SPEC.md), and the document it asks about is nested whole under `program`, and what surrounds it belongs to the asking. A program no node writes back as itself is written there as data, `(tree …)`, and is the same `program` in the tree.

Each format declares itself, and that is how the two are told apart: a case says `test`, a document says `warp`, and each is refused by the other's reader for **what it is** rather than for the keys it happens to carry. The `test` number moves for the same reason `warp` does and on its own schedule.

`expect` holds one of `answers`, `reads`, `spells`, `builds` or `refuses`. One slot, so "one of them and exactly one" is the shape of the dictionary rather than a rule about keys that could all be written or none.

**What a case expects is matched strictly.** A value `answers` expects, and what `reads` and `spells` read, match the value written where both are of one kind and one spelling, part by part: an `Int` does not match a `Double`, nor bytes the array of the same numbers, though `equal` says each pair is one value under [when two values are the same](../WARP-4/SPEC.md). A string in what `answers` expects matches as values compare it, and a string that `reads` and `spells` read, a key included, matches only a string of the same Unicode scalars, since the spelling a reading gives is what those two ask about. A dictionary matches one of matching keys bound to matching values, and a struct one of the same name and the same fields.

**`vocabulary` is what the runner brings.** Most of what a document may say about a native procedure is not something a case can write down: the code is the host's. So a case writes the part that is in the document, and the runner builds the rest.

It is written as a **module**, because that is what a host takes in, and its keys are a document's under [the module](../WARP-8/SPEC.md), these and no other:

| key | takes | required |
|---|---|---|
| `imports` | as a document's | yes, and empty where it uses none |
| `types`, `contracts`, `extensions` | as a document's | no |
| `procedures` | as a document's: the procedures it brings, each below | no |

A case writing any other key there **refuses** as a case. Which version this module is read at is the runner's, so it says no `warp`, and what a program keeps beside its procedures, `const` and `var`, is a document's. The module stands first in the link as a document of its own, so what the host brings is there to be named, and a `private` declaration in it is that document's, under [who may name a declaration](../WARP-13/SPEC.md). That document is the module's keys beside `warp` at the version the runner reads, each procedure written without the two keys below, and its identity is that document's, under [identity and dependencies](../WARP-91/SPEC.md). Each procedure it brings, one under `procedures` and a member a type or an extension gives, is keyed by its name and written the way a declaration is, `returns`, `failing`, `const` and `isolated` among it, with two keys of its own beside it:

    answers     what it returns, whatever it was sent. Absent: null
    sends       the spellings it sends, in name order, each once and never
                empty: what a native procedure declares it sends, which the
                runner declares and never calls. Absent: it sends none

One declared `const` is implemented as a const procedure, handed what [a native procedure](../WARP-14/SPEC.md) gives one, and any other as one that reaches outside the run. What one declares under `sends` is held to the rest of what it declares under [a native procedure](../WARP-14/SPEC.md), and counts among what its module uses under [the imports list](../WARP-10/SPEC.md), so a case asks with `sends` what a host's sends may reach and what they may not.

It returns the same thing every time, because a case asks what a declaration permits rather than what arithmetic does. Its parameters are named for the places it reads its arguments at, in order: it declares none, one named `first`, or two named `first` and `second`, and any other names **refuse** as a case. A native procedure reads its arguments at fixed places, and a case cannot invent a place in another runner.

This is the only way a case reaches what being const permits and what it does not, both of which need a procedure with no body: a slot asking a `const` procedure type, an operand calling one, and a constant that folds from one and is refused for it.

**`documents` are other documents in the link.** A rule about two documents, a `private` declaration one of them names or a spelling two of them declare, is asked with the program and a document beside it. Each is written as any document is and read the way the program is, and stands between what the runner brings and the program: laid one after another in the order written, each against what stands before it, and the program last, the way a host lays documents as they arrive. One that does not read **refuses** as a case, since the question was about the program. A link is built whole, so one that reads and does not build is the case's refusal at the `build`, as the program's own is: a rule about two documents may be broken in either. Only a program has documents beside it, and only an object is read under a `document` the case names, which is why the table under *what a case is* gives each key to that subject alone.

Current format: **1**, and a runner refuses any other.

Both kinds matter equally. **An implementation that accepts a program another refuses has failed in the same way as one that returns differently**, so half of these say what must *not* run, and where it must stop. The stage is part of the expectation, for the reason [the specification](../README.md) gives.

### What a runner does

Read the file, and read `test` before the rest of the dictionary, for the reason a document reads its own version first: a later case may say something this runner has no name for, and "I am too old for this" is a different refusal from "this is not a case". Then read `program` as a document. Read each entry of `vocabulary` the same way a declaration is read, and build the host's side of it from the declaration and the keys beside it. `arguments` is a dictionary from the names of the parameters `entry` declares to the values it is handed, and a key naming no parameter, or a parameter no key names, **refuses at the run** under [where a run starts](../WARP-69/SPEC.md). `arguments` written as anything but a dictionary is a case no two runners would read alike, and it **refuses** as a case rather than reading as if it were absent. What refuses as a case is asked by no case: the folders hold the suite, and a runner that refuses one of its files stops on it, because the suite is what is wrong then. Then build the program against that vocabulary, the documents beside it and the standard vocabulary. A case expecting `builds` compares the object its program's own document compiles to, and starts no run. A case expecting `answers` or `refuses` starts a run from the `public` procedure spelled `entry` with `arguments` and compares, and one whose link holds no `public` procedure spelled `entry` is refused **at the run**, under [who may name a declaration](../WARP-13/SPEC.md). If the case expects `refuses`, check that it fails at that stage and no earlier or later. A failure a procedure raised that escapes the entry is not a refusal and matches no expectation, so the runner fails the case and names the failure's type and message; a case that measures a failure catches it with `try` and returns what the catch saw. What a runner reports does not depend on the machine's locale, and a runner that leans on a host's locale for case mapping or ordering runs the cases under one that tailors them, Turkish for one, to find out.

Where an object is written or read, in a `builds` case and an `object` case, a runner keys every object it compiles under the SHA-256 digest of the object's canonical binary writing, and identifies every document by the digest of its own, so that what a `builds` case writes under `dependencies` and `document` is what every runner works out. An `object` case is read under the identity it writes, or under `document` where the case writes one.

A case is the file named its `name` followed by `.test.warpt`, and what else a folder holds is not the suite's business.

A runner reaches inside nothing and imports what any host imports. One that could see inside its implementation could pass by agreeing with the implementation rather than with the specification.

**Note.** Some of these sentences bind the runner rather than the implementation it runs, and no case can hold them: that what a case expects is matched strictly, that `test` is read before the rest of the case, that a failure escaping the entry fails the case, that what a runner reports does not depend on the locale, and that a runner reaches inside nothing. Each decides what a runner reports, and a runner breaking one reports a case held or failed for a reason the case does not measure.

### How a case is written

A case may be written by hand, since the text reader takes any layout, or authored as any document is (a front end, a literal in a host language). Either way it is run through the writer before it lands in `conformance/`, so every case sits in the writer's layout and a diff shows what changed rather than who indented it.

The extension is `.test.warpt`: the file is a text, which the text reader reads, and what it holds is a test, which nothing that runs programs takes.

**Note.** The suite covers the constructs, the vocabulary, the encodings and the objects, and a few rules no case can hold. Every construct, the naming and leaving rules, the version and the imports list, the doors' judgements, every standard procedure, what a binary reader must refuse and what a build writes down for each operation are held as cases, and each WARP holds its own under `conformance/`. The rest no case can hold, and each is a **Note.** in the WARP it is about.

## Interactions

- The identity a runner keys objects and documents under: [WARP-91](../WARP-91/SPEC.md).
- The vocabulary module is written as a document's module is, and its procedures as native ones: [WARP-8](../WARP-8/SPEC.md), [WARP-14](../WARP-14/SPEC.md).

## Alternatives considered

- Four stages, `load`, `compile`, `link` and `run`. A stage is in the expectation because what has happened by then cannot be undone, and nothing runs between compiling and linking. Which half of the build refused is no fact a case may hold, and holding it would bind how an implementation divides its own work.
- Matching a refusal's reason or place. No rule states a refusal's wording, so a runner that matched it would hold implementations to something the specification does not say. A runner measures the stage, and a case is written so that the rule it names is the one that refuses.

## Notes
