# WARP-75: A procedure that takes procedures runs them

Status: accepted

## Summary

A procedure that takes procedures runs them. The rules decide that a row taking a procedure that may fail has a twin named with the try prefix, and that a call reads the one it names.

## Motivation

A caller handing a closure to `map` has to know from the declarations alone whether the call may fail. If one `map` took closures that may fail and passed their failures on, whether a call of it fails would depend on what it was handed, and the build would work that out from the argument rather than read it from a declaration.

## Rules

**A procedure that takes procedures runs them, and its name says whether they may fail.** Where a caller would hand a `Standard.Collection`, `Standard.Logic` or `Standard.Optional` row a procedure that may fail, the row has a twin, which takes one that may fail with anything and fails with what it fails with. The two are two procedures under two names: a call reads the one it names and nothing chooses between them. The twin's name is the row's procedure's name with its last `identifier`, under [names](../WARP-67/SPEC.md#the-grammar), replaced by `twin` below: `Standard.Collection.map` has the twin `Standard.Collection.tryMap`. [The standard vocabulary](../WARP-74/SPEC.md) lists both names whole.

```
twin = "try" upper-first rest
```

| part | what it is |
|---|---|
| `upper-first` | the row's last `identifier`'s first `letter`, upper-cased |
| `rest` | the row's last `identifier` after its first `letter` |

## Interactions

- How a declaration and a procedure type write what they fail with is [what a body may fail with](../WARP-26/SPEC.md).
- The rows with twins are in [Standard.Logic](../WARP-76/SPEC.md), [Standard.Collection](../WARP-80/SPEC.md) and [Standard.Optional](../WARP-81/SPEC.md). [Standard.Concurrent](../WARP-83/SPEC.md) has none: its procedures fail with their own failure, `concurrent_failed`, whatever the pieces fail with.

## Alternatives considered

- A failure parameter, a procedure declaring that it fails with whatever the procedure handed to it fails with. Exact, but the build would solve that parameter at every call, and the IR holds declarations the build checks against rather than facts it works out.
- Overloading in the IR, two declarations under one spelling and the build choosing by the argument. A spelling would stop naming exactly one declaration, a procedure taken as a value could not be chosen, and every runtime would implement one ranking rule alike. A front end may show the two under one name and write the one it means.

## Notes

**Note.** A `try` twin fails with anything, which says less than what the closure handed to it may fail with.
