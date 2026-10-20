# The text

How a document and a case are written as the IR's own nodes: the text encoding's second layer. The first, atoms and lists, is under [encodings](encoding.md), and knows nothing of Warp. This layer reads a list by the word it begins with and makes the tree's node, and it judges nothing: what a tree says is the load's to judge, under [checking](checking.md), whether the tree came from a text or from bytes. One tree, one text. The writer gives a tree the one text below, and refuses a tree no node writes back as itself.

Only text is quoted, always, so a name stands bare wherever it reads back bare, under [encodings](encoding.md). A type and a path are nodes too, and the node writes the string the tree holds for it.

## The rule

- **A list's first atom is a word**, and the word says which node it is. Every other position holds an operand: a name, a value, a type, a path or another node.
- **A mapping of the tree is a node, and each of its keys a node inside it**, `(key …)`. A node a map holds under a name carries the name first: `(procedure App.g …)`, `(field x Int)`.
- **A list of the tree** is a node holding its elements in order where they are values, types or statements: `(array …)`, `(body …)`, `(failing …)`, `(satisfies …)`, a procedure type's `(parameters …)`. Where its elements are mappings or pairs, each element is a node of the key's singular, repeated in order: `(import …)`, `(parameter …)`, `(typeParameter …)`, a contract's `(type …)` and `(document …)`, and the first four stand free among the other nodes of what holds them. A case's `arguments` is a mapping, and each of its entries is an `(argument name value)`. Three element words name what the tree gives no key: a dictionary's `(entry k v)`, a struct's `(field x …)`, an extension's `(head …)`.
- **Some operands stand by position**: a call's and an apply's callee and then its arguments, a cast's subject and then its type, a statement's name and then its value, a document variable's name, type and start, a leave's operand. Two things stand bare: an expression written where a statement stands is the statement `{ value: e }`, and a name where a value stands is the path of that one name, `{ ref: x }`.
- **An operand is never a word where a name could stand.** The two operands that are words, an access and a stage, stand where no name does. What a body may fail with is either the word `anything` or names, so the word is a node, `(failing (anything))`, and `(failing anything)` is a failure named `anything`. A break's operand is a name, so `(break null)` **refuses** (`null` is no name) and ``(break `null`)`` names a loop called `null`.
- **One word may name two nodes in two places, and the place decides**, each the tree's own key there:
  - `type`: a slot's type inside `parameter`, `let` and `var`; a type a document declares, or a struct or an extension gives; a type a contract asks.
  - `field`: a type in a struct's declaration, a value in a struct expression, a segment in a path.
  - `struct`: a declaration at the top, a value or an expression where a value stands.
  - `const` and `var`: declarations at the top; a flag and a statement inside a procedure.
  - `procedure`: a declaration, a procedure type inside a type.
  - `array` and `dictionary`: an expression or a value, a type inside a type.
  - `var`: a field's mark inside a type.
  - `const`, `isolated` and `failing`: a procedure's, and a procedure type's inside a type.
  - `document`: an identity's bytes in a case, a document inside `documents`.
- **What a text is, is the word it begins with**: `(warp …)` a document, `(test …)` a case. A text beginning with any other **refuses**, and so does an atom standing at the top, in no node. `(warp 1)` stands first at the top of a text; inside a case, under `program` and `document`, it stands among the other nodes like any key's.
- **Layout is free on the way in**: white space between atoms, and the nodes for a mapping's keys in any order. What the tree holds as a list keeps the order written: imports, parameters, statements, `satisfies`, type parameters, a contract's types, `failing`, a composition, a bound. A key written twice **refuses**: two values under one key are two documents, not one document laid out twice.

## A document

