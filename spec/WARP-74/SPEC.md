# WARP-74: The standard vocabulary

Status: accepted

## Summary

The standard vocabulary is the procedures every implementation brings. The rules decide which bundles exist, what each depends on, what each procedure returns, and which an implementation must write in its own language.

## Motivation

A document that calls `Standard.Math.min` has to run on every implementation without its author fetching anything. What reaches outside the run, a file, a clock, a network, cannot be in the vocabulary: an obligation is in every link, and a procedure every program holds is no longer something a host grants.

## Rules

The procedures every implementation brings, what each returns, and which of them an implementation has to write in its own language rather than take from `lib/standard`. This is the layer a program does its work in: the language has no arithmetic, no comparison and no collections of its own, and a program that is granted none of these can compute nothing.

Eight bundles, each taken with what it depends on, so a host grants what its programs have use for and no more. What a bundle depends on is what its written half sends and what its signatures mention, and the written half's `imports` is the list. `Standard` is the shared ground: the contracts `Standard.Numeric`, `Standard.Comparable` and `Standard.Collection`, the claims putting the types the language names under them, and the procedures backing those claims. Every bundle below links with `Standard` in the link, and a document calling a contract's procedure stands behind it, so what the call reaches stands before the document does. Beyond that, `Standard.Math`, `Standard.Logic`, `Standard.Optional` and `Standard.Control` stand alone; `Standard.Collection` links with `Standard.Logic`; `Standard.Concurrent` with `Standard.Collection`; `Standard.Text` with `Standard.Collection`, `Standard.Control` and `Standard.Logic`. Two bundles that send to each other are not a cycle, because a bundle is not a module, below:

| bundle | procedures |
|---|---|
| `Standard` | The contracts [below](../WARP-77/SPEC.md), the claims putting the types the language names under them, and the procedures backing those claims: `Int.plus` `Int.minus` `Int.times` `Int.dividedBy` `Int.remainder` `Int.lessThan`, the same six for `Double`, `String.lessThan`, and `Array.count` `Dictionary.count` `String.count` |
| `Standard.Logic` | `equal` `notEqual` `not` `and` `or` `select` `tryAnd` `tryOr` `trySelect` |
| `Standard.Math` | `min` `max` `absolute` `floored` `rounded` `greaterThan` |
| `Standard.Text` | `text` `characters` `contains` `startsWith` `uppercased` `lowercased` `trimmed` `split` `joined` `replacing` `decoded` `encoded` |
| `Standard.Collection` | `append` `contains` `first` `last` `reversed` `appending` `prepending` `gathering` `dropFirst` `dropLast` `sorted` `map` `filter` `reduce` `tryMap` `tryFilter` `tryReduce` `keys` `values` `setting` |
| `Standard.Optional` | `unwrapped` `tryUnwrapped` |
| `Standard.Control` | `abort`. Nothing runs after it |
| `Standard.Concurrent` | `all` `allKeyed` `first` `firstKeyed` `map`. Run closures at once |

