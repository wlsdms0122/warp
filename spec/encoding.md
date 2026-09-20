# Encodings

An encoding is bytes for a value tree. Two are specified, and they are not
peers: the binary is the document and the text is for people. An encoding
carries a tree and never learns what a tree means, so a document, an
[object](object.md) and a conformance case travel under the same two, and
each says what it is under a key of its own, read before anything laid out by
it. The file suffixes `.warp` and
`.warpt` name the encoding and nothing about what the file holds; what
identifies bytes is the header, since bytes that cross a wire carry no name.
Whatever the encoding, three promises hold:

1. **A whole number and a fraction are told apart.** However the encoding does
   it, `1` and `1.0` must arrive as the values they were. They are one value
   to a program and two byte strings here, so two documents a program cannot
   tell apart may carry two signatures, and that is the intended order: the
   encoding is faithful to what was written, and sameness of worth is the
   value model's, not the bytes'.
2. **The same document is the same bytes, in binary.** Writers are canonical:
record keys are written in one order. **ascending by their UTF-8 bytes**. and
every value has one spelling. This is what makes a document cacheable,
comparable and signable, and the binary reader holds the same line:
non-canonical bytes **refuse**, they are not normalised. Were that reader
forgiving, one document would have many byte spellings again, and what a
signature was checked against could differ from what the reader went on to read.
The text reader is the one that is forgiving, under Warp text below: text is for
people, and the binary is the document.
3. **Nothing but data.** A procedure value has already run far enough to close
   over a scope; no encoding writes one, and refusing every such value rather
   than only the ones that captured nothing is the decision. It costs an
   author nothing and saves every reader a rule about which captures are empty.
   Infinity and NaN are likewise refused on the way out and on the way in.

Every reader also refuses: bytes after the document ends, bytes that end inside
a value, and nesting deeper than **128** containers. A container is an array,
a record or a dictionary, the document's own record being the first, and
bytes are none: they open nothing. The depth is an exact bound, not a floor: a
document 129 deep is not a document anywhere, and one 128 deep is a document
everywhere. A sender chooses how deep a document is,
and the bound is what keeps that choice from being a cost the receiver never
agreed to.

**A writer refuses at the bound and nowhere short of it.** A writer is handed
a value a caller built, and one that gave out at some depth of its own would
refuse a document the bound admits, and a document the bound admits is a
document everywhere.

**The bound is the wire's, and a run is not on it.** A running program builds values as deep as it likes: a loop wrapping its last answer in an array each time around builds one deeper than any document, and the language refuses it nowhere. A run's values are the run's cost, the way its loops are, and stopping a run that spends too much is its caller's. The bound is met where a value is written: a writer handed one deeper than 128 refuses, as a reader would have.

**Record keys are NFC.** Unicode writes some characters more than one way. A
letter, or the same letter as letter-plus-combining-mark, and a name that had
several byte spellings would break promise 2 quietly: two fields one name, or
one name sorted to two places. So a key must be in Unicode Normalization Form
C, and a key that is not **refuses**. A key with nothing in it **refuses** for
the same reason a name does: a field is called something. One name, one byte
spelling; the ascending-bytes order is then an order on *names*. ASCII is NFC
already, so a document that never leaves ASCII never meets this rule. String
*values* are data, not names: they travel byte-for-byte as written and are
never normalised.

**A document is read whole.** Streaming and incremental decoding are
deliberately not offered: a program is checked whole before any of it runs, so
nothing downstream could act on a prefix anyway. This buys the budget rule:
lengths claimed inside a document are charged against **one budget. The byte
count of the document itself**. At the cheapest cost a claimed thing could
possibly occupy on the wire, one byte for each byte, element or character
claimed and two for each entry of a record, and a claim the budget cannot cover
**refuses** before anything is set aside for it. Nested containers cannot each claim the
whole document, and no document can make a reader hold more than a small
multiple of its own size.

**Compact was the goal that lost.** In a small document most bytes are field
names, and the format leaves them there: a key table would give one document an
inline spelling and a referenced spelling. Promise 2 gone, and schemas are a
meaning the encodings must not learn. Of canonical, self-contained and
compact, the encodings choose the first two; repeated names compress well, and
compression is the transport's job.