```
(warp 1)                                    warp: 1, first
(description "…")                           description
(import Standard.Numeric.plus)              imports += "Standard.Numeric.plus"
(import App.Point Hashable)                 imports += "App.Point: Hashable", a claim
(const seven <expression>)                  const.seven
(var count <expression>)                    var.count: <expression>
(var count (type Int) <expression>)         var.count: { type: Int, value: <expression> }
(type App.Id Int)                           types."App.Id": "Int"
(struct App.Box …)                          types."App.Box": { struct: …, … }
(contract App.Named …)                      contracts."App.Named"
(extension (head <type>) …)                 extensions."<the head's string>"
(procedure App.g …)                         procedures."App.g"
```

- A document is a sequence of nodes, `(warp 1)` first. A document writing no `import` writes `imports: []`.
- An import holds a spelling, under [the document format](document.md). A claim is two names, joined with `: ` in the tree.
- A document's variable always has a start: `(var count)` writes no tree.
- **Names the tree joins into one string have a text where the load reads the string back as those names.** An import is cut at each `:`, its halves read without white space at their ends; a `typeParameter` and a contract's `type` at their first `:`, and their bound, as a `bound`'s, at each `&` outside brackets. So a name the cut reads otherwise, one holding `:` or `&` or with white space at an end among them, has no text there, and **refuses**.

## Declarations

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
- A member is a procedure under its short name, called as `(call App.Box.area …)`.
- A contract's procedure is its signature, `const` and `isolated` among it. One writing a `body`, a `result`, a `description` or an `access` has a tree, which the load refuses.
- A bound is the contracts' names after the name it bounds. A head is a type, and the tree's key is its string.

## Procedures and closures

```
(procedure App.g
  (description "…")                         description
  (access public)                           access: public; also internal, private
  (const)                                   const: true
  (isolated)                                isolated: true
  (parameter f (type <type>) (description "…"))   parameters += { name: f, type, description }
  (returns <type>)                          returns
  (failing aborted cast_refused)            failing: [aborted, cast_refused]
  (bound C.Item Hashable)                   bounds."C.Item": "Hashable"
  (sameType C.Item Int)                     sameTypes."C.Item": "Int"
  (body <statement> …)                      body: [...]
  (result <expression>))                    result
(closure …)                                 closure: { the same keys }, no name
```

- **A closure is a procedure without a name**, the same nodes under `closure`.
- `(const)` and `(isolated)` write `true`. A tree holding `false` there has no node.
- `(parameter f)` writes no `type`, and takes anything. `(parameter f (type Any))` writes `type: "Any"`, which the load refuses as a second spelling.
- `(failing (anything))` writes `failing: "anything"`. `(failing)` writes `failing: []`, which the load refuses.
- A type parameter's bound stands at its first naming in a slot, `(parameter of (type (some C Lib.Container)))`, and an associated type's in `bound` and `sameType`.
- A procedure writing no `body` writes none in the tree; `(body)` writes `body: []`, which the load refuses.

## Types

A type is an atom or a node, and the node writes the string the tree holds for it: the type's spelling under [types](type.md), parts in the order written.

```
Any Never Null Bool Int Double String Procedure Self     the types the language names
App.Point  App.Named                        a declared type or contract, by its name
(array T)                                   "Array<T>"
(dictionary K V)                            "Dictionary<K, V>"
(named App.Box Int String)                  "App.Box<Int, String>"
(nullable T)                                "T?", and "(T)?" where T is a `(procedure …)` node
(composition A B)                           "A & B"
(some T)  (some T App.Named Hashable)       "some T", "some T: App.Named & Hashable"
(some T.Item)  Self.Item                    "some T.Item", "Self.Item"
(inout T)  (var T)                          "inout T", "var T"
(procedure (const) (isolated) (parameters A (inout B)) (failing x) (returns R))
                                            "const isolated (A, inout B) throws(x) -> R"
(procedure (const))                         "const Procedure"
```

