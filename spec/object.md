# Objects

What a build writes down: one document compiled, in its own coordinates, laid out so that any implementation reads what any other wrote. This page is the layout. What the parts *mean* is the pages that judge them: a row's claims are [checking](checking.md), a body's operations are [statements](statement.md) and [expressions](expression.md) with every fact the build proved written in, and the bytes an object travels as are [encodings](encoding.md).

An object is a **value**, and nothing more than one: it is written by the binary encoding, laid out by the text encoding, and identified by its bytes the way a document is. What crosses a wire is a document; what a build keeps, hands to a cache, or receives from one is an object, and both cross under the same encodings. A file holding either is named by its encoding and not by what it holds, `.warp` or `.warpt`, and what it holds is what the value says it is: a document says `warp`, an object says `object`.

## What an object holds

An object is one record. It carries **exactly** these keys, and a key none of them names, or one of them missing, **refuses**. Current format: **1**.

| key | holds | order |
|---|---|---|
| `object` | int. This layout's format. Read before anything laid out by it, the keys included | |
| `document` | the document's identity, or nothing where the program was never written down | |
| `dependencies` | the objects behind every declaration this document named, each by what the host keyed it under | ascending by bytes, none twice |
| `types` | name → *type*, as the document wrote them | by name |
| `constraints` | name → list of *type* | by name |
| `contracts` | name → (procedure name → `[ signature, constness, isolation ]`, the two marks as a row writes them) | by name, then by name |
| `claims` | type name → the contracts it says it answers | by name; the contracts ascending |
| `leaned` | the pairs its bodies lean on: (type, contract, *place*), unresolved | by type, then contract |
| `rows` | the declarations, each a *row* under its spelling | by name |
| `lifted` | the closures its bodies lifted, each a *row* with no spelling | as the numbering counts them |
| `answers` | name → *lowered type*: what the build read off a body whose declaration wrote no `returns` | by name |
| `numbering` | two lists: what it sends, and how many closures each declaration wrote | below |
| `typeNumbering` | two lists: the declared types its bodies stand on, and the memberships, each ascending by name | below |
| `variables` | (name, *value*): what each variable starts a run holding | by name |
| `constants` | the constants it declared, by spelling | by name |

**The record is keyed and its parts are not.** The record names each part by its key; inside a part the fields stand in order and a kind says itself by its tag. A reading holds an object to the format it reads before it reads a part.

**Order is spelling.** Every list a name keys stands ascending by the names' bytes, none twice, and so does every set written as a list. That is the whole of what makes one object one value: a dictionary lends no order, so the layout says one, and a reading takes no other. A list out of order, or naming one thing twice, **refuses**.

**The rows.** A declaration's row stands under its spelling in `rows`, in name order; the rows its bodies lifted stand in `lifted`, without a spelling, in the order the numbering counts them. A body numbers its calls and its types from the document itself, under [procedures](procedure.md): the spellings it sends first, in name order, then its own declarations in name order, then the closures its declarations wrote, in the order the numbering lists the declarations and, within one, the order the body wrote them. Where a row lands in a link is the link's answer, so nothing here says it, and one object answers every entry asked of it.

**`numbering`** writes what a reading uses and cannot work out: the spellings sent, in name order; then `(declaration, count)` for each declaration that wrote a closure, counts above zero. A *declaration* is `[0, name]` for a procedure and `[1, name]` for a constant or a variable, since a procedure and a constant may be spelled alike; the procedures stand first, then the constants and variables, each in name order, none twice. **`typeNumbering`** writes the declared types the lowered bodies stand on, ascending by name, none twice, then the memberships, likewise: a body numbers its types in that order. What a number stands for is arithmetic over these lists and the declared spellings, so the numbers themselves are not written.

## How a part is laid out

Inside the record, a part is written as its fields **in order**, and a kind as its **tag** before them, so a reading beside the same tables reads it back and one that is not refuses it. The rules, used everywhere below:

