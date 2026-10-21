# Encodings

An encoding is bytes for a value tree. Two are specified, and they are not peers: the binary is the document and the text is the IR's own spelling, for people and for the diffs they read. The binary carries any tree and never learns what a tree means, so a document, an [object](object.md) and a conformance case travel under it alike, and each says what it is under a key of its own, read before anything laid out by it. The text writes a document or a case, and a value inside either as data; there is no text of a bare value. The file suffixes `.warp` and `.warpt` name the encoding and nothing about what the file holds; what identifies bytes is what they begin with, since bytes that cross a wire carry no name. Whatever the encoding, three promises hold:

1. **A whole number and a fraction are told apart.** However the encoding does it, `1` and `1.0` must arrive as the values they were. They are of two types, `Int` and `Double`, under [types](type.md), and one value only by the sameness under [values](value.md): the encoding is faithful to what was written, and sameness of worth is the value model's, not the bytes'.
2. **The same document is the same bytes, in binary.** Writers are canonical: a map's keys are written in one order, **the key order** under [values](value.md), a struct's fields **ascending by their names' UTF-8 bytes**, and every value has one spelling. This is what makes a document cacheable, comparable and signable, and the binary reader holds the same line: non-canonical bytes **refuse**, they are not normalised. The text reader is the one that is forgiving, under Warp text below: text is for people, and the binary is the document.
3. **Nothing but data.** A procedure value has already run far enough to close over a scope, and no encoding writes one, one that captured nothing included. Infinity and NaN are likewise refused on the way out and on the way in.

Every reader also refuses: bytes after the document ends, bytes that end inside a value, and nesting deeper than **128** containers. A container is an array, a map or a struct, the document's own map being the first and a map's key opening what it holds like any value, and bytes are none: they open nothing. The depth is an exact bound, not a floor: a document 129 deep is not a document anywhere, and one 128 deep is a document everywhere.

**A type or a path nests on from its string**, against the same 128, under [types](type.md) and [expressions](expression.md). An encoding's reader does not read a string as a type, so the load is where this bound is met.

**A writer refuses at the bound and nowhere short of it.** A writer is handed a value someone built, a host or a front end, and one that gave out at some depth of its own would refuse a document the bound admits.

**The bound is the wire's, and a run is not on it.** A running program builds values as deep as it likes: a loop wrapping its last answer in an array each time around builds one deeper than any document, and the language refuses it nowhere. A run's values are the run's cost, the way its loops are, and stopping a run that spends too much is its host's. The bound is met where a value is written: a writer handed one deeper than 128 refuses, as a reader would have.

**Field names are NFC.** Unicode writes some characters more than one way (a letter, or the same letter as letter-plus-combining-mark), and a name that had several byte spellings would break promise 2 quietly: two fields one name, or one name sorted to two places. So a struct's field name must be in Unicode Normalization Form C, and one that is not **refuses**. A field name with nothing in it **refuses** for the same reason a name does: a field is called something. One name, one byte spelling; the ascending-bytes order is then an order on *names*. ASCII is NFC already, so a document that never leaves ASCII never meets this rule. A map's key is a value, and text is data wherever it stands: a string, a key included, travels byte-for-byte as written and is never normalised, and the empty text is a key like any other. The keys a document's own maps write are names, under [the document format](document.md).

**A document is read whole.** A program is checked whole before any of it runs, so a reader takes the whole document and nothing downstream acts on a prefix. This buys the budget rule: lengths claimed inside a document are charged against **one budget: the byte count of the document itself**, at the cheapest cost a claimed thing could possibly occupy on the wire (one byte for each byte a string or bytes claims, one for each element of an array, and two for each entry of a map or field of a struct), and a claim the budget cannot cover **refuses** before anything is set aside for it. Nested containers cannot each claim the whole document, and no document can make a reader hold more than a small multiple of its own size.

