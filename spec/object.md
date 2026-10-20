# Objects

What a build writes down: one document compiled, in its own coordinates, laid out so that any implementation reads what any other wrote. This page is the layout. What the parts *mean* is the pages that judge them: a row's claims are [checking](checking.md), a body's operations are [statements](statement.md) and [expressions](expression.md) with every fact the build proved written in, and the bytes an object travels as are [encodings](encoding.md).

An object is a **value**, and nothing more than one: it is written by the binary encoding and identified by its bytes the way a document is, and a text writes one as data, inside a case. What crosses a wire is a document; what a build keeps, hands to a cache, or receives from one is an object, and both cross under the binary. A file holding either is named by its encoding and not by what it holds, and what it holds is what the value says it is: a document says `warp`, an object says `object`.

## What an object holds

An object is one map. It carries **exactly** these keys, and a key none of them names, or one of them missing, **refuses**. Current format: **1**.

| key | holds | order |
|---|---|---|
| `object` | int. This layout's format. Read before anything laid out by it, the keys included | |
| `document` | the document's identity, or nothing where the program was never written down | |
| `dependencies` | the objects behind every declaration this document named, each by what the host keyed it under | ascending by bytes, none twice |
| `types` | name → what the document declared: a struct as `[9, …]` under *type* below, and an alias as the *type* it stands for | by name |
| `contracts` | name → `[ types, bounds, procedures ]`: the types the contract asks; name → the contracts bounding the type of that name, ascending, at least one, for each one it bounds; and procedure name → *signature* | by name; the types ascending, the bounds and the procedures by name |
| `claims` | *head* → the contracts it says the values the head takes answer, at least one | by head; the contracts ascending |
| `members` | *head* → the members it gives the type under the head, at least one, each the name of a row under the type's name and its own | by head; the members ascending |
| `typeMembers` | *head* → (name → *type*): the type members it gives the type under the head, at least one, each written in the head's type parameters, or the struct's where the head is bare and the document declares the struct | by head, then by name |
| `importedClaims` | the claims its document imports, each `[type, contract]`, the pair the claim is about | by type, then by contract |
| `rows` | the declarations, each a *row* under its spelling | by name |
| `numbering` | two lists: what it sends, and how many closures each declaration wrote | below |
| `lifted` | the closures its bodies lifted, each a *row* with no spelling | as the numbering counts them |
| `typeNumbering` | the declared types its bodies stand on, ascending by name | below |
| `variables` | (name, *value*): what each variable starts a run holding | by name |
| `constants` | the constants it declared, by spelling | by name |
| `typeTable` | the *type* entries | as the parts number them, below |
| `loweredTypeTable` | the *lowered type* entries | as the parts number them |
| `valueTable` | the *value* entries | as the parts number them |
| `operationTable` | the *operation* entries | as the parts number them |
| `addressTable` | the *address* entries | as the parts number them |

**The map is keyed and its parts are not.** The map names each part by its key; inside a part the fields stand in order and a variant says itself by its tag. A reading holds an object to the format it reads before it reads a part.

**Order is spelling.** Every list a name keys stands ascending by the names' bytes, none twice, and so does every set written as a list. That is the whole of what makes one object one value: a list keeps the order it is written in, so the layout says which, and a reading takes no other. A list out of order, or naming one thing twice, **refuses**.

**What nests stands in a table.** A *type*, a *lowered type*, a *value*, an *operation* and an *address* are each written once, as an entry of their own table, and whatever holds one writes the entry's number. An entry is laid out the way this page lays its kind out, with a number wherever it holds another of these. So an object nests no deeper for a program nesting deeper. An entry stands right after everything it holds: the parts are read in the order of the keys above, the fields of a part and of an entry in their order, and each table numbers its entries from zero in the order they are finished. Every entry is held exactly once, and an entry held twice, held nowhere, or standing at another number than that order gives it **refuses**. Entries nest no deeper than a written tree may, [128](encoding.md) levels: an entry is a level, and an entry of its own table it holds is a level below it. A table nesting deeper **refuses**, and no object is written for a compiled document whose entries would.

