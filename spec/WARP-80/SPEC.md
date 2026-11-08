# WARP-80: Standard.Collection

Status: accepted

## Summary

Standard.Collection holds the procedures over arrays and dictionaries. The rules decide what each returns, for append, first, last, sorted, gathering and the rest, and which inputs refuse at the run.

## Motivation

Arrays and dictionaries are values with no operations of their own, so every walk, every read by position and every rewrite of an entry is a procedure here. Most of them are written in Warp from four builtins, and what each returns, its order and its spelling included, is said here, so that no body is the only place it is decided.

## Rules

| procedure | parameters | returns |
|---|---|---|
| `append` | `array`, a variable handed in place, and `element` | nothing, having written the element onto the end of the array the variable holds, in place |
| `contains` | `array`, `element` | whether the array holds the element |
| `first`, `last` | `array` | the first and the last element, as its some. Over nothing there is no element, and each returns the none, `null`, so over `[null]` of `Array<Int?>` `first` returns the some of the inner none, which the caller tells apart from the none of an empty list |
| `reversed`, `dropFirst`, `dropLast` | `array` | the elements in the other order, without the first and without the last. Over nothing, `dropFirst` and `dropLast` return nothing |
| `sorted` | `array` | every element once, in order where `lessThan` is a strict order, and elements of which neither orders before the other in the order they arrived in |
| `appending`, `prepending` | `array`, `element` | the array with the element at the end and at the start |
| `gathering` | `array`, `positions`. Where to read, in the order to read it | the collection's own elements at those positions, in the collection's spelling. A position the collection does not hold refuses at the run |
| `map`, `tryMap` | `array`, `transform`, handed the item | what `transform` returns for each item |
| `filter`, `tryFilter` | `array`, `isIncluded`, handed the item | the items it returns `true` for |
| `reduce`, `tryReduce` | `array`, `initialResult`, `nextPartialResult`, handed the carried value, then the item | the carried value after the last item |
| `keys` | `dictionary` | the keys the dictionary holds, in its key order |
| `values` | `dictionary` | what the dictionary holds, in its key order |
| `setting` | `dictionary`, `key`, `value` | the dictionary with the entry under the key written, as [a dictionary's keys](../WARP-3/SPEC.md) says a key is written. The dictionary's keys and the key read as one type, and its entries and the value as another, so two types there that neither takes **refuse at the build** |

`gathering` is how a procedure returns a collection's own elements. It says which by position, and the return value comes back in the spelling the collection arrived in: bytes rearranged are bytes. This is the whole of what `reversed`, `dropFirst`, `dropLast`, `filter` and `sorted` add to a walk, and it is the reason those are written in Warp rather than asked of an implementation. A body that read the elements out and put them back would return an array of numbers, because an array it started empty has no spelling to keep. The standard name for reading one collection at another's positions is a **gather**.

`map`, `filter`, `reduce` and their twins hand over the items one at a time, in the array's order, and a twin fails with the first failure and hands over no item after it.

## Interactions

- What bytes are, and why a procedure returning a collection's own elements keeps them bytes, is [the vocabulary says about bytes](../WARP-84/SPEC.md).
- `tryMap`, `tryFilter` and `tryReduce` are the twins of [WARP-75](../WARP-75/SPEC.md), and the closures the walks are handed follow the convention stated under [Standard.Concurrent](../WARP-83/SPEC.md).
- `Standard.Text.contains` asks the other `contains` question, under [Standard.Text](../WARP-79/SPEC.md).

## Alternatives considered

## Notes
