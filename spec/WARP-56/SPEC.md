# WARP-56: A claim holds to members

Status: accepted

## Summary

The build holds a claim to the type's members. The rules decide that each procedure the contract asks is matched by a member of that name whose signature fits with the type in place of Self, how this works under a head, and how type members are matched.

## Motivation

The build checks a claim at the claim, whether or not anything calls through the contract. A claim that held only when called would build in one program and refuse in another for the same document, and a host linking a library could not rely on a claim it reads there.

## Rules

**The build holds the claim to the type's members.** For every procedure the contract asks, it takes the type's member of that name (`Bank.Account`'s `describe`), under [members](../WARP-58/SPEC.md), and holds its signature to the contract's with the type in place of `Self` wherever the contract writes it. A name that stands for a declared struct or [enum](../WARP-94/SPEC.md) names that type there, as wherever types are compared, so a declaration may write another name for the struct the contract writes. A declaration that writes no `returns` is held to `Null`, which it returns under [a procedure](../WARP-12/SPEC.md).

**A member satisfies the requirement for every value the head it is given under takes**, and backs a claim where that is every value the claim's head takes. Under a type's bare name that is every value of the type, under [claims](../WARP-54/SPEC.md), and under a head applying the type it is the type as the head applies it, each of the head's type parameters one no call fills held to its bounds. So a member given under `Array<Int>` alone backs no claim about `Array`, and one taking `App.Box<Int>` alone none under `App.Box<some T: Hashable>`.

**For every type the contract asks**, the build takes the type's type member of that name, under [associated types](../WARP-59/SPEC.md), and reads `Self.Item` as what it gives.

## Interactions

- Members and where a claim may take them from are under [members](../WARP-58/SPEC.md).
- A claim backed by a declaration that does less than the contract asks, or by a `private` one, is under [what the build decides](../WARP-66/SPEC.md).

## Alternatives considered

- A contract asking a property, a field a conforming type must have. A field answering a procedure's requirement would be a branch of its own in the judgement. A front end that has stored properties writes a member that reads the field.

## Notes
