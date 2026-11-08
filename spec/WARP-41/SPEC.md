# WARP-41: Expressions and paths, in the text

Status: accepted

## Summary

The text spelling of expressions and paths. The rules decide the node for each form, namely scalars, paths and their steps, calls, casts, arrays, dictionaries, structs and closures, and what each becomes in the tree.

## Motivation

A path in the tree is one string, `a.b?.c[0]`, and a call a dictionary of `procedure` and `arguments`. A path node writes the string from its names and segments, so a name cannot carry a step of its own into it: with no rule on the name, ``(path a (index `1`))`` writes `a[1]`, which reads back as a position, and one implementation would answer the element at 1 where another refuses the same text.

## Rules

```
null true false 1 1.5 "hi" x"6a"            the scalar
x                                           { ref: x }
(path a (field b) (field? c) (index 0) (index "k") (index i) (index? j))
                                            { ref: "a.b?.c[0][\"k\"][i]?[j]" }
(call App.g 1 x)                            { call: { procedure: "App.g", arguments: [1, { ref: x }] } }
(apply f 1)  (apply (apply f) 2)            { call: { procedure: <expression>, arguments } }
(as e Int)  (as? e Int)                     { as: { of: e, type: Int } }, { as?: { … } }
(array 1 x)                                 [1, { ref: x }]
(dictionary (entry "a" 1) (entry k 2))      { dictionary: [["a", 1], [{ ref: k }, 2]] }
(struct (field x 1) (field y e))            { struct: { x: 1, y: e } }
(struct App.Point (field x 1))              the struct value, as a literal
(case remote (field port 1))                { case: { remote: { port: 1 } } }
(closure …)
```

- **A path is a node** of its head name and its segments, under *a path node* [below](#a-path-node).
- **`call` calls a declaration and `apply` a value**, both written under `call` in the tree. `call`'s first operand is the declaration's name, which the tree holds as a string; `apply`'s is any expression. A string as `apply`'s callee has no tree, since a string under `procedure` names a declaration, and **refuses**. With no arguments neither writes `arguments`.
- A construct is not an expression, so `(call f (loop …))` is no node.
- A struct with a name is a value, and what stands inside it is read as data: `(dictionary …)` there is a dictionary, and a path or a call there has no tree. The load refuses a literal holding a struct's name, under [values](../WARP-2/SPEC.md).
- A case literal's parts are written as [enums](../WARP-93/SPEC.md#in-the-text) writes them.

### A path node

A path node reads `identifier` from [names](../WARP-67/SPEC.md#the-grammar), and `list`, `name-atom`, `integer-atom` and `string-atom` from [Warp text](../WARP-7/SPEC.md#the-grammar). Each node is a `list`, its elements the atoms and nodes shown.

```
path-node        = name-atom | "(" "path" name-atom segment { segment } ")"
segment          = "(" ( "field" | "field?" ) name-atom ")"
                 | "(" ( "index" | "index?" ) index-node ")"
index-node       = integer-atom | string-atom | path-node
```

| part | what it may be |
|---|---|
| a `path-node`'s `name-atom`, and a `field`'s or a `field?`'s | an `identifier` |

A path node writes the string a `ref` or a `set` holds, a `path` under [a path](../WARP-31/SPEC.md#the-grammar): its `name-atom` is the head, `(field b)` the step `.b` and `(field? b)` the step `?.b`, and `(index …)` the step `[…]` and `(index? …)` the step `?[…]`, the brackets holding the `integer` an `integer-atom` is, the `string` a `string-atom` is, and the `path` a `path-node` writes. A name alone is the path of that one name. A node the grammar does not produce, `(path a)` with no segment among them, and one with a part the table above does not let it be **refuse**. A tree holding a string there that is no `path` has no path node, and it is written as data, under [data, in the text](../WARP-42/SPEC.md).

## Interactions

## Alternatives considered

- A mark inside an atom for calling a value, such as `@f`. Meaning would then hang on a character inside an atom, where everywhere else it hangs on a list's first word.

## Notes
