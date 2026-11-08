# WARP-82: Standard.Control

Status: accepted

## Summary

Standard.Control holds abort. The rules decide that it fails on purpose with a message, that a null message says aborted, and that its declared return of Never makes the checking work.

## Motivation

A program that finds what it was handed wrong has to stop with a reason, and a document reaches nothing outside the run to report one with. `abort` is that one way, a failure like any other, so the caller's `try` decides what happens next.

## Rules

| procedure | parameters | returns |
|---|---|---|
| `abort` | `message`. What the failure says. Null says `aborted` | nothing: it fails |

**`abort`**. Fail on purpose, with a message. Its declaration is everything the checking needs: nothing runs after it, and no name binds it. The failure it raises, a `Failure` under [`try`](../WARP-25/SPEC.md), holds what the table below gives. It is a failure like any other, so a `try` around it catches it. Leaving is what a catch does not take, and this is failing, not leaving.

| field | holds |
|---|---|
| `type` | `aborted` |
| `message` | what `text` returns for `message`, under [Standard.Text](../WARP-79/SPEC.md); `aborted` where `message` is null |
| `details` | a dictionary holding nothing |

## Interactions

- A body calling `abort` declares `aborted` under [what a body may fail with](../WARP-26/SPEC.md).
- `split` and `replacing` fail with the same `aborted`, under [Standard.Text](../WARP-79/SPEC.md).

## Alternatives considered

- An abort construct in the grammar. A construct is for what the checking needs and a signature cannot say, and a declaration returning `Never` already says that nothing runs after the call.
- Aborting as a trap, ending the process as a fatal error does. The run stands inside the host's process, so a trap would end the host.

## Notes
