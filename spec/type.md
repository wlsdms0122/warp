# Types

What a name may stand for, and what a slot takes. A type is judged at the build against the declarations the grammar read; what a type *admits* is asked of a value at a boundary, which is sometimes the build and sometimes the run. Reads [the value model](value.md). Read by procedures, statements and expressions, each of which writes a slot.

A type is written as a string, or as a record for what a string cannot say:

| written | means |
|---|---|
| `Null` `Bool` `Int` `Double` `String` | the scalar kinds |
| `Any` | anything |
| `Never` | never answers. The type `Standard.Control.abort` declares, and what makes a leaving call checkable |
| `Array<T>` / `Dictionary<T>` | a list / map of `T`; `Array<Any>` is a list of anything, and `Array` or `Dictionary` written bare **refuses at the load** |
| `Procedure` | some procedure, signature unsaid |
| `const <Procedure type>` | a procedure that answers without running, under *what answers without running* in [procedures](procedure.md) |
| `isolated <Procedure type>` | a procedure that touches no name another body could touch at once; `const isolated Procedure` says both, `const` first |
| `inout <type>` | a parameter handed a variable in place; written on a parameter's type and nowhere else |
| `{ linear: <type> }` | a type whose values are handed on exactly once; written on a type in `types` and nowhere else, and every slot naming that type carries it |
| `consuming <type>` / `borrowing <type>` | what a parameter does with a linear value: takes the obligation, or reads and leaves it. Written on a parameter's type and nowhere else |
| `var <type>` | a field a path may write through; written on a field of a type declared in `types` and nowhere else |
| `Task` (any declared name) | the type a module declares under that name |
| `some T` | a type parameter: worked out from the call, same reading everywhere it appears; bounded when the signature's `bounds` names it |
| `Self` | the type answering a contract, written in that contract's procedures alone |
| `Describable` (a declared contract's name) | a value of whatever type satisfies the contract. Nothing ties one slot's to another's |
| `Describable & Standard.Comparable` | a value of whatever type satisfies every contract named; the names in name order, and each a contract's |
| `Int(0...255)`, `Double(0.0..<1.0)` | a number the slot admits only inside the range. The kind written out, either bound optional but not both, and `..<` leaving the far bound outside |
| `Int?` (any string spelling and `?`) | the declared type or null. The one union written inline, and it is null-only. Any other is said with a contract the types claim, and the contract is named |
| `{ record: { title: String, done: Bool } }` | a record type, its fields under `record`; structural, and it names nothing. A field may be called anything |
| `{ procedure: { parameters: [<type>, …], returns: … } }` | a procedure type: the types it is called with, in position order, and what it answers. No names, since a name is a declaration's and a value is called by position; a mark such as `inout` is written on the type it stands in front of |
| `{ "const procedure": { … } }` | a procedure type with its marks and modifiers on the key, `inout` or `consuming` or `borrowing` first, then `const` and `isolated`, the way they stand in front of the string form |
| `{ array: <type> }` / `{ dictionary: <type> }` | a list / map of a type that has no string spelling, a procedure type or a record type. Where the element has a spelling the type is written `Array<T>`, and the record form around it **refuses at the load** |

`Int` and `Double` are two types, and neither takes the other: a value's type is fixed at the build, so a whole number never stands where a fraction is declared, and the reverse **refuses** too. A whole number written as a literal is read as the fraction it names where the place it is written into declares a `Double`, a range of fractions included: a slot, an answer, a name that says what it holds, a write, a list or a record's part there, and a parameter a call fills beside a fraction. Anywhere else it is an `Int`, and a name it is bound to holds an `Int`. `Any` accepts everything. A slot that takes either kind of number is bounded by the contract `Standard.Numeric`, under [the standard vocabulary](vocabulary.md).

**A declared record is nominal.** A type declared in `types` whose structure is a record is a name as well as a structure. When a nameless record settles into a slot declaring the type, it settles to the declared structure and takes the name; a record already under that name is settled again and keeps it; a record under another name **refuses** at the slot, whatever its structure: at the **build** where the build can see the name, at the **run** where the value arrived through `Any`, and `as?` reads it as null. Two declared records of one structure under two names are two types, and a value fits only its own. A declared name whose structure is not a record, an alias such as `Standard.Byte`, attaches no name. An inline record type and `Dictionary<T>` are structural: a named record fits them by structure, and what settles there is built on the slot's own layout, which has no name. `Any` declares nothing, so a value passes it as it is, name included. A declared type may name itself in a field, nullable or as a list's element, so a tree is one declaration. A declared name that comes back to itself through names alone, a `?` included, stands for no type and **refuses at the build**.

`inout` and `var` stand in front of the whole type, `?` included: `inout Int?` is a nullable handed in place. They say something about the slot and nothing about the value, so what fits the slot is judged by the type after the procedure. Writing either where it is not allowed **refuses** at the build. A slot asking `isolated` takes what the build derived as isolated. Answering without running is a separate claim and does not stand in for it. A value standing in a procedure-typed slot takes exactly the positions the slot's type hands, each accepting what the slot may hand at that position, and answers what the slot's `returns` accepts. The names the value's declaration wrote are its own and take no part: one closure fits two slots that name their parameter differently. That is held at the **build** where the value's type is known, and at the **run** where the value arrived through `Any`, under *one calling convention* in [procedures](procedure.md).

**What a slot takes, exactly.** Where a value meets a declaration (an argument, an answer, and a write into a box that said what it holds), the settlement is one rule per type:

- `Any` passes the value through untouched, null and procedures included. Nothing settles, because nothing was declared.
- A **record type** says which fields there are. A value carrying at least them fits, and what settles is built on the declared fields: each is settled against its type, and a field the declaration never named is not carried past it. To keep names the declaration does not have, declare `Dictionary<T>`, where the names are the value's own.
- A **declared name** whose structure is not a record is an alias: settling resolves the name and judges by what it stands for. One whose structure is a record is nominal, under *a declared record is nominal* above.
- A **nullable** (`T?`) passes null through and settles anything else against the declared half. `T?` takes `T`, null and `T?`; a `T?` reading does not fit a plain `T` slot. The `?` is written once, on the whole spelling, and only where it says something new: `Int??`, `Null?`, `Any?`, `Never?` and `some T?` each **refuse at the load**, and the same `?` behind a declared name standing for one of them **refuses at the build**, where the name resolves. A type with no string spelling, a record, has no `?` to trail; a nullable record is reached through a declared name (`Task?`).
- The numeric edge is value-independent: `Int` refuses every fraction, `2.0` included. Taking the whole ones would make fitting depend on the value rather than the type. `Double` refuses every whole number for the same reason. A literal read as a fraction names the binary64 fraction nearest it, so digits past 2^53 round as binary64 rounds.
- A **range** (`Int(0...255)`, `Double(0.0..<1.0)`) is a slot's condition on a number, not a kind: the value is an `Int` or a `Double`, and the bounds are judged where a value is settled, the way `enum` is. At the **build** for a constant argument, at the **boundary** for what only the run can see.
  - **The kind is written out**, because a bound is a value of the kind it bounds: `Int(0...255)` writes whole numbers and `Double(0.0...1.0)` fractions, each in that kind's one spelling. `Int(0.0...)` and `Double(0...)` both **refuse at the load**. Neither range can be written with the other's bounds. A fraction range takes fractions alone, and a whole literal written into one is the fraction it names (`2` written at `Double(0.0...5.0)` is `2.0`).
  - **The far bound may be left outside.** `a...b` holds it and `a..<b` does not: the half-open interval is what a position below a length is written against, and for a fraction it is the one nothing can spell by moving a bound. The near bound is always inside, which is the convention every half-open interval is already read by; there is one spelling per range because of it. `..<` with nothing after it **refuses at the load**. It says the far bound is outside, and there is no far bound.
  - Before the run, acceptance reads a range as the kind under it on either side. Only what is provably outside is refused early, and a reading's worth is not knowable, so a call handing a declared `Int` to an `Int(0...255)` slot builds and the boundary judges. Two ranges are both the text's fact, so bounds that cannot overlap are refused early, and ranges of two kinds hold no value in common.
  - Either bound may be open (`Int(0...)`, `Int(...255)`); neither may be (`Int(...)` says nothing and **refuses at the load**), and a range whose bounds admit nothing (`Int(9...1)`, or `Int(5..<5)` where the far bound is excluded and the near one stands on it) is a slot no call could fit, **refused at the build** where the declaration wrote it, exactly as an empty `enum` is. A whole bound must be a number an `Int` holds, and a padded or signed spelling (`Int(007...)`, `Int(+1...)`) or a bound past what an `Int` holds both **refuse at the load**, each named as what it is.
  - A module gives a range a name the way it names any type, and a name takes no range of its own, so `Standard.Byte(0...10)` is not a type: `Standard` declares `Standard.Byte = Int(0...255)`, and there is no separate byte kind.
  - A bound is written as the value it is, so a fraction bound is a fraction's one spelling. A host may assemble a range bounded by an infinity. It orders like any other bound, and the build takes it, but no document spells one, so **writing that range out refuses**, the way every type a document cannot say does, rather than coming back as something a reader would reject.

`Never` is a real type and fits **every** slot, by never arriving: an expression typed `Never` may be written where any value is expected, such as an argument that calls `Standard.Control.abort`, and evaluating it ends the evaluation it is inside. The statement rules (no name, nothing follows) are statement rules; in expression position there is nothing extra to say, because nothing after the expression is reached at all.

**Type parameters.** A declaration may leave a type parameter and let the call fill it: a procedure taking `Array<some T>` and a `some T` answers what it was given. Inside the declaration the parameter is one type its body does not know. A parameter handed in place, or an element of one, takes only a value of that parameter, since the caller reads its own variable as what filled it and nothing settles a write there, and a call filling a parameter from such a variable holds every other argument read at it to the same, so a value of a type the bounds hold is no more a value of the parameter handed to a call than written directly; the call judges the variable against what filled the parameter once the call is over, whether it answered or failed, and a value outside it **refuses at the run** there. The answer takes a value of that parameter or a reading of `Any`; the call judges what arrives against what filled the parameter, and a value outside it **refuses at the run** where the call reads it. A list or record literal written there is judged part by part, each element or field against what the slot asks at it, and an empty list holds no element wherever in the literal it stands: `[]` is a value of `Array<some T>`, `[[], [x]]` of `Array<Array<some T>>` where `x` is one of `some T`, and `[{ a: [] }, { b: [x] }]` of `Array<Dictionary<Array<some T>>>`. A call reads a literal handed to it as one type to fill a parameter, its parts joined part by part, so records of other fields read there as `Any`, and handed beside such a parameter it is then judged part by part as a write is. A record handed where a dictionary of the parameter is declared fills it with what each of its fields reads it as, joined part by part as a list's elements are, and each field is held where it stands. Where bounds hold the parameter, only what stands at the parameter in a literal handed there is held to them, what a name the literal holds reads as included, and a closure in the literal is judged as any closure handed to its procedure type is. A parameter read twice must be read the same both ways. Two readings where one accepts the other settle on the one that holds both, position by position through lists, dictionaries, what may be null and record fields: a range meeting its kind or another range of it gives the kind, a declared record meeting a nameless record of its fields gives the nameless one, since that is the one a value is sure to fit, two records of other fields give a nameless record of the looser one's fields, each settled with the other's field of that name, a reading of `Any` makes its position `Any`, as it does the whole parameter, and elsewhere the looser stands; a reading that leaves, or an empty list's element, holds no value and fills nothing; two readings that do not fit **refuse at the build**, and do not widen to `Any`. Where bounds hold the parameter, what each argument hands there is held to them before its readings are joined, so text handed beside a reading of `Any` **refuses at the build** though the parameter reads `Any`. Appending a whole number to a list of text is a parameter read as text and as a number, and there is no answer that is both. A closure written in a declaration with a type parameter may name it in its own signature, and the run does not know what filled it: where the closure is judged against a procedure type, the parameter is read as what that type asks there and held to its bounds, refusing there where what it asks is outside them, and a variable handed to it in place at the parameter is judged once the call of the closure is over against what the call holds it as.

**Bounds.** A type parameter may be bounded: a signature declares `bounds: { T: Standard.Comparable }` once, its slots write `some T`, and every occurrence of the name takes only what answers the contract the bound names, under **Contracts** below. A bound may name several, joined with `&`: `bounds: { T: Standard.Comparable & Describable }` holds `T` to what answers every one of them. The signature owns the bound. A slot names the parameter and never the bound, so one bound is one claim however many slots mention the name. A bound names contracts and nothing else, and what answers one is whatever type a document claims does, so the set a bound holds a parameter to is open. The judgment is made twice, once per surface: at the **build**, a reading provably outside the bound refuses (two booleans meeting `lessThan` never run), and a reading the text says nothing about (`Any`) passes; at the **boundary**, the value that actually arrived is judged by the type it is an instance of, so what travelled in through `Any` is refused where it arrives. One name is held to one set of bounds: `bounds` writes the set once, every occurrence of the name reads it, and a signature assembled with two occurrences holding different sets is refused at the build and written by no document. `bounds` naming a parameter no slot mentions refuses at the load. Only the declaring procedure writes `bounds`. A procedure *type* nested in a slot carries none, because its parameters are the declaring signature's own slots and the declaring signature owns their bounds. A closure written in the body reads the same names: its `some T` is the `T` the caller filled, held to the bounds the declaration wrote, so a closure may send what the body around it may. A bound naming what no module declares as a contract **refuses at the build**. And a type parameter lives in a signature: a declared type writing `some` outside a procedure signature refuses at the build, because nothing there is filled by a call.

**Linear types.** A type written `linear` says the values of it are given away: to a procedure, or as a body's answer. A body holding one hands it on **on every way through, once**, and the build says so before anything runs.

The mark is written on the declaration, so the obligation rides with the name: a slot naming the type has it, and nothing can take it off. Writing `linear` anywhere else **refuses at the build**, and so does carrying such a type inside another type (a list, a record, another declaration): what follows the value is the name holding it, and nothing follows one into a type.

**A slot naming such a type says what it does with it.** Two marks, written on a parameter's type the way `inout` is, and a parameter that names the type and writes neither **refuses at the build**:

| written | means |
|---|---|
| `consuming <type>` | the obligation moves to this slot. The caller's name is empty afterwards, and this body owes the value from here |
| `borrowing <type>` | the obligation stays where it was. This body reads the value and the caller still owes it |

Either is written on a slot that **names the type**, because the name is what the build follows the value by. On `some T` it **refuses**: what fills a type parameter is the call's, so a body that took the obligation there would have no name to carry it on and the check would end at that slot.

**A linear type answers no contract.** A contract standing where a type is written holds a value under no name of its own, and nothing follows a linear value but the name that holds it. A claim that such a type satisfies a contract **refuses at the build**, where the claim is written.

**A declaration whose body answers one writes `returns`.** What a declaration answers is read off its body where nobody wrote it, and the mark is not something a reading keeps, so a caller binding that answer would take an obligation nothing told it about. It **refuses at the build**, by the result and by every `return` that carries a value alike.

**A reading that may answer nothing does not take one.** `as?` onto a linear type **refuses at the build**, and so does writing `?` on one: what such a value needs is a name holding it on every way through, and a `?` says there is a way through where nothing is there.

**A closure is a procedure, and its body is held to all of this.** It is walked the way a declaration's body is, seeded with what the closure itself was handed: a closure that opens one and reaches its end still holding it is refused exactly as a declaration would be. What it runs an unfixed number of times is the *capture*, and a name the closure declared is its own.

**What such a body may not do is answer one.** A procedure type whose `returns` is linear **refuses at the build**, closure literals included, and a body that wrote no `returns` is held to the same rule by what the walk finds: the rule turns neither on whether a key was typed nor on how the answer was written. Nothing reads inside a body that travels as a value, so what one handed back would arrive with nothing to say it is owed. A declaration is not held to this: what it answers lands on the name its caller binds.

Writing `consuming` or `borrowing` where nothing is linear **refuses at the build** too, the way a `?` that says nothing new does: both say what a slot does with an obligation, and there is none.

What a body may do with one:

- hand it to a slot that says `consuming`, which ends the obligation here;
- hand it to a slot that says `borrowing`, which ends nothing: the body still holds it and still owes it;
- answer it, which hands it to the caller, who owes it from there;
- read a part of it (`handle.name`), which hands nothing on.

What a body may do with one it **borrowed**: read it, read a part of it, bind it to another name, and pass it to another slot that borrows. That is all. Writing the name anywhere a value leaves by refuses, wrapping it in a list or a record included: that carries the whole value out rather than reading a part of it.

What **refuses at the build**:

- reaching the end of a body still holding one;
- handing one on a second time. Within one call that counts in position order, the order the run evaluates the arguments in (see [running](running.md)), so a slot that borrows reads what a consuming slot standing before it already took;
- handing one on in one arm of a conditional and not the other, since what a body holds afterwards would depend on which arm ran. An arm that **returns** is not one of those arms: no run comes back from it, so what the body holds afterwards stands on the arms that finish. An arm that `break`s is one of them, and is held to the same rule: the run comes back out of the loop still holding what the arm held;
- handing one on inside a loop round, inside an `attempt`, in a call of a value, or capturing one in a closure, and writing one into a box inside a loop round or an `attempt`. Each of those runs no fixed number of times, or fails somewhere the text does not show, so "exactly once" is not something the text says. Leaving is not one of these unless it leaves the procedure: a `break` leaves the construct and a `continue` ends the round, and what the body was holding it holds still on the other side of either;
- writing over a name still holding one;
- writing one into a **list or a record**, whether it is a name still holding one, a value nothing holds yet, or what a cast, a block or an `attempt` hands out. What follows the value is the name, and a name does not follow it into a type, so the obligation would be neither handed on nor still held;
- handing a borrowed one to a slot that says `consuming`, or answering it, or keeping it in a box. Each gives away what this body never took, and a box outlives the call that lent the value.

Only a procedure with **no body** ends the obligation. A body that takes one has to hand it on like any other, so the chain runs out at a native procedure.

**Contracts.** A contract says which **procedures** a value answers: the types that answer them are open, and new ones arrive with new documents. A module declares one the way it declares a type: a name bound to the procedures, each written as a signature whose first parameter is `Self`, the type that answers the contract, since the value standing there is the one the procedure is answered about. `Self` may stand at any of the procedure's positions and in its answer, and it is that one type wherever it stands: a claim reads it as the type the claim is about, and a call through the contract reads it as one type parameter the contract bounds, filled from the call the way any type parameter is. A contract's procedure taking anything else first **refuses at the build**, the contract's own name included, since that is a value of whichever type answers it. `Self` written anywhere but a contract's procedures **refuses at the build**, and `some Self` **refuses at the load**.

A contract's name stands where a type is written, and so does `A & B`: the slot takes a value of whatever type satisfies every contract named. This is how the language says **A or B**: each type claims one contract and the slot names it, so no slot writes an inline union. It is a type parameter with no name, so nothing ties one slot's reading to another's, and a call fills nothing. A type parameter a contract bounds is one type wherever it stands, and a value of a contract is of whichever type answers it, so such a value fills one only where the parameter stands alone at one of the procedure's positions: `App.Described.describe` takes one, and a call handing one where the parameter stands twice, `Self` of `lhs` and `rhs` included, or inside a list or a record, **refuses at the build**. A closure literal's parameter is such a slot too, and a call of the value holds what it hands to the contract by the rule a call to a declaration is held by. A name that is not a contract's joined with `&` **refuses at the build**.

A type **satisfies** a contract when a document says it does. The document writes the claim under `satisfies`, keyed by the type: `satisfies: { "Bank.Account": ["App.Describable"] }`. Any document may make one, about a type it declared or about another document's, which is how a document that arrives later gives a type the procedures a contract asks. A type the language names is a type the way a declared one is, and a claim may be about it: `satisfies: { Int: ["App.Describable"] }`, answered by `Int.describe`. A list and a map are named bare, `Array` and `Dictionary`. Every list is an instance of `Array` whatever it holds, since a value does not say which elements a slot declared it to hold, and a claim written about `Array<Int>` **refuses at the load**. Bytes are an instance of `Array`, and a record with no name an instance of `Dictionary`, its names being data. `Any`, `Never`, `Null` and `Procedure` are types no value is an instance of by name, and a claim about one **refuses at the load**. A claim about a declared name that is not itself a record, an alias included, **refuses at the build**: a value of a declared type is an instance of the record it is, and of no other name.

The build holds the claim to the declarations behind it. For every procedure the contract asks, it takes the declaration named for the type and that procedure (`Bank.Account` and `describe` give `Bank.Account.describe`) and holds its signature to the contract's with the type in place of `Self` wherever the contract writes it. A name that stands for a declared record names that record's type there, as wherever types are compared, so a declaration may write another name for the record the contract writes. A declaration that wrote no `returns` is held by what its body answers, read the way a call site reads it.

Whether a type answers a contract is therefore a fact of the whole list, and a claim may be written in a document the one leaning on it never names. A document handing a type where a contract is asked is not judged where it is compiled: the pair leaves the compile unresolved, the way a procedure the document sends and does not declare leaves it, and **refuses at the call that leaned on it** where the build cannot answer. A claim missing a procedure, or holding one whose signature does not fit, puts its type under no contract and its reason is what that refusal says.

A claim whose two names the list declares as something other than what the claim needs of them **refuses at the build, at the claim**: a contract where the type belongs, or a type where the contract belongs. One name has one declarer, so no document arriving later makes that right. A name the list declares as nothing at all waits with the rest: the claim holds nothing, and that is refused only **where a call leaned on the pair**, with the reason the claim came to nothing. A claim nobody leans on refuses nowhere.

Two documents claiming one pair are one claim: a claim holds nothing but the pair, so the second says what the first said.

A declaration named for a type and a procedure that no claim names is that document's procedure and nothing else. So what a link declares never decides what an unrelated document may call things, and a document that names no contract builds the same whichever documents stand beside it.

A contract may ask no procedures. It is then a mark a claim gives a type, and a type answers it where a document claims it does, as for any contract. A name is a type or a contract and never both.

A signature bounds a type parameter by a contract as **Bounds** above says: `bounds: { T: App.Describable }`, and the slots write `some T`. A value reaching such a slot is judged twice, once per surface: at the **build** a reading provably outside refuses, and at the **boundary** the value that arrived is judged by the type it is an instance of.

A body calls a contract's procedure by writing the contract's name and the procedure's with a dot between them: `App.Describable.describe`. That spelling is the contract's declaration of the procedure, and it is a send like any other: a document calling a contract another module declares lists the spelling in `imports`. It names no type's declaration, and what it means is settled by the value at its first position, so a call writing nothing there refuses. What a call hands it and what it answers are the contract's, not any one declaration's.

**The build builds the table and the run reads it.** For every contract, the build gathers every type that satisfies it and lowers one call per type, each against the row that answers, arguments in that row's own slot order. The run reads the type the first argument is an instance of and picks. Nothing is resolved while a program is running.

A declaration answering a contract's procedure is reached **through the contract**, which is the spelling that says which contract is meant. Two types answering one procedure is the ordinary case. Such a declaration takes exactly the contract's positions and answers what the contract's answer takes: its own type first, then **at the contract's positions** a parameter taking everything the contract's takes there and taking a place only where the contract hands one, the contract's type parameters standing for types no call fills and the declaration's own filled by what the contract writes at the same positions; the names are its own. One declaring a parameter beyond them, `T?` included, **refuses at the build** where the claim is leaned on. The run hands the arguments to the same positions whichever declaration answers.

**A name is its declared spelling.** The key a document declares a type, contract or procedure under is the whole of its name: `Standard.Math.floored` is declared under that key, and `Wallet.Account` under that one. A mention is a declared spelling, written out, and it means the same declaration wherever it was written, inside the declaring document too. A dot is a character of the spelling and nothing more: the language has no nesting, no scope and no prefix, so what a document chooses to put before a dot is the author's convention, and one document may declare `Wallet.fee` beside `Bank.rate` while another declares `Wallet.rate`. A spelling no module in the link declares **refuses at the build** where it is mentioned. There are two namespaces, procedures and types, and a procedure may be spelled like a type. Types and contracts share the second, and no name in it is both, so a mention reaches whatever declares it: a slot names a type or a contract, and a bound names a contract.

The shared `Standard` bundle declares the contracts the standard procedures are bounded by, `Standard.Numeric`, `Standard.Comparable` and `Standard.Collection`, claims them for the types the language names (`Int` and `Double` are numbers that order, `String` orders and has a count, `Array` and `Dictionary` have a count) and declares the procedures answering them, `Int.plus` and the rest, under [the standard vocabulary](vocabulary.md). A bundle whose signatures mention them links with `Standard` in the build.

## Cases

What `conformance/` asks about this page, by the name each case's file carries.

- `a-bare-array-refuses`
- `a-bare-contract-name-refuses`
- `a-bare-dictionary-refuses`
- `a-bare-name-for-another-modules-procedure-refuses`
- `a-body-answering-a-value-for-its-own-type-parameter-refuses`
- `a-body-cannot-answer-what-it-borrowed`
- `a-body-handing-its-own-type-parameter-in-place-to-a-type-refuses`
- `a-body-writing-a-value-into-its-own-type-parameter-refuses`
- `a-borrow-captured-by-a-closure-refuses`
- `a-borrow-handed-to-a-consuming-slot-refuses`
- `a-borrow-inside-a-loop-round-stands`
- `a-borrow-kept-in-a-box-refuses`
- `a-borrow-passes-to-another-borrow`
- `a-borrow-written-into-a-list-refuses`
- `a-borrowing-slot-reads-and-leaves-the-obligation`
- `a-bound-may-name-several-and-holds-to-every-one`
- `a-bound-names-a-contract-another-document-declares`
- `a-bound-naming-a-parameter-no-slot-mentions-refuses`
- `a-bound-past-an-int-refuses`
- `a-box-that-handed-one-on-takes-another`
- `a-break-does-not-excuse-the-arm-it-leaves-from`
- `a-break-does-not-strand-what-the-body-holds`
- `a-byte-is-a-whole-number-a-range-refines`
- `a-call-filling-a-parameter-beside-the-caller-parameter-from-a-reading-of-any-is-judged-refuses`
- `a-call-filling-a-parameter-from-a-list-of-any-reads-it-as-any`
- `a-call-filling-a-parameter-from-a-variable-held-in-place-takes-a-value-of-that-parameter`
- `a-call-filling-a-parameter-from-a-variable-held-in-place-takes-no-other-value-refuses`
- `a-call-through-a-contract-with-nothing-first-refuses`
- `a-cast-between-aliases-of-two-nullable-records-reads-null-answers`
- `a-cast-does-not-carry-a-held-name-into-a-list`
- `a-cast-naming-a-linear-type-does-not-go-into-a-list`
- `a-cast-of-a-nullable-record-to-another-record-refuses`
- `a-cast-of-a-record-with-a-var-field-to-a-record-it-never-is-refuses`
- `a-cast-of-a-recursive-record-to-a-field-it-never-holds-further-down-refuses`
- `a-cast-of-an-alias-of-a-nullable-record-to-another-record-refuses`
- `a-cast-to-an-alias-of-a-nullable-record-names-the-record-answers`
- `a-claim-about-a-list-of-one-kind-refuses`
- `a-claim-about-a-name-that-is-not-a-record-refuses`
- `a-claim-about-a-type-no-value-is-refuses`
- `a-claim-naming-a-contract-where-the-type-belongs-refuses`
- `a-claim-naming-a-type-where-a-contract-belongs-refuses`
- `a-claim-nobody-leans-on-refuses-nowhere`
- `a-claim-stands-in-a-document-the-leaning-one-never-names`
- `a-closure-a-generic-body-wrote-hands-back-in-place-what-is-judged-refuses`
- `a-closure-a-generic-body-wrote-is-read-as-the-procedure-type-it-is-judged-against`
- `a-closure-a-generic-body-wrote-read-past-its-bounds-is-not-that-type`
- `a-closure-a-generic-body-wrote-read-within-its-bounds-is-the-type-it-is-judged-against`
- `a-closure-a-generic-body-wrote-taking-a-list-in-place-is-read-as-the-type-it-is-judged-against`
- `a-closure-a-generic-body-wrote-taking-by-value-is-called-where-a-slot-takes-in-place`
- `a-closure-capturing-a-linear-value-refuses`
- `a-closure-reads-the-bounds-of-the-procedure-around-it`
- `a-closure-without-returns-answering-one-refuses`
- `a-closures-parameter-names-are-not-part-of-its-type`
- `a-constant-outside-a-range-refuses`
- `a-contract-asking-no-procedures-is-answered-by-what-claims-it`
- `a-contract-asking-no-procedures-refuses-what-no-claim-names`
- `a-contract-carries-a-procedure-into-a-generic-body`
- `a-contract-declared-twice-refuses`
- `a-contract-is-named-by-its-qualified-spelling`
- `a-contract-or-null-slot-refuses-a-type-not-answering-the-contract`
- `a-contract-or-null-slot-takes-a-parameter-bounded-by-the-contract-and-another`
- `a-contract-or-null-slot-takes-a-type-answering-the-contract`
- `a-contract-procedure-names-what-it-may-fail-with`
- `a-contract-procedure-takes-self-first`
- `a-contract-procedure-taking-the-contract-first-refuses`
- `a-contract-slot-refuses-a-name-for-what-may-be-null`
- `a-contract-slot-refuses-a-parameter-or-null`
- `a-contract-slot-refuses-what-may-be-null`
- `a-contract-stands-in-a-closures-parameter`
- `a-contract-stands-in-a-declared-types-field`
- `a-contract-stands-where-a-type-is-written`
- `a-declaration-answering-a-contract-answering-any-may-answer-its-parameter`
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
- `a-declaration-answering-a-contract-names-its-parameters-its-own-way`
- `a-declaration-answering-a-contract-reading-a-bounded-parameter-beside-any-refuses`
- `a-declaration-answering-a-contract-takes-its-parameters-in-the-contracts-order`
- `a-declaration-answering-a-contract-takes-no-parameter-beyond-it`
- `a-declaration-answering-a-contract-taking-in-place-where-it-hands-a-value-refuses`
- `a-declaration-answering-a-contract-with-a-bounded-parameter-where-it-writes-a-parameter-refuses`
- `a-declaration-answering-a-contract-with-a-bounded-parameter-where-it-writes-what-the-bound-refuses-refuses`
- `a-declaration-answering-a-contract-with-a-contract-where-it-answers-another-refuses`
- `a-declaration-answering-a-contract-with-a-type-not-answering-it-where-it-promises-it-or-null-refuses`
- `a-declaration-answering-a-contract-with-a-type-where-it-writes-a-contract-refuses`
- `a-declaration-answering-a-contract-with-a-type-where-it-writes-a-parameter-refuses`
- `a-declaration-answering-a-contract-with-another-answer-refuses`
- `a-declaration-answering-a-contract-with-another-contract-where-it-writes-a-contract-refuses`
- `a-declaration-answering-a-contract-with-any-is-judged-where-the-call-reads-it-refuses`
- `a-declaration-answering-a-contract-with-its-own-parameter-for-a-type-refuses`
- `a-declaration-answering-a-contract-with-what-may-be-null-where-it-answers-a-contract-refuses`
- `a-declaration-answering-one-without-returns-refuses`
- `a-declaration-no-claim-names-is-its-documents-own-procedure`
- `a-declaration-writing-no-returns-backs-a-claim-by-what-its-body-answers`
- `a-declared-name-and-the-record-it-stands-for-are-one-reading`
- `a-declared-name-is-a-type`
- `a-declared-type-names-itself-in-its-fields`
- `a-dictionary-of-a-contract-or-null-takes-a-record-whose-variable-field-may-be-null`
- `a-dictionary-of-a-contract-takes-a-record-whose-variable-field-is-of-it`
- `a-fraction-is-not-a-whole-number`
- `a-fraction-range-takes-no-whole-number-from-outside-refuses`
- `a-generic-answer-carried-through-another-generic-is-judged-where-the-call-reads-it-refuses`
- `a-generic-answer-handed-back-in-place-is-judged-once-the-call-is-over-refuses`
- `a-generic-answer-of-any-is-judged-where-the-call-reads-it-refuses`
- `a-generic-body-appends-its-parameter-to-a-list-of-it-or-null`
- `a-handle-already-given-away-is-not-read-again`
- `a-handle-borrowed-after-a-consuming-parameter-in-one-call-refuses`
- `a-kind-no-claim-names-refuses`
- `a-linear-type-answers-no-contract`
- `a-linear-type-inside-another-refuses`
- `a-linear-value-does-not-go-into-a-list`
- `a-linear-value-does-not-go-into-a-list-unbound`
- `a-linear-value-handed-on-in-a-call-of-a-value-refuses`
- `a-linear-value-handed-on-inside-an-attempt-refuses`
- `a-linear-value-is-ended-by-a-host-procedure`
- `a-linear-value-is-handed-on`
- `a-linear-value-that-is-dropped-refuses`
- `a-linear-value-written-into-a-box-inside-an-attempt-refuses`
- `a-list-a-closure-hands-in-place-to-a-call-is-judged-refuses`
- `a-list-literal-of-closures-answering-outside-the-bounds-refuses`
- `a-list-literal-of-closures-handed-at-a-bounded-parameter-answers`
- `a-list-literal-of-names-holding-lists-handed-at-a-bounded-parameter-refuses`
- `a-list-of-a-reading-of-any-behind-a-name-handed-beside-a-variable-in-place-refuses`
- `a-list-of-a-reading-of-any-handed-beside-a-variable-in-place-refuses`
- `a-list-of-two-types-handed-where-a-contract-is-asked-is-read-element-by-element-refuses`
- `a-literal-of-names-at-a-contract-bound-leans-on-each-claim-refuses`
- `a-mark-where-nothing-is-linear-refuses`
- `a-module-declares-a-contract-a-bound-names`
- `a-name-declared-as-both-a-type-and-a-contract-refuses`
- `a-name-that-is-not-a-bound-joined-with-and-refuses`
- `a-named-list-handed-where-a-list-of-a-contract-stands-is-held-to-it`
- `a-named-record-arrives-as-an-argument`
- `a-nullable-of-a-linear-type-refuses`
- `a-nullable-that-says-nothing-new-behind-a-name-refuses`
- `a-nullable-that-says-nothing-new-refuses`
- `a-padded-bound-refuses`
- `a-parameter-handed-in-place-handed-on-beside-a-list-of-an-empty-list-answers`
- `a-parameter-handed-in-place-handed-on-beside-an-empty-list-and-a-list-of-it-answers`
- `a-parameter-handed-in-place-handed-on-beside-an-empty-list-answers`
- `a-parameter-handed-in-place-handed-on-beside-records-of-it-and-of-an-empty-list-answers`
- `a-parameter-handed-in-place-handed-on-beside-records-of-other-fields-refuses`
- `a-parameter-handed-in-place-handed-on-to-a-generic-beside-an-empty-list-answers`
- `a-parameter-handed-in-place-holding-a-dictionary-of-a-parameter-takes-a-record-of-it`
- `a-parameter-handed-in-place-holding-a-dictionary-of-lists-of-a-parameter-takes-a-record-of-an-empty-list`
- `a-parameter-handed-in-place-holding-a-list-of-a-parameter-or-null-takes-a-list-of-it`
- `a-parameter-handed-in-place-holding-a-list-of-a-parameter-or-null-takes-null`
- `a-parameter-handed-in-place-holding-a-list-of-a-parameter-takes-an-empty-list`
- `a-parameter-handed-in-place-holding-a-procedure-of-a-parameter-takes-a-closure-of-it`
- `a-parameter-handed-in-place-holding-dictionaries-of-a-parameter-takes-records-of-other-fields-of-it`
- `a-parameter-handed-in-place-holding-dictionaries-of-lists-of-a-parameter-takes-records-of-an-empty-list-and-of-it`
- `a-parameter-handed-in-place-holding-dictionaries-of-lists-of-a-parameter-takes-records-of-other-fields`
- `a-parameter-handed-in-place-holding-lists-of-a-parameter-refuses-an-attempt-whose-rescue-answers-a-number`
- `a-parameter-handed-in-place-holding-lists-of-a-parameter-takes-a-block-answering-an-empty-list-beside-a-list-of-it`
- `a-parameter-handed-in-place-holding-lists-of-a-parameter-takes-a-list-of-an-empty-list`
- `a-parameter-handed-in-place-holding-lists-of-a-parameter-takes-an-empty-list-beside-a-list-of-it`
- `a-parameter-handed-in-place-holding-nullable-dictionaries-of-lists-of-a-parameter-takes-null-and-a-record-of-an-empty-list`
- `a-parameter-handed-in-place-takes-no-reading-of-any-refuses`
- `a-parameter-naming-a-type-nothing-declares-refuses`
- `a-parameter-read-as-a-declared-range-and-its-kind-is-the-kind`
- `a-parameter-read-as-a-declared-record-and-its-alias-keeps-the-name`
- `a-parameter-read-as-a-declared-record-with-a-var-field-and-a-nameless-one-is-handed-in-place-beside-a-nameless-record-answers`
- `a-parameter-read-as-a-declared-record-with-a-var-field-and-a-nameless-one-reads-the-nameless-one-refuses`
- `a-parameter-read-as-a-record-and-a-nameless-one-of-its-fields-is-the-nameless-one`
- `a-parameter-read-as-an-alias-of-a-nullable-record-and-as-a-wider-record-answers`
- `a-parameter-read-as-dictionaries-of-a-record-and-of-a-nameless-one-is-a-dictionary-of-the-nameless-one-refuses`
- `a-parameter-read-as-lists-of-a-record-and-of-a-nameless-one-is-a-list-of-the-nameless-one`
- `a-parameter-read-as-ranges-of-two-kinds-refuses`
- `a-parameter-read-as-records-of-other-fields-keeps-an-any-field-any`
- `a-path-written-from-any-into-a-list-of-a-parameter-is-judged-refuses`
- `a-procedure-type-answering-a-linear-type-refuses`
- `a-range-below-the-smallest-int-admits-nothing`
- `a-range-judges-a-runtime-value-at-the-boundary`
- `a-range-that-admits-nothing-refuses`
- `a-range-whose-bounds-meet-on-an-excluded-edge-admits-nothing`
- `a-range-with-neither-bound-refuses`
- `a-range-with-nothing-after-the-open-edge-refuses`
- `a-range-written-with-the-other-kinds-bounds-refuses`
- `a-reading-beside-any-at-a-bounded-parameter-is-held-where-it-stands-refuses`
- `a-reading-outside-a-bound-refuses`
- `a-record-field-reading-a-parameter-two-ways-at-a-dictionary-refuses`
- `a-record-form-array-of-a-named-element-refuses`
- `a-record-handed-at-a-dictionary-fills-a-parameter-part-by-part-refuses`
- `a-record-handed-at-a-dictionary-of-a-bounded-parameter-fills-it-by-its-fields-refuses`
- `a-record-handed-at-a-dictionary-of-a-contract-leans-on-each-claim-refuses`
- `a-record-literal-holding-a-closure-handed-at-a-bounded-parameter-answers`
- `a-record-of-fields-answering-the-bound-handed-at-a-dictionary-of-a-bounded-parameter-answers`
- `a-record-of-other-fields-with-an-any-field-appended-to-a-declared-list-refuses`
- `a-record-read-as-a-dictionary-after-any-at-a-bounded-parameter-refuses`
- `a-record-settles-to-the-fields-declared`
- `a-record-takes-the-name-of-the-slot-it-settles-into`
- `a-record-type-may-name-a-field-for-a-form`
- `a-record-under-another-name-refuses`
- `a-record-under-another-name-refuses-through-any`
- `a-record-whose-fields-do-not-join-handed-at-a-dictionary-of-a-bounded-parameter-refuses`
- `a-record-with-a-var-field-handed-at-a-dictionary-fills-a-parameter-by-its-values-answers`
- `a-record-with-a-var-field-handed-at-a-dictionary-fills-a-parameter-by-its-values-refuses`
- `a-return-answering-one-without-returns-refuses`
- `a-row-of-readings-of-any-appended-to-a-table-of-text-refuses`
- `a-signed-bound-refuses`
- `a-slot-naming-a-linear-type-says-what-it-does`
- `a-some-outside-a-signature-refuses`
- `a-type-form-beside-other-keys-refuses`
- `a-type-no-claim-names-in-a-closures-contract-parameter-refuses`
- `a-type-parameter-named-self-refuses`
- `a-type-parameter-read-as-any-and-as-a-type-holds-any`
- `a-type-parameter-read-loosely-and-tightly-holds-the-loose-reading`
- `a-type-parameter-read-two-ways-is-refused`
- `a-type-parameter-written-nullable-refuses`
- `a-type-reaching-itself-through-names-alone-refuses`
- `a-type-that-misses-a-procedure-does-not-answer-the-contract`
- `a-type-the-language-names-answers-a-contract`
- `a-value-arriving-through-any-answers-by-the-type-it-is`
- `a-value-called-through-any-is-judged-by-its-own-type`
- `a-value-declares-every-parameter-the-slot-hands`
- `a-value-handed-on-in-one-arm-and-not-the-other-refuses`
- `a-value-handed-on-inside-a-loop-round-refuses`
- `a-value-of-a-contract-at-two-self-positions-refuses`
- `a-value-of-a-contract-inside-a-list-at-a-bounded-parameter-refuses`
- `a-value-outside-a-contract-in-a-closures-parameter-refuses`
- `a-value-outside-a-contract-standing-as-a-type-refuses`
- `a-value-outside-a-declared-type-refuses-at-the-boundary`
- `a-value-taken-inside-an-attempt-body-is-still-owed`
- `a-value-taking-a-parameter-in-place-does-not-fit-a-slot-handing-a-value`
- `a-value-through-any-is-judged-against-the-bound-where-it-arrives`
- `a-value-written-into-a-box-inside-a-loop-refuses`
- `a-value-written-into-a-box-is-still-owed`
- `a-value-written-into-a-list-element-refuses`
- `a-variable-a-closure-took-written-from-any-is-judged-refuses`
- `a-variable-a-closure-writes-from-any-is-judged-refuses`
- `a-variable-a-closure-writes-with-a-value-of-the-parameter-answers`
- `a-variable-a-generic-closure-writes-when-called-through-a-procedure-type-is-judged-refuses`
- `a-variable-handed-back-in-place-is-judged-when-the-call-fails-refuses`
- `a-variable-handed-in-place-that-a-closure-writes-is-judged-refuses`
- `a-whole-literal-where-a-bounded-parameter-stands-refuses`
- `a-whole-literal-written-into-a-fraction-range-is-the-fraction-it-names`
- `a-whole-number-a-name-holds-is-no-fraction-refuses`
- `a-whole-number-is-a-fraction`
- `a-witness-failing-with-what-its-contract-does-not-name-refuses`
- `a-witness-may-write-another-name-for-the-record-a-contract-names`
- `a-witness-takes-the-claimed-type-wherever-the-contract-writes-self-refuses`
- `an-alias-of-a-contract-answers-the-contract`
- `an-alias-of-a-declared-record-settles-to-the-records-name`
- `an-alias-of-a-record-answers-the-records-contracts`
- `an-answer-read-through-any-is-settled-at-the-boundary`
- `an-arm-that-leaves-holds-nothing-afterwards`
- `an-array-of-bytes-and-a-list-of-numbers-joins-to-a-list-of-lists`
- `an-asking-cast-onto-a-linear-type-refuses`
- `an-attempt-returning-one-without-returns-refuses`
- `an-inline-record-slot-takes-a-named-record`
- `an-inout-type-parameter-a-procedure-slot-fills-first-reads-the-value`
- `an-inout-type-parameter-a-variable-fills-first-reads-the-value`
- `an-unsaid-generic-answer-carried-through-another-is-judged-where-the-call-reads-it-refuses`
- `any-written-nullable-refuses`
- `consuming-on-a-type-parameter-refuses`
- `inout-written-on-a-name-refuses`
- `inout-written-on-returns-refuses`
- `linear-on-a-slot-refuses`
- `never-written-nullable-refuses`
- `null-written-nullable-refuses`
- `records-of-two-layouts-holding-one-value-read-as-a-dictionary-at-a-bounded-parameter-refuses`
- `records-of-two-layouts-of-fields-answering-the-bound-read-as-a-dictionary-at-a-bounded-parameter-answers`
- `records-of-two-layouts-read-as-a-dictionary-at-a-bounded-parameter-refuses`
- `self-in-an-answer-is-what-the-call-filled-it-with`
- `self-outside-a-contract-refuses`
- `self-stands-for-the-type-answering-a-contract`
- `the-far-bound-of-a-range-may-be-left-outside`
- `two-documents-claiming-one-pair-are-one-claim`
- `var-written-on-an-inline-record-field-refuses`
- `what-was-read-out-of-a-parameter-is-not-the-parameter`
- `whole-ranges-meeting-past-two-to-the-fifty-third-overlap`
- `writing-over-a-name-holding-a-linear-value-refuses`
