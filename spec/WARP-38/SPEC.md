# WARP-38: A document, in the text

Status: accepted

## Summary

The text spelling of a document and its declarations. The rules decide how the document header, imports, constants, variables, types, contracts, extensions and procedures are written, and what each becomes in the tree.

## Motivation

A conformance case writes its program in the text, and runners in other languages read the same file. Were a declaration's spelling an implementation's own, `(var count (type Int) 0)` would read as a module variable in one runner and as no document in another, and the case would measure the runner rather than the program. So each declaration has one node, and the tree it writes is the one [the document format](../WARP-8/SPEC.md) gives.

## Rules

```
(warp 1)                                    warp: 1
(import Standard.Numeric.plus)              imports += "Standard.Numeric.plus"
(import App.Point Hashable)                 importedClaims += [App.Point, Hashable], a claim
(const seven <expression>)                  const.seven
(var count (type Int) <expression>)         var.count: { type: Int, value: <expression> }
(type App.Id Int)                           types."App.Id": "Int"
(struct App.Box …)                          types."App.Box": { struct: …, … }
(enum App.Target …)                         types."App.Target": { enum: …, … }
(contract App.Named …)                      contracts."App.Named"
(extension (head <type>) …)                 extensions."<the head's string>"
(procedure App.g …)                         procedures."App.g"
```

- A document is a sequence of nodes, `(warp 1)` among them, standing where [the text](../WARP-37/SPEC.md#the-rule) places it: first at the top of a text, and in any order among the others inside a conformance case. A document writing no `import` of a name writes `imports: []`, and one writing no `import` of a claim writes no `importedClaims`.
- An import's node holds an `import` or the two names of a `claim` under *the grammar* in [the imports list](../WARP-10/SPEC.md#the-grammar).
- A document's variable always declares its type and has a start, `(var <name> (type <type>) <expression>)`, so `(var count)`, `(var count 0)` and `(var count (type Int))` write no tree, and **refuse**.
- **Names the tree joins into one string have a text where the load reads the string back as those names.** A `typeParameter` and a contract's `type` are an `entry` under *the grammar* in [a struct may take type parameters](../WARP-50/SPEC.md#the-grammar). So a name that grammar reads otherwise, one holding `:` or `&` or with white space at an end among them, has no text there, and **refuses**.

### Declarations

```
(struct App.Box
  (typeParameter K App.Named Hashable)      typeParameters += "K: App.Named & Hashable"
  (typeParameter V)
  (satisfies App.Named App.Other)           satisfies: [App.Named, App.Other]
  (field balance (var Int))                 struct.balance: "var Int"
  (type Item K)                             types.Item: "K"
  (procedure area …))                       procedures.area
(contract App.Named
  (type Item Hashable)                      types += "Item: Hashable"
  (type Key)
  (procedure name (const) (parameter self (type Self)) (returns String)))
(extension (head (array Int))
  (satisfies App.Named)
  (type Item Int)
  (procedure name …))
```

- A struct always writes `struct` in the tree, a struct with no field included.
- An enum's parts are written as [enums](../WARP-93/SPEC.md#in-the-text) writes them.
- A member is a procedure under its short name, called as `(call App.Box.area …)`.
- A contract's procedure is its signature, `const` and `isolated` among it. One writing a `body` or an `access` has a tree, which the load refuses.
- A bound is the contracts' names after the name it bounds. A head is written as a type node, and the tree's key is its string, a head under [heads](../WARP-55/SPEC.md#the-grammar).

### Procedures and closures

```
(procedure App.g
  (access public)                           access: public; also internal, private
  (const)                                   const: true
  (isolated)                                isolated: true
  (parameter f (type <type>))               parameters += { name: f, type }
  (returns <type>)                          returns
  (failing aborted cast_refused)            failing: [aborted, cast_refused]
  (bound C.Item Hashable)                   bounds."C.Item": "Hashable"
  (sameType C.Item Int)                     sameTypes."C.Item": "Int"
  (body <statement> …))                     body: [...]
(closure …)                                 closure: { the same keys }, no name
```

- **A closure is a procedure without a name**, the same nodes under `closure`.
- `(const)` and `(isolated)` write `true`. A tree holding `false` there has no node.
- `(parameter f)` writes no `type`, and takes anything. `(parameter f (type Any))` writes `type: "Any"`, which the load refuses as a second spelling.
- `(failing (anything))` writes `failing: "anything"`. `(failing)` writes `failing: []`, which the load refuses.
- A type parameter's bound stands at its first naming in a slot, `(parameter of (type (some C Lib.Container)))`, and an associated type's in `bound` and `sameType`.
- A procedure writing no `body` writes none in the tree; `(body)` writes `body: []`, which the load refuses.

## Interactions

- A key written as what leaving it out says: [a procedure](../WARP-12/SPEC.md) and [a document says each thing one way](../WARP-11/SPEC.md).
- The order the writer gives these nodes: [the writer's layout](../WARP-45/SPEC.md).

## Alternatives considered

## Notes
