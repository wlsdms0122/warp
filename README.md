# Warp

A runtime build system: a front end, an IR and a runtime, composed so that any front end works with any runtime. What it is for is one boundary, the one between a running program and code that arrives after it was built, and what it does is make that boundary the language's rather than each program's.

An ordinary language goes one way:

```
source  ->  build  ->  machine code
```

Warp is the half in front of that:

```
source  ->  build  ->  IR        (Warp)
                       IR  ->  build  ->  machine code   (the runtime's own toolchain)
```

It takes a language, builds it, and answers with a language again. That answer is the IR document, and what turns the document into machine code is the ordinary toolchain that built the runtime. Warp has no part in that half, which is why this is a build system and not a compiler.

## Why it exists

A compiled application cannot run code it did not ship with. Every way of changing what it does without shipping it again ends at the same place: the application has to expose what it can do, and what arrives has to be written against that. A screen description, a workflow file, a rules document. Each of these is a boundary between a host and a program, and each grows conditions, variables and branches until it is a language nobody designed, with no checking and no tools.

Warp is that boundary designed once, as a language. A host declares the procedures it can answer, its **vocabulary**. A program arrives as a **document** written against that vocabulary. The host **builds** the document before any of it runs, checking every call against the declaration it reaches, every type, every claim, and refuses what does not hold. What passes runs, and reaches nothing the host did not declare.

Two people meet at this boundary and neither designs it:

- whoever **implements** a host writes procedures in the host's language and declares them. A module of vocabulary is a declaration and a place it reaches, and nothing else;
- whoever **provides** programs writes documents, through a front end that suits them. The syntax is the front end's, the document is the language's.

## What it is not

It is not a machine. Wasm, a bytecode VM, a JIT: those run code, and the boundary between that code and the host is theirs to design afterwards. Warp starts at the boundary and stays there. Heavy computation belongs to the vocabulary, in the host's language at the host's speed, and what a document holds is the flow and the decisions between those calls: short, and checked.

It is not a script engine. A script can do anything the engine can, and what it will do is found out by running it. A document can do what the vocabulary declares, and what it will do is read before it runs.

## Where it is now

One runtime exists, in Swift. The IR is settled against it and measured by the cases under `spec/conformance/`, which are the specification written as data: a runtime is one when it passes them. One front end exists, for YAML. Hosts lend vocabulary as modules and programs are written against them.

## The pieces

```
what a person writes      YAML, a syntax of your own, …    front ends. Many
        ↓
the document              one format, defined in spec/     ← what travels
        ↓  as bytes       binary · text                    encodings
        ↓
a runtime                 Swift today, others by spec       runtimes. Many
        ↳ an object       one format, defined in spec/     ← what its build keeps
```

A **front end** turns what a person wrote into a document and stops there. A **runtime** reads documents, checks, links and runs them, and brings the host's vocabulary. The document is the IR, and it is the only place the two meet. A server can author with one front end while two applications on two platforms run with another, and none of them share code.

## This repository

| directory | what | is |
|---|---|---|
| [`spec/`](spec/README.md) | the language: constructs, document format, encodings, object format, refusal rules, conformance cases | the specification |
| [`runtime/warp-runtime-swift/`](runtime/warp-runtime-swift/README.md) | `Warp` `WarpSyntax` `WarpStandard` | one runtime |
| [`frontend/warp-frontend-yaml/`](frontend/warp-frontend-yaml/README.md) | `WarpYAML` | one front end |

The specification is the language. An implementation, this runtime included, is complete when it does what the specification says, and no more complete for doing anything else. A front end or runtime in another language starts from `spec/` and `spec/conformance/`, not from the Swift source.

## The shortest tour

Author with the front end, run with the runtime. The same steps whether the document crossed a network or a function call:

```swift
import WarpYAML          // authoring side
import WarpSyntax        // arriving side
import Warp
import WarpStandard

let document = try YAMLFrontend().document(from: yaml)   // → canonical document
let module = try Loader().load(                           // checked, or refused
    document,
    identity: try Identity.of(document)                   // which document, for refusals
)
let image = try await Builder().build([module] + Module.standard + host)  // linked, or refused
let answer = try await Executor(environment: environment).run(image, entry: "greet", arguments: [:])
```

`host` is the vocabulary this host lends, and `environment` is what its procedures reach. A program that stays in Swift skips the document entirely and builds the program directly; a program that travels is written down by `WarpSyntax`. Bytes to carry it, text to read it.