What each procedure is called is a name under [names](../WARP-67/SPEC.md#the-grammar):

| procedure | what it is called |
|---|---|
| one the row of a bundle other than `Standard` lists | a procedure's name: the bundle's name, `.` and the name the row gives, `Standard.Math.min` |
| a member `Standard` gives | a member's spelling: `Int.plus` |
| a contract's procedure | a contract's procedure's spelling: `Standard.Numeric.plus` |

### What an implementation must write

Not all of these. Most are written in Warp, from a small set that cannot be: **builtin**. An implementation writes the builtin procedures in its own language and takes the rest as a Warp module, the way any other module arrives.

| bundle | builtin |
|---|---|
| `Standard` | every member it gives: arithmetic, ordering and counting for each type it claims a contract for |
| `Standard.Logic` | `equal` |
| `Standard.Math` | `floored` |
| `Standard.Text` | `text` `joined` `characters` `uppercased` `lowercased` `encoded` `decoded` `trimmed` |
| `Standard.Collection` | `appending` `gathering` `keys` `setting` |
| `Standard.Control` | `abort` |
| `Standard.Concurrent` | `all` `allKeyed` `first` `firstKeyed` |

Thirty-five, beside the contracts `Standard` declares. What makes one builtin is that the language cannot express it: arithmetic, ordering and counting are the machine's, written once for each type conforming to the contract that asks them, case mapping and encoding carry Unicode's tables with them, running at once is the host's scheduler, `appending` is the only way an array grows, and `gathering` the only way a return value holds a collection's own elements in their spelling. Everything else is written from those.

`greaterThan` is written from `lessThan`, with its sides swapped, and takes `lhs` and `rhs` as `lessThan` does.

`rounded` is written from `floored`: what is left of the number above its floor is exact in binary64, so a body compares it with `0.5` and tells the exact halfway apart, under [Standard.Math](../WARP-78/SPEC.md).

`trimmed` is builtin beside `characters` because a body written from `characters` could not compute it: whether a character is white space is a question about the code points inside it, and `characters` returns characters.

**A bundle is not a module.** A module is compiled against the modules standing before it, so the modules of a link have to have an order, and two that send to each other have none. What a bundle declares for its host to implement has no body and so waits for nothing; what it writes in Warp sends to whatever it needs. So a bundle links as two modules, its builtin half standing before every written half, and the same set of procedures links whatever the written halves send. A bundle with nothing builtin, `Standard.Optional`, links as its written half alone.

**The signatures are the standard vocabulary's interface**, [`lib/standard/interface/standard.interface.warpt`](../../lib/standard/interface/standard.interface.warpt), under *an interface* in [the text](../WARP-43/SPEC.md). It declares every contract, claim and procedure this WARP and [WARP-75](../WARP-75/SPEC.md) to [WARP-84](../WARP-84/SPEC.md) name, builtin or written in Warp alike, and it is the authority for each one's parameters and their order, what each parameter and the procedure return, the bounds, and whether the procedure is `const`, touches no name another body could touch at once (`isolated`) and what it fails with. An implementation brings a standard vocabulary that declares exactly it, and a front end writes calls against it. [WARP-75](../WARP-75/SPEC.md) to [WARP-84](../WARP-84/SPEC.md) say what each procedure does: the *parameters* column names a parameter to say of it what its type does not.

What a host brings beyond these (its own procedures, and which of them are const) is the host's, and is the boundary to the outside world: a program reaches nothing except by sending a procedure the host declared.

## Interactions

- A builtin procedure is a [native procedure](../WARP-14/SPEC.md) whose host is the implementation.
- The order documents stand in, which a bundle's two halves rely on, is [what the build decides](../WARP-66/SPEC.md).
- Linking `Standard.Concurrent` or not is the grant under [concurrency](../WARP-73/SPEC.md).

## Alternatives considered

- Builtin by what an implementation happens to write natively, counted upward by asking of each procedure whether some other derives it. The set then follows accident (a procedure is builtin because nothing else happened to grow an array), and every procedure the vocabulary gains is another obligation.
- A regular-expression procedure. It cannot be written in Warp, and the pattern syntax differs from host to host, so one document would answer differently from host to host. A procedure that is neither builtin nor written does not wear the standard vocabulary's spelling.
- `Standard.Concurrent` left to hosts. Left optional, a document using it would run on some implementations and not others. It reaches nothing outside the run, so bringing it costs no grant: a host still decides whether to link it.

## Notes

**Note.** A contract and a bundle may share a spelling: `Standard.Collection.count` is the contract `Standard.Collection`'s procedure, declared by `Standard`, and the bundle `Standard.Collection` is the bundle whose procedures the table lists in its row.

**Note.** No case can hold which bundles link with which, or which procedures are builtin. A runner builds every case against the standard vocabulary whole, under [conformance](../WARP-1/SPEC.md), no case key chooses a bundle, and a builtin procedure and a written one return alike. The cases hold what each procedure returns.
