# The Warp specification

Warp is a language, and this is where the language is. The directories beside
this one hold implementations of it; nothing they do adds to the language, and
the work of these pages is to owe them nothing. [Known gaps](gap.md) says where
that is still not true.

This describes **Warp 0.1.0**. Nothing has shipped: no document exists anywhere
this specification does not control, and the numbers below start moving at the
first release.

These pages are written the way a protocol is written: they say what a
conforming implementation **must** do, field by field and byte by byte, and the
cases under `conformance/` are the same statements as data. An implementation is
a thing you can be *wrong at*.

## What Warp is

A runtime build system: a front end, an IR and a runtime, composed so that any
front end works with any runtime. Where an ordinary language goes source to
build to machine code, Warp is the half in front of that, and what it answers
with is a language again. This specification is that language. Turning it into
machine code belongs to the toolchain that built the runtime.

What a build does here is what a build does anywhere. It reads, it checks, it
links, and nothing runs until it has answered. The three things that differ are
**when**, **where** and **how much at a time**: the build runs while a program
is already running, on the machine the program is running on, and one document
at a time.

What the language is *for*, and every property below that follows from it:

A language for programs that arrive after the program running them was built.

A compiled application cannot run code it did not ship with. Handed a source
file at run time it has no compiler, and on the platforms this exists for it may
not acquire one, so the only way a decision reaches a running program without
rebuilding and re-shipping it is for something inside to read that decision and
carry it out. Warp is what that something reads.

Everything else follows from *arrive*:

- **The program comes from elsewhere**, so nothing arrives with it that says it
  was checked. There is no place to put such a thing that the receiver could
  read, so the receiver builds it.
- **The program crosses machines as bytes**, so there is a document format, and
  the two ends have to agree about what the bytes say.
- **The sender and the receiver may be different implementations**. A server in
  one language, two applications in two others, so agreement cannot mean "the
  same code".
- **What a program may do is the receiver's to set**, since the receiver
  assembles the modules and a document cannot name what nobody put in front of
  it.

What bounds it is the vocabulary. A program does exactly what the procedures in
its link let it do, and every procedure past the ones this specification spells
is one the receiver put there. The language checks what a program *sends*; what
answering a procedure means is the host's. So a receiver draws its line once,
where it assembles the modules, and a module of native procedures it takes in
reaches whatever host code reaches there. That is the same decision as taking in
a library, and it is not one a document can make.

## The pieces

```
what a person writes        YAML, a syntax of your own, …   front ends. Many, replaceable
        ↓
the document                one format, this specification  ← what travels
        ↓  as bytes         binary / text                   encodings of the document
        ↓
the constructs              this specification              what a program is made of
        ↓
a runtime                   Swift, Kotlin, …                implementations. Many, replaceable
```

- A **front end** turns what a person wrote into a document. Its input syntax
  and its shorthands are its own; its output is this specification's. A front
  end owes nothing to any runtime and never produces anything runnable.
- The **document** is a program written down: a tree of data whose keys and
  slots this specification fixes. It is the only thing that crosses machines.
- An **encoding** is bytes for that tree. Two are specified in [encodings](encoding.md); a document
  is the same document in either of them.
- A **runtime** reads documents, checks, links and runs them, and brings the
  host's vocabulary. How it holds a program in memory is its own business.

## Conformance language

**must / must not** are requirements. **refuses** means the implementation
raises an error naming what was wrong and produces nothing else. No partial
value, no best guess, no reading what it recognised and skipping the rest.

Refusals happen at one of three stages, and the stage is part of the behaviour:

1. **Reading**. The bytes or the tree are not a document.
2. **Building**. The document is a document, and the program it writes is not
   sound: a name resolves nowhere, a call does not fit the declaration it
   reaches, a procedure no module provides. Nothing has run yet.
3. **Running**. The program was sound and the world disagreed: division by
   zero, overflow, a failure a procedure raised.

**Note.** A paragraph opening with **Note.** is not a requirement. It says
what a rule is for, what an implementation is likely to get wrong, or what the
rule would cost written another way. Removing every one of them removes
nothing an implementation is held to, and the cases under `conformance/` never
measure one.

Two implementations that run the same programs identically and disagree about
which programs to refuse, or *where*. Are not the same language. A refusal at
the run where another implementation refuses at the build means something
already happened, and what already happened cannot be taken back.

The cases under `conformance/` name the stages **`load`**, **`build`** and
**`run`**. `load` is reading plus the half of the checking a document answers
alone. A document is checked as it is loaded, and to a caller the two are one
refusal surface; `build` is everything that needs the other documents.
Procedures, declared type names, signatures; `run` is running. So a `ref` that
resolves nowhere in its own document refuses at `load`, and a procedure no
module declares refuses at `build`.

Building is compiling and linking, the way it is anywhere else. Compiling
settles what each document says on its own, against the interfaces of the
documents it reaches. Linking lays the compiled documents down together and
answers what only the list can answer, such as which type answers which
contract. Which of the two refused is not part of the stage, because nothing
has run either way.

## The pages

Each page is one part of the language, and ends with the cases under
`conformance/` that measure it.

| page | what it says |
|---|---|
| [The value model](value.md) | what a value is, and when two are the same |
| [Types](type.md) | what a type is, what a slot takes, membership, ownership |
| [The document format](document.md) | what a document is, and the module it holds |
| [Procedures](procedure.md) | a declaration, what the host answers, what answers without running, a parameter |
| [Statements](statement.md) | what a statement is, and the constructs |
| [Expressions](expression.md) | what is read rather than run |
| [What an implementation checks, and when](checking.md) | which stage answers which refusal |
| [Running](running.md) | what a run does, and what it may not do |
| [The standard vocabulary](vocabulary.md) | the procedures every implementation brings |
| [Encodings](encoding.md) | bytes for a document: `.warp` and `.warpt` |
| [Conformance](conformance.md) | what a case is, and what a runner does |
| [Known gaps](gap.md) | where these pages still owe an implementation |

## Where to start

The pages can be read in any order and cannot be *built* in any order. What
follows is the order in which each one's questions become answerable, which is
also the order in which an implementation can keep its tests green as it grows.

1. [The value model](value.md) and [Encodings](encoding.md). A value and its
   bytes owe nothing to anything else here, and until they read and write a
   reader has no document to hand the rest of the work.
2. [The document format](document.md), [Procedures](procedure.md),
   [Statements](statement.md) and [Expressions](expression.md). The grammar.
   Reading one of these turns bytes into declarations, and what refuses here
   refuses without any other document present.
3. [Types](type.md). What a slot takes, judged against the declarations the
   grammar read.
4. [What an implementation checks, and when](checking.md). The list is the
   contract: two implementations can agree on every answer and still not be
   the same language if one of them refuses later than the other.
5. [Running](running.md) and [The standard vocabulary](vocabulary.md). What a
   sound program does, and the procedures it does it with.
6. [Conformance](conformance.md). The cases, which by then are the only thing
   worth asking whether the work is finished.

A reader looking for *why* rather than *what* has two entry points that are
neither grammar nor rules: **What Warp is** above, which says what the language
is for, and [Known gaps](gap.md), which says where these pages still leave an
implementation to guess.