**The rows.** A declaration's row stands under its spelling in `rows`, in name order; the rows its bodies lifted stand in `lifted`, without a spelling, in the order the numbering counts them. A body numbers its calls and its types from the document itself, under [procedures](procedure.md): the spellings it sends first, in name order, then its own declarations in name order, then the closures its declarations wrote, in the order the numbering lists the declarations and, within one, the order the body wrote them. Where a row lands in a link is the link's answer, so nothing here says it, and one object answers every entry asked of it.

**`numbering`** writes what a reading uses and cannot work out: the spellings sent, in name order; then `(declaration, count)` for each declaration that wrote a closure, counts above zero. A *declaration* is `[0, name]` for a procedure and `[1, name]` for a constant or a variable, since a procedure and a constant may be spelled alike; the procedures stand first, then the constants and variables, each in name order, none twice. **`typeNumbering`** writes the declared types the lowered bodies stand on, ascending by name, none twice: each of them numbers its types in that order. A start in `variables` is a value, which carries a struct's name as its spelling and numbers no type. A contract a bound names is written by its name and numbered nowhere. What a number stands for is arithmetic over these lists and the declared spellings, so the numbers themselves are not written.

## How a part is laid out

Inside the map, a part is written as its fields **in order**, and a variant as its **tag** before them, so a reading beside the same tables reads it back and one that is not refuses it. The rules, used everywhere below:

- A *name* is a string, and one that is not in normal form, or not a name, **refuses**.
- A list a name keys is `[[name, value] …]`, in name order.
- A field that may hold nothing is a list of none or one: `[]` or `[value]`. So a value that is itself null is told from no value at all.
- A variant is `[tag, fields …]`, and a tag this page does not name **refuses**.
- A count, a slot, a row and a position are whole numbers at or above zero, and one below zero **refuses** where it is read.

### Types, as a document writes them

A *type* is the number of an entry in `typeTable`, and the entry is `[tag, …]`:

| tag | type | fields |
|---|---|---|
| 0 | `Any` | |
| 1 | `Never` | |
| 2 | `Null` | |
| 3 | `Bool` | |
| 4 | `Int` | |
| 5 | `Double` | |
| 6 | `String` | |
| 7 | `Array<T>` | *type* |
| 8 | `Dictionary<K, V>` | the key's *type*, the value's *type* |
| 9 | struct, written in `types` as the declaration itself and never as an entry | name → *type*; where it takes type parameters, then their names in order, at least one and none twice, and name → the contracts bounding the type parameter of that name, ascending, at least one, for each one it bounds |
| 10 | `Procedure` | *procedure type* or nothing, *constness*, *isolation* |
| 11 | `var T` | *type* |
| 12 | `inout T` | *type* |
| 13 | `T?` | *type* |
| 14 | a declared name | name; where it applies a struct to types, then a list of *type*, at least one |
| 15 | a type parameter | name |
| 16 | a composition `A & B` | names ascending, two or more: one contract is written as its name, tag 14 |
| 18 | `Self` | |
| 19 | an associated type, `some T.Item` or `Self.Item` | what it stands on, a type parameter's name or another associated type's label, `T.Item` for `some T.Item.Key`; its name |

A *head* is what a document gives a type under, under [types](type.md): a name where it is bare, and otherwise `[name, arguments, bounds]`, the types it applies the named type to, a list of *type*, at least one, and name → the contracts bounding the type parameter of that name, ascending, at least one, for each one it bounds. A list a head keys stands in the order of the heads' spellings, as names, none twice.

A *procedure type* is `[parameters, returns, failing]`: a list of *type*, in position order, a *type*, and a *failing*. A *signature* is `[parameters, returns, failing, constness, isolation, bounds, sameTypes]`: a list of *parameter*, in the declaration's order; a *type*; a *failing*; a *constness*; an *isolation*; name → the contracts bounding the type parameter or the associated type of that name, ascending, at least one, for each one the signature bounds; and name → *type* for each associated type the signature says is a type. A *parameter* is `[name, type, description]`: the name, then each a list of none or one: a *type*, none where the parameter takes anything, so `Any` is never written there; a string.

*Constness* is `0` unstated or `1` const. *Isolation* is `0` unstated or `1` isolated. *Failing* is `[0]`, anything, or `[1, names]`, the names ascending.

