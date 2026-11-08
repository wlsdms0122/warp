# WARP-25: `try`

Status: accepted

## Summary

A try runs a body and, if it fails, a catch. The rules decide that a try has no value, that a catch takes failure and not leaving, which empty or unreachable catches refuse, and what the failure name binds.

## Motivation

A protected body is the IR's, because a failure passes through every call between where it was raised and the body that handles it, and the build judges what each body may fail with under [what a body may fail with](../WARP-26/SPEC.md), which it can do only where it sees the protected body. A front end lowering `do { try fetch() } catch { … }` writes `{ let: failed, value: { try: { body: [ … ], catch: [ … ] } } }`, and `failed.type` reads the same field whichever runtime's host raised the failure, since the envelope is this specification's and not the procedure's.

## Rules

| key | takes | required |
|---|---|---|
| `body` | statements | yes |
| `catch` | statements. Runs if the body fails | yes |

A try is a statement: it **has no value**, the way a `conditional` does. Its body and its catch are its two ways through, and what either keeps it writes to an outer variable with `set`. A catch takes failure (what the world did), not leaving (what the program said). A catch with no statement in it **refuses at the load**: it would drop a failure without a trace. A catch over a body that cannot fail, one whose casts and calls say no failure, **refuses at the build** for the other half of the same reason: it is a body no run reaches. A refusal at the run is not a failure and does not make a body one that can fail, under [running](../WARP-72/SPEC.md). The statement's own name binds the failure **while the catch runs** and nowhere after the try, a try written nameless binds none, and what a name binds is a **`Failure`**, a struct the language declares as `{ struct: { type: String, message: String, details: Dictionary<String, Any> } }`, under [types](../WARP-61/SPEC.md). `type` names what happened (`aborted`, `concurrent_failed`), `message` is a string for a person, and `details` is what the failing procedure carried. Every failure holds all three by construction: a runtime assembles the payload from what a failure declares, so no procedure can hand over one without them.

The envelope is this specification's; what rides in `details` is the procedure's own, the standard vocabulary's under [the standard vocabulary](../WARP-74/SPEC.md).

```
{ ref: "failed.details[\"failures\"]" }
```

`cast_refused` has no procedure behind it, so this specification names its `message` and `details` too. `details` holds two strings:

| key | holds |
|---|---|
| `expected` | the type the cast reads as, in its string spelling under [types](../WARP-46/SPEC.md#the-grammar): every alias in it, at any depth, read as what it stands for until none is left, and every type parameter of the procedure the cast stands in, and every associated type of one (`some T.Item`), read as the call filled it, under [a cast](../WARP-32/SPEC.md) |
| `actual` | the type the value is an instance of, by the type's name with nothing it is applied to, below |

| value | `actual` |
|---|---|
| null, a bool, an int, a double, a string | `Null`, `Bool`, `Int`, `Double`, `String` |
| a list, bytes among them | `Array` |
| a dictionary | `Dictionary` |
| a `Some`, the some of an Optional under [the value model](../WARP-2/SPEC.md) | `Optional` |
| a value of an [enum](../WARP-94/SPEC.md) | the enum's name |
| any other struct | the name it carries |
| a procedure | `Procedure` |

```
message  = "expected " expected ", got " actual
```

Its `message` is that line, `expected` and `actual` standing for what `details` holds under them: `expected Array<Int>, got Array`. Both halves, because what was asked for is readable from the program and what turned up is not.

```
{ ref: "failed.details[\"actual\"]" }
```

`details` holds `Any`, so a value read out of it is read as anything until a type is named for it. A field the envelope does not name is not reached by a dot on the failure itself: `failed.failures` **refuses at the build**, and what `details` holds is read through brackets, `failed.details["failures"]`.

## Interactions

- Which bodies can fail: [what a body may fail with](../WARP-26/SPEC.md).
- Where `cast_refused` is raised: [a cast](../WARP-32/SPEC.md).
- A try whose body and catch both leave: [nothing after a leave](../WARP-29/SPEC.md).
- `concurrent_failed`: [`Standard.Concurrent`](../WARP-83/SPEC.md).

## Alternatives considered

- Failure as a returned value, a result a front end branches on, with no `try` in the IR. Each front end would then implement unwinding its own way, and the build could not see a protected body, so a catch over a body that cannot fail could not be refused.
- A failure as a bare `Dictionary<String, Any>`, with no envelope. Even which failure happened would become a fact of the run, read out of a dictionary, rather than a field every failure has.
- Each procedure declaring its own failure payload type. A vocabulary outside the contract could then give failures shapes the IR does not know, and a document would not carry across runtimes whose vocabularies differ.

## Notes
