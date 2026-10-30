# The document format

What a document is: the dictionary a program travels as, and the module it declares. This page is the outline. What each of its slots holds is [procedures](PROCEDURE.md), [statements](STATEMENT.md), [expressions](EXPRESSION.md) and [types](TYPE.md), and the bytes it arrives as are [encodings](ENCODING.md).

A document is one dictionary. Every dictionary this grammar names, on this page and on the pages it points to, is keyed by names, strings in normal form C with something in it, and is **closed**: a key that is no name, and a key none of them names, **refuse at the load**. Every slot marked *expression*, *statements* or *type* takes the grammar of that name.

## The module

| key | takes | required |
|---|---|---|
| `warp` | int. The language version this document is written for | yes |
| `imports` | array of strings. Every name the program uses and does not declare: the procedures it sends, and the types and contracts it names; and the claims of other documents it stands on, each written as the type and the contract it is about | yes, and empty where the program uses none |
| `types` | dictionary: name → `{ struct: { field: type, … }, typeParameters?, satisfies?, types?, procedures? }` for a struct, its fields, the type parameters it takes in order, each beside its bound where it has one, `"K: Hashable"`, the contracts it adopts, its type members, which an [object](OBJECT.md) writes under `typeMembers`, and its members, or a type, which the name is then a second spelling of, under [types](TYPE.md) | no |
| `contracts` | dictionary: name → `{ types?, procedures? }`: the types the contract asks, an array of names, each beside what holds it where something does, `"Item: Hashable"`, none listed twice, and dictionary: procedure → `{ parameters, returns?, failing?, const?, isolated? }`, written the way a declaration's are under [procedures](PROCEDURE.md), an empty dictionary for a contract asking nothing; the procedure takes `Self` first, so one leaving `parameters` out **refuses at the load**, and writes no bound and no `sameTypes`, so one writing them **refuses at the load**, under [types](TYPE.md); what it says, it asks of every declaration satisfying it | no |
| `extensions` | dictionary: head → `{ satisfies?, types?, procedures? }`: what the document gives a type under a head, a type's name or the type applied to what its brackets hold, `Array<Int>`, `App.Box<some T: Hashable>`, the contracts the type adopts under the head, the type's type members and its members, under [types](TYPE.md) | no |
| `const` | dictionary: name → expression; a constant may read the constants beside it, and constants that read each other back have no order to fold in and **refuse at the load** | no |
| `var` | dictionary: name → expression, or `{ type, value }` where the variable says what it holds; a variable every procedure beside it may read and write | no |
| `procedures` | dictionary: name → procedure | no |

**A module variable.** Its start is written like a constant and folds the same way: at the **build**, from what a constant folds from, beside the constants and reading them, and them only: a start that reads another variable **refuses at the load**. Its type is what it declares under `type`, and where it declares none, the type its start reads as (a cast's type where a cast is written there, and where it reads a constant, the type its place in the constant's type has, under *a constant-headed path* in [expressions](EXPRESSION.md)), with every procedure it holds read without the constness, isolation or failing its type says, since a write may put another procedure there; a start the declared type does not take **refuses at the build**, and every write into it is judged against that type. A start that reads as an empty collection says nothing about what the box will hold, so a variable that declares no type and whose start reads as an empty list or dictionary, at whatever depth and under no cast, **refuses at the build**. It is private to the document like a constant, as a procedure written `private` is under [procedures](PROCEDURE.md), read by the same spelling (`ref`), and written by a `set` in a procedure the document declares, or through a parameter such a procedure hands it to in place; another document reaches it only through such a procedure. A name is a constant or a variable, not both: one declared under both keys **refuses** at the load. Either may be spelled like a procedure: a reference reads the constant or the variable, and a call names the procedure. Every run starts each variable at its folded value, so two runs of one image never see each other.

**The version.** Every document says it, and one that does not **refuses at the load**, as not a document rather than as a malformed one.

The current version is **1**. A reader reads the version it implements and **refuses** any other, before judging the document's keys. A document for an earlier version is written again: a document is spelled the way the writer of its version spells it, so one written for another version is another text. The number goes up when anything portable changes what an existing program *means*: a type added, a type read differently, a checking rule moved, a standard procedure returning differently. It does not move when a procedure is *added*, since a program that does not call it cannot tell, and one that does is refused by name.