- A *name* is a string, and one that is not in normal form, or not a name, **refuses**.
- A list a name keys is `[[name, value] …]`, in name order.
- A field that may hold nothing is a list of none or one: `[]` or `[value]`. So a value that is itself null is told from no value at all.
- A kind is `[tag, fields …]`, and a tag this page does not name **refuses**.
- A count, a slot, a row and a position are whole numbers at or above zero, and one below zero **refuses** where it is read.

### Types, as a document writes them

A *type* is `[tag, …]`:

| tag | type | fields |
|---|---|---|
| 0 | `any` | |
| 1 | `never` | |
| 2 | `null` | |
| 3 | `bool` | |
| 4 | `int` | |
| 5 | `double` | |
| 6 | `string` | |
| 7 | ranged | *refinement* |
| 8 | `array<T>` | *type* |
| 9 | `dictionary<T>` | *type* |
| 10 | record | name → *type* |
| 11 | `procedure` | *procedure type* or nothing, *constness*, *isolation* |
| 12 | `var T` | *type* |
| 13 | `inout T` | *type* |
| 14 | `linear T` | *type* |
| 15 | `consuming T` | *type* |
| 16 | `borrowing T` | *type* |
| 17 | `T?` | *type* |
| 18 | a declared name | name |
| 19 | a type parameter | name, its bounds: names ascending |
| 20 | a composition `A & B` | names ascending, at least one |
| 21 | a projection | the parameter projected, the path: *segment* list |

A *refinement* is `[0, from, to]` over whole numbers or `[1, from, to]` over fractions, each end a list of none or one; the upper end is an *edge*, `[0, bound]` where the bound is inside or `[1, bound]` where it is out. A *segment* is `[0, name, optional]`, `[1, index, optional]` or `[2, path, optional]` for an index read from a path.

A *procedure type* is `[parameters, returns]`: a list of *type*, in position order, and a *type* or nothing. A *signature* is `[parameters, returns]`: a list of *parameter*, in the declaration's order, and a *type* or nothing. A *parameter* is `[name, type, candidates, description]`: the name, then each a list of none or one: a *type*; the strings it admits; a string.

*Constness* is `0` unstated or `1` const. *Isolation* is `0` unstated or `1` isolated. *Failing* is `[0]` unstated or `[1, names]`, the names ascending.

### Places

A *place* is where in a document something was written: `[document, steps]`, the document's identity or nothing, and a list of *step*:

| tag | step | fields |
|---|---|---|
| 0 | a key the document writes | string, as typed |
| 1 | a part of the program | *part* |
| 2 | the construct a statement writes | *construct* |
| 3 | a position in an array | position |
| 4 | a statement | its name or nothing, its position |
| 5 | a landmark in a program nobody wrote down | string |

A *part* is `[tag]`: 0 `procedures`, 1 `constants`, 2 `variables`, 3 `types`, 4 `constraints`, 5 `contracts`, 6 `satisfies`, 7 `imports`, 8 `parameters`, 9 `returns`, 10 `body`, 11 `result`, 12 a cast's subject, carrying `true` for `as?` or `false` for `as`, 13 `callee`, 14 `arguments`, 15 `closure`, 16 a condition, carrying `[0]` for a conditional's or `[1]` for a loop's, 17 `then`, 18 `otherwise`, 19 `rescue`, 20 a record's fields.

A *construct* is `[tag]`: 0 literal, 1 reference, 2 array, 3 record, 4 closure, 5 cast, 6 block, 7 conditional, 8 loop, 9 attempt, 10 call, 11 leave, carrying its *reach*: `0` the procedure, `1` the construct, `2` the round.

### Rows

A *row* is a declaration as its own document settled it:

    [ label, signature, access, constness, isolation, failing, handsBackAsDeclared, implementation ]

