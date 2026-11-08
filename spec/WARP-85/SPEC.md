# WARP-85: What an object holds

Status: accepted

## Summary

An object is one document compiled, written as a value in the binary encoding. The rules decide which entries it carries exactly, how it is identified by its bytes, and what a build keeps and a cache receives.

## Motivation

An object is kept on disk and on a server and read back by another process, another version of the runtime, or another implementation. Left to each implementation, an object one runtime wrote could be read only by that runtime, and a cache could serve only the tool that filled it.

## Rules

What a build writes down: one document compiled, in its own coordinates, laid out so that any implementation reads what any other wrote. This WARP and [WARP-86](../WARP-86/SPEC.md) to [WARP-92](../WARP-92/SPEC.md) are the layout. What the parts *mean* is the WARPs that judge them: a row's claims are [checking](../WARP-66/SPEC.md), a body's operations are [statements](../WARP-19/SPEC.md) and [expressions](../WARP-30/SPEC.md) with every fact the build proved written in, and the bytes an object travels as are [the binary encoding](../WARP-6/SPEC.md).

An object is a **value**, and nothing more than one: it is written by the binary encoding and identified by its bytes the way a document is, and a text writes one as data, inside a case. What crosses a wire is a document; what a build keeps, hands to a cache, or receives from one is an object, and both cross under the binary. A file holding either is named by its encoding and not by what it holds, and what it holds is what the value says it is: a document says `warp`, an object says `object`.

An object is one dictionary. It carries **exactly** these keys, and a key none of them names, or one of them missing, **refuses**. Current format: **1**.

