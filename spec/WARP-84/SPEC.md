# WARP-84: What the vocabulary says about bytes

Status: accepted

## Summary

The vocabulary treats bytes as an array of integers from 0 to 255. The rules decide that a bytes value stands where Array<Int> is declared and crosses it whole, how bounded elements read it, and how the collection vocabulary applies to it.

## Motivation

Bytes arrive from the host, a file read or a message received, and a program reads them, cuts them and turns them into text. As a kind of value of their own, bytes would need every collection procedure twice. As an array with a compact spelling, the collection vocabulary applies to them as it is, and what is left to say is when that spelling survives what a procedure returns.

## Rules

What the vocabulary says about **bytes**: they are an array of integers from 0 to 255, `Array<Int>`, and `x"6869"` is that array's compact spelling, under [values](../WARP-2/SPEC.md). A slot taking bytes is written `Array<Int>`, or any other array the bytes fit. **The spelling is the value's own fact rather than the slot's**: a bytes value stands where `Array<Int>` is declared and crosses it *whole*, because the slot asked for an array and bytes are one. `Array<Double>` takes no byte at all, a byte being an integer. An element declared as a **bounded** type parameter stands for one type the call filled, so `sorted`, whose element carries `Standard.Comparable`, reads a compact spelling the way `reversed` does. An array of byte worths written out one by one stays as written: the compact spelling is the value's, and no slot puts it on.

An index reads an element out as an `Int`, and so does `some Element` filled by bytes: `first` of bytes returns an `Int?`. The collection vocabulary (`count`, `first`, `contains`, `reversed`, `map`, all of it) applies directly. A procedure that returns a collection's **own** elements (`reversed`, `filter`, `sorted`, `dropFirst`, `dropLast`) returns them in the spelling they arrived in, so bytes stay bytes. `appending` and `prepending` keep that spelling where what they add is a byte, so `appending` `105` to `x"68"` returns `x"6869"`; put something among them that is not a byte (`appending` a `300`) and the return value is the array it is. A procedure that builds **new** elements does not: `map` returns whatever its procedure returned, which its declaration says by naming a second type parameter for it. Two bytes values do **not** order: `Standard.Comparable` is claimed for numbers and strings, not for `Array`. Reading bytes *as* a string is a procedure that names its encoding: `decoded` and `encoded` are the two directions of one mapping, and the encoding they are handed is a string: one `encoding` below produces is an encoding they have, `utf8` naming UTF-8, and any other is not. `decoded` completes no broken sequence, which would return a string nobody sent. `encoded` writes the string's code points as they stand and normalises nothing, and `decoded` keeps a byte order mark as the character it is: normalising the one or dropping the other would be an opinion about the string rather than a reading of it. The encodings are this specification's: each is one every implementation writes.

```
encoding = "utf8"
```

## Interactions

- `x"6869"` and the array it spells are the same value under [when two values are the same](../WARP-4/SPEC.md).
- A procedure returns a collection's own elements in their spelling through `gathering`, under [Standard.Collection](../WARP-80/SPEC.md).

## Alternatives considered

- Bytes as an opaque kind of value, with a count and sameness and nothing inside to read. Opaqueness was a property of the wire: `x"6869"` is a compact spelling of an array, and an array's elements are read like any other's.

## Notes
