# Warp

A runtime build system: front ends, an IR and runtimes, where any front end works with any runtime. It is for the boundary between a running program and code that arrives after the program was built. Warp defines that boundary as a language, so each program does not design its own.

A front end writes a program as an IR document, the language the specification under `spec/` describes. A runtime builds that document where it arrives, the whole of it before any of it runs, and runs it.

## Why it exists

A compiled application runs the code it shipped with. To change what it does without shipping again, it exposes what it can do and accepts something written against that: a screen description, a workflow file, a rules document. Each is a boundary between a host and a program.

Warp is that boundary as a language. A host declares the procedures it implements, its **vocabulary**. A program arrives as a **document** written against that vocabulary. The host **builds** the document before any of it runs. The build checks every call against the declaration it reaches, and every type and claim, and refuses what does not hold. What passes runs, and reaches only what the host declared.

Two roles meet at this boundary:

- whoever **implements** a host writes procedures in the host's language and declares them. A module of vocabulary is declarations and the code behind them.
- whoever **provides** programs writes documents through a front end. The syntax is the front end's; the document is the language's.

## Where the work runs

A document holds the flow and the decisions between calls to the vocabulary. Heavy computation is vocabulary, and it runs in the host's language at the host's speed. A document is built where and when it arrives: in the running host, one document at a time, before any of it runs.

## The pieces

The specification draws them in [the pieces](spec/README.md#the-pieces). A **front end** turns what a person wrote into a document. A **runtime** reads documents, builds and runs them, and brings the host's vocabulary. The document is the IR, and it and the interfaces of the modules a document calls into, under [the text](spec/TEXT.md), are all the two share. A server can author with one front end while applications on two platforms run the documents on two runtimes.

## This repository

| directory | what |
|---|---|
| [`spec/`](spec/README.md) | the language: constructs, document format, encodings, object format, refusal rules, conformance cases |
| [`lib/standard/`](lib/standard) | the part of the standard vocabulary written in Warp, and in [`interface/`](lib/standard/interface) the vocabulary's interface: every declaration it makes, without its implementation |
| [`example/`](example/README.md) | programs written in Warp, and the vocabulary a host lends them |

Implementations live in repositories of their own:

| repository | is |
|---|---|
| `warp-runtime-swift` | one runtime |
| `warp-frontend-yaml` | one front end |

The specification is the language, and the cases under `spec/conformance/` are the specification written as data. An implementation is complete when it does what the specification says, and a runtime that fails a case does not conform. A front end or runtime in another language starts from `spec/` and `spec/conformance/`.

## Using it

Each implementation's README says how to use it: `warp-frontend-yaml`'s how to write a document from YAML, and `warp-runtime-swift`'s how to read, build and run one with the vocabulary a host lends. Whether a document crossed a network or a function call, it arrives the same way: it is read, built whole, and only then run, and each of the three may refuse it, under [the specification](spec/README.md).
