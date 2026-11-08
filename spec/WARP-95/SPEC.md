# WARP-95: A switch

Status: accepted

## Summary

`switch` takes a value of an [enum](../WARP-93/SPEC.md) apart by its case: an arm per case it names, which binds what that case carries, and a `default` for the cases no arm names. The build holds the arms to the enum's declaration, so a switch handles every case. It is a statement, its ways meet as a conditional's arms do, and an object writes it as an operation of its own.

## Motivation

Two things in the document under [enums](../WARP-93/SPEC.md#motivation) are the IR's to say, and neither is a front end's:

- **Which case a value is needs `switch`.** A cast asks whether a value is of a type, and a case is not a type, so no cast the live set has asks which case `target` holds or binds what that case carries. `switch` is the one construct that does.
- **That a switch handles every case is a fact of the text.** The build reads the cases from the enum's declaration and holds the arms to them, so a switch missing `remote` with no `default` refuses at the build. It is a check of the program's own declaration, not of what a value means, and no front end could make it over structs under a contract, since the types that conform to a contract are open, under [types](../WARP-53/SPEC.md).

## Rules

### `switch`

| key | takes | required |
|---|---|---|
| `of` | expression. Its reading is an enum | yes |
| `cases` | dictionary: case → arm. An **arm** is `{ binds?, then }`: `binds`, a dictionary from a field the case carries to the name it binds; `then`, statements, which run where `of` holds that case | yes, and at least one arm |
| `default` | statements. Run where `of` holds a case no arm names | no |

A switch is a statement: it **has no value** and **takes no name**, the way a `conditional` does under [statements](../WARP-23/SPEC.md), so a naming key on one **refuses at the load**. Where `of` holds a case an arm names, that arm's `then` runs, and otherwise `default` does. What `of` takes apart is an operand, read rather than run, as what an unwrap takes apart is under [procedures](../WARP-15/SPEC.md). An `of` whose reading is no enum, `Never`, `Any`, a contract, a type parameter, a declared struct and an Optional of an enum among them, **refuses at the build**: a cast or an unwrap says which enum first. A `cases` naming a case the enum does not declare **refuses at the build**, where the enum's declaration is read, and one holding no arm **refuses at the load**, since the switch would say what its `default` says alone. An arm writing `binds` empty says what its absence says, and **refuses at the load**, under [the document format](../WARP-11/SPEC.md).

**An arm binds what its case carries**, each field it names to a name under `binds`, `{ binds: { port: p }, then: … }`; a field it does not name is not bound. A bound name reads the type the enum's declaration writes for the field, the enum's type parameters read as `of`'s reading applies them: in a switch over `App.Result<Int, String>`, a name bound to `success`'s `value` reads `Int`. That is the type written for it, under [procedures](../WARP-15/SPEC.md). Where a bound name is read and may be introduced again, and how far a name an arm or the `default` declares is read, is under [statements](../WARP-21/SPEC.md), which introduces a bound name as an unwrap's payload. It is fixed as the payload is, so a `set` of it **refuses at the load**. Two fields bound to one name in one arm **refuse at the load**. `binds` naming a field the case does not carry **refuses at the build**.

**A switch handles every case.** The build holds its arms to the enum's declaration: a switch that has no arm for a case the enum declares and writes no `default` **refuses at the build**, since a run holding that case would have no way through. A `default` takes the cases no arm names and binds nothing, since what those cases carry differs. A `default` beside an arm for every case is a body no run reaches, and **refuses at the build**, as a catch over a body that cannot fail does under [statements](../WARP-25/SPEC.md). An arm's `then` and the `default` may hold no statement, which is how a switch does nothing for a case.

**The ways meet as a conditional's arms do**, under [checking](../WARP-68/SPEC.md). Each arm and the `default` is a way, and there is no other, since the switch handles every case: a write every way makes is unconditional, a way that leaves contributes nothing, a write only some ways make joins with what the name held, and where a value one way leaves would change to stand at the reading the ways meet at, promoted to its some or its held type dropped at `Any`, the build **refuses**. Every way is checked whether or not a run takes it.

**Whether a switch leaves**, what may follow one that does and at which stage that is held, is under [statements](../WARP-29/SPEC.md), which reads a switch's arms and its `default` as its ways.

**What it may fail with** is what its ways fail with and what `of` fails with, under [statements](../WARP-26/SPEC.md); it raises nothing of its own. Nor does it refuse anything at the run: every value a reading of an enum holds was judged one of its cases where it came in, at a door or a cast under [where an enum stands](../WARP-94/SPEC.md) or a literal under [enums](../WARP-93/SPEC.md#a-cases-value), so every run finds its way.

### In the text

```
(switch t                                   { value: { switch: { of: { ref: t }, … } } }
  (case local                               cases.local: { then: [...] }
    (then …))
  (case remote                              cases.remote: { binds: { port: p }, then: [...] }
    (bind port p)
    (then …))
  (default …))                              default: [...]
```

- Past a switch's subject, `case` is an arm, under [enums](../WARP-93/SPEC.md#in-the-text).
- A switch's nodes are under *the nodes* in [the text](../WARP-37/SPEC.md#the-nodes): its subject first, by position, as what an unwrap takes apart stands, and its arms and its `default` after it. The first operand is `of` whatever node it is, so in `(switch (case local) (case local (then)))` the first `case` is a case literal at `of`, which gives it no enum, and it **refuses at the build** as a case literal written where no enum is read does.
- `(then)` and `(default)` holding none write `[]`. An arm always writes its `(then …)`, as an arm under [`switch`](#switch) always holds `then`.
- The writer lays out `switch`, an arm and `default` under [the writer's layout](../WARP-45/SPEC.md).

### In the binary and in an object

**A switch is an operation of its own**:

| tag | operation | fields |
|---|---|---|
| 17 | a switch | the *operation* it takes apart; the enum's name; the arms, a list of `[case, binds, then]` ascending by case name, *binds* a list of `[field, slot]` ascending by field name and *then* an *instruction* list; the default, an *instruction* list or nothing, as an unwrap's `else` is |

A switch names its enum once, as a string, the way a layout names a struct, and each arm by its case's name alone, so the run matches a value's spelling against the enum's name and an arm's case. The name is the enum's declared name whatever `of`'s reading applies the enum to, `App.Result` in a switch over `App.Result<Int, String>`, since a value carries nothing of what the enum was applied to and the run matches its spelling by name. It stands on its enum through that name and on no entry of `typeNumbering`. The default is a field that may hold nothing, written under [objects](../WARP-86/SPEC.md) as a list of none or one: a switch writing no `default` writes `[]`, and one whose `default` holds no statement writes `[[]]`, a list holding the empty *instruction* list, so the two stay apart.

A body lowers it the way it lowers an unwrap, under [objects](../WARP-88/SPEC.md): what it takes apart first, then each arm in the order the operation writes them, its bound names taking slots in the order of their fields before its `then` is walked, then `default`. A reading refuses arms out of name order or naming one case twice, binds out of name order or naming one field twice, and a bound slot past the frame, under [objects](../WARP-92/SPEC.md). What a build judged, an object writes down as judged, so a reading and a link do not ask again whether the arms cover the enum: the declaration the compile read is the one the object's `dependencies` stand on.

## Interactions

- A switch meets the ways a conditional's do, leaves and failures as the other constructs do, under [`switch`](#switch): [WARP-25](../WARP-25/SPEC.md), [WARP-26](../WARP-26/SPEC.md), [WARP-29](../WARP-29/SPEC.md), [WARP-68](../WARP-68/SPEC.md).
- The text and the object format, under [in the text](#in-the-text) and [in the binary and in an object](#in-the-binary-and-in-an-object): [WARP-37](../WARP-37/SPEC.md), [WARP-45](../WARP-45/SPEC.md), [WARP-86](../WARP-86/SPEC.md), [WARP-88](../WARP-88/SPEC.md), [WARP-92](../WARP-92/SPEC.md).

## Alternatives considered

## Notes

**Note.** A front end could write the cases as structs under one contract, but the types that conform to a contract are open, under [types](../WARP-53/SPEC.md), so no build could hold a switch over them to every case. `default` is core for the same reason: it takes the cases a front end could not see, so a switch with a `default` over an enum another document declares still builds when that document adds a case, where one arm for each case the front end saw would refuse at the build. A source language's switching past one arm per case is written with a switch:

| source | written as |
|---|---|
| nested patterns, `where` guards, several cases in one arm, `if case` | a switch inside an arm, a `conditional` inside an arm, the arm written once for each case, a switch with an empty `default` |
| a `switch` or `match` read as a value | a `var` every arm `set`s, which reads unconditional past the switch |
