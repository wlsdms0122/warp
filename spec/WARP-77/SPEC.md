# WARP-77: Standard

Status: accepted

## Summary

Standard holds the shared contracts Numeric, Comparable and Collection. The rules decide their procedures, which language types claim them, and what count reads. They also decide the edges: Int arithmetic with no Int result, Double arithmetic with no finite result and a zero divisor refuse at the run, dividedBy returns a Double, and remainder truncates toward zero.

## Motivation

One implementation wraps an `Int` past its edge, one widens it, one traps; one truncates a remainder toward zero and one floors it; one divides two integers to an integer and one to a fraction. A document whose answer depends on any of these would answer differently from runtime to runtime.

## Rules

The contracts. A call writes the contract's spelling, `Standard.Numeric.plus`, and the run picks the declaration satisfying it by the type that fills `Self`, under *calling a contract's procedure* in [types](../WARP-63/SPEC.md): `Int.plus` for an `Int`, `Double.plus` for a `Double`.

| contract | procedure | parameters | returns |
|---|---|---|---|
| `Standard.Numeric` | `plus`, `minus`, `times`, `remainder` | `lhs`, `rhs` | the sum, the difference, the product and the remainder |
| `Standard.Numeric` | `dividedBy` | `lhs`, `rhs` | the quotient, a `Double` |
| `Standard.Comparable` | `lessThan` | `lhs`, `rhs` | whether `lhs` orders before `rhs` |
| `Standard.Collection` | `count` | `collection` | how many it holds |

| type | claims |
|---|---|
| `Int`, `Double` | `Standard.Comparable`, `Standard.Numeric` |
| `String` | `Standard.Collection`, `Standard.Comparable` |
| `Array`, `Dictionary` | `Standard.Collection` |

`count` reads a list's elements, bytes included, a dictionary's entries, and a string's characters as a person reads them. A declared struct or [enum](../WARP-94/SPEC.md) is an instance of its own name, so `count` takes one only where a document claims `Standard.Collection` for it.

Behaviour at the edges, where implementations quietly differ, stated as requirements:

- Arithmetic takes two of one type under `Standard.Numeric`, as the interface declares it. An `Int` added to a `String` **refuses at the build**, and so do two `String`s, because no claim puts `String` under `Standard.Numeric`.
- Ordering (`lessThan`, `greaterThan`, `sorted`, `min`, `max`) compares two of one type under `Standard.Comparable`, `String` among them: two strings order as [the key order](../WARP-3/SPEC.md) orders `String` keys. A type no claim puts under it, or a reading whose type the build does not know, refuses at the build, under **Bounds** in [types](../WARP-52/SPEC.md).
- `Int` arithmetic with no `Int` result **refuses at the run**. It does not wrap and does not silently widen. The rule covers every standard procedure that returns an `Int` and can miss it: `plus`, `minus`, `times` off the int's edge, `absolute` of the int's own minimum, and `floored`/`rounded` of a `Double` whose integer part is past what an `Int` holds. `remainder` is not on the list because its result always fits. A remainder is smaller in size than its divisor, and the one divisor that trips a machine's division instruction still has one: `-9223372036854775808 remainder -1` returns `0`. These run-stage refusals (overflow, and the zero divisor below) are the program's own defect, not a failure of the work: a `try` does **not** catch them, the way it does not catch an index past the end. What a catch takes is `abort` and a procedure's own failure.
- `Double` arithmetic with no finite result **refuses at the run**, at the door its result crosses under [running](../WARP-71/SPEC.md): infinity is a value the arithmetic can reach and no document can carry.
- `dividedBy` returns a `Double`, integral or not. Division by zero **refuses at the run**. The quotient is binary64's own: an `Int` operand reads as the `Double` nearest it first, as binary64 rounds, a tie going to the even neighbour, and the division rounds once more, so two implementations spell the same quotient bit for bit.
- `remainder` truncates toward zero, for `Int` and `Double` alike: what is left takes the dividend's sign, so `-7 remainder 3` is `-1`, `7 remainder -3` is `1` and `-5.5 remainder 2.0` is `-1.5`. A `Double` remainder is exact, as IEEE 754's `fmod` gives it: the dividend less the divisor times the exact quotient truncated toward zero, which binary64 holds without rounding, so `1.0 remainder 0.1` is `0.09999999999999995`. A zero divisor **refuses at the run**, the same as under `dividedBy`.
- An `Int` is no `Double`, and a `Double` is no `Int`, under [types](../WARP-47/SPEC.md), which says too where an integer literal is read as the `Double` it names.

### The standard contracts

**The shared `Standard` bundle declares the contracts the standard procedures are bounded by**, `Standard.Numeric`, `Standard.Comparable` and `Standard.Collection`, claims them for the types the language names (`Int` and `Double` are numbers that order, `String` orders and has a count, `Array` and `Dictionary` have a count) and gives those types the members backing those claims, `Int.plus` and the rest. Which bundles link with `Standard` is [the standard vocabulary](../WARP-74/SPEC.md)'s rule.

## Interactions

- `floored`, `rounded` and `absolute` share the int's edge under [Standard.Math](../WARP-78/SPEC.md).

## Alternatives considered

- An unbounded `Int`, an integer that never overflows. `Int` has the meaning an integer type has nearly everywhere, a machine word, and an integer past it is a library's to bring.
- A quotient rounded once from the exact value. `dividedBy` widens each operand to binary64 and divides, one rule whatever its operands, which every implementation's binary64 division gives bit for bit.

## Notes

**Note.** `minus` is builtin because arithmetic is the machine's, under [the standard vocabulary](../WARP-74/SPEC.md). A body written from `plus` and `times` would also get an edge wrong: `-1` minus the int's minimum has an `Int` result, and the body would multiply the minimum by `-1` and refuse where `minus` returns.