| key | holds | order |
|---|---|---|
| `object` | int. This layout's format. Read before anything laid out by it, the keys included | |
| `document` | a list of none or one: `[identity]`, the document's identity, bytes, under [identity and dependencies](../WARP-91/SPEC.md), or `[]` where the program was never written down | |
| `dependencies` | a list of bytes: for the object behind every declaration this document named, the key the host keyed it under | ascending by bytes, none twice |
| `types` | name → what the document declared: a struct as `[9, …]` under *type* in [how a part is laid out](../WARP-86/SPEC.md), an enum as `[20, …]` under [enums](../WARP-93/SPEC.md#in-the-binary-and-in-an-object), and an alias as the *type* it stands for | by name |
| `contracts` | name → `[ types, bounds, procedures ]`: the types the contract asks; name → the contracts bounding the type of that name, ascending, at least one, for each one it bounds; and procedure name → *signature* | by name; the types ascending, the bounds and the procedures by name |
| `claims` | *head* → the contracts it says the type adopts under the head, at least one | by head; the contracts ascending |
| `members` | *head* → the members it gives the type under the head, at least one, each a member's name | by head; the members ascending |
| `typeMembers` | *head* → (name → *type*): the type members it gives the type under the head, at least one, each written in the head's type parameters, or the struct's or the enum's where the head is bare and the document declares it | by head, then by name |
| `importedClaims` | the claims its document imports, each `[type, contract]`, two *name*s as the document's `importedClaims` writes them under [the imports list](../WARP-10/SPEC.md#the-grammar): the name of the type its head is about, then the contract | by type, then by contract |
| `rows` | the procedures it declares, each a *row* under its spelling | by name |
| `numbering` | `[sends, counts]`: the spellings it sends, a list of *name*, and how many closures each declaration wrote, a list of `[declaration, count]` | below |
| `lifted` | the closures its bodies lifted, each a *row* with no spelling | as the numbering counts them |
| `typeNumbering` | a list of *name*: the declared types its bodies stand on | ascending by name, under [operations](../WARP-88/SPEC.md) |
| `variables` | a list of `[name, value]`: each module variable's *name* and the *value* it starts a run holding | by name |
| `constants` | a list of *name*: the constants it declared, by spelling | by name |
| `typeTable` | the *type* entries | as the parts number them, below |
| `loweredTypeTable` | the *lowered type* entries | as the parts number them |
| `valueTable` | the *value* entries | as the parts number them |
| `operationTable` | the *operation* entries | as the parts number them |
| `addressTable` | the *address* entries | as the parts number them |

**The dictionary is keyed and its parts are not.** The dictionary names each part by its key; inside a part the fields stand in order and a variant says itself by its tag. A reading holds an object to the format it reads before it reads a part.

**Order is spelling.** Every list a name keys stands ascending by the names' bytes, none twice, and so does every set written as a list. Every list a slot or a position keys stands ascending by that slot or position, none twice, and the part that lays the list out says which of its fields keys it. That is the whole of what makes one object one value: a list keeps the order it is written in, so the layout says which, and a reading takes no other. A list out of order, or holding one thing twice, **refuses**.

**What nests stands in a table.** A *type*, a *lowered type*, a *value*, an *operation* and an *address* are each written once, as an entry of their own table, and whatever holds one writes the entry's number. An entry is laid out the way [WARP-86](../WARP-86/SPEC.md) to [WARP-90](../WARP-90/SPEC.md) lay its kind out, with a number wherever it holds another of these. So an object nests no deeper for a program nesting deeper. An entry stands right after everything it holds: the parts are read in the order of the keys above, the fields of a part and of an entry in their order, and each table numbers its entries from zero in the order they are finished. Every entry is held exactly once, and an entry held twice, held nowhere, or standing at another number than that order gives it **refuses**.

**The rows.** A declaration's row stands under its spelling in `rows`, in name order; the rows its bodies lifted stand in `lifted`, without a spelling, in the order the numbering counts them. A body numbers what its calls and its closure literals reach from the document itself: the spellings it sends first, in name order, then its rows in name order, then the closures its declarations wrote, in the order the numbering lists the declarations and, within one, in the order they are finished, so a closure written inside another counts before it. It numbers the declared types it stands on in the order `typeNumbering` lists them. Where a row lands in a link is the link's to decide, so nothing here says it, and one object serves every entry asked of it.

**`numbering`** writes what a reading uses and cannot work out: the spellings sent, in name order; then `[declaration, count]` for each declaration that wrote a closure, each count above zero. A *declaration* is `[0, name]` for a procedure and `[1, name]` for a constant or a variable, since a procedure and a constant may be spelled alike; the procedures stand first, then the constants and variables, each in name order, none twice. **`typeNumbering`** writes the declared types the lowered bodies stand on, ascending by name, none twice: each of them numbers its types in that order. A start in `variables` is a value, which carries a struct's name as its spelling and a type it holds as a document writes one, and numbers no type. A contract a bound names is written by its name and numbered nowhere. What a number stands for is arithmetic over these lists and the declared spellings, so the numbers themselves are not written.

### One object

The document

```
(warp 1)
(import Standard.Collection.appending)

(procedure entry
  (access public)
  (const)
  (isolated)
  (parameter n (type (array Int)))
  (returns (array Int))
  (body
    (return (call Standard.Collection.appending n 1))))
```

compiles to an object with one row, written as data, one entry a line and `rows` broken onto a few more, and its two digests elided:

```
(dictionary
  (entry "addressTable" (array (array 0 (array) false)))
  (entry "claims" (array))
  (entry "constants" (array))
  (entry "contracts" (array))
  (entry "dependencies" (array x"…"))
  (entry "document" (array x"…"))
  (entry "importedClaims" (array))
  (entry "lifted" (array))
  (entry "loweredTypeTable" (array (array 4)))
  (entry "members" (array))
  (entry "numbering" (array (array "Standard.Collection.appending") (array)))
  (entry "object" 1)
  (entry "operationTable" (array (array 1 0) (array 0 0) (array 11 (array 0 (array (array 0) (array 1)) (array) (array 0))) (array 13 0 (array 2))))
  (entry "rows" (array
    (array "entry"
      (array (array (array "n" (array 1))) 3 (array 1 (array)) 1 1 (array) (array))
      2
      (array 0 (array (array (array) 3)) (array 1 (array 0) (array) (array) (array) (array "n"))))))
  (entry "typeMembers" (array))
  (entry "typeNumbering" (array))
  (entry "typeTable" (array (array 4) (array 7 0) (array 4) (array 7 2)))
  (entry "types" (array))
  (entry "valueTable" (array (array 2 1)))
  (entry "variables" (array)))
```

Read it back: `rows` holds `entry`, whose signature takes `n` as type `1` and returns type `3`. In `typeTable`, entry `1` is an array (tag 7) of entry `0`, `Int` (tag 4), and entry `3` is the same over entry `2`: both are `Array<Int>`, each written once where it is held. The signature fails with nothing (`(array 1 (array))`), is const (`1`) and isolated (`1`), bounds nothing and says no associated type is a type (`(array) (array)`); the row is public (`2`). Its implementation is a body (`0`) of one instruction, which binds nothing and computes operation `3`. Operation `3` leaves (`13`) the procedure (`0`) and returns operation `2`: a call (`11`) to row `0` of the numbering, which is `Standard.Collection.appending`, with two arguments, operations `0` and `1`, neither handed in place, and one lowered type, entry `0` of `loweredTypeTable`, `Int` (tag 4), filling the one type parameter the callee's signature names. Operation `0` reads (`1`) address `0`, slot `0` with no steps and no promotion, and operation `1` is the literal (`0`) value `0`, the int (`2`) `1`. Every number stands before the entry holding it. The frame has one slot, filled by the parameter, called `n`. The dependency is what the host keyed the standard vocabulary's object under.

## Interactions

- An object's `document` is the identity of [identity and dependencies](../WARP-91/SPEC.md).

## Alternatives considered

- Numbering by the order a lowering meets things. That order can depend on the documents beside it: which type adopts which contract is a fact of the link, and a document this one never names can change it.
- An encoder of its own for objects. The binary encoding already writes one value one way in both directions, and a second encoder would be a second promise of determinism to keep.

## Notes

**Note.** A case writes a document and an object as values its text holds, and never as a file, so how a file holding either is named is held only by tests inside the implementation.