**Keys and field names are written in full.** A key table would give one document an inline spelling and a referenced spelling, which promise 2 rules out, and a schema is a meaning the encodings do not learn. Repeated names compress well, and compression is the transport's.

The binary's header carries the *encoding's* format version, distinct from the document's `warp` key: the one says how the bytes are laid out, the other says what the program means. A reader refuses bytes laid out by a later format than it implements, and a format number that never existed. The text carries no format of its own: it spells the tree's nodes, so it is laid out by the version the tree says it is in, under [the text](text.md).

## Warp binary: `.warp`

The carrying form: what a document travels as. Current format: **1**.

```
"W" "A" "R" "P"  0x01        magic, then the format version
<value>                       exactly one, then end of input
```

Each value is a tag byte, then its payload:

| tag | value | payload |
|---|---|---|
| `0x00` | null | none |
| `0x01` | false | none |
| `0x02` | true | none |
| `0x03` | int | ZigZag, then unsigned LEB128 |
| `0x04` | double | 8 bytes, IEEE-754 binary64, big-endian |
| `0x05` | string | length varint, then that many bytes of UTF-8 |
| `0x06` | array | count varint, then that many values |
| `0x07` | map | count varint, then that many of: key, which is any value, then the value under it |
| `0x08` | bytes | length varint, then that many raw bytes |
| `0x09` | struct | name (length varint + UTF-8), count varint, then that many of: field name (length varint + UTF-8), value. The name is a struct's, under [values](value.md): a type's name, or one the language declares, as `Failure` and `Round` are |

A tag this table does not name **refuses**.

- **Varint** is unsigned LEB128: seven bits a byte, low bits first, high bit says another byte follows. At most 64 bits of payload. The largest zigzagged value takes exactly ten bytes, the tenth carrying bit 63 alone, so an eleventh byte, or a tenth-byte bit that would carry past bit 63, **refuses**; overflow is not wrapped, masked or truncated. A trailing zero group (`0x80 0x00` for zero) is a longer spelling of the same number and **refuses**. One value, one spelling.
- **ZigZag** maps signed to unsigned: `(n << 1) ^ (n >> 63)`.
- A map's keys are **strictly ascending** in the key order, and a struct's field names by their UTF-8 bytes, which refuses a shuffle and a duplicate with the same rule: these are bytes the writer would not write. Two keys that are one value, `1` and `1.0`, or bytes and the array of their numbers, stand at one place in the key order, so the second of them is a duplicate.
- A claimed length larger than the bytes that remain **refuses** before anything is set aside for it.
- Invalid UTF-8 in a string **refuses**.

The golden case, held as `the-golden-map-reads-and-writes-back` under `conformance/`:

```
(dictionary (entry "a" 1) (entry "b" (array true null)) (entry "c" "hi") (entry "d" 1.5) (entry "e" x"6a73"))

57 41 52 50 01                       WARP, format 1
07 05                                a map of five
05 01 61 03 02                       "a": int 1        (zigzag 2)
05 01 62 06 02 02 00                 "b": [true, null]
05 01 63 05 02 68 69                 "c": "hi"
05 01 64 04 3F F8 00 00 00 00 00 00  "d": 1.5
05 01 65 08 02 6A 73                 "e": two bytes
```

## Warp text: `.warpt`

The readable form: a document or a case written as the IR's own nodes, in two layers. The first reads atoms and lists and knows nothing of Warp, the way the binary's reader knows nothing of what a tree means; it is this section. The second reads a list by the word it begins with and makes the tree's node, under [the text](text.md).

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