### Rows

A *row* is a declaration as its own document compiled it:

    [ label, signature, access, implementation ]

The label is the declared spelling. A row in `lifted` is the same without the label, its fields starting at the signature. `access` is `0` private, `1` internal or `2` public, under *who may name a declaration* in [procedures](procedure.md); a lifted row is private, since nothing names it.

The *implementation* is `[0, body, frame]` for a written body, or `[1, sends]` for a procedure the host answers, each send `[position, selector, handing]`: where the send stands among the declaration's sends, the spelling it reaches, and how many arguments it hands over, from the first position of what that spelling declares. The sends stand one to a place from the first, and each reaches the number the document's `numbering` gives its spelling.

A *frame* is `[size, parameters, variables, captures, names]`: how many slots; which slots the parameters fill, in parameter order; `[variable, slot]` for each module variable the body reads, by its position in `variables`; which slots a closure fills from what it took with it; and what each slot was called, one name per slot, for a refusal that names one.

A *body* is `[instructions, result]`, the result an *operation* or nothing. An *instruction* is `[binding, operation, label]`: the binding or nothing, what to compute, and the string a trace calls the statement. A *binding* is `[0, slot]` to bind, `[1, slot]` to declare, or `[2, address]` to assign.

An *address* is the number of an entry in `addressTable`, and the entry is `[slot, steps]`, each *step* `[0, position, name, optional]` for a field of a struct whose layout the build proved, `[1, name, optional]` for a field read by its name, written past a null or a `Never` the build laid out no struct for, `[2, value, optional]` for a *value* between the brackets, a position on a list and a key on a map, or `[3, address, optional]` for one read from a slot.

### Operations

An *operation* is the number of an entry in `operationTable`, and the entry is `[tag, …]`. These are the constructs and the expression forms of a document with every name the build resolved written as the slot or the row it stands for; nothing computes: what a body does it does by calling, under [the standard vocabulary](vocabulary.md).

| tag | operation | fields |
|---|---|---|
| 0 | a literal | *value* |
| 1 | a slot, read through a path | *address* |
| 2 | an array built from parts | list of *operation* |
| 3 | a struct built from parts | `[layout, operations]`: the *layout*, and a list of *operation* in the layout's field order |
| 4 | a closure literal | the closure's number, captures: `[outer slot, inner slot]` list |
| 5 | calling a value | the callee *operation*, arguments: list of *argument*, in position order |
| 6 | a cast | *operation*, *lowered type*, optional |
| 8 | a conditional | the condition *operation*, then: *instruction* list, else: *instruction* list or nothing |
| 9 | a loop | the condition *operation*, the round: *instruction* list, the round's slot or nothing |
| 10 | an attempt | *body*, the rescue *body*, the failure's slot or nothing |
| 11 | a call | *call* |
| 12 | a call through a contract | *dispatch* |
| 13 | leaving | *reach*, the target name or nothing, what it takes or nothing |
| 14 | a map built from parts | a list of `[key, value]`, each an *operation*, in the order written |

A *layout* is `[name, fields]`: the declared struct's name, and the field names ascending. A *call* is `[procedure, arguments, handed]`: the row the call reaches, numbered by the document; one *operation* or nothing per parameter of the callee, in parameter order, nothing exactly where the call hands that parameter an address in place; and `[position, address]` for each parameter handed in place, by position ascending. A *dispatch* is `[contract, procedure, first, arguments]`: the contract's name, the procedure's, the first argument's *operation*, and the arguments after it by position, each an *argument*. Which row answers is the link's, and stands nowhere in an object. An *argument* is `[0, operation]` by value or `[1, address]` by reference: the place a call of a value hands in place, or one a call through a contract hands to whichever row takes it in place.

### Lowered types

A *lowered type* is a type as a body stands on it, the number of an entry in `loweredTypeTable`, and the entry is `[tag, …]`:

