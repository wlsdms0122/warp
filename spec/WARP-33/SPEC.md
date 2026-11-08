# WARP-33: A dot reads a name

Status: accepted

## Summary

A dot reads a name and nothing else. The rules decide, segment by segment, what a dot does on a struct type, on a type with no fields and on Any, and that the value arriving at run time has no say.

## Motivation

Which name a dot reads is the IR's, because a dot decided at the run reads whatever happened to arrive. `{ ref: "task.title" }` on a value read as `App.Task` is judged against the declaration, so every runtime refuses `task.titel` before anything runs. On a value read as `Any` there is no declaration, and a runtime that looked the name up in the value would run a document another runtime refuses, which is why the reading is named first with a cast.

## Rules

**A dot reads a name and nothing else.** Every `ref` path is judged where names resolve, and the judgement is written into the image; the value that arrives at run time has no say in it. A procedure is sent with a written `call`, which spells the declaration it means. Segment by segment:

- On a **struct type**, a dot reads the field the type declares. A field it does not declare **refuses at the build**, `?.` or not. The type rules the field out, and no spelling reads past that. A procedure on a struct is written as a call. A struct type says which fields there are, and a value fits it only with exactly them, so there is nothing else to reach.
- On a type that has no fields (`String`, `Int`, `Double`, `Bool`, a list, a dictionary, a procedure, an [enum](../WARP-94/SPEC.md), whose fields are its cases' and none its own), a dot **refuses at the build**: there is no name there to read. The procedure by that spelling is reached by writing the call, and what a list or a dictionary holds through brackets.
- On **`Any`**, a dot or an index **refuses at the build**. Nothing is declared here, so there is nothing for the reading to be judged against, and a dot nothing declares is the one thing a run would have to decide for itself. The type is read by naming it: `{ as: { of: <value>, type: <type> } }` says what the author expects, and every dot after it is judged against that.
- On a **contract**, a dot or an index **refuses at the build** as on `Any`. A contract declares procedures and types and no field, and a value read as one is of a type the build does not know, under [what a slot takes](../WARP-48/SPEC.md), so nothing is declared here for a reading to be judged against. The type is read by naming it, under [a cast](../WARP-32/SPEC.md).
- On a **type parameter** (`some T`), or an associated type, a dot or an index **refuses at the build** as on `Any`. The parameter is one type the body does not know, so nothing is declared here for a reading to be judged against. What a type gives is asked through a contract it conforms to, under [types](../WARP-52/SPEC.md).

## Interactions

- Reading a value read as `Any` or as a contract: [a cast](../WARP-32/SPEC.md).
- A dot past an Optional: [null is not read through](../WARP-34/SPEC.md); what a list or a dictionary holds: [brackets](../WARP-36/SPEC.md).

## Alternatives considered

- A dot that sends a procedure where the type has no field, `items.count`. Answering which declaration the bare name means takes a table over everything a link reaches, so one shorthand widens what building a document reads. A front end that wants the shorthand writes the full `call`.

## Notes
