# WARP-45: The writer's layout

Status: accepted

## Summary

The writer's layout fixes how the text is laid out. The rules decide which lists break, how deep their parts are indented, the order of parts inside each node, and how a text begins and separates its nodes.

## Motivation

A list breaks by the node it is and what it holds, so where a line breaks does not depend on how long a name happens to be.

## Rules

- **A list breaks when it is a node that breaks by place and holds a list, or holds a list that breaks.** A list that breaks keeps the atoms it begins with on its first line and writes each part after them on a line of its own, two spaces deeper; its `)` closes the last line. Every other list is written on one line.
- At the top of a text, one node a line, and a blank line before each node that breaks.
- **A node's parts stand in the order the table below gives, and it breaks by place where the table says so.** Each kind of part a row names more than one of stands by name, ascending by the UTF-8 bytes of the names with no case mapping, save where the row says otherwise. A node the table does not name holds its operands in the order [the text](../WARP-37/SPEC.md#the-nodes) gives them and does not break by place, a type's `procedure`, a struct value and data among them. Data writes a dictionary's entries in the key order and a struct's fields ascending by their names' bytes, under [values](../WARP-3/SPEC.md). The text ends with one newline.

| node | its parts, in the writer's order | breaks by place |
|---|---|---|
| a document, at the top of a text and inside `program`, a `document` inside `documents`, and `vocabulary` | `warp`, or an interface's `interface`, the `import`s of names in the order `imports` lists them, then the `import`s of claims in the order `importedClaims` lists them, the `const`s, the `var`s, the nodes of `types`, `type`, `struct` and `enum` alike, by name, the `contract`s, the `extension`s by the bytes of their heads' strings and the `procedure`s | `program`, a `document` inside `documents`, and `vocabulary` |
| a case, at the top of its text | `test`, `name`, `note`, `documents`, `vocabulary`, `program` or `tree`, `bytes`, `text`, `object`, `document`, `arguments`, `expect` | |
| `documents` | the `document`s in the order the list holds them | yes |
| `struct` | its name, the `typeParameter`s in the order `typeParameters` lists them, `satisfies`, the `field`s, the `type`s, the `procedure`s | at the top of a document |
| `enum` | its name, the `typeParameter`s in the order `typeParameters` lists them, `satisfies`, the `case`s, the `type`s, the `procedure`s | at the top of a document |
| `case`, an enum's in its declaration | the case's name, the `field`s | |
| `contract` | its name, the `type`s in the order its `types` lists them, the `procedure`s | at the top of a document |
| `extension` | `head`, `satisfies`, the `type`s, the `procedure`s | at the top of a document |
| `procedure`, and `closure` | a procedure's name, `access`, `const`, `isolated`, the `parameter`s in the order `parameters` lists them, `returns`, `failing`, the `bound`s, the `sameType`s, `body`, `answers` | at the top of a document and inside a declaration; `closure` everywhere |
| `conditional` | `when`, `then`, `else` | yes |
| `loop` | `while`, `body` | yes |
| `try` | `body`, `catch` | yes |
| `unwrap` | what it takes apart, `then`, `else` | yes |
| `switch` | what it takes apart, the arms, by case name, `default` | yes |
| an arm, `case` past a switch's subject | the case's name, the `bind`s, by field name, `then` | yes |
| `body`, `then`, `else`, `catch`, `default` | the statements in order | yes |
| `struct` where an expression stands | the `field`s | |
| `case` where a value stands, a case literal | the case's name, the `field`s | |
| `arguments` | the `argument`s | |

### The bytes

What the rules above lay out is these bytes, in the notation of [names](../WARP-67/SPEC.md#the-grammar), each `atom` as the writer writes it under [Warp text](../WARP-7/SPEC.md#the-grammar):

```
written-text     = top-node { line-feed [ line-feed ] top-node } line-feed
top-node         = one-line-list | broken
one-line         = atom | one-line-list
one-line-list    = "(" one-line { space one-line } ")"
broken           = "(" atom { space atom } part { part } ")"
part             = line-feed indent ( one-line | broken )
indent           = space space { space space }
space            = U+0020 space
line-feed        = U+000A line feed
```

| part | what it may be |
|---|---|
| a `broken` | a list that breaks, under the first rule above; every other list is a `one-line-list` |
| the `atom`s a `broken` begins with | every atom it holds before its first list |
| the `[ line-feed ]` before a `top-node` | written where that node is a `broken`, and only there |
| a `part`'s `indent` | two `space`s for each `broken` that holds the part |

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
    (body
      (return (call Standard.Numeric.plus 1 (apply f)))))
  (procedure entry
    (access public)
    (returns Int)
    (body
      (return
        (call App.g
          (closure
            (const)
            (returns Int)
            (body
              (return 1))))))))
(expect (answers 2))
```

## Interactions

## Alternatives considered

## Notes