The label is the declared spelling. A row in `lifted` is the same without the label, its fields starting at the signature. `access` is `0` private, `1` internal or `2` public, under *who may name a declaration* in [procedures](procedure.md); a lifted row is private, since nothing names it. `handsBackAsDeclared` is `true` where what the body hands back, its answer and every variable handed to it in place, is at every type parameter that parameter, so nothing a call filled has to be judged again where the call stands, and `false` otherwise. A body proves it only where every call it makes whose answer or variable handed back names a type parameter reaches a row that proved it too, and where nothing it reads as a type parameter may hold what is not a value of it: no call fills one from an argument that is not, such as a value every member of the bounds takes or a reading of `any`, no write leaves a variable reading as one while it writes what is not, and no closure that is not isolated reaches a variable whose type names one, since a closure read as a procedure type may be called with what the parameter stands for nowhere. A native's row writes `true`, on its host's word. A link reads it as said, the way it reads `constness` and `isolation`, and leaves out the judgement a call takes where the row the call reaches says `true`, or, for the answer alone, where every row a call through a contract may reach settles exactly what the call reads and the call hands nothing back to judge.

The *implementation* is `[0, body, frame]` for a written body, or `[1, sends]` for a native, each send `[position, selector, handing]`: where the send stands among the declaration's sends, the spelling it reaches, and how many arguments it hands over, from the first position of what that spelling declares. The sends stand one to a place from the first, and each reaches the number the document's `numbering` gives its spelling; a native row whose sends say otherwise **refuses**.

A *frame* is `[size, parameters, variables, captures, names]`: how many slots; which slots the parameters fill, in parameter order; `[variable, slot]` for each module variable the body reads, by its position in `variables`; which slots a closure fills from what it took with it; and what each slot was called, one name per slot, for a refusal that names one. A body standing on a slot the frame does not hold, or a frame naming fewer slots than it has, **refuses**.

A *body* is `[instructions, result]`, the result an *operation* or nothing. An *instruction* is `[binding, operation, label]`: the binding or nothing, what to compute, and the string a trace calls the statement. A *binding* is `[0, slot, settling]` to bind, `[1, slot, settling]` to declare, or `[2, address, settling]` to assign, `settling` a *lowered type* or nothing.

An *address* is `[slot, steps]`, each *step* `[0, position, name, optional]` for a field of a record whose layout the build proved, `[1, name, optional]` for a key only the run knows, `[2, index, optional]`, or `[3, address, optional]` for an index read from a slot.

### Operations

An *operation* is `[tag, …]`. These are the constructs and the expression forms of a document with every name the build resolved written as the slot or the row it stands for, and the judgement the build left a call's answer where the call reads it narrower than its callee settles; nothing computes: what a body does it does by calling, under [the standard vocabulary](vocabulary.md).

| tag | operation | fields |
|---|---|---|
| 0 | a literal | *value* |
| 1 | a slot, read through a path | *address* |
| 2 | an array built from parts | list of *operation* |
| 3 | a record built from parts | `[layout, operations]`: the *layout*, and a list of *operation* in the layout's field order |
| 4 | a closure literal | the closure's number, captures: `[outer slot, inner slot]` list |
| 5 | calling a value | the callee *operation*, arguments: list of *argument*, in position order |
| 6 | a cast | *operation*, *lowered type*, optional |
| 7 | a block | *body* |
| 8 | a conditional | the condition *operation*, then: *instruction* list, else: *instruction* list or nothing |
| 9 | a loop | the condition *operation*, *body*, the round's slot or nothing, keeps: `[from, to)` or nothing |
| 10 | an attempt | *body*, the rescue *body*, the failure's slot or nothing |
| 11 | a call | *call* |
| 12 | a call through a contract | *dispatch* |
| 13 | leaving | *reach*, the target name or nothing, what it takes or nothing |
| 14 | a call judged where it stands | the call's *operation*, the answer's *lowered type* or nothing, `[position, lowered type]` for each variable handed back in place, judged once the call is over through the hold the call made, and the *lowered type* the answer settles to or nothing: what a declaration wrote, a value's slot or a contract, with the type parameters it names left standing, and nothing where the answer is what the call filled a declaration's type parameter with |

A *layout* is `[name, fields]`: the declared name or nothing, and the field names ascending. A *call* is `[procedure, arguments, handed]`: the row the call reaches, numbered by the document; one *operation* or nothing per parameter of the callee, in parameter order, nothing where the call wrote nothing or a hold stands; and `[position, address]` for each parameter handed in place. A *dispatch* is `[contract, procedure, first, arguments]`: the contract's name, the procedure's, the first argument's *operation*, and the arguments after it by position, each an *argument*. Which row answers is the link's, and stands nowhere in an object. An *argument* is `[0, operation]` by value or `[1, address]` by reference: the place a call of a value hands in place, or one a call through a contract hands to whichever row takes it in place.