- **One type, one node.** A type node writes its string, and the string read back with the type grammar under [types](type.md) is the node again; a node that comes back as another **refuses**. So `(named Array Int)` refuses, since `(array Int)` writes `Array<Int>`; `(composition A)` and `(named App.Box)` refuse, since a name alone is the atom; `(nullable (inout T))` refuses, since `inout T?` reads as `(inout (nullable T))`; a name holding what the grammar cuts a type at, such as `>` or `&`, refuses; and a procedure type's parts stand in the order its modifiers, `parameters`, `failing`, `returns`.
- **A procedure type** writes `(parameters …)` and `(returns …)` both, or neither, with `const` or `isolated`, which is `const Procedure`. `Procedure` bare is the atom, so `(procedure)` **refuses**, and so does a procedure type writing one of the two alone. `(failing (anything))` writes `throws`, and `(failing)` writes `throws()`, which the load refuses.
- **A string is a node's where the grammar reads it as one and that node writes it back.** A string the grammar gives no structure, such as `Array<>`, and one written in another spacing, such as `Array< Int>`, has no node, and its tree is written as data. What a type says is the load's to judge, so `(named Dictionary Int)`, `(procedure (isolated) (const))` and `(some Self)` are written, and the load refuses each.
- **A type's and a path's nodes nest at most 128 levels**: a type written inside another is one level deeper than it, and a path between brackets one deeper than the path around it, so `(array Int)` nests one level and `Int` none. Both directions refuse past it before walking further. How deep a type or a path may stand in a document is the load's to judge, counted on from the containers around its string, under [types](type.md) and [expressions](expression.md).

## Statements

```
<expression>                                { value: <expression> }
(let x <value>)                             { let: x, value }
(let x (type Double) <value>)               { let: x, type: Double, value }
(var x)  (var x (type Int))                 { var: x }, { var: x, type: Int }
(var x <value>)  (var x (type Int) <value>)
(set <path> <value>)                        { set: "<the path's string>", value }
<value> := <expression> | <construct>
```

The constructs, each where a statement's value stands:

```
(conditional (when c) (then <statement> …) (else <statement> …))
(loop (while c) (body <statement> …))
(attempt (body <statement> …) (result e) (rescue (body …) (result e)))
(return)  (return e)                        return: null, return: e
(break)  (break w)  (continue)  (continue w)    break: null, break: w
```

- A loop's and an attempt's name is the statement's: `(let w (loop …))`, `(let failed (attempt …))`.
- **A leave's operand is optional, and its `)` says so.** A `return` of null is `(return)`, so `(return null)` **refuses**.
- A binding takes any value, so `(let x (return 1))` and `(let r (conditional …))` are written, and the load refuses each for what it says, under [statements](statement.md). So are `(let x)` and `(set x)` with no value and `(set x (type Int) 1)`. `(var x)` writes no `value` and `(var x null)` writes `value: null`, two trees. A `type` with no name is a statement no node writes, and **refuses**.
- A conditional's arms and a loop's body are statements, and `(then)` or `(body)` holding none writes `[]`.

## Expressions and paths

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
(closure …)
```

- **A path is a node** of its head name and its segments: `(field b)` and `(field? b)` for `.b` and `?.b`, `(index …)` and `(index? …)` for `[…]` and `?[…]`, the index a whole number, text, or a name or a path read from. The node writes the path's string under [expressions](expression.md), an index's text with `\"` and `\\` its only escapes.
- A name alone is the path of that one name, and `(path a)` with no segment **refuses**. A path whose string reads back as another path has no tree and **refuses**: a name holding `.`, `[`, `]` or `?`, or white space at an end, and an index name that reads as a number. A path with a marked head or an index first is no node, and its tree is written as data (below).
- **`call` calls a declaration and `apply` a value**, both written under `call` in the tree. `call`'s first operand is the declaration's name, which the tree holds as text; `apply`'s is any expression. Text as `apply`'s callee has no tree, since text under `procedure` names a declaration, and **refuses**. With no arguments neither writes `arguments`.
- A construct is not an expression, so `(call f (loop …))` is no node.
- A struct with a name is a value, and what stands inside it is read as data: `(dictionary …)` there is a map, and a path or a call there has no tree. The load refuses a literal holding a struct's name, under [values](value.md).

