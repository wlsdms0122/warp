# WARP-78: Standard.Math

Status: accepted

## Summary

Standard.Math holds min, max, absolute, floored, rounded and greaterThan. The rules decide what each returns, how ties are broken, how rounding goes at halves and below zero, and which edges refuse at the run.

## Motivation

`rounded` of `2.5` is `2` under a rounding that goes to the even neighbour and `3` under one that goes away from zero, and `floored` of `-2.1` is `-2` under one that truncates.

## Rules

| procedure | parameters | returns |
|---|---|---|
| `min`, `max` | `lhs`, `rhs` | the lesser and the greater of the two |
| `absolute` | `number` | the number without its sign |
| `floored`, `rounded` | `number` | the integer it floors to and the integer it rounds to |
| `greaterThan` | `lhs`, `rhs` | whether `lhs` orders after `rhs` |

`min` and `max` return one of the two as it arrived. On a tie, where the two order the same, `min` returns `lhs` and `max` returns `rhs`, so `min(0.0, -0.0)` is `0.0` and `max(0.0, -0.0)` is `-0.0`.

`floored` goes to the nearest integer toward the smaller side, below zero too: `-2.1` floors to `-3`. `rounded` goes to the nearest integer, and away from zero at the exact halfway: `2.5` rounds to `3`, `-2.5` to `-3`. `floored` and `rounded` return an `Int`, and only where an `Int` holds the result. `absolute` drops the sign and keeps the type it was given. The int's edge refuses at the run, as the edge rules [of `Standard`](../WARP-77/SPEC.md) require.

## Interactions

- `floored` is builtin under [the standard vocabulary](../WARP-74/SPEC.md), and the rest are written in Warp.

## Alternatives considered

## Notes

**Note.** The obvious body of `rounded` is wrong: `floored` of the number plus `0.5` returns `1` for `0.49999999999999994`, since the sum rounds up to `1.0` in binary64, where `rounded` returns `0`. The body written takes what is left of the number above its floor, which binary64 holds exactly, and compares that with `0.5`: below it goes to the floor, above it to the floor plus one, and at the exact halfway away from zero.
