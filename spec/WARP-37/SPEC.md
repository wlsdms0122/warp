# WARP-37: The text

Status: accepted

## Summary

The text encoding's second layer reads a list by the word it begins with and makes the tree's node. The rules decide how a first atom names a node, how operands are written, and that one tree has one text.

## Motivation

The writer refuses a tree no node writes back as itself because a tree written as some other tree would be changed between writing and the load, whether or not the build later refuses it.

## Rules

How a document, an interface and a conformance case are written as the IR's own nodes: the text encoding's second layer. The first, atoms and lists, is under [Warp text](../WARP-7/SPEC.md), and knows nothing of Warp. This layer reads a list by the word it begins with and makes the tree's node, and it judges nothing else: what a tree says is the load's to judge, under [checking](../WARP-65/SPEC.md), whether the tree came from a text or from bytes. One tree, one text. The writer gives a tree the one text below, and refuses a tree no node writes back as itself.

Only a string is quoted, always, so a name stands bare wherever it reads back bare, under [Warp text](../WARP-7/SPEC.md). A type and a path are nodes too, and the node writes the string the tree holds for it.

### The rule

- **A list's first atom is a word**, and the word says which node it is. Every other position holds an operand: a name, a value, a type, a path or another node.
- **Each part of the tree is written as the table under *the nodes* [below](#the-nodes) gives it**, by the key it stands under and what holds that key. A part is **wrapped**, one node of its key's word holding what the key holds, `(returns Int)`, `(body …)`, `(satisfies …)`; or **repeated**, one node for each element of a list or each entry of a dictionary, standing among the other nodes of what holds the key, an entry's name first, `(import …)`, `(procedure App.g …)`, `(field x Int)`. A statement and an expression are one node, or an atom, where the tree holds them, and an operand the table gives no node of its own stands by position, in the order the table gives.
- **An operand is never a word where a name could stand.** The two operands that are words, an access and a stage, stand where no name does. What a body may fail with is either the word `anything` or names, so the word is a node, `(failing (anything))`, and `(failing anything)` is a failure named `anything`. A break's operand is a name, so `(break null)` **refuses** (`null` is no name) and ``(break `null`)`` names a loop called `null`.
- **One word may name two nodes in two places, and the place decides**, each the tree's own key there:
  - `type`: a slot's type inside `parameter`, `let`, `var` and `set`; a type a document declares, or a struct, an enum or an extension gives; a type a contract asks.
  - `field`: a type in a struct's declaration or in an enum's case, a value in a struct expression or in a case literal, a segment in a path.
  - `case`: an enum's case in its declaration, an arm past a switch's subject, a case literal where a value stands.
  - `struct`: a declaration at the top, a value or an expression where a value stands.
  - `const` and `var`: declarations at the top; a flag and a statement inside a procedure.
  - `procedure`: a declaration, a procedure type inside a type.
  - `array` and `dictionary`: an expression or a value, a type inside a type.
  - `var`: a field's mark inside a type.
  - `const`, `isolated` and `failing`: a procedure's, and a procedure type's inside a type.
  - `document`: an identity's bytes in a conformance case, a document inside `documents`.
  - `answers`: a vocabulary procedure's fixed return value, a conformance case's expectation.
  - `returns`: a declaration's return type, a procedure type's inside a type.
- **What a text is, is the word it begins with**: `(warp …)` a document, `(interface …)` an interface, `(test …)` a conformance case. A text beginning with any other **refuses**, and so does an atom standing at the top, in no node. At the top of a text `(warp 1)` or `(interface 1)` stands first. Inside a conformance case, under `program` and under a `document` inside `documents`, `(warp 1)` is the node of one key among the others and stands in any order among them.
- **Layout is free on the way in**: white space between atoms, and the order of the nodes for keys among themselves. An operand that stands by position stands where the table gives it, and so does a node the table gives between two of them, the `(type …)` of a `let`, a `set`, and a `var` statement or module variable, between its name or path and its value. Every other node for a key, wrapped or repeated, stands after the operands that stand by position, in any order among the other nodes for keys of what holds it. What the tree holds as a list keeps the order written: `imports`, `importedClaims`, `typeParameters`, `satisfies`, a contract's `types`, `parameters`, a procedure type's parameters, `failing`, a bound's contracts, a composition, statements, an array's elements, a call's arguments, a dictionary expression's pairs and `documents`. A key written twice **refuses**: two values under one key are two documents, not one document laid out twice.

### The nodes

In the operands, a *name* is a `name-atom` under [Warp text](../WARP-7/SPEC.md#the-grammar), a *type* a type's node under [types, in the text](../WARP-39/SPEC.md), a *path* a path node under [a path node](../WARP-41/SPEC.md#a-path-node), *data* a value under [data, in the text](../WARP-42/SPEC.md), and an expression, a statement and a procedure's, a declaration's or a document's *parts* the nodes the tables below give them. *The names an element is read as* are those [a document, in the text](../WARP-38/SPEC.md) gives an import, a `typeParameter` and a contract's `type`.

A document, at the top of a text and inside a case's `program`, a `document` inside `documents`, and `vocabulary`:

| key | node | stands | operands, in order |
|---|---|---|---|
| `warp`, or an interface's `interface` | `warp`, `interface` | wrapped | the version, data |
| `imports`, each element | `import` | repeated | the names the element is read as |
| `importedClaims`, each element | `import` | repeated | the claim's two names, the type's and the contract's |
| `const`, each entry | `const` | repeated | the name, the expression |
| `var`, each entry | `var` | repeated | the name, then `(type …)` holding the entry's `type`, then the entry's `value`, the start |
| `types`, each entry holding a string | `type` | repeated | the name, the type |
| `types`, each entry holding `struct` | `struct` | repeated | the name, the declaration's parts |
| `types`, each entry holding `enum` | `enum` | repeated | the name, the declaration's parts |
| `contracts`, each entry | `contract` | repeated | the name, the declaration's parts |
| `extensions`, each entry | `extension` | repeated | `(head …)` holding the type its key is, then the declaration's parts |
| `procedures`, each entry | `procedure` | repeated | the name, the procedure's parts |

A declaration's parts, a struct's, an enum's, a contract's and an extension's:

| key | node | stands | operands, in order |
|---|---|---|---|
| `typeParameters`, each element | `typeParameter` | repeated | the names the element is read as |
| `satisfies` | `satisfies` | wrapped | each contract's name |
| a struct's `struct`, each entry | `field` | repeated | the field's name, the type |
| an enum's `enum`, each entry | `case` | repeated | the case's name, then a `(field …)` for each of its entries, holding the field's name and the type |
| a contract's `types`, each element | `type` | repeated | the names the element is read as |
| a struct's, an enum's or an extension's `types`, each entry | `type` | repeated | the type member's name, the type |
| `procedures`, each entry | `procedure` | repeated | the name, the procedure's parts |

A procedure's parts, a declaration's, a member's, a contract's procedure's, a closure's and a vocabulary's procedure's:

| key | node | stands | operands, in order |
|---|---|---|---|
| `access` | `access` | wrapped | the access, a word |
| `const`, `isolated` | `const`, `isolated` | wrapped | none, for `true` |
| `parameters`, each element | `parameter` | repeated | its `name`, then `(type …)` holding its `type` where it writes one |
| `returns` | `returns` | wrapped | the type |
| `failing` | `failing` | wrapped | each failure's name, or `(anything)` for `"anything"` |
| `bounds`, each entry | `bound` | repeated | the label, then each contract's name the bound joins |
| `sameTypes`, each entry | `sameType` | repeated | the label, the type |
| `body` | `body` | wrapped | each statement |
| `answers` | `answers` | wrapped | the value, data |

A statement, and a construct, which a statement's `value` holds as a dictionary of one key:

| tree | node | operands, in order |
|---|---|---|
| `{ value: v }` | none: `v`, an expression or a construct, stands bare | |
| `let`, `var` | `let`, `var` | the name, then `(type …)` holding its `type` where it writes one, then its `value` where it writes one |
| `set` | `set` | the path, then `(type …)` holding its `type` where it writes one, then its `value` where it writes one |
| `conditional` | `conditional` | `(when …)` holding the expression, then `(then …)` and `(else …)` holding statements, each where it writes the key |
| `loop` | `loop` | `(while …)` holding the expression, then `(body …)` holding statements, each where it writes the key |
| `try` | `try` | `(body …)` and `(catch …)` holding statements, each where it writes the key |
| `unwrap` | `unwrap` | its `of`, then `(then …)` and `(else …)` holding statements, each where it writes the key |
| `switch` | `switch` | its `of`, then for each entry of `cases` a `(case …)` holding the case's name, a `(bind …)` for each entry of its `binds` holding the field's name and the name bound, and `(then …)` holding statements, then `(default …)` holding statements where it writes `default` |
| `return` | `return` | the expression, none for null |
| `break`, `continue` | `break`, `continue` | the name, none for null |

An expression:

| tree | node | operands, in order |
|---|---|---|
| a scalar | none: the atom stands bare | |
| `ref` | none: its path stands bare, `(path …)` or a name alone | |
| `call` holding a string under `procedure` | `call` | the procedure's name, then each argument |
| `call` holding an expression under `procedure` | `apply` | the expression, then each argument |
| `as`, `as?` | `as`, `as?` | its `of`, then the type |
| an array | `array` | each element |
| `dictionary` | `dictionary` | an `(entry …)` for each pair, holding the key and the value |
| `struct` | `struct` | a `(field …)` for each entry, holding the field's name and the expression |
| a struct value | `struct` | data |
| `case` | `case` | the case's name, then a `(field …)` for each of its entries, holding the field's name and the expression |
| `closure` | `closure` | the procedure's parts |

A case, at the top of its text:

| key | node | stands | operands, in order |
|---|---|---|---|
| `test`, `name`, `note`, `bytes`, `text`, `object`, `document` | the key | wrapped | the value, data |
| `documents` | `documents` | wrapped | a `(document …)` for each element, holding the document's parts |
| `vocabulary` | `vocabulary` | wrapped | the vocabulary's parts, a document's |
| `program` | `program`, or `tree` | wrapped | the program's parts, a document's, or under `tree` the program as data, under [a case, in the text](../WARP-44/SPEC.md) |
| `arguments` | `arguments` | wrapped | an `(argument …)` for each entry, holding the name and the value as data |
| `expect` | `expect` | wrapped | a node of the one key it holds: `answers`, `reads`, `spells` or `builds` holding the value as data, or `refuses` holding the stage, a word |

**Note.** No case holds the writer's refusal of a tree no node writes back as itself. A `spells` case writes only a tree read from a text, which a node writes, and a `refuses` case asks the reader, so an implementation holds that refusal by tests of its own.

## Interactions

- A key written twice, and one spelling: [a document says each thing one way](../WARP-11/SPEC.md).

## Alternatives considered

- The value tree written as data, one general syntax for any tree. Names are then quoted, types written as strings and structure words written as bare keys, and a bare key collides with a struct's name written bare.
- A text shaped like a source language, punctuation around the IR's words. The text is read by cases, dumps and objects, while a person's program comes through a front end.

## Notes

The text is no general syntax for any tree, so a runtime in another language writes a parser for the text's nodes as well as for its atoms and lists.
