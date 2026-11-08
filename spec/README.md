# The Warp specification

Warp is a language, and this is where the language is. Its implementations live in repositories of their own, and nothing they do adds to the language. Where a decision lands a cost on one, or where the suite cannot hold a rule, the WARP that makes the decision says so in a **Note.**, so a second implementation is told rather than left to find it.

This describes **Warp 0.1.0**.

These WARPs are written the way a protocol is written: they say what a conforming implementation **must** do, field by field and byte by byte, and the cases under each WARP's `conformance/` are the same statements as data.

## What Warp is

A runtime build system: a front end, an IR and a runtime, composed so that any front end works with any runtime. This specification is the IR, the language a front end writes and a runtime builds. Turning it into machine code belongs to the toolchain that built the runtime.

What a build does here is what a build does anywhere. It reads, it checks, it links, and nothing runs until it has finished. The three things that differ are **when**, **where** and **how much at a time**: the build runs while a program is already running, on the machine the program is running on, and one document at a time.

What the language is *for*, and every property below that follows from it:

A language for programs that arrive after the program running them was built.

A compiled application cannot run code it did not ship with. Handed a source file at run time it has no compiler, and on the platforms this exists for it may not acquire one, so the only way a decision reaches a running program without rebuilding and re-shipping it is for something inside to read that decision and carry it out. Warp is what that something reads.

Everything else follows from *arrive*:

- **The program comes from elsewhere**, so nothing arrives with it that says it was checked. There is no place to put such a thing that the host could read, so the host builds it.
- **The program crosses machines as bytes**, so there is a document format, and the two ends have to agree about what the bytes say.
- **The sender and the host may be different implementations** (a server in one language, two applications in two others), so agreement cannot mean "the same code".
- **What a program may do is the host's to set**, since the host assembles the modules and a document cannot name what nobody put in front of it.

What bounds it is the vocabulary. A program does exactly what the procedures in its link let it do, and every procedure past the ones this specification spells is one the host put there. The language checks what a program *sends*; what a native procedure does is the host's. So a host draws its line once, where it assembles the modules, and a module of native procedures reaches whatever the host code implementing them reaches.

**The boundary is this specification's.** Everything that crosses between a host and a program is fixed here and nowhere else: what a value is ([values](WARP-2/SPEC.md)), how a host's procedure is declared and what it is handed ([procedures](WARP-14/SPEC.md)), what a failure carries ([statements](WARP-25/SPEC.md)), who may name a declaration, and what is checked before anything runs ([checking](WARP-65/SPEC.md)). A host declares procedures against these WARPs and designs no protocol of its own; a front end writes documents against them and designs no protocol either. What a document holds is the flow between the procedures a host declared, and what the host declares holds the work.

## The pieces

```
what a person writes        YAML, a syntax of your own, …   front ends, replaceable
        ↓
the document                one format, this specification  ← what travels
        ↓  as bytes         binary / text                   encodings of the document
        ↓
a runtime                   a host language                 implementations
        ↳ an object         one format, this specification  ← what its build keeps
```

- A **front end** turns what a person wrote into a document. Its input syntax and its shorthands are its own; its output is this specification's. A front end owes nothing to any runtime and never produces anything runnable.
- The **document** is a program written down: a tree of data whose keys and slots this specification fixes. It is the only thing that crosses machines.
- An **encoding** is bytes for that tree. Two are specified in [encodings](WARP-5/SPEC.md); a document is the same document in either of them.
- A **runtime** reads documents, checks, links and runs them, and brings the host's vocabulary. How it holds a program in memory is its own business.
- An **object** is one document compiled, written down so that any implementation reads what any other wrote, under [objects](WARP-85/SPEC.md). It is what a build keeps or hands to a cache; what travels is the document.

## Conformance language

**must / must not** are requirements. **refuses** means the implementation raises an error naming what was wrong and produces nothing else. No partial value, no best guess, no reading what it recognised and skipping the rest.

Refusals happen at one of three stages, and the stage is part of the behaviour:

1. **Loading**. The bytes or the tree are not a document, or the document does not hold together on its own: a name resolves nowhere in it, a statement follows a leave, its `imports` list is not what its program uses.
2. **Building**. The document holds together, and the program it writes is not sound against the declarations it reaches: a call does not fit the declaration, a procedure no module provides, a type nobody declared. Nothing has run yet.
3. **Running**. The program was sound and the run went past what it holds: division by zero, overflow, an index or a key that is not there, a value its slot does not take at a door.

**Note.** A paragraph opening with **Note.** is not a requirement. It says what a rule is for, what an implementation is likely to get wrong, or what the rule would cost written another way. Removing every one of them removes nothing an implementation is held to, and the cases under `conformance/` never measure one.

