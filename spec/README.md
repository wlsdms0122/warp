# The Warp specification

Warp is a language, and this is where the language is. The directories beside this one hold implementations of it; nothing they do adds to the language. [Known costs](cost.md) says where a decision lands a cost on one.

This describes **Warp 0.1.0**. Nothing has shipped: no document exists anywhere this specification does not control.

These pages are written the way a protocol is written: they say what a conforming implementation **must** do, field by field and byte by byte, and the cases under `conformance/` are the same statements as data.

## What Warp is

A runtime build system: a front end, an IR and a runtime, composed so that any front end works with any runtime. This specification is the IR, the language a front end writes and a runtime builds. Turning it into machine code belongs to the toolchain that built the runtime.

What a build does here is what a build does anywhere. It reads, it checks, it links, and nothing runs until it has answered. The three things that differ are **when**, **where** and **how much at a time**: the build runs while a program is already running, on the machine the program is running on, and one document at a time.

What the language is *for*, and every property below that follows from it:

A language for programs that arrive after the program running them was built.

A compiled application cannot run code it did not ship with. Handed a source file at run time it has no compiler, and on the platforms this exists for it may not acquire one, so the only way a decision reaches a running program without rebuilding and re-shipping it is for something inside to read that decision and carry it out. Warp is what that something reads.

Everything else follows from *arrive*:

- **The program comes from elsewhere**, so nothing arrives with it that says it was checked. There is no place to put such a thing that the host could read, so the host builds it.
- **The program crosses machines as bytes**, so there is a document format, and the two ends have to agree about what the bytes say.
- **The sender and the host may be different implementations** (a server in one language, two applications in two others), so agreement cannot mean "the same code".
- **What a program may do is the host's to set**, since the host assembles the modules and a document cannot name what nobody put in front of it.

What bounds it is the vocabulary. A program does exactly what the procedures in its link let it do, and every procedure past the ones this specification spells is one the host put there. The language checks what a program *sends*; what answering a procedure means is the host's. So a host draws its line once, where it assembles the modules, and a module of procedures the host answers reaches whatever host code reaches there.

**The boundary is this specification's.** Everything that crosses between a host and a program is fixed here and nowhere else: what a value is ([values](value.md)), how a host's procedure is declared and what it is handed ([procedures](procedure.md)), what a failure carries ([statements](statement.md)), who may name a declaration, and what is checked before anything runs ([checking](checking.md)). A host declares procedures against these pages and designs no protocol of its own; a front end writes documents against them and designs no protocol either. What a document holds is the flow between the procedures a host declared, and what the host declares holds the work.

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

- A **front end** turns what a person wrote into a document. Its input syntax and its shorthands are its own; its output is this specification's. A front end owes nothing to any runtime and never produces anything runnable.
- The **document** is a program written down: a tree of data whose keys and slots this specification fixes. It is the only thing that crosses machines.
- An **encoding** is bytes for that tree. Two are specified in [encodings](encoding.md); a document is the same document in either of them.
- A **runtime** reads documents, checks, links and runs them, and brings the host's vocabulary. How it holds a program in memory is its own business.

## Conformance language

**must / must not** are requirements. **refuses** means the implementation raises an error naming what was wrong and produces nothing else. No partial value, no best guess, no reading what it recognised and skipping the rest.

Refusals happen at one of three stages, and the stage is part of the behaviour:

1. **Loading**. The bytes or the tree are not a document, or the document does not hold together on its own: a name resolves nowhere in it, a statement follows a leave, its `imports` list is not what its program uses.
2. **Building**. The document holds together, and the program it writes is not sound against the declarations it reaches: a call does not fit the declaration, a procedure no module provides, a type nobody declared. Nothing has run yet.
3. **Running**. The program was sound and the run went past what it holds: division by zero, overflow, an index or a key that is not there, a value its slot does not take at a door.

**Note.** A paragraph opening with **Note.** is not a requirement. It says what a rule is for, what an implementation is likely to get wrong, or what the rule would cost written another way. Removing every one of them removes nothing an implementation is held to, and the cases under `conformance/` never measure one.

Two implementations that run the same programs identically and disagree about which programs to refuse, or *where*, are not the same language. A refusal at the run where another implementation refuses at the build means something already happened, and what already happened cannot be taken back.

The cases under `conformance/` name the stages **`load`**, **`build`** and **`run`**. `load` is reading plus the checks a document answers alone, listed in [checking](checking.md). A document is checked as it is loaded, and to the host the two are one refusal surface. `build` is everything judged against a signature or another document: what a call fits, what a slot takes, which module declares a procedure, which type answers a contract. `run` is running. The stage is the rule's and not the program's: a `ref` that resolves nowhere in its own document refuses at `load`, a call in that same document handing a value of the wrong type refuses at `build`, and a procedure no module declares refuses at `build`.

Building is compiling and linking, the way it is anywhere else. Compiling judges what each document says on its own, against the interfaces of the documents it reaches. Linking lays the compiled documents down together and answers what only the list can answer, such as which type answers which contract. Which of the two refused is not part of the stage, because nothing has run either way.

## The pages

Each page is one part of the language, and each page of rules ends with the cases under `conformance/` that measure it.

| page | what it says |
|---|---|
| [The value model](value.md) | what a value is, and when two are the same |
| [Types](type.md) | what a type is, what a slot takes, type parameters, contracts |
| [The document format](document.md) | what a document is, and the module it holds |
| [Procedures](procedure.md) | a declaration, what the host answers, what answers without running, a parameter |
| [Statements](statement.md) | what a statement is, and the constructs |
| [Expressions](expression.md) | what is read rather than run |
| [What an implementation checks, and when](checking.md) | which stage answers which refusal |
| [Running](running.md) | what a run does, and what it may not do |
| [The standard vocabulary](vocabulary.md) | the procedures every implementation brings |
| [Encodings](encoding.md) | bytes for a value tree: `.warp` and `.warpt` |
| [The text](text.md) | a document and a case written as the IR's own nodes |
| [Objects](object.md) | what a build writes down, laid out so any implementation reads any other's |
| [Conformance](conformance.md) | what a case is, and what a runner does |
| [Known costs](cost.md) | where a decision lands a cost on an implementation |

## Where to start

The pages can be read in any order and cannot be *built* in any order. What follows is the order in which each one's questions become answerable, which is also the order in which an implementation can keep its tests green as it grows.

1. [The value model](value.md) and [Encodings](encoding.md). A value and its bytes owe nothing to anything else here, and until they read and write a reader has no document to hand the rest of the work.
2. [The document format](document.md), [Procedures](procedure.md), [Statements](statement.md) and [Expressions](expression.md). The grammar. Reading one of these turns bytes into declarations, and what refuses here at the load refuses without any other document present. [The text](text.md) writes the same grammar as nodes.
3. [Types](type.md). What a slot takes, judged against the declarations the grammar read.
4. [What an implementation checks, and when](checking.md). The list is the contract: two implementations can agree on every answer and still not be the same language if one of them refuses later than the other.
5. [Running](running.md) and [The standard vocabulary](vocabulary.md). What a sound program does, and the procedures it does it with.
6. [Objects](object.md). What the build above writes down, which is the whole of it laid out as a value, and so the last thing that can be.
7. [Conformance](conformance.md). The cases, and the runner that asks them.

A reader looking for *why* rather than *what* has two entry points that are neither grammar nor rules: **What Warp is** above, which says what the language is for, and [Known costs](cost.md), which says where a decision lands a cost on an implementation.
