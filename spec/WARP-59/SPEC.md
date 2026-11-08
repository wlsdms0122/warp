# WARP-59: Associated types

Status: accepted

## Summary

A contract may ask types as well as procedures. The rules decide how associated types are listed and bounded, how a procedure names one as Self.Item, and how a type gives one by a type member, whose spelling names that type as an alias does.

## Motivation

With `Self` alone, a container contract's `first` could name the container and not what it holds, so it would return `Any` and every caller would cast.

## Rules

**A contract may ask types as well as procedures**, its associated types. It lists them under `types`, each once and each an `entry` under *the grammar* in [a struct may take type parameters](../WARP-50/SPEC.md#the-grammar) whose `identifier` is a type member's name, `{ types: [Item], procedures: { first: { parameters: [Self], returns: "Self.Item" } } }`, and may hold each to contracts beside its name there, `types: ["Item: Hashable"]`, the way a struct holds a type parameter it lists; a name listed twice **refuses at the load**. Its procedures name one as `Self.Item`, the type the type conforming to the contract gives under that name, and an associated type of one as `Self.Item.Key`: `Self` followed by one or more type members' names, each after a dot. The first name is one the contract asks, and one it does not ask **refuses at the load**. Each name after it is an associated type standing on the one before, judged as one standing on another is under [the associated types of a type parameter](../WARP-60/SPEC.md): one no contract bounding what it stands on asks **refuses at the build**, since that contract may stand in another document.

**A type gives one by its type member of that name**, written under `types` beside `procedures` where the document gives the type what it gives it, a dictionary from a type member's name to a type, `types: { Item: "some T" }`, in a struct's or an enum's declaration or in an extension. Under a head a type member writes the head's own type parameters, in a struct's declaration the struct's, and under a bare head elsewhere none, so one taking the type's parameters is given under a head applying the type.

**A type member is named by its spelling**, `App.Box.Item`, which with its name holds the grammar [names](../WARP-67/SPEC.md#the-grammar) gives it, one type member per spelling: one document giving one type a type member under one name twice, under two heads, **refuses at the load**, and two documents giving it **refuse at the build**, as two declarers of a name do. A type member's spelling is a name of the second namespace, under [names](../WARP-64/SPEC.md), and the type member is the one declaration under it, as the case is under a case's spelling under [enums](../WARP-93/SPEC.md#the-declaration): no type, contract or case is declared under it. One document declaring one there beside the type member **refuses at the load**, and two documents, one each, **refuse at the build**, as two declarers of one name do.

**A type member's spelling is an alias of the type the type member gives**, under [what a slot takes, exactly](../WARP-48/SPEC.md): written as a type, it is that type, and a claim or an extension about it is one about an alias, under [claims](../WARP-54/SPEC.md). A type applied to what its brackets hold, followed by a dot and a type member's name, `App.Wrapper<String>.Item`, is an alias too, of the type member's type read under the head it is given under, the head's type parameters read as what the brackets hold. The type before the dot is named as any mention names it, under [how a type is written](../WARP-46/SPEC.md), so one that lists type parameters named without brackets, `App.Wrapper.Item` or `Array.Item`, **refuses at the build**, as `App.Wrapper` does, and so does an Optional's, `Optional.Item`, since no mention names the Optional. So does a reading the head does not take, `App.Wrapper<Any>.Item` where the type member is given under `App.Wrapper<some T: Hashable>`, and a name no type member of the type is given under. Each of these refuses where no module declares a type or a contract under that spelling: a dot is a character of a spelling under [names](../WARP-64/SPEC.md), so `App.Box.Tag` or `Array.Item` declared as a struct is that struct wherever it is mentioned.

**A claim holds where the type gives every type the contract asks**: for each, the type's type member of that name is given in the claim's document or in one it stands on, under a head taking every value the claim's head takes, and its type, read under the claim's head, conforms to what the contract holds it to. A claim that does not **refuses at the build, at the claim**. Two contracts asking one name ask one type member of a type conforming to both.

## Interactions

- An associated type of a type parameter, `some T.Item`, is under [the associated types of a type parameter](../WARP-60/SPEC.md).

## Alternatives considered

## Notes
