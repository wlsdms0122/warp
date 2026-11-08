# WARP-57: What a document stands on

Status: accepted

## Summary

What a document stands on is the documents declaring what it names, those they stand on, and the claims they import. The rules decide that conformance is judged at the build against those claims, and that a door and a cast judge against every claim the link holds.

## Motivation

Read against the whole link, one document would build or refuse depending on which other documents were handed beside it, and the object it builds to could not be keyed by the document and its dependencies alone.

## Rules

**A document stands on** the documents declaring what it names, on the documents those stand on, and on the claims it and they import: a claim imported is the claim, every copy of it the link holds, and not what the documents making it stand on, since the copies are one claim.

**A claim is imported by its pair**, under *a claim imported* in [the imports list](../WARP-10/SPEC.md).

**Whether a type conforms to a contract is judged at the build**, against the claims made within what the asking document stands on, the language's among them: a reading of a type no claim there is about, or one the claim's head does not take, conforms to nothing, and **refuses at the build** where it is handed. So what a document builds to is a fact of it and of what it stands on, whatever else the link holds.

**A door and a cast judge what arrives against every claim the link holds**, since what arrives is no reading any one document asked. A fold runs at the build, before any of that arrives, and holds a value to the claims within its document's reach, under [what a constant folds from](../WARP-16/SPEC.md).

**A claim is judged where it is written**, against what its document stands on, whether or not anything asks the contract of the type: one that does not hold under [a claim holds to members](../WARP-56/SPEC.md), [associated types](../WARP-59/SPEC.md) and [what the build decides](../WARP-66/SPEC.md) **refuses at the build, at the claim**.

**A claim's two names are declared as what it needs of them.** A claim whose type the link declares as a contract, or whose contract it declares as a type, **refuses at the build, at the claim**. One name has one declarer, so no document arriving later makes that right.

**A type conforms to a contract one way.** Two documents claiming one type a contract under heads that take the same values are one claim: a claim holds nothing but the values and the contract, so the second says what the first said, whether it writes the head alike or as `App.Box<some U: Hashable>` beside `App.Box<some T: Hashable>`, through an alias, or as the type applied to its own parameters under its own bounds beside the bare name. Claims across documents under heads taking different values, `Array<Int>` and `Array<String>`, **refuse at the build**. One document says each thing one way, so it claiming one type a contract under a second head, however that head is spelled, **refuses at the load**.

## Interactions

- An associated type is read within the same reach, under [associated types](../WARP-59/SPEC.md).
- A document's identity and dependencies are under [identity and dependencies](../WARP-91/SPEC.md).

## Alternatives considered

- Conformance settled only at the link, across every claim the link holds. An associated type needs its type when the document builds, which the link comes too late to give.

## Notes
