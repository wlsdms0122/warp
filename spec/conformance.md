# Conformance

How a case is written, and what a runner does with one. An implementation that answers every case is not thereby correct, and one that fails a case is thereby wrong.

The rules these pages state, as cases that run: `conformance/`. Which cases belong to which rules is written where the rules are: each page ends with the ones that measure it, and every case is named by exactly one page. Data rather than code, so an implementation written in another language runs the same cases and finds out the same things.

## What a case is

One file, one question: a subject, what to ask it with, and what should happen.

    test        int. The case format this file is written for
    name        what the case is called
    note        why it exists. The rule it holds an implementation to
    program     a document; the runner starts a run from the procedure
                spelled `entry`
    bytes       a document's bytes, in the binary encoding
    text        a document's text, in the text encoding; a string, or bytes
                where the question is whether they are text at all
    object      an object, written the way the text encoding lays one out
    document    bytes. The identity the runner reads the object under, where
                it is not the one the object writes; only an object case
                writes it
    arguments   what the entry procedure is given, if anything; a record
                under a name is written as the text encoding writes one
    vocabulary  the procedures the runner brings, if any
    documents   documents laid beside the program, if any, each written as
                a document is; only a program case writes them
    expect      answers <value>   it runs and answers this, named records
                                  written the same way
                reads <value>     it reads as that value
                spells <value>    it reads as that value, and writing that
                                  value gives exactly it
                builds <object>   building the program's own document writes
                                  exactly this object
                refuses <stage>   it is refused, at load, build or run

**A case carries exactly one of `program`, `bytes`, `text` and `object`,** and which one it carries decides what it may expect. A case carrying two would be two cases sharing one answer.

A case carrying a **program** is the ordinary kind: it is read, built and run, and it expects `answers` or `refuses`. It may instead expect `builds`: the program's own document, compiled against the standard vocabulary and whatever the case asked the runner to bring, writes exactly this object, as a value, under [objects](object.md). That is the writer's half of the object format, the way `spells` is the writer's half of an encoding.

A case carrying an **object** asks the reader's half: the object is read, linked with the standard vocabulary and run from `entry`, and it expects `answers` or `refuses`. It may write `arguments` and not `vocabulary`, since what it leans on is already written inside it. It is read under the identity it writes for its document, or under `document` where the case writes one, which is how a case asks whether an object kept under one document is refused when handed back under another. An object refused where it is read refuses at `load`; one refused where it is laid beside the vocabulary, at `build`.

A case carrying **bytes** or **text** asks about an encoding rather than about a program. `spells <value>` is both directions at once: reading answers the value, *and* writing the value answers exactly those bytes or that text, which is what holds a writer to one spelling. A writer that agrees with no reader and a reader that agrees with no writer each satisfy half of it, and half of it is what leaves one document with two spellings. `reads <value>` is the reading half alone. `refuses "load"` is the other direction: it is not a document, and reading is the only stage it reaches, so no other stage may be written beside it. A case carrying either writes neither `arguments` nor `vocabulary`, since nothing runs and nothing is brought, and one that does **refuses** as a case.

A case carrying **bytes** expects `spells` or `refuses`. The bytes are the **binary** encoding, which is the one a document travels in and the one that is canonical: a non-canonical byte spelling is refused, which leaves no bytes that read one way, so a bytes case writing `reads` **refuses** as a case.

A case carrying **text** expects `reads`, `spells` or `refuses`. A text has many layouts of one value, since layout is free on the way in, so most text cases are `reads`, and the ones in the writer's layout are `spells`. A text case is read by one reader on both sides, so a reader taking a spelling for the wrong value would agree with itself; every scalar and every name a text case reads therefore appears in some bytes case, which is where a spelling is pinned. A container's structure is not a spelling and is not pinned. What the text encoding must read at all is asked of every case in passing, since a case is warpt text and a runner reads it before it can ask anything at all.

A case is **not a document**. It is written in the same text. An encoding carries a tree of data and never learns what a tree means, so there is one of those and not two, but the document it asks about is nested whole under `program`, and what surrounds it belongs to the asking.

Each format declares itself, and that is how the two are told apart: a case says `test`, a document says `warp`, and each is refused by the other's reader for **what it is** rather than for the keys it happens to carry. The `test` number moves for the same reason `warp` does and on its own schedule.

`expect` holds one of `answers`, `reads`, `spells`, `builds` or `refuses`. One slot, so "one of them and exactly one" is the record rather than a rule about keys that could all be written or none.

**`vocabulary` is what the runner brings.** Most of what a document may say about a procedure the host answers is not something a case can write down: the code is the host's. So a case writes the part that is in the document, and the runner builds the rest.

