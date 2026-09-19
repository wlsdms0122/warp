# Conformance

How a case is written, and what a runner does with one. An implementation that
answers every case is not thereby correct, and one that fails a case is
thereby wrong, which is the only asymmetry a suite like this can offer.

The rules these pages state, as cases that run: `conformance/`. Which cases
belong to which rules is written where the rules are: each page ends with the
ones that measure it, and every case is named by exactly one page. Prose ages
against an implementation that keeps moving, and an implementation is the last
thing that should be asked whether it is correct. These are the questions asked
instead. Data rather than code, so an implementation written in another language
runs the same cases and finds out the same things.

## What a case is

One file, one question: a subject, what to ask it with, and what should happen.

    test        int. The case format this file is written for
    name        what the case is called
    note        why it exists. The rule it holds an implementation to
    program     a document, declaring a procedure spelled `entry`, which is
                where the runner starts
    bytes       a document's bytes, in the binary encoding
    text        a document's text, in the text encoding
    arguments   what the entry procedure is given, if anything; a record
                under a name is written as the text encoding writes one
    vocabulary  the procedures the runner brings, if any
    expect      answers <value>   it runs and answers this, named records
                                  written the same way
                reads <value>     those bytes are that value, both ways;
                                  that text reads as that value
                refuses <stage>   it is refused, at load, build or run

**A case carries exactly one of `program`, `bytes` and `text`,** and which one
it carries decides what it may expect. A case carrying two would be two cases
sharing one answer.

A case carrying a **program** is the ordinary kind: it is read, built and run,
and it expects `answers` or `refuses`.

A case carrying **bytes** asks about an encoding rather than about a program,
and the two things an encoding is held to are the two it may expect. `reads`
is both directions at once: reading those bytes answers that value, *and*
writing that value answers those bytes. A writer that agrees with no reader and
a reader that agrees with no writer each satisfy half of it, and half of it is
what leaves one document with two byte spellings. `refuses "load"` is the other
direction: those bytes are not a document, and reading is the only stage they
reach, so no other stage may be written beside them.

The bytes are the **binary** encoding, which is the one a document travels in
and the one that is canonical.

A case carrying **text** asks about the text encoding the same way, and
expects `reads` or `refuses "load"`. `reads` is one direction here: reading
that text answers that value. One value has many layouts in text, since layout
is free on the way in, so what a writer lays out is not asked of a text but of
the cases themselves: every case file is in the writer's layout, and a runner
that writes each one back and compares has asked its writer the same question
the binary cases ask. What the text encoding must read at all is asked of
every case in passing, since a case is warpt text and a runner reads it before
it can ask anything at all.

A case is **not a document**, and this is the record where that is said out
loud. It is written in the same text. An encoding carries a tree of data and
never learns what a tree means, so there is one of those and not two, but the
document it asks about is nested whole under `program`, and what surrounds it
belongs to the asking.

Each format declares itself, and that is how the two are told apart: a case
says `test`, a document says `warp`, and each is refused by the other's reader
for **what it is** rather than for the keys it happens to carry. The `test`
number moves for the same reason `warp` does and on its own schedule. The day
a case may say something new is not the day a document may.

`expect` holds one of `answers`, `reads` or `refuses`. One slot, so "one of
them and exactly one" is the record rather than a rule about keys that could
all be written or none.

**`vocabulary` is what the runner brings.** Most of what a document may say
about a procedure the host answers is not something a case can write down: the
code is the host's. So a case writes the part that is in the document, and the
runner builds the rest.

It is written as a **module**, because that is what a receiver takes in: it may
declare `types`, `constraints`, `contracts` and `satisfies` the way any document
does, and it declares the procedures under `procedures`. It does not say `warp`
or `imports`: which version this module is read at is the runner's, and its
declarations send nothing. A case writing either **refuses** as a case. The
module stands in front of the case's own document in the link, so what the host
brings is there to be named. Each procedure is keyed by its name and written the way a
declaration is, with four keys of its own beside it:

    answers     what it answers, whatever it was sent. Default null
    runs        bool. Whether it reaches outside the run. Default false,
                which is a procedure that answers without running
    isolated    bool. Default true
    failing     array of strings. What it may fail with. Default empty