| tag | lowered type | fields |
|---|---|---|
| 0 to 6 | `Any` `Never` `Null` `Bool` `Int` `Double` `String` | |
| 7 | array | *lowered type* |
| 8 | dictionary | the key's *lowered type*, the value's *lowered type* |
| 10 | procedure | parameters or nothing, a list of *lowered type* in position order; returns or nothing, and a *failing* or nothing, each nothing exactly where the parameters are nothing; *constness*; *isolation* |
| 11 | variable | *lowered type* |
| 12 | inout | *lowered type* |
| 13 | nullable | *lowered type* |
| 14 | a declared type | its place in `typeNumbering`; where it applies a struct to types, then a list of *lowered type*, at least one |
| 15 | a type parameter, or an associated type labelled as it is written, `T.Item` or `Self.Item` | its label, the contracts bounding it ascending, those of an associated type being what the contracts asking it and the signature hold it to |
| 16 | a composition | the contracts ascending, at least one |

### Values

A *value* is the number of an entry in `valueTable`, and the entry is `[tag, …]`: 0 null; 1 bool; 2 int; 3 double; 4 string; 5 bytes, each carrying the value; 6 array, carrying its elements as *value*; 7 struct, carrying its name, the field names in name order, the field values; 8 a closure, carrying the identity of the document that wrote it, the *declaration* that wrote it, which of that declaration's closures it is, and `[slot, value]` for what it captured; 9 map, carrying two lists, its keys as *value* in the key order and then its values in the same order, a key out of that order or written twice **refusing**. A closure written by a document nobody wrote down, or holding a box of the run that made it, is not a value an object holds, and such an object is not written.

## Identity and dependencies

A document is told from another by the **digest of its canonical binary writing**, SHA-256 of the bytes the binary writer produces, and by nothing it says about itself. It is derived and never declared. An object does write one down, under `document`, so a reading is handed the identity the object was kept under.

What an object was compiled against is written under `dependencies` by what the host keyed each object under. The language derives nothing there: what tells one compile of a document from another is the host's cache, and the host hands the same key back when it reads the object. An object standing on one the host worked no key out for is not written.

## What a reading refuses

A reading refuses what it cannot read and traps on nothing: the reading runs inside a host's process, and a trap there ends the host. What refuses is the layout, above, and what a layout admits but the language cannot stand on:

- a lifted row where the numbering counts no closure, a numbering counting more closures than `lifted` holds, a count of none for a declaration it counts, and counts that add up past what an int holds
- a frame naming other than one name per slot, standing other than one slot per parameter its declaration takes, or standing a parameter, a variable or a capture past its end
- a body standing on a slot past its frame or on a variable past its document's `variables`, and a loop keeping a run its frame does not hold
- a call handing in place at other positions than the ones it writes nothing at, or out of ascending order
- a closure literal taking what it captured into slots other than the captures of its own row's frame
- a `keeps` that ends before it begins
- a contract's bound holding a type the contract does not ask
- a declared type that is no struct and comes back to itself through what it stands for, which the load refuses in a document, under [types](type.md)
- a struct built from parts holding other than one part per field its layout names
- a lowered procedure type writing what it answers or what it may fail with other than exactly where it writes what it takes
- a row of a procedure the host answers whose sends do not stand one to a place from the first, or reach a spelling the document's `numbering` does not number
- an object standing against a document other than the one it was kept under

Every one of these is refused where the object is read, before it is laid beside anything. What only the documents beside it can answer is refused at `build`, where a compile lays the object down or a link does, under [checking](checking.md): whether every object under its `dependencies` is beside it, which row a number is and whether a call stands as many arguments as that row takes, which type answers a contract, and whether it stands after every document it names, so two objects that need each other refuse as two documents do. A type its declarations, signatures and bodies name is the declaration its compile read, which its `dependencies` say is beside it, and a build does not ask that again.

The names an object writes are the ones its document wrote, and each held the grammar of where it is written when that document was loaded, under [checking](checking.md): a type's, a contract's, a claim's, a member's, a bound's and a part joined with `&` alike. An object is what a build wrote, so a reading asks those names nothing again, and what a name stands for beside the documents is the link's to say, for an object as for a document.

