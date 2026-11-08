# WARP-93: Enums

Status: accepted

## Summary

A declared type whose values are its cases: a name, the cases it has, and for each case the values it carries. Its values travel as structs do, so the value model gains no kind, and a body makes one with a case literal, which writes its case and is read as the enum its place reads. Reads [the value model](../WARP-2/SPEC.md) and *a declared struct is nominal* in [types](../WARP-49/SPEC.md). Where an enum stands among the types is under [where an enum stands](../WARP-94/SPEC.md), and taking a value apart by its case under [a switch](../WARP-95/SPEC.md).

## Motivation

A front end that has an enum, Swift's, Rust's, Kotlin's sealed class, wants to hand one across the door and take it apart by its case. Take this document, whose entry a host calls with a target, and a host's native procedure declared in its module's interface with the same parameter, `(parameter target (type App.Target))`:

```
(warp 1)

(enum App.Target
  (case local)
  (case remote (field host String) (field port Int)))

(procedure entry
  (access public)
  (parameter target (type App.Target))
  (returns String)
  (body
    (switch target
      (case local
        (then
          (return "here")))
      (case remote
        (bind host h)
        (then
          (return h))))))
```

Two things in it are the IR's to say here, and neither is a front end's:

- **The signature names the enum.** The entry's parameter and the native procedure's are signatures, and a signature is the IR's: a host reads it to know what to hand and what it is handed, and a front end has no place in it to put a type the IR lacks. Lowered to `String` and checks, the parameter would say `String`, and a host would hand any string; lowered to structs under a contract, it would say the contract, which any struct may adopt.
- **A value has one shape at the door.** `remote` carrying `"a"` and `8080` crosses as `(struct App.Target.remote (field host "a") (field port 8080))`, whichever front end wrote the document and whichever host calls it. Left to front ends, each would pick its own encoding, a tagged dictionary, a string, a struct per case, and a host could not hand one value to two of them.

A body makes a value of an enum with a case literal, and that too is the IR's: a value of an enum is made where its enum is read, so the literal writes its case and no enum's name, and a front end gets the enum from the place, as it gets a struct literal's declared struct. A struct literal cannot stand in for it, since its place says the enum and not the case.

Everything else a source language's enum has, raw values and `CaseIterable` among them, is written with these in place, under [Notes](#notes), and nested patterns and guards under [a switch](../WARP-95/SPEC.md#notes).

## Rules

### The declaration

An enum is declared in `types` under its name, as a struct is, its cases under `enum`:

```
{ enum: { local: {}, remote: { host: String, port: Int } }, typeParameters?, satisfies?, types?, procedures? }
```

| key | takes | required |
|---|---|---|
| `enum` | dictionary: case → dictionary: field → type. Each case by its name, and the fields it carries, each by its name and its type; `{}` for a case that carries nothing | yes, and at least one case |
| `typeParameters` | the type parameters it takes, in order, each beside its bound where it has one, as a struct's under [types](../WARP-50/SPEC.md) | no |
| `satisfies` | the contracts it adopts, as a struct's under [types](../WARP-54/SPEC.md) | no |
| `types` | its type members, as a struct's under [types](../WARP-59/SPEC.md) | no |
| `procedures` | its members, as a struct's under [types](../WARP-58/SPEC.md) | no |

**A case's name and its spelling**, `App.Target.remote`, **hold the grammar** [names](../WARP-67/SPEC.md#the-grammar) gives them, and its spelling is the name a value of it carries, below. A field is named as a struct's field is, and its type is written as any type is, `some T` for a type parameter the enum lists.

**A case's field writes a type as a struct's field does, short of `var`**, under *a case's field* in *where a type is written* in [bounds](../WARP-52/SPEC.md#where-a-type-is-written): nothing writes into a value of an enum through a path, under [where an enum stands](../WARP-94/SPEC.md).

