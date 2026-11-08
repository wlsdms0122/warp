# WARP-40: Statements, in the text

Status: accepted

## Summary

The text spelling of statements. The rules decide how let, var, set, the constructs and the leaves are written, and how an optional operand of a leave is shown by the closing parenthesis.

## Motivation

A statement in the tree is a dictionary whose keys say what it is, `{ let: x, type: Int, value: 1 }`. Its node writes it as what it does, `(let x (type Int) 1)`, operands by position and parts by their words, so that every implementation reads `(conditional (else) (then) (when c))` as the conditional the writer lays out `when`, `then`, `else`, and refuses `(return null)`, which would otherwise be a second text for `(return)`.

## Rules

```
<expression>                                { value: <expression> }
(let x <value>)                             { let: x, value }
(let x (type Double) <value>)               { let: x, type: Double, value }
(var x)  (var x (type Int))                 { var: x }, { var: x, type: Int }
(var x <value>)  (var x (type Int) <value>)
(set <path> <value>)                        { set: "<the path's string>", value }
```

The constructs, each where a statement's value stands:

```
(conditional (when c) (then <statement> …) (else <statement> …))
(loop (while c) (body <statement> …))
(try (body <statement> …) (catch <statement> …))
(unwrap o (then <statement> …) (else <statement> …))
(switch o (case c (then <statement> …)) … (default <statement> …))
(return)  (return e)                        return: null, return: e
(break)  (break w)  (continue)  (continue w)    break: null, break: w
```

- A loop's, a try's and an unwrap's name is the statement's: `(let w (loop …))`, `(let failed (try …))`, `(let card (unwrap found (else (return))))`.
- **A leave's operand is optional, and its `)` says so.** A `return` of null is `(return)`, so `(return null)` **refuses**.
- A binding takes any value, so `(let x (return 1))` and `(let r (conditional …))` are written, and the load refuses each for what it says, under [statements](../WARP-19/SPEC.md). So are `(let x)` and `(set x)` with no value and `(set x (type Int) 1)`. `(var x)` writes no `value` and `(var x null)` writes `value: null`, two trees, and the load refuses the second. A `type` with no name is a statement no node writes, and **refuses**.
- A switch's arms, its `bind`s and its `default` are written as [a switch](../WARP-95/SPEC.md#in-the-text) writes them.
- A conditional's arms, an unwrap's ways and a loop's body are statements, and `(then)` or `(body)` holding none writes `[]`.

### The grammar

A statement's node reads `list` and `name-atom` from [Warp text](../WARP-7/SPEC.md#the-grammar) and `path-node` from [a path node](../WARP-41/SPEC.md#a-path-node). Each node is a `list`, its elements the atoms and nodes shown.

```
statement        = value | binding
binding          = "(" ( "let" | "var" ) name-atom [ typed ] [ value ] ")"
                 | "(" "set" path-node [ typed ] [ value ] ")"
typed            = "(" "type" type-node ")"
value            = expression | construct
construct        = "(" "conditional" { when-part | then-part | else-part } ")"
                 | "(" "loop" { while-part | body-part } ")"
                 | "(" "try" { body-part | catch-part } ")"
                 | "(" "unwrap" expression { then-part | else-part } ")"
                 | switch
                 | "(" "return" [ expression ] ")"
                 | "(" ( "break" | "continue" ) [ name-atom ] ")"
when-part        = "(" "when" expression ")"
while-part       = "(" "while" expression ")"
then-part        = "(" "then" { statement } ")"
else-part        = "(" "else" { statement } ")"
body-part        = "(" "body" { statement } ")"
catch-part       = "(" "catch" { statement } ")"
expression       = an expression's node, under expressions and paths, in the text
type-node        = a type's node, under types, in the text
switch           = a switch's node, under a switch
```

| part | what it may be |
|---|---|
| a `return`'s `expression` | any but the atom `null` |
| the parts of a `conditional`, a `loop`, a `try` or an `unwrap` | each of `when-part`, `while-part`, `then-part`, `else-part`, `body-part` and `catch-part` once at most |

The nodes a construct holds under its keys, `when`, `while`, `then`, `else`, `body` and `catch`, stand in any order on the way in, each once, after what an `unwrap` takes apart, under [the text](../WARP-37/SPEC.md). A binding's `typed` stands between its name or path and its `value`, and nowhere else. A `switch` is under [a switch](../WARP-95/SPEC.md#in-the-text), an `expression` under [expressions and paths, in the text](../WARP-41/SPEC.md), and a `type-node` under [types, in the text](../WARP-39/SPEC.md).

## Interactions

- A break's operand is a name: [the text](../WARP-37/SPEC.md).

## Alternatives considered

- The text refusing a statement the language never allows, such as `(let x (return 1))`. The rule would then live in two places, the text's and the load's.

## Notes
