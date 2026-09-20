# Warp

A runtime build system. A front end, an IR and a runtime, composed so that any
front end works with any runtime.

An ordinary language goes one way:

```
source  ->  build  ->  machine code
```

Warp is the half in front of that:

```
source  ->  build  ->  IR        (Warp)
                       IR  ->  build  ->  machine code   (the runtime's own toolchain)
```

It takes a language, builds it, and answers with a language again. That answer
is the IR document, and what turns the document into machine code is the
ordinary toolchain that built the runtime. Warp has no part in that half.

Its product being another language rather than something a processor executes
is why this is a build system and not a compiler.

## Why it exists

A compiled application cannot run code it did not ship with. There is no
compiler at run time, and on the platforms this exists for there is no way to
acquire one. Warp is how a decision reaches a running program without
rebuilding and re-shipping it: the program arrives as a **document**, is
**checked before any of it runs**, and runs inside a runtime the receiver
controls, reaching nothing the receiver did not hand it.

## Where it is now

One runtime exists, in Swift. The IR is being settled on top of it, so the
specification moves where the runtime shows it has to.

## The pieces

```
what a person writes      YAML, a syntax of your own, …    front ends. Many
        ↓
the document              one format, defined in spec/     ← what travels
        ↓  as bytes       binary · text                    encodings
        ↓
a runtime                 Swift today, others by spec       runtimes. Many
        ↓
an object                 one format, defined in spec/     ← what a build keeps
```

A **front end** turns what a person wrote into a document and stops there. A
**runtime** reads documents, checks, links and runs them, and brings the host's
vocabulary. The document is the IR, and it is the only place the two meet. A
server can author with one front end while two applications on two platforms
run with another, and none of them share code.

## This repository

| directory | what | is |
|---|---|---|
| [`spec/`](spec/README.md) | the language: constructs, document format, encodings, object format, refusal rules, conformance cases | the specification |
| [`runtime/warp-runtime-swift/`](runtime/warp-runtime-swift/README.md) | `Warp` `WarpSyntax` | one runtime |
| [`frontend/warp-frontend-yaml/`](frontend/warp-frontend-yaml/README.md) | `WarpYAML` | one front end |

The specification is the language. An implementation. This runtime included. Is
complete when it does what the specification says, and no more complete for
doing anything else. A front end or runtime in another language starts from
`spec/` and `spec/conformance/`, not from the Swift source.

## The shortest tour

Author with the front end, run with the runtime. The same two steps whether
the document crossed a network or a function call:

```swift
import WarpYAML          // authoring side
import WarpSyntax      // arriving side
import Warp

let loader = Loader()
let document = try YAMLFrontend().document(from: yaml)   // → canonical document
let module = try loader.load(                             // checked, or refused
    document,
    identity: try Identity.of(document)                   // which document, for refusals
)
let image = try loader.reading {                          // refusals in the
    try Builder().build([module] + Module.standard, entry: "greet")  // document's procedures
}
let answer = try await Executor().run(image)
```

A program that stays in Swift skips the document entirely and builds the program
directly; a program that travels is written down by `WarpSyntax`. Bytes to carry
it, text to read it.