**A case's spelling is a name of the second namespace**, the one types and contracts share under [names](../WARP-64/SPEC.md): no type, contract or type member is declared under it, since a value under that name has to say one declaration. One document declaring one there **refuses at the load**, and two documents **refuse at the build**, as two declarers of one name do. The document declaring the enum declares each of its cases' spellings, which [the imports list](../WARP-10/SPEC.md) reads. A program writes a value of an enum with a case literal, under *a case's value* below, and a literal holding a struct **refuses at the load** whatever its name, under [values](../WARP-2/SPEC.md), a case's spelling included: `(const light (struct App.Light.red))` refuses, and a constant reaches an enum through a cast, `(const light (as (case red) App.Light))`. A value from outside under a case's spelling is held to its case at the door, under [where an enum stands](../WARP-94/SPEC.md). A procedure stands in the first namespace, so a member spelled like a case, `App.Target.remote` beside the case `remote`, is a member like any other.

**An enum may name itself** in a case's field, at any depth, directly included: `App.Expr` declaring `add: { lhs: App.Expr, rhs: App.Expr }` beside `number: { value: Int }`. A case that does not name it is where a value ends, so a tree is one declaration. An enum every case of which names it, `App.Loop` declaring only `more: { next: App.Loop }`, stands all the same, as a struct whose field names the struct does under [types](../WARP-50/SPEC.md): where no value of it can end, that is a front end's mistake, and no stage refuses it.

Each of these **refuses at the load**, since the document shows it alone:

- a declaration writing `enum` beside `struct`, or writing no case, `enum: {}`. The type that has no value is spelled `Never`, and an enum with no case would be a second spelling of it, which a document does not write, under [the document format](../WARP-11/SPEC.md);
- a case or a case's field whose name does not hold its grammar under [names](../WARP-67/SPEC.md), `remote.tls` or `2fa`;
- a case or a field written twice. A dictionary holds each key once, so the binary has no such tree and a text writing one **refuses**, under [the text](../WARP-37/SPEC.md);
- a field writing what the row *a case's field* of *where a type is written* in [bounds](../WARP-52/SPEC.md#where-a-type-is-written) does not let it write, and `typeParameters` listing a name twice, as a struct's does under [types](../WARP-50/SPEC.md);
- `typeParameters`, `satisfies`, `types` or `procedures` written empty, under [the document format](../WARP-11/SPEC.md);
- an enum declared under a name that holds no type's name grammar or under a word the language writes itself, under [checking](../WARP-67/SPEC.md);
- an extension of an enum the document declares, under the enum's bare name, as of a struct under [types](../WARP-58/SPEC.md).

### A case's value

**A value of an enum is a struct under one of its cases' spellings**, its fields the values that case carries: `remote` of `App.Target` carrying `"a"` and `8080` is `(struct App.Target.remote (field host "a") (field port 8080))`, and `local` is `(struct App.Target.local)`. Sameness under [values](../WARP-4/SPEC.md), the key order under [values](../WARP-3/SPEC.md), `text` under [the standard vocabulary](../WARP-79/SPEC.md) and both encodings under [encodings](../WARP-5/SPEC.md) read it as the struct it is: two values of one enum are the same where they are of one case and carry the same values, two cases are two values, and `Standard.Text.text` spells the value above `App.Target.remote {host:"a",port:8080}`. A host hands one in this shape and is handed one in it. A value carries its case's spelling and nothing of what the enum was applied to, as a struct carries nothing of what it was applied to.

**A body makes one with a case literal**, `{ case: { remote: { host: <expression>, port: <expression> } } }`: a dictionary of one entry, the case's name and its fields, each an expression, made in the order of their names, and `{ case: { local: {} } }` for a case that carries nothing. One holding no entry or more than one **refuses at the load**. It writes no enum's name and is read as the enum its place reads, as a struct literal is read as the declared struct its place reads under [types](../WARP-49/SPEC.md), an Optional's some included, and takes its case's spelling there. The build judges it there: the case is one the enum declares, and its fields are exactly those the case carries, each held to its type as a struct literal's field is. A case the enum does not declare, a field short or over, and a case literal written where no enum is read (at `Any`, at a contract, at a type parameter no call fills with an enum, or at a declared struct) **refuse at the build**. A cast is a place, so `(as (case local) App.Target)` is how one reaches `Any`, under [expressions](../WARP-32/SPEC.md).