- **White space** is space, tab, line feed and carriage return, and nothing depends on a line break. Any other character, one Unicode counts as white space included, is part of the token it touches. There are no comments.
- **A list** is `(`, then its elements, then `)`. An element is an atom or a list.
- **An atom's first characters say its kind.** A digit, or `-` or `+` then a digit, begins a number; `x"` begins bytes; `"` begins text; `` ` `` begins a name; anything else is `null`, `true`, `false` or a name. A token so begun that is not that kind's one spelling **refuses**: `1.50`, `01`, `+1` and `1.` are no number and no name.
- **A number with a point or an exponent is a fraction; with neither it is whole.** The difference is grammar, not a reader's guess. A double is spelled as the shortest decimal that reads back to the same binary64, of two as short the one nearer the value, with the point or exponent always present, and with a `-` where its sign bit is set, `-0.0` included. Which form those digits take is the document's rule, not a host library's: writing the value `d.ddd…×10^k`, the point form when `-5 < k < 16`, otherwise the exponent form, its exponent written `e` with an explicit sign and at least two digits. `0.0001` but `1e-05`, `1000000000000000.0` but `1e+16`, so one value keeps one spelling down to its last character. An int is spelled with no leading zeros and a `-` only when negative, and one past what an `Int` holds **refuses**.
- **Text** is double-quoted. Exactly `"`, `\` and the three control characters with short escapes are escaped as `\"` `\\` `\n` `\r` `\t`; every other control character (below U+0020) as `\uXXXX` with lowercase hex; **nothing else is escaped**, and no character that has a shorter escape may take a longer one. A control character written raw **refuses**.
- **Bytes** are `x"…"`. Lowercase hex, two digits a byte, no spaces.
- **A name** is a run of characters other than white space, `(`, `)`, `"` and `` ` ``, holding no character below U+0020 and reading as no other atom, or any text of one character or more in backticks. In backticks a name is escaped as text is, with `` \` `` for the backtick in place of `\"`, which is no escape there, and `"` as itself. A name in backticks is the same atom as the name written bare, `` `x` `` and `x` alike, and `` `null` `` is a name where `null` is not. The writer writes a name bare where it reads back bare.
- **An atom or a list is followed by white space, a parenthesis or the end.** A bare token running straight into a quote, a quote into a bare token and bytes into bytes are not a layout of two tokens, and **refuse**.
- **Lists nest at most 257 deep**, the outermost list the first, which is as deep as a tree within the bound writes them. A document's first level is written in no list and each level after it in two at most, a dictionary and its entry or a procedure type and its parameters, and one level on a way down holds a third, the key a value stands under, `(description …)` or `(type App.A …)`: 255. A case writes the documents beside its program two lists further down, and a type or a path in one counts on from that document's containers, under the load, while the containers count across the whole case: 257. A text nesting deeper **refuses**, and so does a writer handed a tree whose text would.

Layout is free on the way in. A reader takes any white space between tokens and any indentation, because a text is written by a person as often as by a writer. The writer still lays a text out one way, under [the text](text.md), so a text that has been through a writer is the same bytes everywhere, and that is the form the conformance cases are kept in. What is not free is the spelling of a value: a fraction written `1.50` and an escape spelled long **refuse**, since those are two texts for one value rather than two layouts of one text. Sameness of documents is the binary's promise, above, and a text makes it by being written out. A text that is refused is refused with the line and column the reader stood at, save one refused as a whole, as no UTF-8 or as a tree past the bound, both counted from one, the column in scalars, and a line ended by a line feed, a carriage return or the two together: a text is the encoding a person edits, and a refusal that names no place leaves them to find it.

## Cases

What `conformance/` asks about this page, by the name each case's file carries. These carry bytes or text rather than a program, under *what a case is* in [conformance](conformance.md).

- `a-byte-order-mark-in-a-string-is-kept`
- `a-field-name-not-in-normal-form-c-refuses`
- `a-format-that-never-existed-refuses`
- `a-key-led-by-a-byte-order-mark-sorts-by-its-bytes`
- `a-key-that-is-a-byte-order-mark-is-kept`
- `a-later-format-refuses`
- `a-length-past-the-end-of-the-document-refuses`
- `a-map-claiming-more-than-the-document-holds-refuses`
- `a-map-key-that-is-the-array-of-the-bytes-before-refuses`
- `a-map-key-the-same-as-the-one-before-refuses`
- `a-map-key-written-twice-refuses`
- `a-map-keyed-by-values-reads-and-writes-back`
- `a-nan-refuses`
- `a-number-written-longer-than-it-is-refuses`
- `a-string-that-is-not-utf8-refuses`
- `a-struct-claiming-more-than-the-document-holds-refuses`
- `a-struct-name-that-is-not-declarable-refuses`
- `a-struct-named-for-a-type-the-language-names-refuses`
- `a-struct-reads-and-writes-back`
- `a-struct-the-language-declares-reads-and-writes-back`
- `a-text-key-not-in-normal-form-c-is-kept`
- `a-varint-carrying-past-bit-63-refuses`
- `a-varint-of-eleven-bytes-refuses`
- `an-array-claiming-more-than-the-document-holds-refuses`
- `an-empty-field-name-refuses`
- `an-infinity-refuses`
- `an-unknown-tag-refuses`
- `bytes-after-the-document-ends-refuse`
- `bytes-claiming-more-than-the-document-holds-refuse`
- `bytes-that-do-not-begin-as-a-document-refuse`
- `bytes-that-end-inside-a-value-refuse`
- `map-keys-out-of-order-refuse`
- `negative-zero-spells-with-its-sign`
- `nesting-past-the-bound-refuses`
- `nesting-through-a-maps-key-past-the-bound-refuses`
- `struct-fields-out-of-order-refuse`
- `the-golden-map-reads-and-writes-back`
- `the-spellings-a-text-reads-are-pinned-by-bytes`

Text:

- `a-bare-token-running-into-a-quote-refuses`
- `a-form-feed-between-tokens-refuses`
- `a-fraction-ending-at-its-point-refuses`
- `a-fraction-in-the-farther-of-two-shortest-decimals-refuses`
- `a-fraction-not-in-its-one-writing-refuses`
- `a-fraction-reads-by-its-point-or-exponent`
- `a-fraction-spells-as-the-nearer-of-two-shortest-decimals`
- `a-list-left-open-refuses`
- `a-name-in-backticks-escapes-a-backtick-and-not-a-quote`
- `a-name-in-backticks-holding-nothing-refuses`
- `a-name-in-backticks-is-the-name-written-bare`
- `a-name-spelled-null-is-written-in-backticks`
- `a-no-break-space-is-part-of-the-name-it-touches`
- `a-parenthesis-closing-nothing-refuses`
- `a-quote-escaped-in-backticks-refuses`
- `a-quote-running-into-a-bare-token-refuses`
- `a-text-as-deep-as-a-tree-writes-is-read`
- `a-text-control-character-written-raw-refuses`
- `a-text-ending-inside-a-name-refuses`
- `a-text-ending-inside-an-escape-refuses`
- `a-text-ending-inside-bytes-refuses`
- `a-text-ending-inside-text-refuses`
- `a-text-led-by-a-byte-order-mark-refuses`
- `a-text-nesting-past-the-bound-refuses`
- `a-text-reads-its-escapes`
- `a-whole-number-past-what-an-int-holds-refuses`
- `a-whole-number-with-a-leading-zero-refuses`
- `a-whole-number-written-with-a-plus-refuses`
- `a-zero-written-with-a-minus-refuses`
- `an-escape-for-a-character-written-as-itself-refuses`
- `an-escape-in-uppercase-hex-refuses`
- `an-escape-spelled-longer-than-its-short-form-refuses`
- `an-escape-text-does-not-have-refuses`
- `an-exponent-not-in-its-one-writing-refuses`
- `bytes-running-into-bytes-refuse`
- `bytes-spell-from-text`
- `bytes-written-in-uppercase-hex-refuse`
- `bytes-written-with-a-space-refuse`
- `bytes-written-with-an-odd-digit-refuse`
- `text-that-is-not-utf8-refuses`
