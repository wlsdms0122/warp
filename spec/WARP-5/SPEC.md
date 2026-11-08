# WARP-5: Encodings

Status: accepted

## Summary

The two encodings of a value tree, the binary and the text, and the promises that hold whichever is used. The rules decide what each encoding carries, how bytes are identified by what they begin with, and which three promises, among them that an Int and a Double stay told apart, every encoding keeps.

## Motivation

If two writers spelled one document two ways, one program would stand under two identities, and a reader that normalised what it was handed would accept bytes no writer writes, so the two spellings would meet again downstream. `1` and `1.0` are values of two types, and an encoding that let one arrive as the other would change which slot takes it.

## Rules

An encoding is bytes for a value tree. Two are specified, and they are not peers: the binary is the document and the text is the IR's own spelling, for people and for the diffs they read. The binary carries any tree and never learns what a tree means, so a document, an [object](../WARP-85/SPEC.md) and a conformance case travel under it alike, and each says what it is under a key of its own, read before anything laid out by it. The text writes a document, an interface or a case, and a value inside any of them as data; there is no text of a bare value. The file suffixes `.warp` and `.warpt` name the encoding and nothing about what the file holds; what identifies bytes is what they begin with, since bytes that cross a wire carry no name, and then the key that says what the tree is:

| bytes beginning with | are | the tree says what it is by |
|---|---|---|
| `"W" "A" "R" "P"`, then the format | the binary, under [Warp binary](../WARP-6/SPEC.md) | the key of its own it carries, read before anything laid out by it: `warp` a document, `object` an [object](../WARP-85/SPEC.md), `test` a case |
| `{ blank } "("`, under *the grammar* in [Warp text](../WARP-7/SPEC.md#the-grammar) | the text, under [Warp text](../WARP-7/SPEC.md) | the word its first element begins with: `warp` a document, `interface` an interface, `test` a case, under [the text](../WARP-37/SPEC.md) |

Whatever the encoding, three promises hold:

1. **An `Int` and a `Double` are told apart.** However the encoding does it, `1` and `1.0` must arrive as the values they were. They are of two types, `Int` and `Double`, under [numbers and readings](../WARP-47/SPEC.md), and one value only by the sameness under [when two values are the same](../WARP-4/SPEC.md): the encoding is faithful to what was written, and sameness of worth is the value model's, not the bytes'.
2. **The same document is the same bytes, in binary.** Writers are canonical: a dictionary's keys are written in one order, **the key order** under [a dictionary's keys](../WARP-3/SPEC.md), a struct's fields **ascending by their names' UTF-8 bytes**, and every value has one spelling. This is what makes a document cacheable, comparable and signable, and the binary reader holds the same line: non-canonical bytes **refuse**, they are not normalised. The text reader is the one that is forgiving, under [Warp text](../WARP-7/SPEC.md): text is for people, and the binary is the document.
3. **Nothing but data.** A procedure value has already run far enough to close over a scope, and no encoding writes one, one that captured nothing included. Infinity and NaN are likewise refused on the way out and on the way in.

Every reader also refuses bytes after the document ends and bytes that end inside a value.

**A struct's field name is a string of one Unicode scalar or more, in Unicode Normalization Form C**, and one that is not **refuses**: one name, one byte spelling, so the ascending-bytes order is an order on *names*, and a field is called something, as a name is. ASCII is NFC already, so a document that never leaves ASCII never meets this rule. What a field of a struct type may be called beyond this is the program's, under [names](../WARP-67/SPEC.md). A dictionary's key is a value, and a string is data wherever it stands, a key included: it travels byte-for-byte as written and is never normalised, and the empty string is a key like any other. The keys a document's own dictionaries write are names, under [the module](../WARP-8/SPEC.md).

**A document is read whole.** A program is checked whole before any of it runs, so a reader takes the whole document and nothing downstream acts on a prefix. This buys the budget rule: lengths claimed inside a document are charged against **one budget: the byte count of the document itself**, at the cheapest cost a claimed thing could possibly occupy on the wire (one byte for each byte a string or bytes claims, one for each element of an array, and two for each entry of a dictionary or field of a struct), and a claim the budget cannot cover **refuses** before anything is set aside for it. Nested containers cannot each claim the whole document, and no document can make a reader hold more than a small multiple of its own size.

**Note.** A document whose claims the budget cannot cover also ends inside a value, since everything claimed takes at least what it is charged, so a reader that checks each claim against the bytes that remain refuses the same documents at the same stage. What sets the two apart is what a reader sets aside before it refuses, and that is held only by tests inside the implementation.

**Keys and field names are written in full.** A key table would give one document an inline spelling and a referenced spelling, which promise 2 rules out, and a schema is a meaning the encodings do not learn. Repeated names compress well, and compression is the transport's.

The binary's header carries the *encoding's* format version, distinct from the document's `warp` key: the one says how the bytes are laid out, the other says what the program means. A reader refuses bytes laid out by a later format than it implements, and a format number that never existed. The text carries no format of its own: it spells the tree's nodes, so it is laid out by the version the tree says it is in, under [the text](../WARP-37/SPEC.md).

**Note.** Unicode writes some characters more than one way, a letter or the same letter as letter-plus-combining-mark, and a field name that had several byte spellings would break promise 2 quietly: two fields one name, or one name sorted to two places.

**Note.** A writer handed a value no reader produces, one holding infinity or NaN, refuses, and a case hands a writer only what a reader read, so those refusals are held only by tests inside the implementation.

## Interactions

- The binary's spelling: [WARP-6](../WARP-6/SPEC.md).
- A `spells` case holds a writer to the one spelling: [WARP-1](../WARP-1/SPEC.md).

## Alternatives considered

- A JSON encoding beside the two. JSON writes one kind of number, so it cannot keep an `Int` and a `Double` apart, and that is the first promise every encoding keeps.
- Claims checked against the bytes that remain. Each nested container could then claim the whole rest of the document, and a small document could make a reader set aside many times its own size.

## Notes
