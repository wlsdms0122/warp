# The document format

What a document is: the map a program travels as, and the module it declares. This page is the outline. What each of its slots holds is [procedures](procedure.md), [statements](statement.md), [expressions](expression.md) and [types](type.md), and the bytes it arrives as are [encodings](encoding.md).

A document is one map. Every map this grammar names, on this page and on the pages it points to, is keyed by names, text in normal form C with something in it, and is **closed**: a key that is no name, and a key none of them names, **refuse at the load**. Every slot marked *expression*, *block*, *statements* or *type* takes the grammar of that name.

## The module

| key | takes | required |
|---|---|---|
| `warp` | int. The language version this document is written for | yes |
| `imports` | array of strings. Every name the program uses and does not declare: the procedures it sends, and the types and contracts it names; and the claims of other documents it stands on, each written as the type and the contract it is about | yes, and empty where the program uses none |
| `description` | string | no |
| `types` | map: name → `{ struct: { field: type, … }, typeParameters?, bounds?, satisfies?, procedures? }` for a struct, its fields, the type parameters it takes in order and their bounds, the contracts it answers and its members, or a type, which the name is then a second spelling of, under [types](type.md) | no |
| `contracts` | map: name → map: procedure → `{ parameters, returns?, const?, isolated?, failing? }`, an empty map for a contract asking no procedures; the procedure takes `Self` first, so one leaving `parameters` out **refuses at the load**, and writes no `bounds`, so one writing them **refuses at the load**, under [types](type.md); the two bools ask what a slot asks with a `const` and an `isolated` procedure type, of every declaration answering, and `failing` names, as an array of strings, what one may fail with, nothing where it is left out | no |
| `extensions` | map: head → `{ satisfies?, procedures? }`: what the document gives a type under a head, a type's name or the type applied to what its brackets hold, `Array<Int>`, `App.Box<some T: Hashable>`, the contracts the values the head takes answer and the type's members, under [types](type.md) | no |
| `const` | map: name → expression; a constant may read the constants beside it, and constants that read each other back have no order to settle in and **refuse at the load** | no |
| `var` | map: name → expression, or `{ type, value }` where the variable says what it holds; a variable every procedure beside it may read and write | no |
| `procedures` | map: name → procedure | no |

**A module variable.** Its start is written like a constant and settles the same way: at the **build**, from what a constant settles from, beside the constants and reading them, and them only: a start that reads another variable **refuses at the load**. Its type is what it declares under `type`, and where it declares none, the type its start reads as (a cast's type where a cast is written there, and where it reads a constant, the type its place in the constant's type has, under *a constant-headed path* in [expressions](expression.md)), with every procedure it holds read without the constness, isolation or failing its type says, since a write may put another procedure there; a start the declared type does not take **refuses at the build**, and every write into it is judged against that type. A start that reads as an empty collection says nothing about what the box will hold, so a variable that declares no type and whose start reads as an empty list or map, at whatever depth and under no cast, **refuses at the build**. It is private to the document like a constant, as a procedure written `private` is under [procedures](procedure.md), read by the same spelling (`ref`), and written by a `set` in a procedure the document declares, or through a parameter such a procedure hands it to in place; another document reaches it only through such a procedure. A name is a constant or a variable, not both: one declared under both keys **refuses** at the load. Either may be spelled like a procedure: a reference reads the constant or the variable, and a call names the procedure. Every run starts each variable at its settled value, so two runs of one image never see each other.

**The version.** Every document says it, and one that does not **refuses at the load**, as not a document rather than as a malformed one.

The current version is **1**. A reader reads the version it implements and **refuses** any other, before judging the document's keys. A document for an earlier version is written again: a document is spelled the way the writer of its version spells it, so one written for another version is another text. The number goes up when anything portable changes what an existing program *means*: a type added, a type read differently, a checking rule moved, a standard procedure answering differently. It does not move when a procedure is *added*, since a program that does not call it cannot tell, and one that does is refused by name.

An implementation implements the **current** version only.

**Note.** A reader that filled in a missing version would be answering, on the sender's behalf, the one question that has to be answerable from the bytes alone, and a file of some other kind would get as far as having its keys judged. A later version may add keys, and checking the keys first would turn "I am too old for this" into "this is malformed". A document written for another version is refused as that, rather than read by rules it was not written to and run to a different answer.

**The imports list.** Every name the program *uses* and does not itself declare, each by its declared spelling: `Standard.Numeric.plus`, never `plus`. Two kinds of name are in it, and they are the two kinds a link resolves. The procedures the program sends, from procedure bodies, from constants and from a variable's start alike; and the types and contracts it names, in a declaration, a bound, a local binding, a cast, a closure's signature, an extension or a claim. The sends a procedure the host answers declares are in it too. What a body sends is read off its text; a module the host assembled in its own language holds procedures with no text a reader could read, so each declares the procedures it sends and those count the same.

The list holds spellings and not kinds: a spelling in it asks for whatever the link declares under it, so a program using the procedure and the type of one spelling lists it once. The list is that set exactly, not a bound around it: **reading refuses** a document whose list disagrees with what its program uses, in either direction. It refuses at the load, since what a program uses is a fact of its text alone. The list is read before the program: the host lays the link from it, whatever kind each spelling turns out to declare, so a list saying less would be trusted and wrong, and a list saying more asks for what the program has no use for.

