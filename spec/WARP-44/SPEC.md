# WARP-44: A case, in the text

Status: accepted

## Summary

The text spelling of a conformance case. The rules decide the nodes that write a case's program, documents, vocabulary, arguments, inputs and expectation, and how a tree case writes its program as data.

## Motivation

The cases are the suite every implementation runs, so the file a case is kept in is read by runners written in other languages. Its nodes are fixed here so that `(expect (refuses load))` asks the same of each runner, and a program no node writes, written `(tree …)`, is still a case each runner reads.

## Rules

```
(test 1)
(name "…")
(note "…")
(program (warp 1) …)                        a document's nodes
(documents (document (warp 1) …) (document …))
(vocabulary (import …) (struct …) (procedure Lib.f (parameter first (type Int)) (returns Int) (answers 5)))
(arguments (argument c false))
(bytes x"…")  (text "…")  (text x"…")  (object <data>)  (document x"…")
(tree <data>)
(expect (answers <data>))                   also reads, spells and builds; refuses load, build or run
```

- A case says what it is by `(test 1)` as a document does by `(warp 1)`, under [conformance](../WARP-1/SPEC.md). `(program …)` writes the nodes the program's tree holds.
- Inside `vocabulary` a procedure, a member included, is its signature's nodes, then `(answers <data>)` and `(sends <name> …)`, each where it writes one, and no body. A vocabulary writing no `import` writes `imports: []`.
- A `text` case holds a document's, an interface's or a case's text, and what it asks of a value's spelling it asks through a literal in that text.
- **`(tree <data>)`** is the case's `program` written as data, `(dictionary (entry "warp" 1) (entry "imports" (array)) …)`, for a program no node writes back as itself: an unknown key, a key beside another it may not stand beside, a value of the wrong kind, a missing `imports`, `const: false`, an empty list no node writes (`parameters: []`, `typeParameters: []`, a contract's `types: []`, `arguments: []`), a construct or a dictionary where a value is wanted, a statement no node writes, a path with a marked head, a type or a path in a spelling no node writes. The case's tree is the same one either way. The writer writes `(program …)` where the program's nodes read back as it, and the reader **refuses** a `(tree …)` whose program a node writes.

The `expect` node reads `list` from [Warp text](../WARP-7/SPEC.md#the-grammar) and `data` from [data, in the text](../WARP-42/SPEC.md). Each node is a `list`, its elements the atoms and nodes shown, and a `stage` is a `name-atom`:

```
expect           = "(" "expect" expectation ")"
expectation      = "(" ( "answers" | "reads" | "spells" | "builds" ) data ")"
                 | "(" "refuses" stage ")"
stage            = "load" | "build" | "run"
```

Which expectation a case may write, and what each asks, is under [conformance](../WARP-1/SPEC.md).

## Interactions

- A vocabulary's signatures: [an interface](../WARP-43/SPEC.md).
- What `answers`, arguments and `(tree …)` are written in: [data, in the text](../WARP-42/SPEC.md).
- The order of a case's nodes: [the writer's layout](../WARP-45/SPEC.md).

## Alternatives considered

## Notes