An encoding's header carries the *encoding's* format version, distinct from the
document's `warp` key: the one says how the bytes are laid out, the other says
what the program means. A reader refuses bytes laid out by a later format than
it implements, and a format number that never existed.

## Warp binary. `.warp`

The carrying form: what a document travels as. Current format: **1**.

```
"W" "A" "R" "P"  0x01        magic, then the format version
<value>                       exactly one, then end of input
```

Each value is a tag byte, then its payload:

| tag | value | payload |
|---|---|---|
| `0x00` | null |. |
| `0x01` | false |. |
| `0x02` | true |. |
| `0x03` | int | ZigZag, then unsigned LEB128 |
| `0x04` | double | 8 bytes, IEEE-754 binary64, big-endian |
| `0x05` | string | length varint, then that many bytes of UTF-8 |
| `0x06` | array | count varint, then that many values |
| `0x07` | record | count varint, then that many of: key (length varint + UTF-8), value |
| `0x08` | bytes | length varint, then that many raw bytes |
| `0x09` | named record | name (length varint + UTF-8), then count and fields exactly as `0x07` writes them. The name is a declared type's spelling: ASCII identifiers joined by dots, no scalar's keyword, and any other **refuses** |

- **Varint** is unsigned LEB128: seven bits a byte, low bits first, high bit
says another byte follows. At most 64 bits of payload. The largest zigzagged
value takes exactly ten bytes, the tenth carrying bit 63 alone. so an eleventh
byte, or a tenth-byte bit that would carry past bit 63, **refuses**; overflow is
not wrapped, masked or truncated. A trailing zero group (`0x80 0x00` for zero)
is a longer spelling of the same number and **refuses**. One value, one
spelling.
- **ZigZag** maps signed to unsigned: `(n << 1) ^ (n >> 63)`.
- Record keys are **strictly ascending** by UTF-8 bytes, which refuses a
  shuffle and a duplicate with the same rule: these are bytes the writer would
  not write.
- A claimed length larger than the bytes that remain **refuses** before
  anything is set aside for it.
- Invalid UTF-8 in a string **refuses**.
- A record with no name is `0x07`; only a record carrying a name is `0x09`.

The golden case, held as `the-golden-record-reads-and-writes-back` under
`conformance/`:

```
{ "a": 1, "b": [true, null], "c": "hi", "d": 1.5, "e": x"6a73" }

57 41 52 50 01                    WARP, format 1
07 05                             a record of five
01 61 03 02                       "a": int 1        (zigzag 2)
01 62 06 02 02 00                 "b": [true, null]
01 63 05 02 68 69                 "c": "hi"
01 64 04 3F F8 00 00 00 00 00 00  "d": 1.5
01 65 08 02 6A 73                 "e": two bytes
```

## Warp text. `.warpt`

The readable form: the same document laid out for eyes. **A dump, not a
syntax**. Machines write it, people read it, and nobody composes one by hand;
composing is a front end's job, in a front end's notation. Nothing can be said
here that the document does not hold, which is why there are no comments to
lose on the way back. Current format: **1**. A text is UTF-8 bytes before it
is anything else, and bytes that are not **refuse**.

```
warpt 1
{
  a 1
  b [
    true
    null
  ]
  c "hi"
  d 1.5
  e x"6a73"
}
```

The layout:

- The first line is `warpt`, a space, the format version as a whole number's
  one spelling, a newline.
- Whitespace separates a bare token, a string and bytes from one another; a
  bracket needs none. A bare token running straight into a quote, or a quote
  into a bare token, is not a layout of two tokens.
- A record is `{ key value … }`; an array is `[ value … ]`. No commas, no
  colons. Containers with anything in them take two-space indentation, one
  element or field per line; empty containers are inline as `[]` / `{}`. The
  text ends with one newline.
- A key is written bare when it is an identifier (`[A-Za-z_][A-Za-z0-9_]*`),
  quoted otherwise. In key position a bare token is always a key. `{ null 1 }`
  is a field called null.
