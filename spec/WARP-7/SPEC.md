# WARP-7: Warp text: `.warpt`

Status: accepted

## Summary

The first layer of the text encoding reads atoms and lists and knows nothing of Warp. The rules decide that a text is UTF-8, what counts as white space, how a list and each kind of atom is spelled, and what a reader refuses.

## Motivation

## Rules

The readable form: a document, an interface or a case written as the IR's own nodes, in two layers. The first reads atoms and lists and knows nothing of Warp, the way the binary's reader knows nothing of what a tree means; it is this section. The second reads a list by the word it begins with and makes the tree's node, under [the text](../WARP-37/SPEC.md).

```
(warp 1)
(import Standard.Numeric.plus)

(procedure entry
  (access public)
  (returns Int)
  (body
    (return (call Standard.Numeric.plus 1 2))))
```

A text is UTF-8 bytes before it is anything else, and bytes that are not **refuse**.

### The grammar

A text reads `digit` from [names](../WARP-67/SPEC.md#the-grammar).

```
text             = items
list             = "(" items ")"
items            = { blank } [ element { { blank } list | blank { blank } atom } { blank } ]
element          = atom | list
atom             = null-atom | bool-atom | integer-atom | double-atom | string-atom | bytes-atom
                 | name-atom
null-atom        = "null"
bool-atom        = "true" | "false"
integer-atom     = "0" | [ "-" ] nonzero-digit { digit }
double-atom      = [ "-" ] ( point-form | exponent-form )
point-form       = ( "0" | nonzero-digit { digit } ) "." digit { digit }
exponent-form    = nonzero-digit [ "." digit { digit } ] "e" ( "+" | "-" ) digit digit { digit }
nonzero-digit    = "1" … "9"
string-atom      = quote { string-scalar } quote
string-scalar    = plain other than quote and backslash | backslash quote | escape
bytes-atom       = "x" quote { hex-digit hex-digit } quote
name-atom        = bare-name | backticked-name
bare-name        = bare-scalar { bare-scalar }
bare-scalar      = plain other than " ", "(", ")", quote and backtick
backticked-name  = backtick name-scalar { name-scalar } backtick
name-scalar      = plain other than backtick and backslash | backslash backtick | escape
escape           = backslash ( backslash | "n" | "r" | "t" | "u" control )
control          = "000" ( "0" … "8" | "b" | "c" | "e" | "f" ) | "001" hex-digit
hex-digit        = digit | "a" … "f"
plain            = any Unicode scalar not below U+0020
blank            = U+0020 space | U+0009 tab | U+000A line feed | U+000D carriage return
quote            = U+0022, the double quote
backtick         = U+0060, the backtick
backslash        = U+005C, the backslash
```

| part | what it may be |
|---|---|
| a `bare-name` | one not beginning with a `digit`, nor with `-` or `+` and a `digit`, and not `null`, `true` or `false` |
| an `integer-atom` | one an `Int` holds |
| a `double-atom` | the one spelling of its binary64 value, below |

A text is its elements in order. **White space** is a `blank`, and nothing depends on a line break: before the first element, after the last and between two it is layout. Any other character, one Unicode counts as white space included, is part of the token it touches, and there are no comments. A list is its elements in order, each an atom or a list. An element is followed by white space, a parenthesis or the end, so a bare token running straight into a quote, a quote into a bare token and bytes into bytes are not a layout of two tokens, and **refuse**.

**An atom's first characters say its kind**: a digit, or `-` or `+` then a digit, begins a number; `x"` begins bytes; `"` begins a string; `` ` `` begins a name; anything else is `null`, `true`, `false` or a name. So a token beginning as a number does is an `integer-atom`, a `double-atom` or nothing: `1.50`, `01`, `+1` and `1.` are no number and no name. **A number with a point or an exponent is a floating-point literal; with neither it is an integer literal.** The difference is grammar, not a reader's guess.

A `double-atom`'s digits are the shortest decimal that reads back to the same binary64, of two as short the one nearer the value, with a `-` where its sign bit is set, `-0.0` included. Which form those digits take is the document's rule, not a host library's: writing the value `d.ddd…×10^k`, the `point-form` when `-5 < k < 16`, otherwise the `exponent-form`, which writes the first digit, a point and the others only where there are others, and `k` with at least two digits. `0.0001` but `1e-05`, `1000000000000000.0` but `1e+16`, so one value keeps one spelling down to its last character.

A `string-atom` is the string of its scalars, an `escape` standing for the backslash, a line feed, a carriage return, a tab, or the scalar its four hex digits spell, and `\"` for the quote. So exactly the quote, the backslash and the scalars below U+0020 are escaped, each by its shortest escape, and nothing else is. A `bytes-atom` is the bytes its digits spell, two a byte. A `name-atom` is the name its scalars spell, a `backticked-name` reading its escapes as a string does, with `` \` `` for the backtick. A name in backticks is the same atom as the name written bare, `` `x` `` and `x` alike, and `` `null` `` is a name where `null` is not. The writer writes a name bare where it reads back bare.

A text the grammar does not produce, and one with a part the table above does not let it be, **refuses**.

Layout is free on the way in. A reader takes any white space between tokens and any indentation, because a text is written by a person as often as by a writer. The writer still lays a text out one way, under [the writer's layout](../WARP-45/SPEC.md), so a text that has been through a writer is the same bytes everywhere, and that is the form the conformance cases are kept in. What is not free is the spelling of a value: a floating-point literal written `1.50` and an escape spelled long **refuse**, since those are two texts for one value rather than two layouts of one text. Sameness of documents is the binary's promise, under [encodings](../WARP-5/SPEC.md), and a text makes it by being written out.

**A refusal names its place.** A text is the encoding a person edits, and a refusal that names no place leaves them to find it. So a text that is refused names a line and a column, save one refused as a whole, as no UTF-8: both counted from one, the column in scalars, and a line ended by a line feed, a carriage return or the two together. The place is where what the reader refuses begins:

| what is refused | its place |
|---|---|
| a bare token: a number, a name, `null`, `true` or `false` | its first scalar |
| bytes holding an odd count of digits | its `x` |
| a scalar a string, a backticked name or bytes does not hold as written | that scalar |
| an escape | its backslash |
| a backticked name holding nothing | its opening backtick |
| a token running straight into another | the first scalar it runs into |
| a list never closed, or a closing parenthesis that closes nothing | that parenthesis |
| a string, a backticked name, an escape or bytes the text ends inside | the end of the text, one scalar past its last |

**Note.** A case matches a refusal by its stage alone, under [conformance](../WARP-1/SPEC.md), so no case holds a place, and the place is held only by tests inside the implementation.

## Interactions

- What is written in it: a case under [WARP-44](../WARP-44/SPEC.md), an interface under [WARP-43](../WARP-43/SPEC.md).

## Alternatives considered

- The text as a writing of the value tree. Inside a value tree everything the IR says is data, so a name would be a quoted string, a type a string and a structural word a bare key, and a bare-key rule collides with the spelling of a struct's name.
- A text shaped like a source language, a source language's punctuation over the IR's words. Programs are built by front ends, and nothing writes programs in it.

## Notes

The text is a grammar of its own, so an implementation in another language writes a reader and a writer for it rather than taking a library's.