What a build judged, an object writes down as judged: what a signature says, `returns`, `failing`, `const` and `isolated`, and the type every reading in a body was judged to be. A reading, a link and a run take each of those as written and judge none of them again. A body is held to its declaration once, by the compile of its document, under [checking](checking.md). An object a reading admits and no build would write, a body answering what its declaration does not take or calling what is no procedure, is one this specification gives no answer for, save one: a run of it **traps on nothing**, for the reason a reading does not, and where it stops, it stops by refusing the run. Whether an object handed over is the one a build wrote is the transport's to say, by whatever seals what it carries. Nothing an object writes proves it, so a reading does not ask.

## One object

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
  (result (call Standard.Collection.appending n 1)))
```

compiles to an object with one row, written as data, one entry a line and `rows` broken onto a few more, and its two digests elided:

```
(dictionary
  (entry "addressTable" (array (array 0 (array))))
  (entry "claims" (array))
  (entry "constants" (array))
  (entry "contracts" (array))
  (entry "dependencies" (array x"…"))
  (entry "document" (array x"…"))
  (entry "importedClaims" (array))
  (entry "lifted" (array))
  (entry "loweredTypeTable" (array))
  (entry "members" (array))
  (entry "numbering" (array (array "Standard.Collection.appending") (array)))
  (entry "object" 1)
  (entry "operationTable" (array (array 1 0) (array 0 0) (array 11 (array 0 (array (array 0) (array 1)) (array)))))
  (entry "rows" (array
    (array "entry"
      (array (array (array "n" (array 1) (array))) 3 (array 1 (array)) 1 1 (array) (array))
      2
      (array 0 (array (array) (array 2)) (array 1 (array 0) (array) (array) (array "n"))))))
  (entry "typeMembers" (array))
  (entry "typeNumbering" (array))
  (entry "typeTable" (array (array 4) (array 7 0) (array 4) (array 7 2)))
  (entry "types" (array))
  (entry "valueTable" (array (array 2 1)))
  (entry "variables" (array)))