**A claim among the imports.** A claim declares no name, so a document stands on a claim another document makes by writing the pair the claim is about, the type's name and the contract's with a colon and a space between: `"T.Card: App.Describable"`. What it stands on is what its build asks a contract of, under [types](type.md): a claim made in a document it stands on is within its reach already, and one made in a document it does not stand on is reached this way alone. Which claims a document asks of is its build's, not its text's, so a claim among the imports is not held to the program's use as a name is. An import naming a claim the document makes itself or one the language makes, and one written as neither a name nor a pair, **refuse at the load**, and one naming a claim no document in the link makes, or one two documents of the link make, **refuses at the build**.

**A module asks and does not carry.** What the list names is supplied by whatever else stands in the link, and a module that shipped its own copy of a bundle it uses would put that bundle's declarations in the link twice, which the build refuses by the rule that one name has one declarer. Which modules are in a link is decided where the link is assembled. The same holds for the types and contracts a signature mentions: the list names them, and what declares them is still the link's to bring.

A document says its list, and one that does not **refuses at the load**, the way one that does not say its version does: the list is read before the program and the link is laid from it, so a reader with no list cannot tell a program that uses nothing from one that uses everything, and the empty list is what says the first.

## A document says each thing one way

A program has one document. Reading **refuses at the load** a document that says what it says another way: a key written with what its absence means (`access "internal"`, `result null`), marks in another order, a list the document keeps in name order written out of it. The one way is what writing the program back out gives, so a document that has been read and written is the document that was read, and one program never stands under two identities.

## Shorthands are the front end's

A front end may offer shorthands that stand in for what the language already writes, such as operator keys like `is:` in a condition slot or a `{ format:, with: }` template. They are the front end's own: it spends them before the document leaves, and what leaves writes the language's own forms.

A reader of documents **refuses** a shorthand where it meets one, the way it refuses any mapping that is no form of the document's: a struct is written under `struct`, so a mapping of `format` and `with` is never read as a struct that happens to have those fields.

## Cases

What `conformance/` asks about this page, by the name each case's file carries.

- `a-claim-import-whose-type-is-no-types-name-refuses`
- `a-constant-closure-may-name-its-documents-own-type`
- `a-constant-is-a-name-a-body-reads`
- `a-constant-may-be-spelled-like-a-procedure`
- `a-constant-sees-only-the-constants-beside-it`
- `a-document-declaring-no-procedure-stands-beside-one-that-names-it`
- `a-document-importing-a-claim-it-makes-refuses`
- `a-document-that-says-no-version-refuses`
- `a-document-without-imports-refuses`
- `a-field-read-names-no-type`
- `a-front-end-shorthand-refuses-in-a-document`
- `a-later-document-refuses`
- `a-list-leaving-out-a-type-the-program-names-refuses`
- `a-mapping-keyed-by-what-is-no-name-refuses`
- `a-module-variable-closure-called-with-another-count-refuses`
- `a-module-variable-closure-may-name-its-documents-own-type`
- `a-module-variable-declares-what-it-holds`
- `a-module-variable-handed-in-place-is-one-box`
- `a-module-variable-is-handed-in-place-to-a-procedure-the-host-answers`
- `a-module-variable-is-not-named-from-another-document`
- `a-module-variable-is-shared-by-the-procedures-beside-it`
- `a-module-variable-keeps-the-type-it-started-as`
- `a-module-variable-start-outside-its-declared-type-refuses`
- `a-module-variable-started-as-null-cast-to-a-nullable-takes-a-value`
- `a-module-variable-started-at-a-constants-element-holds-the-lists-element-type`
- `a-module-variable-started-at-a-contract-no-claim-names-its-type-for-refuses`
- `a-module-variable-started-by-a-cast-holds-the-casts-type`
- `a-module-variable-started-by-a-cast-to-a-nullable-takes-null`
- `a-module-variable-started-with-a-const-closure-takes-one-that-runs`
- `a-module-variable-starting-empty-without-a-type-refuses`
- `a-module-variable-writing-no-type-holds-a-procedure-without-what-its-start-fails-with`
- `a-name-declared-as-both-a-constant-and-a-variable-refuses`
- `a-result-written-as-null-refuses`
- `a-send-is-a-declared-spelling-or-an-import`
- `a-struct-literal-written-into-a-module-variable-declaring-a-struct-takes-the-name-answers`
- `a-variable-start-reading-another-variable-refuses`
- `a-version-that-never-existed-refuses`
- `a-write-into-a-module-variable-is-judged-against-the-type-it-declares-refuses`
- `an-access-written-as-what-its-absence-means-refuses`
- `an-else-written-empty-refuses`
- `an-import-of-a-claim-no-document-makes-refuses`
- `an-import-of-a-claim-the-language-makes-refuses`
- `an-import-of-a-claim-two-documents-make-refuses`
- `an-import-written-as-neither-a-name-nor-a-claim-refuses`
- `an-overstated-imports-list-refuses`
- `an-unknown-key-refuses`
- `an-untruthful-imports-list-refuses`
- `claims-written-out-of-order-refuse`
- `constants-settle-in-the-order-they-read-each-other`
- `constants-that-name-each-other-refuse`
- `imports-written-out-of-order-refuse`
- `modifiers-written-in-another-order-refuse`
- `names-joined-with-and-out-of-order-refuse`
- `what-a-document-says-for-a-reader-is-carried`