An implementation implements the **current** version only.

**Note.** A reader that filled in a missing version would be deciding, on the sender's behalf, the one question that has to be decided from the bytes alone, and a file of some other kind would get as far as having its keys judged. A later version may add keys, and checking the keys first would turn "I am too old for this" into "this is malformed". A document written for another version is refused as that, rather than read by rules it was not written to and run to a different result.

**The imports list.** Every name the program *uses* and does not itself declare, each by its declared spelling: `Standard.Numeric.plus`, never `plus`. Two kinds of name are in it, and they are the two kinds a link resolves. The procedures the program sends, from procedure bodies, from constants and from a variable's start alike; and the types and contracts it names, in a declaration, a bound, a local binding, a cast, a closure's signature, an extension or a claim. The sends a native procedure declares are in it too. What a body sends is read off its text; a module the host assembled in its own language holds procedures with no text a reader could read, so each declares the procedures it sends and those count the same.

The list holds spellings and not kinds: a spelling in it asks for whatever the link declares under it, so a program using the procedure and the type of one spelling lists it once. The list is that set exactly, not a bound around it: **reading refuses** a document whose list disagrees with what its program uses, in either direction. It refuses at the load, since what a program uses is a fact of its text alone. The list is read before the program: the host lays the link from it, whatever kind each spelling turns out to declare, so a list saying less would be trusted and wrong, and a list saying more asks for what the program has no use for.

**A claim among the imports.** A claim declares no name, so a document stands on a claim another document makes by writing the pair the claim is about, the type's name and the contract's with a colon and a space between: `"T.Card: App.Describable"`. What it stands on is what its build asks a contract of, under [types](TYPE.md): a claim made in a document it stands on is within its reach already, and one made in a document it does not stand on is reached this way alone. Which claims a document asks of is its build's, not its text's, so a claim among the imports is not held to the program's use as a name is. An import naming a claim the document makes itself or one the language makes, one written as neither a name nor a pair, and one written as a pair whose halves are no type's name and no contract's **refuse at the load**, and one naming a claim no document in the link makes **refuses at the build**. What a claim imported brings is under *a document stands on* in [types](TYPE.md).

**A module asks and does not carry.** What the list names is supplied by whatever else stands in the link, and a module that shipped its own copy of a bundle it uses would put that bundle's declarations in the link twice, which the build refuses by the rule that one name has one declarer. Which modules are in a link is decided where the link is assembled. The same holds for the types and contracts a signature mentions: the list names them, and what declares them is still the link's to bring.

A document says its list, and one that does not **refuses at the load**, the way one that does not say its version does: the list is read before the program and the link is laid from it, so a reader with no list cannot tell a program that uses nothing from one that uses everything, and the empty list is what says the first.

## A document says each thing one way

A program has one document. Reading **refuses at the load** a document that says what it says another way, so a document that has been read and written is the document that was read, and one program never stands under two identities. A writer gives each program its one document by these rules; every other rule of form is the grammar's, on the page that writes it.

- **What its absence says is not written.** A key a document may leave out is left out where it would say what its absence says: `access` where it would be `internal`, `const` and `isolated` where they would be `false`, `returns` where it would be `Null`, a parameter's `type` where it would be `Any`, and a `var` statement's `value` where it would be `null`, under [statements](STATEMENT.md). So is a key that would hold an empty list or an empty dictionary: a signature's `parameters`, `failing`, `bounds` and `sameTypes`, a call's `arguments`, a procedure's `body`, a conditional's `else`, a struct's `typeParameters`, `satisfies`, `types` and `procedures`, a contract's `types` and `procedures`, an extension's keys, and the document's own `const`, `var`, `types`, `contracts`, `extensions` and `procedures`; an extension giving nothing is not written, under *members* in [types](TYPE.md). `imports` is written whatever it holds, under *the imports list* above.
- **A list the document keeps in name order is written in it**, names compared by their bytes: `imports`, names and claims together, `satisfies`, `failing` and a contract's `types`. Every other list keeps the order it is written in, since the order is what it says: `parameters`, `arguments`, statements, a struct's `typeParameters`.
- **What is given a struct the document declares is written in its declaration**, under *members* in [types](TYPE.md).
- **A bound stands where the name it bounds is introduced**, under *bounds* in [types](TYPE.md).
- **A statement writes its expression under `value`**, a construct there as a mapping of its one key, `{ value: { loop: … } }`, beside its binding and the `type` it declares, under [statements](STATEMENT.md). A `break` or `continue` names no loop where it ends the nearest one, under *the constructs* there.
- **A type and a path are written in their one spelling**: a type under *how a type is written* in [types](TYPE.md), an extension's key as its head's type is, and a path under [expressions](EXPRESSION.md).