### Lowered types

A *lowered type* is a type as a body stands on it, `[tag, …]`:

| tag | lowered type | fields |
|---|---|---|
| 0 to 6 | `any` `never` `null` `bool` `int` `double` `string` | |
| 7 | ranged | *refinement* |
| 8 | array | *lowered type* |
| 9 | dictionary | *lowered type* |
| 10 | record | `[layout, types]`: the *layout*, and a list of *lowered type* in the layout's field order |
| 11 | procedure | parameters or nothing, a list of *lowered type* in position order; returns or nothing; *constness*; *isolation* |
| 12 | variable | *lowered type* |
| 13 | inout | *lowered type* |
| 14 | nullable | *lowered type* |
| 15 | a declared type | its number in `numbering` |
| 16 | a type parameter | its label, bounds ascending |
| 17 | a composition | bounds ascending, at least one |
| 18 | a projection | the parameter projected, *segment* list |
| 19 | undeclared | its label, why: `[0, name]` nothing declares it, `[1, name]` nothing declares it as a membership or a contract, `[2]` it names itself |

A *bound* is `[0, number]` for a membership or `[1, name]` for a contract.

### Values

A *value* is `[tag, …]`: 0 null; 1 bool; 2 int; 3 double; 4 string; 5 bytes, each carrying the value; 6 array, carrying its elements as *value*; 7 record, carrying the name or nothing, the field names, the field values; 8 dictionary, carrying `[name, value]` in name order; 9 a closure, carrying the identity of the document that wrote it, the *declaration* that wrote it, which of that declaration's closures it is, `[slot, value]` for what it captured, and the *lowered type* the slot it settled into wrote for its answer, or nothing. A closure written by a document nobody wrote down, or holding a box of the run that made it, is not a value an object holds, and such an object is not written.

## Identity and dependencies

A document is told from another by the **digest of its canonical binary writing**, SHA-256 of the bytes the binary writer produces, and by nothing it says about itself. It is derived and never declared. An object does write one down, under `document`, so a reading is handed the identity the object was kept under and an object saying it belongs somewhere else **refuses**.

What an object leaned on is written under `dependencies` by what the host keyed each object under. The language derives nothing there: what tells one compile of a document from another is the host's cache, and the host hands the same key back when it reads the object. An object leaning on one the host worked no key out for is not written.

## What a reading refuses

A reading refuses what it cannot read and traps on nothing: the reading runs inside a host's process, and a trap there ends the host. What refuses is the layout, above, and what a layout admits but the language cannot stand on:

- a lifted row where the numbering counts no closure, a count of none for a declaration it counts, and counts that add up past what an int holds
- a body standing on a slot past its frame, a loop keeping a run its frame does not hold, a frame naming fewer slots than it has, a call standing more arguments than the row it reaches takes
- a native row whose sends do not stand one to a place from the first, or reach a spelling the document's `numbering` does not number
- an object standing against a document other than the one it was kept under

Every one of these is refused where the object is read, before it is laid beside anything. What only a link can answer, which row a number is, which type answers a contract, is refused at `build`, under [checking](checking.md).

## One object

The document

```
warpt 1
{
  imports [ "std.math.plus" ]
  procedures {
    entry {
      access "public"
      parameters [ { name "n" type "int" } ]
      result { call { arguments [ { ref "n" } 1 ] procedure "std.math.plus" } }
      returns "int"
    }
  }
  warp 1
}
```

compiles to an object with one row, laid out as text and packed onto fewer lines than the writer uses:

```
warpt 1
{
  answers []
  claims []
  constants []
  constraints []
  contracts []
  dependencies [ x"…" ]
  document [ x"…" ]
  leaned []
  lifted []
  numbering [ [ "std.math.plus" ] [] ]
  object 1
  rows [
    [
      "entry"
      [ [ [ "n" [ [ 4 ] ] [] [] ] ] [ [ 4 ] ] ]
      2
      1
      1
      [ 1 [] ]
      true
      [
        0
        [ [] [ [ 11 [ 0 [ [ [ 1 [ 0 [] ] ] ] [ [ 0 [ 2 1 ] ] ] ] [] ] ] ] ]
        [ 1 [ 0 ] [] [] [ "n" ] ]
      ]
    ]
  ]
  typeNumbering [ [] [] ]
  types []
  variables []
}
```

Read it back: `rows` holds `entry`, whose signature takes `n` as `int` (type tag 4) and answers `int`; it is public (`2`), const (`1`) and isolated (`1`) and fails with nothing (`[1 []]`); its answers are what it declares (`true`); its implementation is a body (`0`) with no instructions and a result, a call (`11`) to row `0` of the numbering, which is `std.math.plus`, with two arguments, the first read from slot `0` and the second the literal (`0`) int (`2`) `1`; and its frame has one slot, filled by the parameter, called `n`. The dependency is what the host keyed the standard vocabulary's object under.

## Cases

What `conformance/` asks about this page, by the name each case's file carries.

- `a-document-is-not-an-object`
- `an-object-counting-no-closures-for-a-declaration-refuses`
- `an-object-leaning-on-one-object-twice-refuses`
- `an-object-leaning-on-what-is-not-laid-refuses`
- `an-object-links-and-runs`
- `an-object-missing-a-part-refuses`
- `an-object-naming-one-type-twice-refuses`
- `an-object-of-a-later-format-refuses`
- `an-object-of-a-later-format-with-keys-of-its-own-refuses`
- `an-object-runs-with-what-the-entry-is-given`
- `an-object-standing-against-another-document-refuses`
- `an-object-whose-body-stands-past-its-frame-refuses`
- `an-object-whose-call-stands-more-arguments-than-its-callee-takes-refuses`
- `an-object-whose-claims-stand-out-of-name-order-refuses`
- `an-object-whose-closure-counts-add-up-past-an-int-refuses`
- `an-object-whose-dependencies-stand-out-of-name-order-refuses`
- `an-object-whose-dictionary-entries-stand-out-of-name-order-refuses`
- `an-object-whose-entry-is-not-public-refuses`
- `an-object-whose-frame-names-fewer-slots-than-it-holds-refuses`
- `an-object-whose-layout-names-stand-out-of-order-refuses`
- `an-object-whose-loop-keeps-a-run-past-its-frame-refuses`
- `an-object-whose-native-sends-a-spelling-its-numbering-does-not-number-refuses`
- `an-object-whose-numbering-closures-stand-out-of-name-order-refuses`
- `an-object-whose-numbering-sends-stand-out-of-name-order-refuses`
- `an-object-whose-rows-stand-out-of-name-order-refuses`
- `an-object-whose-type-numbering-stands-out-of-name-order-refuses`
- `an-object-whose-types-stand-out-of-name-order-refuses`
- `an-object-whose-variables-stand-out-of-name-order-refuses`
- `an-object-with-a-key-nothing-names-refuses`
- `an-object-with-a-lifted-row-nothing-counts-refuses`
- `an-object-writing-a-count-below-zero-refuses`
- `an-object-writing-a-name-not-in-normal-form-refuses`
- `an-object-writing-a-tag-the-layout-does-not-name-refuses`
- `an-object-writing-an-empty-name-refuses`
- `the-object-of-a-block`
- `the-object-of-a-call`
- `the-object-of-a-cast`
- `the-object-of-a-closure`
- `the-object-of-a-composition`
- `the-object-of-a-conditional`
- `the-object-of-a-declared-type-and-a-constraint`
- `the-object-of-a-dispatch`
- `the-object-of-a-leave`
- `the-object-of-a-literal`
- `the-object-of-a-local`
- `the-object-of-a-loop`
- `the-object-of-a-module-constant-and-a-variable`
- `the-object-of-a-native-declaration`
- `the-object-of-a-record-built-from-parts`
- `the-object-of-an-array-built-from-parts`
- `the-object-of-an-attempt`
- `the-object-of-every-type-spelling`
