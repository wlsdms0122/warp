# WARP-79: Standard.Text

Status: accepted

## Summary

Standard.Text holds the procedures over strings. The rules decide what each returns, such as contains, split, joined, characters, decoded and encoded, and which inputs refuse at the run.

## Motivation

A platform's case mapping can follow the device's locale, and its set of white space can hold characters Unicode's does not: one widely used set holds the zero-width space U+200B, so `trimmed` taken from it would shorten a string another implementation leaves whole.

## Rules

| procedure | parameters | returns |
|---|---|---|
| `text` | `value` | its spelling |
| `contains` | `text`, `other` | whether `other` stands inside `text` |
| `startsWith` | `text`, `prefix` | whether `text` begins with `prefix` |
| `uppercased`, `lowercased`, `trimmed` | `text` | the text upper-cased, lower-cased and trimmed |
| `characters` | `text` | its characters, each a string |
| `split` | `text`, `separator` | the pieces between the separators |
| `joined` | `strings`, `separator`, written between each two | the strings joined |
| `decoded` | `bytes`, `encoding` | the text the bytes are in the encoding. **refuses at the run** when an element is no byte (an integer from 0 to 255), the encoding is not one it has under [bytes](../WARP-84/SPEC.md), or the bytes are not text in it |
| `encoded` | `text`, `encoding` | the bytes the text is in the encoding. **refuses at the run** when the encoding is not one it has under [bytes](../WARP-84/SPEC.md) |
| `replacing` | `text`, `target`, `replacement` | the text with every occurrence of the target replaced |

`characters` returns the string as an array of its characters, each one a string of its own, counted the way `count` counts. Computed for the whole string rather than read one at a time: a character is an extended grapheme cluster, so where the tenth one starts is only known by walking the nine in front of it, and a body reading them in order would pay that walk every round.

**Two bundles declare `contains`, and they ask different questions.** `Standard.Collection.contains` asks whether an array holds an element; `Standard.Text.contains` asks whether a string holds another string inside it. They are two procedures because a string is not an array here: it has a `count` but no elements to read by position, since where the tenth character starts is only known by walking the nine in front of it. A program that wants a string's characters as a collection asks `characters` for them.

`uppercased` and `lowercased` apply Unicode's full default case mapping and no locale's tailoring: `ß` uppercases to `SS`, a capital sigma ending a word lowercases to the final `ς`, and `i` uppercases to `I` on every machine, whatever its locale says about a dotted `i`.

`trimmed` removes the whitespace at either end and nothing from the middle. A character goes only if **every one of its code points** has Unicode's `White_Space` property, and nothing a platform adds to that set is whitespace here. Both halves of that rule are load-bearing: `\r\n` is one character and two code points, both of them `White_Space`, so it goes; a space carrying a combining mark is also one character and two code points, and the mark is not `White_Space`, so it stays where it was written. A zero-width space is not whitespace in Unicode and so is not trimmed, however a platform's own set decides.

`replacing` rewrites every occurrence, not only the first, and `split` cuts at every occurrence of the separator. For both, occurrences are taken from the start, each search beginning after the last one taken, so in `aaa` the target `aa` is taken once, at the start. `joined` over an array with nothing in it returns the empty string, whatever the separator: there is nothing to put between. `split` keeps the empty pieces a separator at either end leaves, since dropping them would be an opinion about the string rather than a reading of it, and a text holding no separator is one piece, the text whole, the empty text among them. `split` fails on a separator holding no characters and `replacing` on a target holding none, since either would match everywhere and consume nothing. The failure is `aborted`, as the table below gives it, so a try around either catches it. The procedures that read strings, `contains` and `startsWith` included, read as a person reads, under the value model's canonical equivalence, and a string looked for matches whole characters: a match begins and ends where a character of the text does.

| procedure | `type` | `message` | `details` |
|---|---|---|---|
| `split` | `aborted` | `split takes no empty separator` | a dictionary holding nothing |
| `replacing` | `aborted` | `replacing takes no empty piece` | a dictionary holding nothing |

`text` spells a value in its own spelling, which is the type's and not a document's, on **one line**, under the grammar below. `spelled` is what it returns for the value it is handed, and `held` is a value inside a container: an array's element, a dictionary's key or value, a struct's field's value. A string, bytes and a procedure stand bare at the top and are quoted inside a container, so `text` of `x"6869"` is `x"6869"`, of `[x"6869"]` is `["x\"6869\""]` and of `[1, 2]` is `[1,2]`: the quotes are the position's, and a value's spelling does not change with how deep it sits. What no document carries is spelled in the language's own markers, never a host formatter's: a procedure is `<procedure>`, so `text` of a list holding one is `["<procedure>"]`.

```
spelled    = simple | own-scalars | bytes-atom | marker | container
held       = simple | string-atom | container
simple     = null-atom | bool-atom | integer-atom | double-atom
marker     = "<procedure>"
container  = array | dictionary | struct
array      = "[" [ held { "," held } ] "]"
dictionary = "{" [ entry { "," entry } ] "}"
entry      = held ":" held
struct     = struct-name " {" [ field { "," field } ] "}"
field      = field-name ":" held
```

| part | what it is |
|---|---|
| `simple` | null, a bool, an int or a double, as the atom that writes it under [encodings](../WARP-7/SPEC.md#the-grammar) |
| `own-scalars` | a string, as its own scalars, unquoted and unescaped |
| `bytes-atom` | bytes, as the atom that writes them under [encodings](../WARP-7/SPEC.md#the-grammar) |
| `marker` | a procedure |
| `string-atom` | a string, bytes or a procedure inside a container: the atom under [encodings](../WARP-7/SPEC.md#the-grammar) that writes the string its `spelled` is |
| `entry` | a dictionary's entry, its key then its value, the entries in the **key order** `keys` returns them in |
| `struct-name` | the struct's name, under *what a name names* in [names](../WARP-67/SPEC.md#what-a-name-names), as its scalars, unquoted and unescaped |
| `field` | a field of the struct, `field-name` its name as its scalars, unquoted and unescaped, the fields ascending by their names' UTF-8 bytes as [encodings](../WARP-5/SPEC.md) order them |

## Interactions

- `decoded` and `encoded` read bytes as [the vocabulary says about bytes](../WARP-84/SPEC.md).
- `split` and `replacing` fail with `aborted`, the failure of [Standard.Control](../WARP-82/SPEC.md).

## Alternatives considered

## Notes

**Note.** `text` is for a person reading a value. A carrier that has to give the value *back* is a different question, and one with no compact spelling writes bytes as what they are: an array of `Int`.