It answers the same thing every time, because a case asks what a declaration
permits rather than what arithmetic does. The names it may declare are `of` and
`value`, in that order, since a procedure the host answers reads its arguments
at fixed places and a case cannot invent a place in another runner.

This is the only way a case reaches what answering without running permits and
what it does not, both of which need a procedure with no body: a slot asking
`const procedure`, an operand calling one, and a constant that settles from one
and is refused for it.

A runner reads `test 2` through `test 5`, and a case says the earliest it
needs, which a runner checks against what the case writes. A case saying a
later one would turn away a runner that could have asked it, and one saying an
earlier one would have that runner refuse it as no case at all:

| version | what moved |
|---|---|
| 1 | spelled the middle stage `link`; a runner that reads `build` cannot honour it, so it is refused |
| 2 | the stages `load`, `build` and `run` |
| 3 | `vocabulary` |
| 4 | `bytes` and `expect reads` |
| 5 | `text` |

Both kinds matter equally. **An implementation that accepts a program another
refuses has failed in the same way as one that answers differently**, so half of
these say what must *not* run, and where it must stop. The stage is part of the
answer: refusing at run what another implementation refuses at build means
something already happened before the refusal, and what already happened
cannot be taken back. That is why the build stands in front of the run, the
same reason it does in any language that has one.

## What a runner does

Read the file, and read `test` before the record, for the reason a document
reads its own version first: a later case may say something this runner has no
name for, and "I am too old for this" is a different answer from "this is not a
case". Then read `program` as a document. Read each entry of `vocabulary` the
same way a declaration is read, `receiver` included where the procedure takes
one in front, and build the host's side of it from the four keys beside it. Each of the four
is written as its kind or not at all: a `runs` that is not a bool, or a
`failing` that is not an array of names, is a case no two runners would read
alike, and it **refuses** as a case rather than reading as a default. What
refuses as a case is asked by no case: the folder holds the suite, and a
runner that refuses one of its files stops on it, because the suite is what is
wrong then. If the
case expects `refuses`, check that it fails at that stage and no earlier or
later. Otherwise build it against that vocabulary and the standard bundles,
start from the procedure declared under `entry`, run it with `arguments`, and
compare. A program that declares no `entry` is refused **at the build**, where
a name nothing in the link declares is refused.

The cases are the files named `<name>.test.warpt`, and what else the folder
holds is not the suite's business. A runner that refused to start over an
editor's leftover would be answering "is this folder tidy" with the same red
light as "is this implementation the language", and only the second is a
question about a language.

A runner reaches inside nothing and imports what any caller imports. One that
could see inside its implementation could pass by agreeing with the
implementation rather than with the specification, which is the one thing it
must not do.

## How a case is written

A case may be written by hand, since the text reader takes any layout, or
authored as any document is (a front end, a literal in a host language). Either
way it is run through the writer before it lands in `conformance/`, so every
case sits in the writer's layout and a diff shows what changed rather than who
indented it. An implementation adding cases writes its own dumper anyway. It
is the same writer conformance already requires of it.

So the suite is the first thing a new implementation reads with its own reader.
The reader is proven before it by the cases that carry bytes, and one whose
reader disagrees with those cannot trust anything the rest of the suite tells
it.

The extension is `.test.warpt` and not `.warpt`, and both halves are true at
once: the file *is* warpt text, which is why the text reader reads it, and what
it holds is a test rather than a document, which is why nothing that runs
programs will take it. Naming the format outright. A single extension of its
own. Would make a file that is spelled in warpt look like it is not, and every
tool that highlights or formats warpt would have to be told about it twice.

## Cases

What `conformance/` asks about this page, by the name each case's file carries.

- `a-program-without-an-entry-refuses-at-the-build`