## Data

Data is the nodes above that hold values, read as values: the scalars, `(array …)`, `(dictionary (entry k v) …)` and `(struct Name (field x v) …)`. A map is keyed by values, and each entry writes its key as the value it is, so the text `"null"` and the value `null` are two keys, and a map keyed by a struct writes `(dictionary (entry (struct App.Point (field x 1)) 5))`. Data is what a case's answer, its arguments and an object are written in, and a sentence quoting a value writes it as data on one line.

## A case

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

- A case says what it is by `(test 1)` as a document does by `(warp 1)`, under [conformance](conformance.md). `(program …)` writes the nodes the program's tree holds.
- Inside `vocabulary` a procedure, a member included, is its signature's nodes and `(answers <data>)`, and no body. A vocabulary writing no `import` writes `imports: []`.
- A `text` case holds a document's text, and what it asks of a value's spelling it asks through a literal in that text.
- **`(tree <data>)`** is the case's `program` written as data, `(dictionary (entry "warp" 1) (entry "imports" (array)) …)`, for a program no node writes back as itself: an unknown key, a key beside another it may not stand beside, a value of the wrong kind, a missing `imports`, `const: false`, an empty list no node writes (`parameters: []`, `typeParameters: []`, a contract's `types: []`, `arguments: []`), a construct or a mapping where a value is wanted, a statement no node writes, a path with a marked head, a type or a path in a spelling no node writes. The case's tree is the same one either way. The writer writes `(program …)` where the program's nodes read back as it, and the reader **refuses** a `(tree …)` whose program a node writes.

## The writer's layout

- **A list breaks when it is a block holding a list, or holds a list that breaks.** A list that breaks keeps the atoms it begins with on its first line and writes each part after them on a line of its own, two spaces deeper; its `)` closes the last line. Every other list is written on one line.
- The blocks, decided by place: a declaration's node (`procedure`, `struct`, `contract` and `extension` at the top, and `procedure` inside them), `closure`, the constructs (`conditional`, `loop`, `attempt`, `rescue`) and their statement lists (`body`, `then`, `else`), and a case's `program`, `documents`, `document` inside `documents`, and `vocabulary`. A type's `procedure`, a struct value and data are not blocks.
- At the top of a text, one node a line, and a blank line before each node that breaks.
- Parts stand in the writer's order: in a procedure `description`, `access`, `const`, `isolated`, the parameters, `returns`, `failing`, `bound`, `sameType`, `body`, `result`, `answers`; in a document `warp`, `description`, the imports, constants, variables, types, contracts, extensions and procedures, each kind by name; in a case `test`, `name`, `note`, `documents`, `vocabulary`, `program` or `tree`, `bytes`, `text`, `object`, `document`, `arguments`, `expect`; inside the other nodes in the order this page shows them, each kind by name. Data writes a map's entries in the key order and a struct's fields ascending by their names' bytes, under [values](value.md). The text ends with one newline.

A case as the writer lays it out:

```
(test 1)
(name "an-operand-calls-a-value-its-type-says-is-const")
(note "…")

(program
  (warp 1)
  (import Standard.Numeric.plus)
  (procedure App.g
    (parameter f (type (procedure (const) (parameters) (returns Int))))
    (returns Int)
    (result (call Standard.Numeric.plus 1 (apply f))))
  (procedure entry
    (access public)
    (returns Int)
    (result
      (call App.g
        (closure
          (const)
          (returns Int)
          (result 1))))))
(expect (answers 2))
```

## Cases

What `conformance/` asks about this page, by the name each case's file carries.

- `a-map-keyed-by-values-spells-as-text`
- `a-return-of-null-written-out-refuses`
- `a-struct-spells-from-text`
- `a-text-key-written-twice-refuses`
- `a-text-reads-in-any-layout`
- `an-atom-outside-every-node-refuses`
- `the-golden-document-spells-as-text`
