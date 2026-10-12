# Types

What a name may stand for, and what a slot takes. A type is judged at the build against the declarations the grammar read; what a type *admits* is asked of a value at a boundary, which is sometimes the build and sometimes the run. Reads [the value model](value.md). Read by procedures, statements and expressions, each of which writes a slot.

A type is written as a string, or as a mapping for what a string cannot say:

| written | means |
|---|---|
| `Null` `Bool` `Int` `Double` `String` | the scalar types |
| `Any` | anything |
| `Never` | never answers. The type `Standard.Control.abort` declares, and what makes a leaving call checkable |
| `Array<T>` / `Dictionary<K, V>` | a list of `T` / a map from keys of `K` to values of `V`, `K` a type that answers `Hashable`; `Array<Any>` is a list of anything, and `Array` or `Dictionary` written bare, or with another count of types, **refuses at the load** |
| `Procedure` | some procedure, signature unsaid: a value of it stands where `Procedure` or `Any` is declared, and is called, or handed where a procedure type is written, only once a cast says what procedure it is |
| `const <procedure type>` | a procedure that answers without running, under *what answers without running* in [procedures](procedure.md) |
| `isolated <procedure type>` | a procedure that touches no name another body could touch at once; `const isolated <procedure type>` says both, `const` first |
| `inout <type>` | a parameter handed a variable in place; written on a parameter's type and nowhere else |
| `var <type>` | a field a path may write through; written on a field of a record a type in `types` declares, and nowhere else |
| `Task` (any declared name) | the type a module declares under that name |
| `some T` | a type parameter: worked out from the call, same reading everywhere it appears; bounded when the signature's `bounds` names it |
| `Self` | the type answering a contract, written in that contract's procedures alone |
| `Describable` (a declared contract's name) | a value of whatever type satisfies the contract. Nothing ties one slot's to another's |
| `Describable & Standard.Comparable` | a value of whatever type satisfies every contract named; two names or more, in name order, and each a contract's |
| `Int?` (any string spelling and `?`) | the declared type or null |
| `{ procedure: { parameters: [<type>, …], returns: … } }` | a procedure type: the types it is called with, in position order, and what it answers. No names, since a name is a declaration's and a value is called by position; a mark such as `inout` is written on the type it stands in front of |
| `{ "const procedure": { … } }` | a procedure type with its marks and modifiers on the key, `inout` first, then `const` and `isolated`, the way they stand in front of the string form |
| `{ array: <type> }` / `{ dictionary: { key: <type>, value: <type> } }` | a list / map of a procedure type that writes its signature, which has no string spelling. Where every type inside has a spelling the type is written `Array<T>` or `Dictionary<K, V>`, and the form around it **refuses at the load** |

`Int` and `Double` are two types, and neither takes the other: a value's type is fixed at the build, so a whole number never stands where a fraction is declared, and the reverse **refuses at the build** too. A literal is read as the place it is written into reads it, where a place is a slot, an answer, a name that says what it holds, a write, a list's, a map's or a record's part there, what stands between a path's brackets, which reads an `Int` on a list and the key type on a map, and the type a cast, `as` or `as?`, names. A whole number written as a literal is read as the fraction it names where its place declares a `Double`, and at a parameter a call fills beside a fraction, which is what that parameter's bounds are held to. Where one value joins what was written beside it, a list literal's elements at every depth and a map literal's keys and its values, a whole literal beside a fraction is the fraction it names too. Anywhere else it is an `Int`, and a name it is bound to holds an `Int`. Two readings of one place join part by part: null beside a value reads as what may be null, two lists join by their elements and two maps by their keys and their values, and two procedures to a procedure that keeps the parameters and answer both write alike and the constness and isolation both carry; two parts that still differ read `Any`. Where ways that each answer meet, each way out of a body that writes no `returns` and each of an attempt's two ways is a place of its own, so one answering a whole literal beside another answering a fraction reads `Any`, which a slot of a type takes only through a cast. `Any` accepts everything. A slot that takes either kind of number is bounded by the contract `Standard.Numeric`, under [the standard vocabulary](vocabulary.md).

**A declared record is nominal.** A record type is written once, as the structure of a type declared in `types`, `{ record: { title: String, done: Bool } }` under the type's name, its fields under `record`, each called anything; everywhere else a type names it. It is a name as well as a structure, and a value of it carries the name. A record type is exact: a declared record fits a value under its own name and no other, so two declared records of one structure under two names are two types, and a declared record and `Dictionary<String, T>` of its fields take nothing of each other. A slot judges a value and hands it on as it came; it does not rebuild one. A record literal is read, as every literal is, as the place it is written into reads it: the declared record that place reads. The build judges it there field by field against the declaration, exactly the declared fields, and it takes the record's name. A record literal written where no declared record is read, at `Any`, at a contract, at a type parameter or at a name that declares nothing, **refuses at the build**. A record under another name **refuses** at the **build** where the build can see the name and at the **run** at the door it comes through, and where a cast reads a value read as `Any` or as a contract, the cast fails with `cast_refused` and `as?` reads it as null. A declared name whose structure is not a record, an alias, attaches no name. A value from outside holds a name only as a record's: at every door, whatever the slot declares, `Any` included, a record under a name is held to the record the name declares, fitted to it and judged against it, an alias's name becoming its record's, and one under a name that declares no record **refuses at the run**, and so does a map at a declared record, which takes no map. So every record under a name is a value of that record. A declared record may name itself in a field, nullable or as a list's element, so a tree is one declaration. A declared name that is no record and comes back to itself through what it stands for, through names alone, a `?` or a structure, spells no type and **refuses at the load**: a type that holds itself is a declared record.

`inout` and `var` stand in front of the whole type, `?` included: `inout Int?` is a nullable handed in place. They stand in front of a string spelling or on the key a procedure type is written under. They say something about the slot and nothing about the value, so what fits the slot is judged by the type after the procedure. Writing either where it is not allowed **refuses at the load**. A slot asking `isolated` takes what the build derived as isolated. Answering without running is a separate claim and does not stand in for it. A value standing in a procedure-typed slot takes exactly the positions the slot's type hands, each accepting what the slot may hand at that position, and answers what the slot's `returns` accepts. The names the value's declaration wrote are its own and take no part: one closure fits two slots that name their parameter differently. That is held at the **build** where the value's type is known, and at the **run** where a cast reads a value read as `Any` or as a contract, under *one calling convention* in [procedures](procedure.md).

**What a slot takes, exactly.** Where a value meets a declaration (an argument, an answer, and a write into a box that said what it holds), the judgement is one rule per type:

- `Any` passes the value through untouched, null and procedures included. Nothing is judged, because nothing was declared, beyond what every door holds of a record's name, under *a declared record is nominal* above.
- A value read as `Any`, as a contract, or along a path a call decides through a type parameter is of a type the build does not know. It stands where `Any` is declared and where a call fills a type parameter no bound holds, and a value read as a contract stands where a contract it is read as is asked, a bound among them; anywhere else it **refuses at the build**, and a cast says what it is. An empty list or map reads as holding `Never`: it holds no element, so it is a value of a list or a map of any type.
- A **declared record** says which fields there are, and a record under its name fits only with exactly them: one short and one over both **refuse**, each field is judged against its type, and the value is held as it came. To hand on fewer fields, write a record literal of another declared record; to keep keys a declaration does not name, declare `Dictionary<String, T>`, where the keys are the value's own. The door a value from outside comes through is the one place a value is fitted: a field the declaration never named is left out of a record under its name there, at whatever depth a record, a list, a map or what may be null holds it.
- A **declared name** whose structure is not a record is an alias, a second spelling of what it stands for: the build reads every mention of it as that type, so it takes, joins and answers wherever that type does. One whose structure is a record is nominal, under *a declared record is nominal* above.
- A **nullable** (`T?`) passes null through and judges anything else against the declared half. `T?` takes `T`, null and `T?`; a `T?` reading does not fit a plain `T` slot. The `?` is written once, on the whole spelling, and only where it says something new: `Int??`, `Null?`, `Any?`, `Never?` and `some T?` each **refuse at the load**, and the same `?` behind a declared name standing for one of them **refuses at the build**, where the name resolves. A procedure type that writes its signature has no string spelling and no `?` to trail; a nullable one is reached through a declared name.
- The numeric edge is value-independent: `Int` refuses every fraction, `2.0` included, and `Double` every whole number. A literal read as a fraction names the binary64 fraction nearest it, so digits past 2^53 round as binary64 rounds.

`Never` is a real type and fits **every** slot, by never arriving: an expression typed `Never` may be written where any value is expected, such as an argument that calls `Standard.Control.abort`, and evaluating it ends the evaluation it is inside. The statement rules (no name, nothing follows) are statement rules.

**Type parameters.** A declaration may leave a type parameter and let the call fill it: a procedure taking `Array<some T>` and a `some T` answers what it was given. Inside the declaration the parameter is one type its body does not know, so every place there that reads it takes only a value of it: the answer, a write into a variable of it or into a part of one, a parameter handed in place, and an argument at a slot a call fills from it. A reading of `Any` or of a contract, and a value of a type the bounds hold, is no value of the parameter, and each **refuses at the build**; a call reads the answer as what filled the parameter. A procedure handed to the call is a value, and what it takes at a position is what it accepts there, not a value the call hands: where anything else handed fills a parameter, the procedure is judged against what filled it, by the rule a procedure-typed slot takes a value, and only where nothing else fills it does what the procedure takes fill it, so a closure whose parameter writes no type, handed to `filter` beside a list of `Int`, leaves `Element` `Int`. Two positions of procedures taking it as two types, one of which takes the other, fill it with the one both take: `(Int) -> Int` beside a closure whose parameter writes no type fills it with `Int`. The run does not know what filled it either, so a closure the body wrote that names the parameter in its own signature is, outside the call that made it, a value of no procedure type that writes a signature, and a value of `Procedure`, which writes none: a door handing one in at such a type **refuses at the run**, and a cast reading one as such a type fails with `cast_refused`. A list or map literal written there is judged part by part, each element, key or value against what the slot asks at it, and an empty list holds no element wherever in the literal it stands: `[]` is a value of `Array<some T>`, `[[], [x]]` of `Array<Array<some T>>` where `x` is one of `some T`, and a list of two map literals, one holding `[]` under `a` and one holding `[x]` under `b`, of `Array<Dictionary<String, Array<some T>>>`. A call reads a literal handed to it as one type to fill a parameter, its parts joined part by part, and handed beside such a parameter it is then judged part by part as a write is. A map literal handed where a dictionary of the parameter is declared fills it with what each of its values reads it as, joined part by part as a list's elements are, an empty one holding no entry, and each value is held where it stands. Where bounds hold the parameter, only what stands at the parameter in a literal handed there is held to them, what a name the literal holds reads as included, and a closure in the literal is judged as any closure handed to its procedure type is. A parameter read twice must be read the same both ways. Two readings where one accepts the other join to the one that holds both, position by position through lists, dictionaries and what may be null: a reading of `Any` makes its position `Any`, as it does the whole parameter, and elsewhere the looser stands; a reading that leaves, or an empty list's element, holds no value, and a parameter only such readings read is filled with `Never`, so `[]` handed at `Array<some T>` answers a list of any type, and a call answering that parameter alone reads `Never` and takes no name, the way a call of `Standard.Control.abort` does; two readings that do not fit **refuse at the build**, and do not widen to `Any`: two declared records, or a declared record and a map, are two types neither of which takes the other. Where bounds hold the parameter, what each argument hands there is held to them before its readings are joined, so a reading among them that does not answer **refuses at the build**, and so does a parameter the readings fill with `Any`, though each answers: a bounded parameter is one type. Appending a whole number to a list of text is a parameter read as text and as a number, and there is no answer that is both.

**Bounds.** A type parameter may be bounded: a signature declares `bounds: { T: Standard.Comparable }` once, its slots write `some T`, and every occurrence of the name takes only what answers the contract the bound names, under **Contracts** below. A bound may name several, joined with `&`: `bounds: { T: Describable & Standard.Comparable }` holds `T` to what answers every one of them. The signature owns the bound. A slot names the parameter and never the bound, so one bound is one claim however many slots mention the name. A bound names contracts and nothing else, and what answers one is whatever type a document claims does, so the set a bound holds a parameter to is open. The judgement is the **build**'s: a reading whose type does not answer the bound refuses (two booleans meeting `lessThan` never run), and so does a reading whose type the build does not know, under *what a slot takes, exactly* above; a cast judges what actually arrived at the **run** by the type it is an instance of. `bounds` naming a parameter no slot mentions refuses at the load. Only the declaring procedure writes `bounds`, and a closure writes none, under [expressions](expression.md). A procedure *type* nested in a slot carries none, because its parameters are the declaring signature's own slots and the declaring signature owns their bounds. A closure written in the body reads the same names: its `some T` is the `T` the caller filled, held to the bounds the declaration wrote, so a closure may send what the body around it may, and one writing a `some T` the procedure around it does not declare, or written where no procedure is, **refuses at the load**. A bound naming what no module declares as a contract **refuses at the build**, and one naming a type the language names, which is no contract, **refuses at the load**. And a type parameter lives in a signature and is filled by what a call hands: a declared type writing `some` outside a procedure signature, and a signature naming one in what it answers and at none of its parameters, at any depth of a procedure-typed one included, each **refuse at the load**, because nothing there is filled by a call.

**Contracts.** A contract says which **procedures** a value answers: the types that answer them are open, and new ones arrive with new documents. A module declares one the way it declares a type: a name bound to the procedures, each written as a signature whose first parameter is `Self`, the type that answers the contract, since the value standing there is the one the procedure is answered about. `Self` may stand at any of the procedure's positions and in its answer, `Self?` included, and it is that one type wherever it stands: a claim reads it as the type the claim is about, and `Self?` as that type or null, which for a claim about `Null` is `Null` itself, so a declaration backing such a claim writes `Null` there, at a parameter as in its answer, and a call through the contract reads it as one type parameter the contract bounds, filled from the call the way any type parameter is. A contract's procedure taking anything else first **refuses at the load**, the contract's own name included, since that is a value of whichever type answers it, and so does one taking `inout Self` first, since a call through the contract picks the declaration by the value standing there and a place handed in is no value. `Self` written anywhere but a contract's procedures **refuses at the load**, and so does `some Self`.

A contract's name stands where a type is written, and so does `A & B`: the slot takes a value of whatever type satisfies every contract named. This is how the language says **A or B**: each type claims one contract and the slot names it. Either is a type parameter with no name, so nothing ties one slot's reading to another's, and a call fills nothing. A value read as a contract is of a type the build does not know and stands where *what a slot takes, exactly* above says: a value read as `A` does not stand where `B` is asked, and one read as `A & B` stands where either is. A reading of what may be null is a value of the type or of `Null`, so it answers a contract where both do. A type parameter a contract bounds is one type wherever it stands, while a value of a contract is of whichever type answers it and a value of what may be null of the type or `Null`, so either fills one only where the parameter stands alone at one of the procedure's positions: `App.Described.describe` takes one, and a call handing one where the parameter stands twice, `Self` of `lhs` and `rhs` included, or inside a list or a map, **refuses at the build**. A closure literal's parameter is such a slot too, and a call of the value holds what it hands to the contract by the rule a call to a declaration is held by. A name that is not a contract's joined with `&` **refuses at the build**, and a type the language names joined with `&` **refuses at the load**.

A type **satisfies** a contract when a document says it does. The document writes the claim under `satisfies`, keyed by the type: `satisfies: { "Bank.Account": ["App.Describable"] }`. Any document may make one, about a type it declared or about another document's, which is how a document that arrives later gives a type the procedures a contract asks. A type the language names is a type the way a declared one is, and a claim may be about it: `satisfies: { Int: ["App.Describable"] }`, answered by `Int.describe`. A list and a map are named bare, `Array` and `Dictionary`. Every list is an instance of `Array` whatever it holds, since a value does not say which elements a slot declared it to hold, and a claim written about `Array<Int>` **refuses at the load**. A claim about `Array` is a claim about every list, and one about `Dictionary` about every map, so a declaration answering it takes one whatever it holds, a map under whatever keys, `Dictionary<some K, Any>` with `bounds: { K: Hashable }`: a claim answered by one taking `Array<Int>` or `Dictionary<String, Any>` alone does not hold, and a call leaning on it **refuses at the build**. A list written as bytes is an instance of `Array` as every list is. `Any` and `Never` are types no value is an instance of by name, `Procedure` and a procedure type name a structure and no type, and `Self` names a type only inside a contract's procedures, so a claim about any of them **refuses at the load**, and a procedure answers no contract. A claim about a declared name that is not itself a record, an alias included, **refuses at the build**: a value of a declared type is an instance of the record it is, and of no other name.

The build holds the claim to the declarations behind it. For every procedure the contract asks, it takes the declaration named for the type and that procedure (`Bank.Account` and `describe` give `Bank.Account.describe`) and holds its signature to the contract's with the type in place of `Self` wherever the contract writes it. A name that stands for a declared record names that record's type there, as wherever types are compared, so a declaration may write another name for the record the contract writes. A declaration that wrote no `returns` is held by what its body answers, read the way a call site reads it.

Whether a type answers a contract is therefore a fact of the whole list, and a claim may be written in a document the one leaning on it never names. A document handing a type where a contract is asked is not judged where it is compiled: the pair leaves the compile unresolved, the way a procedure the document sends and does not declare leaves it, and **refuses at the call that leaned on it** where the build cannot answer. A claim missing a procedure, or holding one whose signature does not fit, puts its type under no contract and its reason is what that refusal says.

A claim whose two names the list declares as something other than what the claim needs of them **refuses at the build, at the claim**: a contract where the type belongs, or a type where the contract belongs. One name has one declarer, so no document arriving later makes that right. A name the list declares as nothing at all waits with the rest: the claim holds nothing, and that is refused only **where a call leaned on the pair**, with the reason the claim came to nothing. A claim nobody leans on refuses nowhere.

Two documents claiming one pair are one claim: a claim holds nothing but the pair, so the second says what the first said.

A declaration named for a type and a procedure that no claim names is that document's procedure and nothing else. So what a link declares never decides what an unrelated document may call things, and a document that names no contract builds the same whichever documents stand beside it.

A contract may ask no procedures. It is then a mark a claim gives a type, and a type answers it where a document claims it does, as for any contract.

**What the language declares.** The language declares three names itself, which stand in every link ahead of its documents: the contract `Hashable` below, and the records `Failure`, which a rescue binds, and `Round`, which a loop binds, under [statements](statement.md). No document declares one of them, and a mention of one, in a slot, a bound, a cast or a claim, is that declaration.

**A map's key.** The language declares one contract, `Hashable`, which asks no procedures and which the key of every map type answers. The language claims it for `Null`, `Bool`, `Int`, `Double`, `String`, `Array` and `Dictionary`, and a declared record answers it where a document claims it does: `satisfies: { "App.Point": ["Hashable"] }`. Which keys are one key is the value model's sameness, under [the value model](value.md), and no procedure decides it. A map type whose key does not answer `Hashable`, `Any`, a procedure type or a type parameter its bounds do not hold to it among them, **refuses at the build** where it is written, reached or not, and one whose key leans on a claim refuses where the link cannot answer it, under the rule above.

A body calls a contract's procedure by writing the contract's name and the procedure's with a dot between them: `App.Describable.describe`. That spelling is the contract's declaration of the procedure, and it is a send like any other: a document calling a contract another module declares lists the spelling in `imports`. It names no type's declaration, and what it means is decided by the value at its first position, so a call writing nothing there **refuses at the build**. What a call hands it and what it answers are the contract's, not any one declaration's.

**The build builds the table and the run reads it.** For every contract, the build gathers every type that satisfies it and lowers one call per type, each against the row that answers, arguments in that row's own slot order. The run reads the type the first argument is an instance of and picks. Nothing is resolved while a program is running.

A declaration answering a contract's procedure is reached **through the contract**, which is the spelling that says which contract is meant. Two types answering one procedure is the ordinary case. Such a declaration takes exactly the contract's positions and answers what the contract's answer takes: its own type first, then **at the contract's positions** a parameter taking everything the contract's takes there and taking a place only where the contract hands one, the contract's type parameters standing for types no call fills and the declaration's own filled by what the contract writes at the same positions; the names are its own. One declaring a parameter beyond them, `T?` included, **refuses at the build** where the claim is leaned on. The run hands the arguments to the same positions whichever declaration answers.

**A name is its declared spelling.** The key a document declares a type, contract or procedure under is the whole of its name: `Standard.Math.floored` is declared under that key, and `Wallet.Account` under that one. A mention is a declared spelling, written out, and it means the same declaration wherever it was written, inside the declaring document too. A dot is a character of the spelling and nothing more: the language has no nesting, no scope and no prefix, so what a document chooses to put before a dot is the author's convention, and one document may declare `Wallet.fee` beside `Bank.rate` while another declares `Wallet.rate`. A spelling no module in the link declares **refuses at the build** where it is mentioned. There are two namespaces, procedures and types, and a procedure may be spelled like a type. A contract's procedure stands in the first under its dotted spelling, which names one contract's procedure by the grammar in [checking](checking.md), and a procedure a document declares under that same spelling **refuses at the build**. Types and contracts share the second, and no name in it is both, so a mention reaches whatever declares it: a slot names a type or a contract, and a bound names a contract. Every name in the second, declared or mentioned, holds a type's name grammar, and a type parameter's name its own, under [checking](checking.md): a document declares no type under `Int` and names no type parameter `Int`, a mention spelled `a b` **refuses at the load**, and a mention of `Int` is the type the language names.

The shared `Standard` bundle declares the contracts the standard procedures are bounded by, `Standard.Numeric`, `Standard.Comparable` and `Standard.Collection`, claims them for the types the language names (`Int` and `Double` are numbers that order, `String` orders and has a count, `Array` and `Dictionary` have a count) and declares the procedures answering them, `Int.plus` and the rest, under [the standard vocabulary](vocabulary.md). A bundle whose signatures mention them links with `Standard` in the build.

## Cases

What `conformance/` asks about this page, by the name each case's file carries.

- `a-bare-array-refuses`
- `a-bare-contract-name-refuses`
- `a-bare-dictionary-refuses`
- `a-bare-name-for-another-modules-procedure-refuses`
- `a-body-answering-a-value-for-its-own-type-parameter-refuses`
- `a-body-answering-a-whole-literal-one-way-and-a-fraction-another-is-no-fraction-refuses`
- `a-body-handing-its-own-type-parameter-in-place-to-a-type-refuses`
- `a-body-writing-a-value-into-its-own-type-parameter-refuses`
- `a-bound-may-name-several-and-holds-to-every-one`
- `a-bound-names-a-contract-another-document-declares`
- `a-bound-naming-a-parameter-no-slot-mentions-refuses`
- `a-bounded-parameter-read-as-text-and-as-any-refuses`
- `a-call-filling-a-parameter-from-a-variable-held-in-place-takes-a-value-of-that-parameter`
- `a-call-filling-a-parameter-from-a-variable-held-in-place-takes-no-other-value-refuses`
- `a-call-filling-a-parameter-from-the-bodys-own-and-a-reading-of-any-refuses`
- `a-call-of-a-value-read-as-any-refuses`
- `a-call-through-a-contract-with-nothing-first-refuses`
- `a-cast-between-aliases-of-two-nullable-records-reads-null-answers`
- `a-cast-of-a-closure-appending-to-a-list-of-its-makers-parameter-fails`
- `a-cast-of-a-closure-over-a-type-parameter-its-making-call-filled-fails`
- `a-cast-of-a-closure-over-a-type-parameter-to-procedure-answers`
- `a-cast-of-a-closure-taking-a-list-of-its-makers-parameter-in-place-fails`
- `a-cast-of-a-closure-taking-its-makers-parameter-to-one-taking-in-place-fails`
- `a-cast-of-a-closure-writing-a-generic-answer-carried-through-another-fails`
- `a-cast-of-a-closure-writing-a-variable-handed-in-place-fails`
- `a-cast-of-a-closure-writing-an-answer-a-caller-appends-in-place-fails`
- `a-cast-of-a-closure-writing-an-answer-read-as-never-fails`
- `a-cast-of-a-closure-writing-an-unsaid-generic-answer-carried-through-another-fails`
- `a-cast-of-a-closure-writing-where-a-declared-record-was-filled-fails`
- `a-cast-of-a-nullable-record-to-another-record-refuses`
- `a-cast-of-a-setter-a-generic-procedure-made-fails-before-its-getter-reads`
- `a-cast-of-an-alias-of-a-nullable-record-to-another-record-refuses`
- `a-claim-about-a-list-of-one-type-refuses`
- `a-claim-about-a-name-that-is-not-a-record-refuses`
- `a-claim-about-any-refuses`
- `a-claim-about-array-answered-for-a-list-of-ints-alone-refuses`
- `a-claim-about-never-refuses`
- `a-claim-about-null-answers-null-where-the-contract-answers-self-or-null`
- `a-claim-about-null-is-answered-for-null`
- `a-claim-about-null-takes-a-list-of-null-where-the-contract-takes-a-list-of-self-or-null`
- `a-claim-about-null-takes-null-where-the-contract-takes-self-or-null`
- `a-claim-about-procedure-refuses`
- `a-claim-about-self-refuses`
- `a-claim-answering-self-or-null-with-another-type-refuses`
- `a-claim-naming-a-contract-where-the-type-belongs-refuses`
- `a-claim-naming-a-type-where-a-contract-belongs-refuses`
- `a-claim-nobody-leans-on-refuses-nowhere`
- `a-claim-stands-in-a-document-the-leaning-one-never-names`
- `a-closure-a-generic-body-wrote-is-read-as-the-procedure-type-it-is-judged-against`
- `a-closure-a-generic-body-wrote-read-past-its-bounds-is-not-that-type`
- `a-closure-a-generic-body-wrote-taking-a-list-in-place-is-read-as-the-type-it-is-judged-against`
- `a-closure-alone-fills-a-parameter-with-what-it-takes`
- `a-closure-inside-a-closure-reads-the-bounds-of-the-procedure-around-them`
- `a-closure-naming-a-type-parameter-its-procedure-does-not-declare-refuses`
- `a-closure-parameter-saying-nothing-takes-the-element-the-list-beside-it-fills`
- `a-closure-reads-the-bounds-of-the-procedure-around-it`
- `a-closure-taking-any-stands-where-its-slot-hands-a-contract`
- `a-closure-taking-anything-beside-a-declared-record-leaves-the-parameter-the-record`
- `a-closure-taking-int-beside-a-declared-record-refuses`
- `a-closure-writing-bounds-refuses`
- `a-closures-parameter-names-are-not-part-of-its-type`
- `a-contract-asking-no-procedures-is-answered-by-what-claims-it`
- `a-contract-asking-no-procedures-refuses-what-no-claim-names`
- `a-contract-carries-a-procedure-into-a-generic-body`
- `a-contract-declared-twice-refuses`
- `a-contract-declared-under-a-spelling-that-is-no-name-refuses`
- `a-contract-is-named-by-its-qualified-spelling`
- `a-contract-or-null-slot-refuses-a-type-not-answering-the-contract`
- `a-contract-or-null-slot-takes-a-parameter-bounded-by-the-contract-and-another`
- `a-contract-or-null-slot-takes-a-type-answering-the-contract`
- `a-contract-procedure-may-answer-self-or-null`
- `a-contract-procedure-may-take-self-or-null`
- `a-contract-procedure-named-with-a-dot-refuses`
- `a-contract-procedure-names-what-it-may-fail-with`
- `a-contract-procedure-takes-self-first`
- `a-contract-procedure-taking-self-in-place-first-refuses`
- `a-contract-procedure-taking-the-contract-first-refuses`
- `a-contract-slot-refuses-a-name-for-what-may-be-null-where-null-does-not-answer`
- `a-contract-slot-refuses-a-parameter-or-null-where-null-does-not-answer`
- `a-contract-slot-refuses-what-may-be-null-where-null-does-not-answer`
- `a-contract-slot-takes-what-may-be-null-where-both-answer`
- `a-contract-stands-in-a-closures-parameter`
- `a-contract-stands-in-a-declared-types-field`
- `a-contract-stands-where-a-type-is-written`
- `a-declaration-answering-a-contract-answering-any-may-answer-its-parameter`
- `a-declaration-answering-a-contract-failing-with-what-the-contract-does-not-name-refuses`
- `a-declaration-answering-a-contract-fills-its-own-parameter-with-the-contracts`
- `a-declaration-answering-a-contract-may-answer-a-contract-where-it-promises-it-or-null`
- `a-declaration-answering-a-contract-may-answer-a-type-answering-it-where-it-promises-it-or-null`
- `a-declaration-answering-a-contract-may-answer-an-alias-of-a-record-answering-it`
- `a-declaration-answering-a-contract-may-answer-an-alias-of-what-it-promises`
- `a-declaration-answering-a-contract-may-answer-another-contract-and-the-contract-where-it-promises-it-or-null`
- `a-declaration-answering-a-contract-may-fill-a-bounded-parameter-with-what-the-bound-takes`
- `a-declaration-answering-a-contract-may-take-a-contract-or-null-where-it-writes-the-contract`
- `a-declaration-answering-a-contract-may-take-a-value-where-it-hands-a-place`
- `a-declaration-answering-a-contract-may-take-a-wider-type`
- `a-declaration-answering-a-contract-may-take-any-where-it-writes-a-contract`
- `a-declaration-answering-a-contract-may-take-anything-where-it-writes-a-parameter`
- `a-declaration-answering-a-contract-may-write-another-name-for-the-record-the-contract-names`
- `a-declaration-answering-a-contract-names-its-parameters-its-own-way`
- `a-declaration-answering-a-contract-reading-a-bounded-parameter-beside-any-refuses`
- `a-declaration-answering-a-contract-takes-its-parameters-in-the-contracts-order`
- `a-declaration-answering-a-contract-takes-no-parameter-beyond-it`
- `a-declaration-answering-a-contract-takes-the-claimed-type-wherever-the-contract-writes-self-refuses`
- `a-declaration-answering-a-contract-taking-in-place-where-it-hands-a-value-refuses`
- `a-declaration-answering-a-contract-with-a-bounded-parameter-where-it-writes-a-parameter-refuses`
- `a-declaration-answering-a-contract-with-a-bounded-parameter-where-it-writes-what-the-bound-refuses-refuses`
- `a-declaration-answering-a-contract-with-a-contract-where-it-answers-another-refuses`
- `a-declaration-answering-a-contract-with-a-type-not-answering-it-where-it-promises-it-or-null-refuses`
- `a-declaration-answering-a-contract-with-a-type-where-it-writes-a-contract-refuses`
- `a-declaration-answering-a-contract-with-a-type-where-it-writes-a-parameter-refuses`
- `a-declaration-answering-a-contract-with-another-answer-refuses`
- `a-declaration-answering-a-contract-with-another-contract-where-it-writes-a-contract-refuses`
- `a-declaration-answering-a-contract-with-any-where-it-asks-text-refuses`
- `a-declaration-answering-a-contract-with-its-own-parameter-for-a-type-refuses`
- `a-declaration-answering-a-contract-with-what-may-be-null-where-it-answers-a-contract-refuses`
- `a-declaration-no-claim-names-is-its-documents-own-procedure`
- `a-declaration-writing-no-returns-backs-a-claim-by-what-its-body-answers`
- `a-declared-name-is-a-type`
- `a-declared-type-names-itself-in-its-fields`
- `a-dictionary-of-an-alias-of-any-at-a-dictionary-of-a-contract-refuses`
- `a-fraction-is-not-a-whole-number`
- `a-generic-answer-of-any-refuses`
- `a-generic-body-appends-its-parameter-to-a-list-of-it-or-null`
- `a-list-literal-of-closures-answering-outside-the-bounds-refuses`
- `a-list-literal-of-closures-handed-at-a-bounded-parameter-answers`
- `a-list-literal-of-names-holding-lists-handed-at-a-bounded-parameter-refuses`
- `a-list-of-a-reading-of-any-behind-a-name-handed-beside-a-variable-in-place-refuses`
- `a-list-of-a-reading-of-any-handed-beside-a-variable-in-place-refuses`
- `a-list-of-an-alias-of-any-handed-to-a-value-at-a-list-of-a-contract-refuses`
- `a-list-of-two-types-handed-where-a-contract-is-asked-is-read-element-by-element-refuses`
- `a-literal-of-names-at-a-contract-bound-leans-on-each-claim-refuses`
- `a-map-handed-through-a-claim-about-dictionary-reads-as-the-map-it-is-refuses`
- `a-map-keyed-by-a-declared-record-claimed-hashable-answers`
- `a-map-keyed-by-a-declared-record-no-document-claims-hashable-refuses`
- `a-map-keyed-by-a-type-parameter-bounded-by-hashable-answers`
- `a-map-keyed-by-a-type-parameter-no-bound-holds-refuses`
- `a-map-keyed-by-any-refuses`
- `a-map-keyed-by-lists-finds-a-list-by-its-elements`
- `a-map-keyed-by-what-may-be-null-holds-null-as-a-key`
- `a-map-literal-handed-at-a-dictionary-of-a-bounded-parameter-fills-it-by-its-values-refuses`
- `a-map-literal-handed-at-a-dictionary-of-a-contract-leans-on-each-claim-refuses`
- `a-map-literal-of-keys-of-two-types-handed-at-a-dictionary-of-a-bounded-key-refuses`
- `a-map-literal-of-values-of-two-types-handed-at-a-dictionary-of-a-bounded-parameter-refuses`
- `a-map-literal-reads-a-whole-key-beside-a-fraction-as-the-fraction`
- `a-map-literal-whose-values-do-not-join-handed-at-a-dictionary-of-a-bounded-parameter-refuses`
- `a-map-type-written-with-one-type-refuses`
- `a-module-declares-a-contract-a-bound-names`
- `a-name-declared-as-both-a-type-and-a-contract-refuses`
- `a-name-that-is-not-a-contracts-joined-with-and-refuses`
- `a-named-list-handed-where-a-list-of-a-contract-stands-is-held-to-it`
- `a-null-cast-to-a-contract-is-held-to-the-claims-about-null`
- `a-nullable-const-procedure-reads-as-written`
- `a-nullable-that-says-nothing-new-behind-a-name-refuses`
- `a-nullable-that-says-nothing-new-refuses`
- `a-parameter-filled-from-a-list-of-any-reads-any-which-a-cast-opens`
- `a-parameter-handed-in-place-handed-on-beside-a-list-of-an-empty-list-answers`
- `a-parameter-handed-in-place-handed-on-beside-an-empty-list-and-a-list-of-it-answers`
- `a-parameter-handed-in-place-handed-on-beside-an-empty-list-answers`
- `a-parameter-handed-in-place-handed-on-beside-maps-of-it-and-of-an-empty-list-answers`
- `a-parameter-handed-in-place-handed-on-to-a-generic-beside-an-empty-list-answers`
- `a-parameter-handed-in-place-holding-a-dictionary-of-a-parameter-takes-a-map-of-it`
- `a-parameter-handed-in-place-holding-a-dictionary-of-lists-of-a-parameter-takes-a-map-of-an-empty-list`
- `a-parameter-handed-in-place-holding-a-list-of-a-parameter-or-null-takes-a-list-of-it`
- `a-parameter-handed-in-place-holding-a-list-of-a-parameter-or-null-takes-null`
- `a-parameter-handed-in-place-holding-a-list-of-a-parameter-takes-an-empty-list`
- `a-parameter-handed-in-place-holding-a-procedure-of-a-parameter-takes-a-closure-of-it`
- `a-parameter-handed-in-place-holding-dictionaries-of-a-parameter-takes-maps-of-other-keys-of-it`
- `a-parameter-handed-in-place-holding-dictionaries-of-lists-of-a-parameter-takes-maps-of-an-empty-list-and-of-it`
- `a-parameter-handed-in-place-holding-dictionaries-of-lists-of-a-parameter-takes-maps-of-other-keys`
- `a-parameter-handed-in-place-holding-lists-of-a-parameter-refuses-an-attempt-whose-rescue-answers-a-number`
- `a-parameter-handed-in-place-holding-lists-of-a-parameter-takes-a-block-answering-an-empty-list-beside-a-list-of-it`
- `a-parameter-handed-in-place-holding-lists-of-a-parameter-takes-a-list-of-an-empty-list`
- `a-parameter-handed-in-place-holding-lists-of-a-parameter-takes-an-empty-list-beside-a-list-of-it`
- `a-parameter-handed-in-place-holding-nullable-dictionaries-of-lists-of-a-parameter-takes-null-and-a-map-of-an-empty-list`
- `a-parameter-handed-in-place-takes-no-reading-of-any-refuses`
- `a-parameter-naming-a-type-nothing-declares-refuses`
- `a-parameter-read-as-a-declared-record-and-its-alias-keeps-the-name`
- `a-path-written-from-any-into-a-list-of-a-parameter-refuses`
- `a-procedure-a-call-filled-from-a-declared-record-takes-no-int-refuses`
- `a-procedure-value-at-a-slot-writing-a-procedure-type-refuses`
- `a-reading-of-any-at-a-bounded-parameter-refuses`
- `a-reading-of-any-at-a-contract-procedure-refuses`
- `a-reading-of-any-beside-a-whole-at-a-contract-procedure-refuses`
- `a-reading-of-any-stands-at-an-alias-of-any`
- `a-reading-outside-a-bound-refuses`
- `a-record-a-block-answers-where-a-declared-record-is-read-takes-the-name`
- `a-record-a-host-procedure-answers-short-of-its-fields-refuses`
- `a-record-a-loop-answers-where-a-declared-record-is-read-takes-the-name`
- `a-record-arrives-as-an-argument`
- `a-record-built-where-a-declared-record-is-read-keeps-its-closure`
- `a-record-declared-without-its-record-key-refuses`
- `a-record-from-outside-at-a-contract-slot-is-fitted-to-its-record`
- `a-record-from-outside-short-of-a-field-at-a-contract-slot-refuses`
- `a-record-from-outside-under-another-name-refuses-at-the-door`
- `a-record-from-outside-under-its-name-at-any-is-held-to-its-record-refuses`
- `a-record-literal-a-name-that-declares-nothing-holds-refuses`
- `a-record-literal-answered-where-a-declared-record-is-answered-takes-the-name`
- `a-record-literal-beside-a-declared-record-at-a-type-parameter-refuses`
- `a-record-literal-short-of-a-field-its-record-declares-refuses`
- `a-record-literal-written-where-no-declared-record-is-read-refuses`
- `a-record-type-may-name-a-field-for-a-form`
- `a-record-under-another-name-refuses`
- `a-record-written-where-a-type-is-written-refuses`
- `a-row-of-readings-of-any-appended-to-a-table-of-text-refuses`
- `a-slot-of-a-type-takes-no-value-read-as-a-contract-refuses`
- `a-some-outside-a-signature-refuses`
- `a-type-declared-under-a-name-the-language-declares-refuses`
- `a-type-declared-under-a-name-the-language-gives-refuses`
- `a-type-declared-under-a-word-a-type-spelling-writes-refuses`
- `a-type-form-array-of-an-element-with-a-spelling-refuses`
- `a-type-form-beside-other-keys-refuses`
- `a-type-mention-that-is-no-name-refuses`
- `a-type-no-claim-names-in-a-closures-contract-parameter-refuses`
- `a-type-no-claim-names-refuses`
- `a-type-parameter-named-for-a-type-the-language-names-refuses`
- `a-type-parameter-named-self-refuses`
- `a-type-parameter-only-the-answer-names-refuses`
- `a-type-parameter-read-as-any-and-as-a-type-holds-any`
- `a-type-parameter-read-loosely-and-tightly-holds-the-loose-reading`
- `a-type-parameter-read-two-ways-is-refused`
- `a-type-parameter-two-procedures-take-as-int-and-as-anything-is-int`
- `a-type-parameter-written-nullable-refuses`
- `a-type-reaching-itself-through-names-alone-refuses`
- `a-type-that-misses-a-procedure-does-not-answer-the-contract`
- `a-type-the-language-names-answers-a-contract`
- `a-value-cast-from-any-to-a-contract-answers-by-the-type-it-is`
- `a-value-cast-from-any-to-a-contract-it-does-not-answer-fails`
- `a-value-declares-every-parameter-the-slot-hands`
- `a-value-from-outside-is-fitted-to-the-fields-declared`
- `a-value-from-outside-under-a-name-no-document-declares-refuses-at-the-door`
- `a-value-from-outside-under-an-alias-at-any-is-a-value-of-its-record-answers`
- `a-value-of-a-contract-at-two-self-positions-refuses`
- `a-value-of-a-contract-inside-a-list-at-a-bounded-parameter-refuses`
- `a-value-of-a-contract-inside-a-map-at-a-bounded-parameter-refuses`
- `a-value-of-a-contract-or-null-at-two-self-positions-refuses`
- `a-value-of-a-contract-through-an-alias-fills-a-parameter-standing-twice-refuses`
- `a-value-of-what-may-be-null-at-two-self-positions-refuses`
- `a-value-outside-a-contract-in-a-closures-parameter-refuses`
- `a-value-outside-a-contract-standing-as-a-type-refuses`
- `a-value-outside-a-declared-type-refuses-at-the-door`
- `a-value-read-as-a-contract-where-another-is-asked-refuses`
- `a-value-read-as-any-sent-to-a-closure-held-at-a-procedure-type-refuses`
- `a-value-taking-a-parameter-in-place-does-not-fit-a-slot-handing-a-value`
- `a-variable-a-closure-took-written-from-any-refuses`
- `a-variable-a-closure-writes-from-any-refuses`
- `a-variable-a-closure-writes-with-a-value-of-the-parameter-answers`
- `a-variable-handed-in-place-to-a-call-whose-cast-fails-stays-as-it-was`
- `a-variable-written-an-alias-and-what-it-stands-for-holds-that-type`
- `a-whole-literal-an-attempt-answers-beside-a-fraction-is-no-fraction-refuses`
- `a-whole-literal-at-a-fraction-slot-is-the-fraction`
- `a-whole-literal-beside-a-fraction-at-a-bounded-parameter-is-held-to-the-bound-as-the-fraction`
- `a-whole-literal-between-the-brackets-of-a-map-keyed-by-fractions-is-the-fraction`
- `a-whole-literal-where-a-bounded-parameter-stands-refuses`
- `a-whole-number-a-name-holds-is-no-fraction-refuses`
- `an-alias-beside-what-it-stands-for-in-a-list-literal-joins-as-that-type`
- `an-alias-coming-back-to-itself-through-a-list-refuses`
- `an-alias-of-a-contract-answers-the-contract`
- `an-alias-of-a-declared-record-gives-a-value-from-outside-the-records-name`
- `an-alias-of-a-record-answers-the-records-contracts`
- `an-alias-of-any-another-document-declares-at-a-contract-slot-refuses`
- `an-alias-of-any-at-a-contract-slot-refuses`
- `an-alias-of-any-at-a-nullable-contract-slot-refuses`
- `an-answer-from-outside-under-a-name-no-document-declares-where-no-returns-is-written-refuses-at-the-door`
- `an-answer-from-outside-under-an-alias-where-no-returns-is-written-is-a-value-of-its-record-answers`
- `an-answer-from-outside-under-its-name-where-no-returns-is-written-is-held-to-its-record-refuses`
- `an-answer-read-as-any-where-a-type-is-declared-refuses`
- `an-array-of-bytes-and-a-list-of-numbers-joins-to-a-list-of-lists`
- `an-empty-list-handed-to-a-generic-answers-a-list-of-any-type`
- `an-inout-type-parameter-a-procedure-slot-fills-first-reads-the-value`
- `an-inout-type-parameter-a-variable-fills-first-reads-the-value`
- `an-optional-cast-of-a-closure-over-a-type-parameter-its-making-call-filled-reads-null`
- `an-optional-read-of-a-field-naming-an-alias-of-a-nullable-reads-that-nullable`
- `any-written-nullable-refuses`
- `elements-of-different-types-join-to-any`
- `inout-written-on-a-name-refuses`
- `inout-written-on-returns-refuses`
- `never-written-nullable-refuses`
- `null-written-nullable-refuses`
- `procedures-apart-only-by-an-alias-join-as-one-procedure-type`
- `self-in-an-answer-is-what-the-call-filled-it-with`
- `self-outside-a-contract-refuses`
- `self-stands-for-the-type-answering-a-contract`
- `two-documents-claiming-one-pair-are-one-claim`
- `what-was-read-out-of-a-parameter-is-not-the-parameter`