**A case literal of an enum taking type parameters** is read as applied to what its place applies the enum to, and where the place leaves a position to a call, to what the fields standing on that parameter read as, joined, and to `Never` where no field does, as a struct literal is under [types](../WARP-50/SPEC.md): `(case failure (field error "x"))` handed where `App.Result<some T, some E>` is declared fills `E` with `String` and `T` with `Never`.

### In the text

```
(enum App.Target                            types."App.Target": { enum: …, … }
  (typeParameter T)                         typeParameters += "T"
  (satisfies Hashable)                      satisfies: [Hashable]
  (case local)                              enum.local: {}
  (case remote (field host String) (field port Int))
                                            enum.remote: { host: String, port: Int }
  (type Item Int)                           types.Item: "Int"
  (procedure describe …))                   procedures.describe

(case remote (field host "a") (field port 8080))
                                            { case: { remote: { host: "a", port: 8080 } } }
(case local)                                { case: { local: {} } }

(struct App.Target.remote (field host "a") (field port 8080))
                                            a value of the enum, as data
```

- An `enum` node writes a `types` entry holding `enum` whatever `case` nodes it holds, under *the nodes* in [the text](../WARP-37/SPEC.md#the-nodes), so `(enum App.Target)` writes `enum: {}`, which the load refuses.
- **`case` names three nodes, and the place decides**, under [the text](../WARP-37/SPEC.md): inside `enum` a case the enum declares, inside `switch` past its subject an arm, under [a switch](../WARP-95/SPEC.md), and where a value stands a case literal. Each carries the case's name first, an `identifier` under [names](../WARP-67/SPEC.md#the-grammar), so `(case App.Target.remote)` refuses at the load.
- A value of an enum is data, `(struct <spelling> …)`, and one carrying nothing `(struct App.Target.local)`, under [data](../WARP-42/SPEC.md), as a value from outside and an answer are written. A program writes it as a case literal, since a literal holding a struct refuses at the load.
- The writer lays out `enum`, an enum's `case` and a case literal under [the writer's layout](../WARP-45/SPEC.md).

### In the binary and in an object

**The binary carries nothing new.** The declaration is a dictionary of the tree, and a value of an enum is a struct, tag `0x09`, under its case's spelling, which holds a type's name's grammar, under [encodings](../WARP-6/SPEC.md).

**An object writes the declaration in `types`**, beside a struct and an alias, under [objects](../WARP-85/SPEC.md), under a type tag of its own, which, like a struct's 9, is written in `types` and never as an entry of `typeTable`:

| tag | type | fields |
|---|---|---|
| 20 | enum, written in `types` as the declaration itself and never as an entry | case → (field → *type*), the cases ascending by name, at least one, each case's fields ascending by name; where it takes type parameters, then their names in order and their bounds, as tag 9 writes them |

A mention of an enum, in `typeTable` and in `loweredTypeTable`, is a declared name, tag 14, applied to a list of types where it takes type parameters, so a body standing on one through a cast, a coercion, a call or a dispatch numbers it in `typeNumbering` as it would a struct. Its claims, members and type members are written under its heads as a struct's are, and `typeMembers` writes the enum's own type parameters under its bare head where the document declares it.

**A case literal is a struct built from parts**, operation 3: its layout is the case's spelling and the fields the case carries, ascending, under [objects](../WARP-88/SPEC.md), and it builds exactly the struct a value of that case is. A value of an enum in `valueTable` is a struct, tag 7. Neither needs a tag of its own.

## Interactions

The rules that say where an enum meets the live set stand in Rules, since they are rules; this lists the meeting points.