```

Read it back: `rows` holds `entry`, whose signature takes `n` as type `1` and answers type `3`. In `typeTable`, entry `1` is an array (tag 7) of entry `0`, `Int` (tag 4), and entry `3` is the same over entry `2`: both are `Array<Int>`, each written once where it is held. The signature fails with nothing (`(array 1 (array))`), is const (`1`) and isolated (`1`), bounds nothing and says no associated type is a type (`(array) (array)`); the row is public (`2`). Its implementation is a body (`0`) with no instructions and a result, operation `2`: a call (`11`) to row `0` of the numbering, which is `Standard.Collection.appending`, with two arguments, operations `0` and `1`, neither handed in place. Operation `0` reads (`1`) address `0`, slot `0` with no steps, and operation `1` is the literal (`0`) value `0`, the int (`2`) `1`. Every number stands before the entry holding it. The frame has one slot, filled by the parameter, called `n`. The dependency is what the host keyed the standard vocabulary's object under.

## Cases

What `conformance/` asks about this page, by the name each case's file carries.

- `a-document-is-not-an-object`
- `an-object-applying-a-struct-to-no-types-refuses`
- `an-object-bounding-a-type-a-contract-asks-by-nothing-refuses`
- `an-object-bounding-a-type-its-contract-does-not-ask-refuses`
- `an-object-bounding-a-type-parameter-by-nothing-refuses`
- `an-object-claiming-no-contract-for-a-type-refuses`
- `an-object-counting-no-closures-for-a-declaration-refuses`
- `an-object-giving-a-type-a-member-no-row-stands-under-refuses`
- `an-object-giving-a-type-no-member-refuses`
- `an-object-giving-a-type-no-type-member-refuses`
- `an-object-holding-a-number-past-its-table-refuses`
- `an-object-holding-an-entry-nowhere-refuses`
- `an-object-holding-an-entry-twice-refuses`
- `an-object-links-and-runs`
- `an-object-listing-a-type-parameter-twice-refuses`
- `an-object-listing-no-type-parameters-for-a-struct-refuses`
- `an-object-missing-a-part-refuses`
- `an-object-naming-one-type-twice-refuses`
- `an-object-nesting-a-table-past-the-bound-refuses`
- `an-object-nesting-its-tables-to-the-bound-runs`
- `an-object-numbering-entries-out-of-order-refuses`
- `an-object-of-a-later-format-refuses`
- `an-object-of-a-later-format-with-keys-of-its-own-refuses`
- `an-object-of-a-struct-taking-a-type-parameter-links-and-runs`
- `an-object-runs-with-what-the-entry-is-given`
- `an-object-standing-against-another-document-refuses`
- `an-object-standing-on-one-object-twice-refuses`
- `an-object-standing-on-what-is-not-laid-refuses`
- `an-object-whose-body-stands-past-its-frame-refuses`
- `an-object-whose-call-stands-more-arguments-than-its-callee-takes-refuses`
- `an-object-whose-call-through-a-contract-stands-more-arguments-than-its-rows-take-refuses`
- `an-object-whose-call-writes-an-argument-where-it-hands-in-place-refuses`
- `an-object-whose-claims-stand-out-of-name-order-refuses`
- `an-object-whose-closure-counts-add-up-past-an-int-refuses`
- `an-object-whose-dependencies-stand-out-of-name-order-refuses`
- `an-object-whose-entry-is-not-public-refuses`
- `an-object-whose-frame-names-fewer-slots-than-it-holds-refuses`
- `an-object-whose-imported-claims-stand-out-of-name-order-refuses`
- `an-object-whose-layout-names-stand-out-of-order-refuses`
- `an-object-whose-map-keys-stand-out-of-the-key-order-refuses`
- `an-object-whose-members-stand-out-of-name-order-refuses`
- `an-object-whose-numbering-closures-stand-out-of-name-order-refuses`
- `an-object-whose-numbering-sends-stand-out-of-name-order-refuses`
- `an-object-whose-procedure-the-host-answers-sends-a-spelling-its-numbering-does-not-number-refuses`
- `an-object-whose-rows-stand-out-of-name-order-refuses`
- `an-object-whose-struct-fields-stand-out-of-name-order-refuses`
- `an-object-whose-type-numbering-stands-out-of-name-order-refuses`
- `an-object-whose-types-name-each-other-refuses`
- `an-object-whose-types-name-each-other-under-a-question-mark-refuses`
- `an-object-whose-types-stand-out-of-name-order-refuses`
- `an-object-whose-variables-stand-out-of-name-order-refuses`
- `an-object-with-a-key-nothing-names-refuses`
- `an-object-with-a-lifted-row-nothing-counts-refuses`
- `an-object-writing-a-composition-of-one-name-refuses`
- `an-object-writing-a-count-below-zero-refuses`
- `an-object-writing-a-name-not-in-normal-form-refuses`
- `an-object-writing-a-procedure-type-that-answers-without-parameters-refuses`
- `an-object-writing-a-procedure-type-that-takes-parameters-and-answers-nothing-refuses`
- `an-object-writing-a-tag-the-layout-does-not-name-refuses`
- `an-object-writing-an-empty-name-refuses`
- `an-object-writing-any-as-a-parameter-type-refuses`
- `an-object-writing-what-a-procedure-type-may-fail-with-and-not-what-it-takes-refuses`
- `the-object-of-a-call`
- `the-object-of-a-cast`
- `the-object-of-a-claim-under-a-head`
- `the-object-of-a-closure`
- `the-object-of-a-composition`
- `the-object-of-a-conditional`
- `the-object-of-a-declaration-the-host-answers`
- `the-object-of-a-declared-type-and-a-contract`
- `the-object-of-a-dispatch`
- `the-object-of-a-field-read-past-a-possible-absence`
- `the-object-of-a-leave`
- `the-object-of-a-literal`
- `the-object-of-a-local`
- `the-object-of-a-loop`
- `the-object-of-a-map-a-variable-starts-with`
- `the-object-of-a-map-built-from-parts`
- `the-object-of-a-module-constant-and-a-variable`
- `the-object-of-a-struct-built-from-parts`
- `the-object-of-a-struct-taking-a-type-parameter`
- `the-object-of-a-write-at-a-constant-key`
- `the-object-of-an-array-built-from-parts`
- `the-object-of-an-attempt`
- `the-object-of-an-imported-claim`
- `the-object-of-associated-types`
- `the-object-of-every-type-spelling`