**How the WARPs write examples.** A dictionary in braces, `{ ref: "x" }`, shows a part of a document's tree, and brackets, `[1, "s"]`, show a list value; neither is an encoding. An example in parentheses, `(array 1 "s")`, is the text, under [the text](WARP-37/SPEC.md).

Two implementations that run the same programs identically and disagree about which programs to refuse, or *where*, are not the same language. A refusal at the run where another implementation refuses at the build means something already happened, and what already happened cannot be taken back.

The cases under `conformance/` name the stages **`load`**, **`build`** and **`run`**. `load` is reading plus the checks a document decides alone, listed in [checking](WARP-65/SPEC.md). A document is checked as it is loaded, and to the host the two are one refusal surface. `build` is everything judged against a signature or another document: what a call fits, what a slot takes, which module declares a procedure, which type conforms to a contract. `run` is running. Each rule names its stage: a `ref` that resolves nowhere in its own document refuses at `load`, a call in that same document handing a value of the wrong type refuses at `build`, and a procedure no module declares refuses at `build`. A rule about two declarations of one spelling names two: `load` where both are in one document, which that document decides alone, and `build` where they are in two, as a compiler refuses a redefinition within a module and a linker a duplicate symbol across modules.

Building is compiling and linking, the way it is anywhere else. Compiling judges what each document says on its own, against the interfaces of the documents it reaches. Linking lays the compiled documents down together and decides what only the list can decide, such as which type conforms to which contract. Which of the two refused is not part of the stage, because nothing has run either way.

## How WARPs work

The rules are a series of WARPs. A WARP is one rule family: `WARP-N/SPEC.md` states it, and `WARP-N/conformance/` holds the cases that measure it, each a file named `<name>.test.warpt`. Beside this page and the template, `spec/` holds the review in [`review/`](review/README.md) and a folder for each WARP, and nothing else. A case's name is unique across the specification, so a case is found by its name without its folder. A WARP takes the next number when it is drafted, a number is never reused, and the number says nothing else about it.

A `SPEC.md` takes the shape [the template](TEMPLATE.md) gives: a summary, the motivation, the rules, which are its only normative part, where they meet the rest of the language, the alternatives not taken, and notes. Every `SPEC.md` holds every section, and a section with nothing to say is left empty. It opens with `# WARP-N:` and its title, then its status:

- **`draft`**: not part of the language. It is changed freely and nothing is held to it. A draft that is not accepted is deleted.
- **`accepted`**: part of the language. A draft is accepted when it meets [the acceptance criteria](review/CRITERIA.md), which a review checks one by one.

**How a rule is written.** A rule gives a form whole, the way a drawing gives a part's dimensions and not only its material. What a name, a spelling, a node or a byte layout may be is a grammar, in the notation [names](WARP-67/SPEC.md) uses, or a table, and the prose beside it says what each part means. A rule says what a thing is. It is not written against the one input that raised it, such as "a procedure's name holds no `:`": that input is a case, and why the form is what it is goes in a **Note.**

An accepted WARP is supplemented in place: its prose made clearer, its cases added to or corrected. A change that would give any of its existing cases another answer is not a supplement. It is a new WARP that replaces the old one whole and says so on the line after its status, `Supersedes: WARP-a, WARP-b`. Nothing replaces part of a WARP. A WARP is superseded when an accepted WARP names it under `Supersedes`, and when that WARP is accepted, the superseded one says so on its own head, `Superseded-By: WARP-c`, so whoever opens it sees at once that it no longer holds. Its text is not touched. `spec-series accept` writes that line, and `spec-series lint` sees that the two agree. Until Warp's first release, an accepted WARP is changed in place even when a case's answer moves.

A draft makes the changes it needs in accepted WARPs beside it, before it is reviewed: a supplement in place, and a WARP whose decision moves named under its `Supersedes`. The review reads the draft with those changes.

The language is every accepted WARP that no accepted WARP supersedes, and a runner runs the cases of those and no others. Which WARPs they are is worked out from the series by a tool and never written down. A runtime that pins a version of this specification conforms to it when it passes the cases of every such WARP at that version.

The WARPs can be read in any order and cannot be *built* in any order. The order in which each one's questions can be decided is the order of their areas, which is also the order in which an implementation can keep its tests green as it grows. Conformance comes first, since every other WARP's cases are written in it. Then values and their bytes, which owe nothing to anything else; the grammar of documents, procedures, statements and expressions, and the text that writes that grammar as nodes; types, what a slot takes, judged against the declarations the grammar read; what an implementation checks, and when; running and the standard vocabulary; and objects, what the build writes down.

A reader looking for *why* rather than *what* has two entry points that are neither grammar nor rules: **What Warp is** above, which says what the language is for, and the **Note.** paragraphs, which say what a rule is for and where a decision lands a cost on an implementation.
