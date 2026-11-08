# WARP-81: Standard.Optional

Status: accepted

## Summary

Standard.Optional holds unwrapped and its try twin. The rules decide that the fallback is a procedure asked only on a none, and that one level is taken off.

## Motivation

An `unwrap` is a statement, so an operand that wants an optional's payload or a fallback has no construct to write it with, and `unwrapped` is the procedure that does.

## Rules

| procedure | parameters | returns |
|---|---|---|
| `unwrapped`, `tryUnwrapped` | `optional`, `else`, a procedure taking nothing | the payload of a some, and on a none what `else` returns |

`unwrapped` takes its fallback as a procedure for the reason `select` does: only a none asks it, so on a some `else` never runs, and a fallback that would refuse is no refusal of the call. It takes one level off, as `unwrap` does under [statements](../WARP-27/SPEC.md): over `Int??`, the some of the inner none returns that none, `null`, and `else` is not asked. Both are written in Warp from `unwrap`, so neither is builtin.

## Interactions

- `select` takes its sides as procedures for the same reason, under [Standard.Logic](../WARP-76/SPEC.md).
- `tryUnwrapped` is the twin of [WARP-75](../WARP-75/SPEC.md).

## Alternatives considered

## Notes
