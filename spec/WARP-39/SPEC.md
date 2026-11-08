# WARP-39: Types, in the text

Status: accepted

## Summary

The text spelling of types. The rules decide the atom or node that writes each type, such as arrays, dictionaries, optionals, compositions, bounded parameters and procedure types, and the string each node stands for.

## Motivation

A type in the tree is a string, `Array<some T: Standard.Comparable>`, which a person editing a text would otherwise write and escape by hand. A node for each type writes it `(array (some T Standard.Comparable))`, and one node for each string keeps one text for each tree: were `(named Array Int)` and `(array Int)` both read as `Array<Int>`, two writers would give one document two texts, and a `spells` case would hold only one of them.

## Rules

A type is an atom or a node, and the node writes the string the tree holds for it: the type's spelling under *the grammar* in [types](../WARP-46/SPEC.md#the-grammar), parts in the order written.

```
Any Never Null Bool Int Double String Procedure Self
Hashable Failure Round                      a language-name: the types and contracts the language names
App.Point  App.Named                        a declared type or contract, by its name
(array T)                                   "Array<T>"
(dictionary K V)                            "Dictionary<K, V>"
(named App.Box Int String)                  "App.Box<Int, String>"
(member (named App.Wrapper String) Item)    "App.Wrapper<String>.Item"
(optional T)                                "T?", and "(T)?" where the grammar groups T
(composition A B)                           "A & B"
(some T)  (some T App.Named Hashable)       "some T", "some T: App.Named & Hashable"
(some T.Item)  Self.Item                    "some T.Item", "Self.Item"
(inout T)  (var T)                          "inout T", "var T"
(procedure (const) (isolated) (parameters A (inout B)) (failing x) (returns R))
                                            "const isolated (A, inout B) throws(x) -> R"
(procedure (const))                         "const Procedure"
```

- **One type, one node.** A type node writes its string, and the string read back with *the grammar* in [types](../WARP-46/SPEC.md#the-grammar) is the node again; a node that comes back as another **refuses**. So `(named Array Int)` refuses, since `(array Int)` writes `Array<Int>`; `(composition A)`, `(named App.Box)` and `(member App.Box Item)` refuse, since a name alone is the atom, `App.Box.Item` for the last; `(optional (inout T))` refuses, since `inout T?` reads as `(inout (optional T))`; a name atom writes its name as the string, so one whose string the grammar reads as another node refuses, `` `A & B` `` and `` `Int?` `` among them; and a procedure type's parts stand in the order its modifiers, `parameters`, `failing`, `returns`.
- **A procedure type** writes `(parameters …)` and `(returns …)` both, or neither, with `const` or `isolated`, which is `const Procedure`. `Procedure` bare is the atom, so `(procedure)` **refuses**, and so does a procedure type writing one of the two alone. `(failing (anything))` writes `throws`, and `(failing)` writes `throws()`, which the load refuses.
- **A string is a node's where the grammar reads it as one and that node writes it back.** A string the grammar does not produce, such as `Array<>` or `Array< Int>`, has no node, and its tree is written as data. What a type says is the load's to judge, so `(named Dictionary Int)`, `(procedure (isolated) (const))` and `(some Self)` are written, and the load refuses each.

## Interactions

- What the load refuses about a type: [checking](../WARP-65/SPEC.md).

## Alternatives considered

- The text refusing a type the language never allows, such as `(some Self)`. The rule would then live in two places, the text's and the load's.

## Notes