- A value crosses the door as the struct it is, under [a case's value](#a-cases-value): [WARP-2](../WARP-2/SPEC.md), and [WARP-14](../WARP-14/SPEC.md) for a native procedure's signature.
- A case literal reaches `Any` through a cast, under [a case's value](#a-cases-value): [WARP-32](../WARP-32/SPEC.md).
- Type parameters in the declaration and in a case literal, under [the declaration](#the-declaration) and [a case's value](#a-cases-value): [WARP-50](../WARP-50/SPEC.md) to [WARP-52](../WARP-52/SPEC.md).
- The text and the object format, under [in the text](#in-the-text) and [in the binary and in an object](#in-the-binary-and-in-an-object): [WARP-37](../WARP-37/SPEC.md), [WARP-45](../WARP-45/SPEC.md), [WARP-85](../WARP-85/SPEC.md), [WARP-86](../WARP-86/SPEC.md), [WARP-88](../WARP-88/SPEC.md).

## Alternatives considered

- **An enum as front-end sugar**, lowered to `String` and checks the front end writes. A host's native procedure and an entry take their signatures from the IR, and a front end cannot reach them, so a signature could say `String` and never the enum. The IR holds what a front end cannot write in place, and the type a signature names is that.
- **Raw values in the IR**, a host reading a case's raw value off the signature. A front end writes `rawValue` and a procedure from a raw value as members, and the host turns a raw value into a case's spelling at its door as a JSON decoder does, as a library. What a front end can write as members is not the IR's.
- **A new kind of value for a case.** The value model is a transport model: it holds what crosses the door, and a named struct already carries a case and its fields. A kind of its own would add a shape to every encoding, every door and every sameness rule for nothing a struct does not carry.
- **A case travelling as a bare `String`**, `"local"` for a case that carries nothing. At `Any` the value would be that string and nothing else, so it could not say which enum it is of, and the enum would be a refinement of `String`, a set of allowed strings, which is a check about what a value means and not a type.
- **Raising the document version.** The version goes up when an existing document's meaning changes, and adding a declaration kind changes no existing document's answers: a document that writes no enum reads as it did. Raising it would, since an implementation reads the current version only under [the version](../WARP-9/SPEC.md), change every case's answer and replace the whole accepted set.

## Notes

**Note.** The core is what a front end cannot write in place: the type a host's signature names, the shape a value crosses the door in, and a [switch](../WARP-95/SPEC.md) the build holds to every case. Every other part of a source language's enum is written with these, and the families below are what the core is measured against:

| source | written as |
|---|---|
| Swift `enum` with associated values | an enum, a case per case. A labelled value is a field under its label, and an unlabelled one a field under a name the front end gives it by position, `_0`, `_1`. `indirect` writes nothing, since an enum may name itself |
| Swift raw values and `CaseIterable` | members: `rawValue` returning by a switch, a procedure `App.Level.fromRawValue` returning an Optional, `allCases` returning a list in the source's order. The host turns a raw value into a case's spelling at its door by the signature, as a JSON decoder is a library |
| Swift `Equatable` and `Hashable` | `Equatable` is sameness and asks no claim; `Hashable` is claimed as the source writes it |
| Rust `enum` | an enum. A unit variant is a case carrying nothing, a tuple variant a case with fields `_0`, `_1`, a struct variant a case with its fields; `Box<Self>` is the enum named directly; `#[derive(PartialEq, Eq, Hash)]` is sameness and a claim of `Hashable`; `match` is a switch |
| Haskell `data` | an enum per type, a case per constructor, its type variables the enum's type parameters. Positional fields are named by position and record fields by their names; `deriving Eq` is sameness, `deriving Show` a member; `case … of` is a switch |
| Kotlin `sealed class` and `sealed interface` | an enum whose cases each carry one struct: a subclass `Remote(val url: String)` is a struct `App.Remote` and a case `remote` carrying it as `value`, and an `object` subclass a case carrying nothing. A `when` with `is` arms is a switch whose arms bind `value`, and a slot of the subclass is a slot of `App.Remote`, which is how Swift writes the same thing |
| TypeScript discriminated union | an enum, a case per member named by its discriminant's literal where that is an identifier and by a name the front end gives it otherwise. The discriminant is the case and no field; the other properties are fields. `switch (x.kind)` is a switch |
| Java `enum` | an enum of cases carrying nothing. What a constant's constructor fixes, `EARTH(5.97e24)`, is a member returning it by a switch; methods, and a constant's own body, are members; `values()`, `ordinal()` and `valueOf` are members |
| C#, C and protobuf integer enums | an enum of cases carrying nothing, its integer a member and a procedure from `Int` returning an Optional, as a raw value is. A protobuf open enum adds a case `unrecognized` carrying `value: Int`, which the procedure from `Int` returns for a number no case names. A C# `[Flags]` enum is an `Int` and its members, since a value of several flags is no one case |
