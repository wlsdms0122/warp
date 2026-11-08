# WARP-35: A constant-headed path

Status: accepted

## Summary

A constant-headed path is one whose head names a constant of its document. The rules decide how it is judged like any path, what type it reads as, and when it folds at the build.

## Motivation

A constant is read at the build, so a path headed by one is the IR's to judge and to fold. `{ ref: "limits.max" }` on a module constant reads as the type its folded value has and becomes that value in the image, and two runtimes agree on what it reads, and on which reads refuse before anything runs, only if the language says when it folds and what it reads as. A front end cannot fold it in its place, since the constant's value may come from a call only the link provides.

## Rules

**A constant-headed path**, one whose head names a constant of its document rather than a name a body introduced under that spelling, is judged first like any path: the constant's type is its folded value's, so an absent field or a needless `?.` refuses by the same rules, and the path reads as the type its place in that type has: a field its own, and an element or an entry the list's or dictionary's one element type, which joins every element's, so `k[0]` of `[1, "s"]` reads `Any`. A procedure the value holds, whole or as a field, reads as the procedure type its expression was judged at, the constness, isolation and failing its signature declares included. A call of it is judged by the parameters and return type that type writes. Then it folds at the build to the value it read, except where an index on it is a reference the run reads (`digits[ch]`, `ch` a parameter): there the run reads the constant's value past the index the way it reads any name, by the rules above. A fold that finds no value where the path reads, a position a list does not hold or a key a dictionary holds no entry under at a step that does not expect its absence, has nothing to fold to, and the path **refuses at the build**; where `?[` expects it, the path folds to the none, under [null is not read through](../WARP-34/SPEC.md). What a constant may fold from is under *what a constant folds from* in [procedures](../WARP-16/SPEC.md), and a body **its own document** declares is not among them: such a body is itself still being resolved beside the constants it may read, so a constant that runs one would be a cycle with no start, and it refuses at the build. Folding asks the procedures this specification names, which every implementation brings, the builtin ones as native procedures and the rest written in Warp in `lib/standard`, so a link provides them before any of the program runs.

## Interactions

- A constant between brackets: [brackets](../WARP-36/SPEC.md).
- The procedures written in Warp in `lib/standard`: [the standard vocabulary](../WARP-74/SPEC.md).

## Alternatives considered

- Refusing a constant-headed path whose index the run reads. A front end would then bind the constant to a name before reading it, which pushes onto every front end what the build can do in place.

## Notes