- `null`, `true` and `false` are bare keywords. **A number with a point or an
exponent is a fraction; with neither it is whole**. The difference is grammar,
not a reader's guess. A double is spelled as the shortest decimal that reads
back to the same binary64 (a Ryū/Grisu-class rendering), with the point or
exponent always present. Which form those digits take is the document's rule,
not a host library's: writing the value `d.ddd…×10^k`, the point form when `-5 <
k < 16`, otherwise the exponent form, its exponent written `e` with an explicit
sign and at least two digits. `0.0001` but `1e-05`, `1000000000000000.0` but
`1e+16`, so one value keeps one spelling down to its last character. An int is
spelled with no leading zeros and a `-` only when negative.
- A string is double-quoted. Exactly `"`, `\` and the three control
  characters with short escapes are escaped as `\"` `\\` `\n` `\r` `\t`;
  every other control character (below U+0020) as `\uXXXX` with lowercase
  hex; **nothing else is escaped**, and no character that has a shorter escape
  may take a longer one.
- Bytes are `x"…"`. Lowercase hex, two digits a byte, no spaces.
- A named record is the name, a space, and the record: `bank.Account {
  balance 1 }`. In value position a bare token followed by `{` is the name; a
  bare token that spells a scalar (`null`, `true`, `false`, a number) is never
  one.

Layout is free on the way in. A reader takes keys in any order, any
whitespace between tokens and any indentation, because a text is written by a
person as often as by a writer. The writer still lays a text out one way,
keys ascending and two spaces an indent, so a text that has been through a
writer is the same bytes everywhere, and that is the form the conformance
cases are kept in. A key is written bare or quoted and is one key either way.
What is not free is the spelling of a value: a fraction written `1.50` and an
escape spelled long **refuse**, since those are two texts for one value rather
than two layouts of one text. Nor is a key written twice, which **refuses**:
two values under one key are two documents, not one document laid out twice. Sameness of
documents is the binary's promise, above, and a text makes it by being
written out.

## Cases

What `conformance/` asks about this page, by the name each case's file carries.
These carry bytes or text rather than a program, under *what a case is* in
[conformance](conformance.md).

- `a-format-that-never-existed-refuses`
- `a-later-format-refuses`
- `a-length-past-the-end-of-the-document-refuses`
- `a-named-record-reads-and-writes-back`
- `a-number-written-longer-than-it-is-refuses`
- `a-record-key-not-in-normal-form-c-refuses`
- `a-record-key-written-twice-refuses`
- `a-record-name-that-is-not-declarable-refuses`
- `a-string-that-is-not-utf8-refuses`
- `a-varint-carrying-past-bit-63-refuses`
- `a-varint-of-eleven-bytes-refuses`
- `an-empty-record-key-refuses`
- `an-infinity-refuses`
- `bytes-after-the-document-ends-refuse`
- `bytes-that-do-not-begin-as-a-document-refuse`
- `bytes-that-end-inside-a-value-refuse`
- `nesting-past-the-bound-refuses`
- `record-keys-out-of-order-refuse`
- `the-golden-record-reads-and-writes-back`
- `the-spellings-a-text-reads-are-pinned-by-bytes`

Text:

- `a-bare-key-that-is-not-an-identifier-refuses`
- `a-bare-token-running-into-a-quote-refuses`
- `a-fraction-not-in-its-one-writing-refuses`
- `a-fraction-reads-by-its-point-or-exponent`
- `a-named-record-reads-from-text`
- `a-quote-running-into-a-bare-token-refuses`
- `a-quoted-key-and-a-bare-key-are-one-key`
- `a-text-control-character-written-raw-refuses`
- `a-text-format-header-not-in-its-one-writing-refuses`
- `a-text-key-written-twice-refuses`
- `a-text-laid-out-by-a-format-that-never-existed-refuses`
- `a-text-laid-out-by-a-later-format-refuses`
- `a-text-reads-in-any-layout`
- `a-text-reads-its-escapes`
- `a-whole-number-with-a-leading-zero-refuses`
- `an-escape-for-a-character-written-as-itself-refuses`
- `an-escape-spelled-longer-than-its-short-form-refuses`
- `an-exponent-not-in-its-one-writing-refuses`
- `bytes-running-into-bytes-refuse`
- `bytes-spell-from-text`
- `bytes-written-in-uppercase-hex-refuse`
- `bytes-written-with-an-odd-digit-refuse`
- `text-after-the-document-ends-refuses`
- `text-that-is-not-utf8-refuses`
- `the-golden-record-spells-as-text`
