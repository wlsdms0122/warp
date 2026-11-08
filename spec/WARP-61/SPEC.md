# WARP-61: What the language declares

Status: accepted

## Summary

The language declares four names itself. The rules decide that the contract Hashable and the structs Failure, Round and Some stand in every link, that a document declaring one refuses at the load, and that a mention of Some refuses.

## Motivation

A catch, a loop, a dictionary's key and a some of a none need these names before any vocabulary is linked. Were they a document's, two documents, or two implementations, could each bring their own `Failure` and mean different things by it.

## Rules

**The language declares four names itself**, which stand in every link ahead of its documents: the contract `Hashable` under *a dictionary's key* [below](../WARP-62/SPEC.md), the structs `Failure`, which a catch binds, under [`try`](../WARP-25/SPEC.md), and `Round`, which a loop binds, under [`loop`](../WARP-24/SPEC.md), and the struct `Some`, `{ struct: { wrapped: Any } }`, which holds `null` or a `Some` under [the value model](../WARP-2/SPEC.md). A document declaring one of them **refuses at the load**. A mention of one of the first three is that declaration, and which of them each place may name is under *what a name names* in [names](../WARP-67/SPEC.md): `extensions: { Round: { satisfies: ["Hashable"] } }` keys a dictionary by `Round`. `Some` is how a value is held and no type a program reads, so no place names it, and a mention of it anywhere **refuses at the load**.

## Interactions

- The four are words no document's type and no type parameter may be called, under [names and their grammar](../WARP-67/SPEC.md).

## Alternatives considered

## Notes