## Cases

What `conformance/` asks about this page, by the name each case's file carries.

- `a-body-written-empty-refuses`
- `a-claim-import-whose-type-is-no-types-name-refuses`
- `a-constant-closure-may-name-its-documents-own-type`
- `a-constant-folded-to-a-some-of-a-none-reads-as-the-optional-it-was-judged`
- `a-constant-is-a-name-a-body-reads`
- `a-constant-may-be-spelled-like-a-procedure`
- `a-constant-reading-other-than-a-constant-refuses`
- `a-contracts-types-written-empty-refuse`
- `a-contracts-types-written-out-of-order-refuse`
- `a-document-declaring-no-procedure-stands-beside-one-that-names-it`
- `a-document-importing-a-claim-it-makes-refuses`
- `a-document-key-written-empty-refuses`
- `a-document-that-says-no-version-refuses`
- `a-document-without-imports-refuses`
- `a-field-read-names-no-type`
- `a-later-document-refuses`
- `a-list-leaving-out-a-type-the-program-names-refuses`
- `a-mapping-keyed-by-what-is-no-name-refuses`
- `a-modifier-written-twice-refuses`
- `a-module-variable-closure-called-with-another-count-refuses`
- `a-module-variable-closure-may-name-its-documents-own-type`
- `a-module-variable-declares-what-it-holds`
- `a-module-variable-handed-in-place-is-one-box`
- `a-module-variable-is-handed-in-place-to-a-standard-procedure`
- `a-module-variable-is-shared-by-the-procedures-beside-it`
- `a-module-variable-named-from-another-document-refuses`
- `a-module-variable-start-outside-its-declared-type-refuses`
- `a-module-variable-started-as-null-cast-to-an-optional-takes-a-value`
- `a-module-variable-started-at-a-constants-element-holds-the-lists-element-type`
- `a-module-variable-started-at-a-contract-no-claim-names-its-type-for-refuses`
- `a-module-variable-started-by-a-cast-holds-the-casts-type`
- `a-module-variable-started-by-a-cast-to-an-optional-takes-null`
- `a-module-variable-started-with-a-const-closure-takes-one-that-runs`
- `a-module-variable-starting-empty-without-a-type-refuses`
- `a-module-variable-writing-no-type-holds-a-procedure-without-what-its-start-fails-with`
- `a-name-declared-as-both-a-constant-and-a-variable-refuses`
- `a-send-neither-declared-nor-imported-refuses`
- `a-struct-literal-written-into-a-module-variable-declaring-a-struct-takes-the-name`
- `a-variable-start-reading-another-variable-refuses`
- `a-version-that-never-existed-refuses`
- `a-write-into-a-module-variable-is-judged-against-the-type-it-declares-refuses`
- `a-write-of-another-type-into-a-module-variable-refuses`
- `an-access-written-as-what-its-absence-means-refuses`
- `an-else-written-empty-refuses`
- `an-extension-giving-nothing-refuses`
- `an-import-of-a-claim-no-document-makes-refuses`
- `an-import-of-a-claim-the-language-makes-refuses`
- `an-import-of-a-claim-two-documents-make`
- `an-import-written-as-neither-a-name-nor-a-claim-refuses`
- `an-overstated-imports-list-refuses`
- `an-unknown-key-refuses`
- `an-untruthful-imports-list-refuses`
- `arguments-written-empty-refuse`
- `bounds-written-empty-refuse`
- `claims-written-out-of-order-refuse`
- `constants-fold-in-the-order-they-read-each-other`
- `constants-that-name-each-other-refuse`
- `failures-written-out-of-order-refuse`
- `imports-written-out-of-order-refuse`
- `modifiers-written-in-another-order-refuse`
- `names-joined-with-and-out-of-order-refuse`
- `parameters-written-empty-refuse`
- `same-types-written-empty-refuse`
- `satisfies-written-empty-refuses`
