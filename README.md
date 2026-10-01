# Warp

A runtime build system: front ends, an IR and runtimes, where any front end works with any runtime. It is for the boundary between a running program and code that arrives after the program was built. Warp defines that boundary as a language, so each program does not design its own.

An ordinary language goes one way:

```
source  ->  build  ->  machine code
```

Warp is the half in front of that:

```
source  ->  build  ->  IR        (Warp)
                       IR  ->  build  ->  machine code   (the runtime's own toolchain)
```

It takes a language, builds it, and answers with a language again: the IR document. The runtime builds that document when it arrives and runs it. The ordinary toolchain that built the runtime is what reaches machine code, and Warp has no part in that half.

## Why it exists

A compiled application runs the code it shipped with. To change what it does without shipping again, it exposes what it can do and accepts something written against that: a screen description, a workflow file, a rules document. Each is a boundary between a host and a program.

Warp is that boundary as a language. A host declares the procedures it can answer, its **vocabulary**. A program arrives as a **document** written against that vocabulary. The host **builds** the document before any of it runs. The build checks every call against the declaration it reaches, and every type and claim, and refuses what does not hold. What passes runs, and reaches only what the host declared.

Two roles meet at this boundary:

- whoever **implements** a host writes procedures in the host's language and declares them. A module of vocabulary is declarations and the code behind them.
- whoever **provides** programs writes documents through a front end. The syntax is the front end's; the document is the language's.

## Where the work runs

A document holds the flow and the decisions between calls to the vocabulary. Heavy computation is vocabulary, and it runs in the host's language at the host's speed. A document is built where and when it arrives: in the running host, one document at a time, before any of it runs.

## Where it is now

One runtime exists, in Swift, and one front end, for YAML. The cases under `spec/conformance/` are the specification written as data, and a runtime that fails one does not conform. Hosts lend vocabulary as modules, and programs are written against them.

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

A **front end** turns what a person wrote into a document. A **runtime** reads documents, builds and runs them, and brings the host's vocabulary. The document is the IR and the only thing the two share. A server can author with one front end while applications on two platforms run the documents on two runtimes.

## This repository

| directory | what | is |
|---|---|---|
| [`spec/`](spec/README.md) | the language: constructs, document format, encodings, object format, refusal rules, conformance cases | the specification |
| [`runtime/warp-runtime-swift/`](runtime/warp-runtime-swift/README.md) | `Warp` `WarpSyntax` `WarpStandard` | one runtime |
| [`frontend/warp-frontend-yaml/`](frontend/warp-frontend-yaml/README.md) | `WarpYAML` | one front end |

The specification is the language. An implementation, this runtime included, is complete when it does what the specification says. A front end or runtime in another language starts from `spec/` and `spec/conformance/`.

## The shortest tour

Author with the front end, run with the runtime. The same steps whether the document crossed a network or a function call:

```swift
import WarpYAML          // authoring side
import WarpSyntax        // arriving side
import Warp
import WarpStandard

let document = try YAMLFrontend().document(from: yaml)   // → canonical document
let module = try Loader().load(                           // read, or refused
    document,
    identity: try Identity.of(document)                   // which document, for refusals
)
let image = try await Builder().build([module] + Module.standard + host)  // built, or refused
let answer = try await Executor(environment: environment).run(image, entry: "greet", arguments: [:])
```

`host` is the vocabulary this host lends, and `environment` is what its procedures reach. A program that stays in Swift can be built from Swift values without a document. A program that travels is written down by `WarpSyntax`, as bytes or as text.
