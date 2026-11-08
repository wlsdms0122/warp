# WARP-83: Standard.Concurrent

Status: accepted

## Summary

Standard.Concurrent runs closures at once. The rules decide what all, allKeyed, first, firstKeyed and map return, and how a failure fails the whole procedure with concurrent_failed and what its details hold.

## Motivation

A program often waits on several things at once, and a document cannot reach the host's scheduler. Brought as procedures over closures, running at once is a grant: what a host does not link, a program cannot do, and what each closure may touch is read from its declaration before anything runs. The answer still has to be the same on every implementation, so what each procedure returns and how its failures are reported is fixed, save the one timing fact a race admits.

## Rules

| procedure | parameters | returns |
|---|---|---|
| `all` | `pieces`, a list of procedures taking nothing | each piece's return value, in the pieces' order |
| `allKeyed` | `pieces`, a dictionary of procedures taking nothing | each piece's return value, under its key |
| `first` | `pieces`, a list of procedures taking nothing | the return value of the first piece to succeed |
| `firstKeyed` | `pieces`, a dictionary of procedures taking nothing | the return value of the first piece to succeed |
| `map` | `array`, `transform`, handed the item, then its index | what `transform` returns for each item, in the collection's order |

**`Standard.Concurrent`**. Running closures at once. `all` takes a list of closures, runs every one, and returns every return value in the list's order; `allKeyed` takes a dictionary of closures under keys, and returns each return value under its key. A failure fails the whole procedure with `concurrent_failed`, [below](#concurrent_failed). `first` and `firstKeyed` take the same and return the first success, asking the rest to stop and returning when they have stopped; which piece wins is the one timing fact this language admits. A piece that refuses at the run before one succeeds ends the race the way a success does, and refuses the whole run. Where more than one piece of `all`, `allKeyed` or `map` refuses, the run refuses with the first of them in the order the procedure returns its values, so which refusal crosses is no timing fact. What a piece does once the rest are asked to stop is not reported. `map` takes a collection and one closure, calls it once per element, handing it the element and then its index, and returns in the collection's order. These are procedures rather than grammar because a closure is already the safe unit of concurrent work, and being procedures makes concurrency a permission: what a host does not link, a program cannot do.

The names are plain ones with the module carrying the context. A call site spells the module, so `Standard.Collection.first` and `Standard.Concurrent.first` are two names, and a link carrying both bundles holds both: every `first` and every `map`, the sequential ones included, is written with its bundle, and concurrency shows at the call site.

What the checking sees comes from the declarations in the interface. `map` is checked the way the sequential one is: the collection's elements against what the closure takes, and what `map` returns is what the closure returns, at the build. Every closure these five run is run at once, so one that writes a captured variable refuses at the build before anything runs, and so does a piece the build reads as something other than a closure; a list or a dictionary literal is held to the slot part by part, so a piece that is not a closure refuses there too, and a list of pieces read as `Any` takes a cast first, the way any value read as `Any` does. Every piece returns the one type the call fills from them; pieces returning two types that neither takes fill it with `Any`, joined part by part the way a literal's parts are, and so does a piece written to return `Any`.

What the procedures hand their closures is one convention, shared with the sequential walks. `Standard.Collection.map`, `filter` and their `try` twins hand over the item, `reduce` and `tryReduce` hand over the carried value then the item, `Standard.Concurrent.map` hands over the item then its index, and a closure written for one of them **declares exactly as many parameters as it is handed, in that order**, under names of its own, whether or not its body goes on to read one. A closure of another count **refuses at the build**, the same as anywhere else a value is called: a walk is not a second calling convention. `Standard.Concurrent.first` run over nothing **refuses at the run**, and so does `firstKeyed` over a dictionary holding nothing: a race needs pieces to run, so a race over nothing is a refusal of the run's shape, not an element that is absent. And a `first` or a `firstKeyed` in which nothing succeeds fails the way `all` and `allKeyed` fail, every piece's failure in `failures`.

### `concurrent_failed`

`concurrent_failed` is a `Failure` under [`try`](../WARP-25/SPEC.md), and its `details` hold `failures` and nothing else:

| key | holds |
|---|---|
| `failures` | a dictionary: each piece that failed, under its key below, as the `Failure` it raised, so a catch reads a piece's own `type`, `message` and `details` through it |

| procedure | a piece's key in `failures` |
|---|---|
| `all`, `first` | the piece's position in `pieces`, an `Int` |
| `map` | the position of the item it was handed, an `Int` |
| `allKeyed`, `firstKeyed` | the key the piece stood under in `pieces` |

Its `message` is this line:

```
message = "concurrent pieces failed: " piece { "; " piece }
piece   = key ": " piece-message
```

| part | what it is |
|---|---|
| `piece` | a piece in `failures`, the pieces in the key order of `failures` |
| `key` | the piece's key as `text` returns it, under [Standard.Text](../WARP-79/SPEC.md): a string unquoted, a position as its digits |
| `piece-message` | the `message` of the piece's own `Failure` |

## Interactions

- Which closures may run at once, and what the build holds them to, is [concurrency](../WARP-73/SPEC.md).
- Where a piece told to stop stops is where a run observes cancellation, under [order](../WARP-70/SPEC.md).

## Alternatives considered

- A third way of waiting, one returning every piece's success or failure. A piece that wraps its body in a `try` and returns its failure as a value writes it with `all`, so it adds nothing a program cannot write. `first` stays because nothing else can stop waiting.

## Notes

**Note.** No case can hold which of two refusing pieces crosses. A runner measures a refusal's stage and not its reason, under [conformance](../WARP-1/SPEC.md), and two pieces that refuse at the run refuse at one stage, so the rule that the first in the order the procedure returns its values crosses is held by no case.