It is written as a **module**, because that is what a caller takes in: it may declare `types`, `constraints`, `contracts` and `satisfies` the way any document does, and it declares the procedures under `procedures`. It does not say `warp` or `imports`: which version this module is read at is the runner's, and its declarations send nothing. A case writing either **refuses** as a case. The module stands in front of the case's own document in the link, so what the host brings is there to be named. Each procedure is keyed by its name and written the way a declaration is, with four keys of its own beside it:

    answers     what it answers, whatever it was sent. Absent: null
    runs        bool. Whether it reaches outside the run. Absent: false,
                which is a procedure that answers without running
    isolated    bool. Absent: true
    failing     array of strings. What it may fail with. Absent: empty

It answers the same thing every time, because a case asks what a declaration permits rather than what arithmetic does. The names it may declare are `first` and `second`, in that order, since a procedure the host answers reads its arguments at fixed places and a case cannot invent a place in another runner.

This is the only way a case reaches what answering without running permits and what it does not, both of which need a procedure with no body: a slot asking `const procedure`, an operand calling one, and a constant that settles from one and is refused for it.

**`documents` are other documents in the link.** A rule about two documents, a `private` declaration one of them names or a spelling two of them declare, is asked with the program and a document beside it. Each is written as any document is and read the way the program is, and stands between what the runner brings and the program: laid one after another in the order written, each against what stands before it, and the program last, the way a host lays documents as they arrive. One that does not read **refuses** as a case, since the question was about the program. Only a program has documents beside it, and only an object is read under a `document` the case names, so a case writing either key about any other subject **refuses** as a case.

A case says `test 1`, and a runner refuses any other: the format moves when what a case may say moves, on its own schedule. Current format: **1**.

Both kinds matter equally. **An implementation that accepts a program another refuses has failed in the same way as one that answers differently**, so half of these say what must *not* run, and where it must stop. The stage is part of the answer: refusing at run what another implementation refuses at build means something already happened before the refusal, and what already happened cannot be taken back. That is why the build stands in front of the run.

## What a runner does

Read the file, and read `test` before the record, for the reason a document reads its own version first: a later case may say something this runner has no name for, and "I am too old for this" is a different answer from "this is not a case". Then read `program` as a document. Read each entry of `vocabulary` the same way a declaration is read, and build the host's side of it from the four keys beside it. The three of them that have a kind, `runs`, `isolated` and `failing`, are written as it or not at all: a `runs` that is not a bool, or a `failing` that is not an array of names, is a case no two runners would read alike, and it **refuses** as a case rather than reading as if it were absent. So does `arguments` written as anything but a record. What refuses as a case is asked by no case: the folder holds the suite, and a runner that refuses one of its files stops on it, because the suite is what is wrong then. If the case expects `refuses`, check that it fails at that stage and no earlier or later. Otherwise build it against that vocabulary, the documents beside it and the standard vocabulary, start a run from the `public` procedure spelled `entry` with `arguments`, and compare. A case whose link declares no `entry` is refused **at the run**, where starting from a name nothing in the link declares is refused, and so is one whose `entry` is not `public`. What a runner answers does not depend on the machine's locale, and a runner that leans on a host's locale for case mapping or ordering runs the cases under one that tailors them, Turkish for one, to find out.

A runner keys every object it compiles under the SHA-256 digest of the object's canonical binary writing, and identifies every document by the digest of its own, so that what a `builds` case writes under `dependencies` and `document` is what every runner works out. An `object` case is read under the identity it writes, or under `document` where the case writes one.

The cases are the files named `<name>.test.warpt`, and what else the folder holds is not the suite's business.

A runner reaches inside nothing and imports what any caller imports. One that could see inside its implementation could pass by agreeing with the implementation rather than with the specification.

## How a case is written

A case may be written by hand, since the text reader takes any layout, or authored as any document is (a front end, a literal in a host language). Either way it is run through the writer before it lands in `conformance/`, so every case sits in the writer's layout and a diff shows what changed rather than who indented it. An implementation adding cases writes its own dumper anyway. It is the same writer conformance already requires of it.

So the suite is the first thing a new implementation reads with its own reader. The reader is proven before it by the cases that carry bytes, and one whose reader disagrees with those cannot trust anything the rest of the suite tells it.

The extension is `.test.warpt` and not `.warpt`, and both halves are true at once: the file *is* warpt text, which is why the text reader reads it, and what it holds is a test rather than a document, which is why nothing that runs programs will take it. Naming the format outright, with a single extension of its own, would make a file that is spelled in warpt look like it is not, and every tool that highlights or formats warpt would have to be told about it twice.

## Cases

What `conformance/` asks about this page, by the name each case's file carries.

- `a-program-without-an-entry-refuses`
