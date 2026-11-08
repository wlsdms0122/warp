# WARP-6: Warp binary: `.warp`

Status: accepted

## Summary

The binary encoding, `.warp`, is the form a document travels as. The rules decide the magic and version header, the tag byte and payload of each kind of value, and what a reader refuses, including an unknown tag.

## Motivation

A reader that took `0x80 0x00` for zero, or two keys in the wrong order, would give one document a second identity, which every cache and every signature would treat as another document.

## Rules

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
| `0x07` | dictionary | count varint, then that many of: key, which is any value, then the value under it |
| `0x08` | bytes | length varint, then that many raw bytes |
| `0x09` | struct | name (length varint + UTF-8), count varint, then that many of: field name (length varint + UTF-8), value. The name is a struct's name, under *what a name names* in [names](../WARP-67/SPEC.md#what-a-name-names) |

A tag this table does not name **refuses**.

- **Varint** is unsigned LEB128: seven bits a byte, low bits first, high bit says another byte follows. At most 64 bits of payload. The largest zigzagged value takes exactly ten bytes, the tenth carrying bit 63 alone, so an eleventh byte, or a tenth-byte bit that would carry past bit 63, **refuses**; overflow is not wrapped, masked or truncated. A trailing zero group (`0x80 0x00` for zero) is a longer spelling of the same number and **refuses**. One value, one spelling.
- **ZigZag** maps signed to unsigned: `(n << 1) ^ (n >> 63)`.
- A dictionary's keys are **strictly ascending** in the key order, and a struct's field names by their UTF-8 bytes, which refuses a shuffle and a duplicate with the same rule: these are bytes the writer would not write. Two keys that are one value, `1` and `1.0`, or bytes and the array of their numbers, stand at one place in the key order, so the second of them is a duplicate.
- A claimed length is charged against the document's budget, under [encodings](../WARP-5/SPEC.md).
- Invalid UTF-8 in a string **refuses**.

The golden case, held as `the-golden-dictionary-reads-and-writes-back` under `conformance/`:

```
(dictionary (entry "a" 1) (entry "b" (array true null)) (entry "c" "hi") (entry "d" 1.5) (entry "e" x"6a73"))

57 41 52 50 01                       WARP, format 1
07 05                                a dictionary of five
05 01 61 03 02                       "a": int 1        (zigzag 2)
05 01 62 06 02 02 00                 "b": [true, null]
05 01 63 05 02 68 69                 "c": "hi"
05 01 64 04 3F F8 00 00 00 00 00 00  "d": 1.5
05 01 65 08 02 6A 73                 "e": two bytes
```

## Interactions

- The promises it keeps and the budget its claims are charged to: [WARP-5](../WARP-5/SPEC.md).
- The key order its dictionaries are strictly ascending in: [WARP-3](../WARP-3/SPEC.md).

## Alternatives considered

## Notes
