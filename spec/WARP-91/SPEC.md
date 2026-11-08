# WARP-91: Identity and dependencies

Status: accepted

## Summary

A document is told from another by the SHA-256 digest of its canonical binary writing. The rules decide that the identity is derived and never declared, how an object writes it down, and how dependencies are written by the host's keys.

## Motivation

An object is kept, cached and read back by hosts and implementations that share nothing but the bytes, so which document an object was compiled from has to be something each of them works out from those bytes alone, the same way.

## Rules

A document is told from another by the **digest of its canonical binary writing**, SHA-256 of the bytes the binary writer produces, and by nothing it says about itself. It is derived and never declared. An identity, wherever a value writes one, is bytes: the 32 bytes of the digest. An object does write one down, under `document`, so a reading is handed the identity the object was kept under.

What an object was compiled against is written under `dependencies` by what the host keyed each object under, each key bytes. The language derives nothing there: what tells one compile of a document from another is the host's cache, and the host hands the same key back when it reads the object. An object standing on one the host worked no key out for is not written.

**Note.** A runner keys every object it compiles and every case's document is written down, so an object standing on one with no key, or holding a closure written by a document nobody wrote down or a box of the run that made it, is not written, under the rule above and [values, in an object](../WARP-90/SPEC.md), and that is held only by tests inside the implementation.

## Interactions

- The canonical binary writing is [the binary encoding](../WARP-6/SPEC.md), under the promises of [encodings](../WARP-5/SPEC.md).
- `document` and `dependencies` are keys of [what an object holds](../WARP-85/SPEC.md), and an object standing against another document refuses under [what a reading refuses](../WARP-92/SPEC.md).
- Whether every object under `dependencies` is beside it is decided at the build under [what the build decides](../WARP-66/SPEC.md).

## Alternatives considered

- A document that declares its name or its identity. A name for a document would be a second namespace beside the spellings a document sends, and a declared identity could disagree with the bytes it names.
- Judging the build by the dependency keys, refusing an object whose keys leave out a document it stands on. The keys are the host's cache's, and a check reading them would answer one case differently on a host that writes no keys.

## Notes
