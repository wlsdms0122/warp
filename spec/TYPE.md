# Types

What a name may stand for, and what a slot takes. A type is judged at the build against the declarations the grammar read; what a type *admits* is asked of a value where it meets a slot, at the build where its reading is known and at the run at a door or a cast. Reads [the value model](VALUE.md). Read by procedures, statements and expressions, each of which writes a slot.

## How a type is written

A type is written as a string:

| written | means |
|---|---|
| `Null` `Bool` `Int` `Double` `String` | the scalar types |
| `Any` | anything |
| `Never` | never returns. The type `Standard.Control.abort` declares, and what makes a leaving call checkable |
| `Array<T>` / `Dictionary<K, V>` | a list of `T` / a dictionary from keys of `K` to values of `V`, `K` a type that conforms to `Hashable`; `Array<Any>` is a list of anything, and `Array` or `Dictionary` written bare, or with another count of types, **refuses at the load** |
| `Procedure` | some procedure, signature unsaid: a value of it stands where `Procedure` or `Any` is declared, and is called, or handed where a procedure type is written, only once a cast says what procedure it is |
| `const <procedure type>` | a const procedure, under *a const procedure* in [procedures](PROCEDURE.md) |
| `isolated <procedure type>` | a procedure that touches no name another body could touch at once; `const isolated <procedure type>` says both, `const` first |
| `inout <type>` | a parameter handed a variable in place; written on a parameter's type and nowhere else |
| `var <type>` | a field a path may write through; written on a field of a struct a type in `types` declares, and nowhere else |
| `Task` (any declared name) | the type a module declares under that name |
| `Box<Int>` (a declared struct and the types it is applied to) | the struct a module declares under that name with its type parameters read as the types between the brackets, in the order it lists them; another count, a struct that lists none named with brackets and one that lists some named without, **refuse at the build**, where the name resolves, and so do brackets on any other declared name, a contract's or an alias's, and on a name nothing declares. Brackets after a type the language names other than `Array` and `Dictionary` **refuse at the load** |
| `some T` | a type parameter: worked out from the call, same reading everywhere it appears; bounded beside the first `some T` the signature's slots write, `some T: Standard.Comparable`. In a field of a struct listing it, the type a mention applies the struct to at its position |
| `Self` | the type conforming to a contract, written in that contract's procedures alone |
| `some T.Item`, `Self.Item` | an associated type: the type the type filling `T` gives under a name a contract bounding `T` asks, and in a contract's procedures the one the type conforming to the contract gives, under *the associated types of a type parameter* below |
| `Describable` (a declared contract's name) | a value of whatever type conforms to the contract. Nothing ties one slot's to another's |
| `Describable & Standard.Comparable` | a value of whatever type conforms to every contract named; two names or more, in name order, and each a contract's |
| `Int?` (any string spelling and `?`) | the Optional of the declared type, a sum of `Null` and the declared type: its none, and a some of each of the declared type's values. The Optional of an Optional is a type of its own, `Int??`, and so are `Null?`, `Any?` and `Never?` |
| `(Int, String) -> Bool` | a procedure type: the types it is called with in parentheses, in position order, and after `->` what it returns, which is all of the type the arrow is followed by, so `(Int) -> Int?` returns an Optional. No names, since a name is a declaration's and a value is called by position; a mark such as `inout` stands in front of a parameter's type, `(inout Int) -> Int`. Types not written in parentheses before `->` **refuse at the load** |
| `(Int) throws -> Bool` / `(Int) throws(aborted, cast_refused) -> Bool` | what a procedure type may fail with, written between its parameters and `->`: `throws` alone says anything, and `throws(…)` the failures it lists, in name order. Written without `throws`, it fails with nothing. `throws()` and a failure listed twice **refuse at the load** |
| `((Int) -> Int)?` / `(const Procedure)?` / `(some W: P)?` | the Optional of a type a `?` written straight after would stand inside: a procedure type, whose return type runs to the end of the spelling and whose modifiers stand in front of all of it, and a type parameter written with its bound, which runs to the end of the spelling too. Parentheses group such a type, so the `?` after them is the whole type's. Around any other type they write a second spelling of it, and **refuse at the load** |

**A type is written one way**, the spelling the writer gives it: no white space at either end of the string or of a type inside it, and none before `?`, `<` or `>`; one space after `some`, `inout`, `var`, `const` and `isolated`, and before `throws`; `, ` between the types brackets or parentheses hold and between the failures `throws(…)` lists, `: ` between `some T` and its bound, ` & ` between the names a bound or a composition joins, and ` -> ` around the arrow. A procedure type's modifiers stand `const` first, and its failures and a composition's names in name order. Any other string for one type, `Dictionary<String,Int>` or `Array< Int>`, is a second spelling and **refuses at the load**, as a document saying a thing another way does under [the document format](DOCUMENT.md).

**A type written inside another is one level deeper**: an element, a key or a value, a type a struct is applied to, a parameter or a return type, and what `?`, `inout` or `var` marks. A modifier and the parentheses that group add none. The levels count on from the containers around the type's string, against the bound of 128 a document's nesting has under [encoding](ENCODING.md): `Array<Int>` where 127 containers stand around its string is 128 deep, and `Array<Array<Int>>` there **refuses at the load**, before it is read further.

## Numbers and readings

**`Int` and `Double` are two types.** Neither takes the other: a value's type is fixed at the build, so an `Int` never stands where a `Double` is declared, and the reverse **refuses at the build** too. A slot that takes either kind of number is bounded by the contract `Standard.Numeric`, under [the standard vocabulary](VOCABULARY.md).

**A literal is read as the place it is written into reads it.** A place is a slot, a procedure's declared return type, a name that says what it holds, a write, a list's, a dictionary's or a struct's part there, what stands between a path's brackets (an `Int` on a list and the key type on a dictionary), the type a cast, `as` or `as?`, names, and a type parameter a call fills. A type parameter reads as what the readings of the call's arguments fill it with once they join, which is what the parameter's bounds are held to; a struct literal there fills nothing, and reads as the declared struct the others fill it with.

**An integer literal is a `Double` where its place reads a `Double`**, the `Double` it names. Where one value joins what was written beside it, a list literal's elements at every depth and a dictionary literal's keys and its values, an integer literal beside a `Double` is the `Double` it names too. Anywhere else it is an `Int`, and a name it is bound to holds an `Int`.

**Two readings of one place join part by part.** A reading beside itself reads itself, so `Null` beside `Null` reads `Null`. Null beside another reading reads that reading where it is an Optional and its Optional otherwise, and an Optional beside a reading other than `Null` reads the Optional of what its payload joins with that reading, or with that reading's payload where it is an Optional. Two lists join by their elements and two dictionaries by their keys and their values; two dictionaries whose keys join to `Any` read `Any` whole, since a dictionary's key conforms to `Hashable`. Two procedures join to a procedure that keeps the parameters and return type both write alike, the constness and isolation both carry and what either may fail with. Two parts that still differ read `Any`.

**Ways that each write a name are places of their own.** A write lands as what the name holds it as, so where two ways meet, one writing an integer literal beside another writing a `Double` reads `Any`, which a slot of a type takes only through a cast.

## What a slot takes, exactly

Where a value meets a declaration (an argument, a return value, and a write into a box that said what it holds), the judgement is one rule per type.

**`Any` accepts everything.** It passes the value through untouched, null and procedures included. Nothing is judged, because nothing was declared, beyond what every door holds of a struct's name, under *a declared struct is nominal* below.

**A value of a type the build does not know** is a value read as `Any` or as a contract. It stands where `Any` is declared and where a call fills a type parameter no bound holds, and a value read as a contract stands where a contract it is read as is asked, a bound among them; anywhere else it **refuses at the build**, and a cast says what it is.

**An empty list or dictionary reads as holding `Never`.** It holds no element, so it is a value of a list or a dictionary of any type.

**A declared struct says which fields there are**, and a struct under its name fits only with exactly them: one short and one over both **refuse**, each field is judged against its type, and the value is held as it came. To hand on fewer fields, write a struct literal of another declared struct; to keep keys a declaration does not name, declare `Dictionary<String, T>`, where the keys are the value's own.

**The door a value from outside comes through is the one place a value is fitted**: a field the declaration never named is left out of a struct under its name there, at whatever depth a struct, a list, a dictionary's key or value or an Optional holds it.

**A declared name whose structure is not a struct is an alias**, a second spelling of what it stands for: the build reads every mention of it as that type, so it takes, joins and conforms to contracts wherever that type does. One whose structure is a struct is nominal, under *a declared struct is nominal* below.

**An Optional (`T?`) takes three readings, in this order.** A reading of an Optional `U?` stands as it is where `T` takes `U` and `U` is as many Optional levels deep as `T` or more. A reading of `Null`, and the literal `null`, is its none, the outermost one whatever `T` is. A reading `T` takes is its some, so a reading of `Int?` where `Int??` is asked is a some of `Int?`. A `T?` reading does not fit a plain `T` slot, and the same holds a level down: a reading of `Int??` does not fit `Int?`.

**A some is the value itself**, except where the value is `null` or a `Some`: then it is the struct `Some` holding the value. Where a reading that may hold one of those, `Null`, `Any`, an Optional, a type parameter, an associated type, a contract or a composition, or an alias of one, meets an Optional as its some, the build writes the promotion down and the run puts `Some` on exactly the `null`s and `Some`s; everywhere else a some is the value as it came. A value of `T?` is `null`, a `Some` holding a value of `T` that is `null` or a `Some`, or a value of `T` that is neither, so the run judges a `Some` by what it holds. Taking one level off is the `unwrap` construct's, under [statements](STATEMENT.md): `null` is the none, a `Some` gives what it holds, and any other value gives itself. A variable handed in place is promoted nowhere, since it is the parameter's type all the way in, under [procedures](PROCEDURE.md).

**A list or a dictionary is promoted part by part.** A list whose elements read a type that may hold a none, where a list of their Optional is asked, is walked, and each element is its some, by value; a dictionary whose keys or values do is walked through them the same way, at any depth of lists and dictionaries. A procedure value is not walked, so it stands at another procedure type only where no value it is handed or returns would be promoted there: `() -> some T` where `() -> some T?` is asked **refuses at the build**.

**Ways that meet are no place.** A variable's ways meet at their readings joined, and where a value one way leaves would be promoted or have its type dropped to stand there, the build refuses and the variable declares its type, under *what a variable reads as* in [checking](CHECKING.md).

**A modifier stands in front of a procedure type**, so one in front of the Optional a `?` makes, `const Procedure?`, **refuses at the load**.

**The numeric edge is value-independent.** `Int` refuses every `Double`, `2.0` included, and `Double` every `Int`. A literal read as a `Double` names the binary64 value nearest it, so digits past 2^53 round as binary64 rounds.

**`Never` fits every slot**, by never arriving. It is a real type: an expression typed `Never` may be written where any value is expected, such as an argument that calls `Standard.Control.abort`, and evaluating it ends the evaluation it is inside. The statement rules (no name, nothing follows) are statement rules.

**`inout` and `var` say something about the slot and nothing about the value.** They stand in front of the whole type, `?` included: `inout Int?` is an Optional handed in place. What fits the slot is judged by the type after the mark. Writing either where it is not allowed **refuses at the load**.

**A slot asking `isolated` takes what is declared isolated.** Being const is a separate claim and does not stand in for it.

**A procedure-typed slot** takes a value that takes exactly the positions the slot's type hands, each accepting what the slot may hand at that position, returns what the slot's return type accepts, and fails with no more than the slot's type says it may fail with. What a closure may fail with is what its signature declares, as its constness is. The names the value's declaration wrote are its own and take no part: one closure fits two slots that name their parameter differently. That is held at the **build** where the value's type is known, and at the **run** where a cast reads a value read as `Any` or as a contract, under *one calling convention* in [procedures](PROCEDURE.md).

## A declared struct is nominal

**A struct type is written once**, as the structure of a type declared in `types`, `{ struct: { title: String, done: Bool } }` under the type's name, its fields under `struct`, each called anything; everywhere else a type names it. It is a name as well as a structure, and a value of it carries the name.

**A struct type is exact.** A declared struct fits a value under its own name and no other, so two declared structs of one structure under two names are two types, and a declared struct and `Dictionary<String, T>` of its fields take nothing of each other. A slot judges a value and hands it on as it came; it does not rebuild one. A struct under another name **refuses** at the **build** where the build can see the name and at the **run** at the door it comes through, and where a cast reads a value read as `Any` or as a contract, the cast fails with `cast_refused` and `as?` reads it as null. A declared name whose structure is not a struct, an alias, attaches no name.

**A struct literal is read as the declared struct its place reads**, as every literal is read as its place reads it. The build judges it there field by field against the declaration, exactly the declared fields, and it takes the struct's name. A struct literal written where no declared struct is read, at `Any`, at a contract, at a type parameter no call fills with a declared struct or at a name that declares nothing, **refuses at the build**.

**A value from outside holds a name only as a struct's.** At every door, whatever the slot declares, `Any` included, a struct under a name is held to the struct the name declares, fitted to it and judged against it, an alias's name becoming its struct's. One under a name that declares no struct **refuses at the run**, and so does a dictionary at a declared struct, which takes no dictionary. So every struct under a name is a value of that struct.

**A dictionary's key from outside is a value**, held there as its value is. Two keys of one dictionary that this makes one key, a struct under an alias's name beside one under its struct's or two structs apart only in a field left out, **refuse at the run**: a dictionary value holds its keys in the key order, so neither of the two is the later one.

**A declared struct may name itself** in a field, inside an Optional or as a list's element, so a tree is one declaration.

## A struct may take type parameters

**A struct lists its type parameters** in order under `typeParameters`, `{ struct: { item: "some T" }, typeParameters: [T] }`, and may hold each to contracts beside its name there, `typeParameters: ["K: Hashable", V]`, the way a signature does beside the first `some T`. A field writes one as `some T`. A field naming one the struct does not list, a field writing a bound, a name listed twice and an empty list each **refuse at the load**.

**A mention applies the struct to one type per parameter**, `Box<Int>`, `Box<some T>` in a signature, and is the struct with each parameter read as the type at its position, so every judgement above asks that of its fields. A type standing at a bounded position conforms to the contracts its bound names, a type parameter by its own bounds, the way a dictionary's key conforms to `Hashable`, or **refuses at the build** where the mention is written. A value of one carries the struct's name and its fields, and nothing of what it was applied to, as a list carries no element type.

**Two mentions of one struct are one type only where they are applied to the same types.** What a reading says of one value and no declaration writes is read as what is declared: an integer literal as the number it names, and `Never` as any type. A procedure type is the same type only where it declares the same constness, isolation and failing. So `Box<Int>` does not stand where `Box<Int?>` is declared, though a list of `Int` stands where a list of `Int?` is, and `Box<isolated () -> Int>` does not stand where `Box<() -> Int>` is; two readings applied to different types join to `Any`; and a constant holding one is the struct its expression was judged as, or, judged at `Any`, what its value reads as, its fields' readings joined.

**A call filling a type parameter walks into what the struct is applied to**, as into a list's element.

**A struct literal of one is read as applied to what its place applies the struct to.** Where the place leaves a position to a call, it is applied there to what the fields standing on that parameter read as, joined as a call's arguments fill a parameter, and to `Never` where no field reads one, as an empty list's element is.

**A door and a cast judge a value's fields against the struct applied to what the slot or the cast writes**, and an alias's name, `Pair: "Box<Int>"`, against the struct applied to what the alias writes. Where nothing does, at `Any`, a contract or a type parameter, a struct from outside reads as applied to its fields' readings joined, as a list value reads as its elements joined, and a bounded parameter is held to its bounds, which `Any`, what readings of several types join to, conforms to none: such a value **refuses at the run** at the door.

**An alias takes no type parameters**, and a mention applying one **refuses at the build**: what it stands for may be a struct applied to types, `Pair: "Box<Int>"`.

**A declared name that is no struct and comes back to itself** through what it stands for, through names alone, a `?` or a structure, spells no type and **refuses at the load**: a type that holds itself is a declared struct.

## Type parameters

**A declaration may leave a type parameter and let the call fill it**: a procedure taking `Array<some T>` and a `some T` returns what it was given.

**Inside the declaration the parameter is one type its body does not know**, so every place there that reads it takes only a value of it: the return value, a write into a variable of it or into a part of one, a parameter handed in place, and an argument at a slot a call fills from it. A reading of `Any` or of a contract, and a value of a type the bounds hold, is no value of the parameter, and each **refuses at the build**. A call reads the return value as what filled the parameter.

**A procedure handed to the call fills a parameter only where nothing else does.** It is a value, and what it takes at a position is what it accepts there, not a value the call hands: where anything else handed fills a parameter, the procedure is judged against what filled it, by the rule a procedure-typed slot takes a value, and only where nothing else fills it does what the procedure takes fill it. So a closure whose parameter writes no type, handed to `filter` beside a list of `Int`, leaves `Element` `Int`. Two positions of procedures taking it as two types, one of which takes the other, fill it with the one both take: `(Int) -> Int` beside a closure whose parameter writes no type fills it with `Int`.

**A call hands what filled each type parameter of the declaration it calls**, as the build read it, and the run holds those types while the body runs: a call the body makes hands on what it read, a type parameter of the body read as what filled it there. A door fills them from what the values handed in read as. A closure the body wrote holds the types of the call that made it, so wherever it goes it is a value of the procedure type its signature writes, each type parameter read as that call filled it.

**A list or dictionary literal written inside the declaration at a parameter is judged part by part**, each element, key or value against what the slot asks at it, and an empty list holds no element wherever in the literal it stands: `[]` is a value of `Array<some T>`, `[[], [x]]` of `Array<Array<some T>>` where `x` is one of `some T`, and a list of two dictionary literals, one holding `[]` under `a` and one holding `[x]` under `b`, of `Array<Dictionary<String, Array<some T>>>`.

**A call reads a literal handed to it as one type** to fill a parameter, its parts joined part by part, and handed beside such a parameter it is then judged part by part as a write is. A dictionary literal handed where a dictionary of the parameter is declared fills it with what each of its keys and values reads it as where it stands at the parameter, joined part by part as a list's elements are, an empty one holding no entry, and each key and value is held where it stands. Where bounds hold the parameter, only what stands at the parameter in a literal handed there is held to them, what a name the literal holds reads as included, and a closure in the literal is judged as any closure handed to its procedure type is.

**A parameter read twice must be read the same both ways.** Two readings where one accepts the other join to the one that holds both, position by position through lists, dictionaries and Optionals: a reading of `Any` makes its position `Any`, as it does the whole parameter, and elsewhere the looser stands. Two readings that do not fit **refuse at the build**, and do not widen to `Any`: two declared structs, or a declared struct and a dictionary, are two types neither of which takes the other. Appending an `Int` to a list of `String`s is a parameter read as `String` and as `Int`, and no type is both. A variable handed in place fills the parameters its slot names exactly, since it is the parameter's type all the way in, and a position handed by value is then a place at that filling, promoted there as any place promotes: appending a `some T` to a list of `some T?` handed in place fills `Element` with `some T?`, and the value appended stands there as its some. Among positions handed by value, two readings that join where a value at one position would change to stand at what the join fills its slot with, promoted to its some or its held type dropped at `Any`, **refuse at the build** too, the way ways that meet do: a slot `some T?` handed an `Int?` reads `T` as `Int`, and beside a reading of `Int?` the join would make the none handed there the some of `Int??`; a slot `some T` handed a value read as `Hashable` and one read as `Any` reads `T` as `Any`, where the first would drop the type it holds. A name declared at the type the call means says which.

**A reading that leaves, or an empty list's element, holds no value**, and a parameter only such readings read is filled with `Never`. So `[]` handed at `Array<some T>` reads as a list of any type, and a call returning that parameter alone reads `Never` and takes no name, the way a call of `Standard.Control.abort` does.

**A bounded parameter is one type.** Where bounds hold the parameter, what each argument hands there is held to them before its readings are joined, so a reading among them that does not conform **refuses at the build**, and so does a parameter the readings fill with `Any`, though each conforms.

## Bounds

**A type parameter is bounded where it is introduced**: beside the first `some T` the signature's slots write, the parameters in order and then the return type, at any depth, a procedure-typed slot's own types included, `parameters: [{ name: of, type: "some T: Standard.Comparable" }, { name: value, type: "some T" }]`. A bound written inside a procedure-typed slot is the declaring signature's, because that procedure type's parameters are the declaring signature's own slots. A head writes its own beside the names it applies, under *heads* below, and a struct beside the names it lists.

**The signature owns the bound and writes it once.** The other slots name the parameter and never the bound, so one bound is one claim however many slots mention the name, and a bound beside a later `some T` **refuses at the load**. Only `some T` names `T`, and `some T.Item` names none. Inside one type the order is the spelling's: a struct's or a dictionary's arguments in order, a procedure type's parameters in order before its return type.

**A bound holds every occurrence of the name** to what conforms to the contract the bound names, under *contracts* below. A bound may name several, joined with `&`: `some T: Describable & Standard.Comparable` holds `T` to what conforms to every one of them. A bound names contracts and nothing else, and what conforms to one is whatever type a document claims does, so the set a bound holds a parameter to is open.

**The judgement is the build's.** A reading whose type does not conform to the bound refuses (two booleans meeting `lessThan` never run), and so does a reading whose type the build does not know, under *what a slot takes, exactly* above. A cast judges what actually arrived at the **run** by what it reads as: the type it is an instance of, applied to what its parts read as, which is what a head is held to under *heads* below.

**An associated type is bounded under `bounds`.** What a signature does not introduce, an associated type of one of its type parameters, it bounds under `bounds`, keyed by its label, `bounds: { "T.Item": Hashable }`, beside what `sameTypes` says of it, under *the associated types of a type parameter* below. A key of `bounds` naming a type parameter, one standing on a parameter no slot mentions, and a bound a slot writes beside an associated type, `some T.Item: Hashable`, each **refuse at the load**.

**Only the declaring procedure, beside its first `some T` and under `bounds`, a head, a struct and a contract's `types` write a bound.** A bound written anywhere else a type is written, a field, an alias, a variable's or a name's declared type, a cast, a type member, a same type or a contract procedure's slot, **refuses at the load**, and a closure writes none, under [expressions](EXPRESSION.md).

**A closure written in the body, and a name the body declares the type of, read the same names**: a `some T` there is the `T` the caller filled, held to the bounds the declaration wrote, so a closure may send what the body around it may. One writing a `some T` the procedure around it does not declare, or written where no procedure is, **refuses at the load**.

**A bound names a contract.** One naming what no module declares as a contract **refuses at the build**, and one naming a type the language names or a struct the language declares, `Failure`, neither of which is a contract, **refuses at the load**.

**A type parameter lives where something fills it**: in a signature, filled by what a call hands; in a struct that lists it, filled by a mention; or in a head, filled by what the claim or the member is asked about. A declared type writing `some` for a name it does not list, an alias's included, and a signature naming one in what it returns and at none of its parameters, at any depth of a procedure-typed one included, each **refuse at the load**, because nothing there fills it.

## Contracts

**A contract says which procedures a type conforming to it gives**, and which types that type gives, under *associated types* below: the types that conform to it are open, and new ones arrive with new documents. A module declares one the way it declares a type: a name bound to the procedures it asks, under `procedures`, each written as a signature whose first parameter is `Self`, the type that conforms to the contract, since what fills `Self` there picks the procedure.

**`Self` is one type wherever it stands.** It may stand at any of the procedure's positions and in its return type, `Self?` included. A claim reads it as the type the claim is about, and `Self?` as the Optional of that type, for a claim about `Null` the Optional of `Null`. A call through the contract reads it as one type parameter the contract bounds, filled from the call the way any type parameter is.

**A contract's procedure takes `Self` first**, by value or in place: a variable handed there in place fills `Self` as a value does, so a contract may ask a procedure that changes the value it is called on, and a contract's variable written whole there holds on the type it held. One taking anything else first **refuses at the load**, the contract's own name included, since that is a value of whichever type conforms to it. `Self` written anywhere but a contract's procedures **refuses at the load**, and so does `some Self`.

**A contract may ask no procedures.** It is then a mark a claim gives a type, and a type conforms to it where a document claims it does, as for any contract.

**A contract's name stands where a type is written, and so does `A & B`**: the slot takes a value of whatever type conforms to every contract named. This is how the language says **A or B**: each type claims one contract and the slot names it. Either is a type parameter with no name, so nothing ties one slot's reading to another's, and a call fills nothing. A name that is not a contract's joined with `&` **refuses at the build**, and a type the language names or a struct the language declares joined with `&` **refuses at the load**.

**A value read as a contract is of a type the build does not know** and stands where *what a slot takes, exactly* above says: a value read as `A` does not stand where `B` is asked, and one read as `A & B` stands where either is.

**A value read as a contract holds the type it was read as.** Where a reading of a type that is no contract meets a contract, at an argument, a return, a write, a key a path reads or writes between brackets other than one folded from a constant, which holds the type it is an instance of, or a part of a list, dictionary or struct literal, and part by part where it meets a list, a dictionary or an Optional of a contract, the value is held beside that reading, which may name a type parameter, read as the call the body runs in filled it. A reading of a contract hands on the type its value holds, so a value read as `A & B` handed where `A` is asked holds what it held. A door, and a cast to a contract of a reading of `Any`, or of an Optional of `Any` whose value is its some, hold the type the value is an instance of. A cast to a contract of any other reading judges the type the value holds at that reading and holds it on: the reading, read as the call the body runs in filled it, and where that is a contract, or an Optional of one and the value its some, the type the value holds, so `maybe as? App.Described` of a `maybe` read as `Int?` is the none where `Int` conforms to `App.Described` and `Int?` does not. A cast to any other type judges the value. The type is the run's and no value's: it drops where the value meets `Any`, in the value and in every list, dictionary and struct field holding one, and where the run hands the host its result, what an entry answers. A native procedure is called by the run and what it returns comes back into the run, so a value it is handed, as an argument or as what a closure it calls or a procedure it sends returns, comes as the run holds it, the type included, and a value it hands back or writes through a parameter handed in place keeps the type it holds. A module variable's start and what a closure captured, which the build folds, keep the type they hold as well: the object writes the type beside the value, under [objects](OBJECT.md), and the link holds the value beside it again, in the box the variable starts in or in the closure. Sameness, `text` and a dictionary's keys read the value, so two keys that are one value are one key, holding what the entry the dictionary keeps holds.

**A value of a contract fills a bounded parameter only where the parameter stands alone.** A type parameter a contract bounds is one type wherever it stands, while a value of a contract is of whichever type conforms to it, so it fills one only where the parameter stands alone at one of the procedure's positions: `App.Described.describe` takes one, and a call handing one where the parameter stands twice, `Self` of `lhs` and `rhs` included, or inside a list, a dictionary or a struct, **refuses at the build**. A closure literal's parameter is such a slot too, and a call of the value holds what it hands to the contract by the rule a call to a declaration is held by. A value of a contract standing there fills the parameter with the type it holds, and the body takes the value. What the call returns is held at that type where the return type writes the parameter, and part by part through an Optional, a list and a dictionary of it, so a call whose return type writes the parameter inside a struct or a procedure type **refuses at the build** where a value of a contract fills it, `Self` included.

## Claims

**A type conforms to a contract when a document says it does.** A document says it where it gives the type what it gives it, under `satisfies`: a struct it declares beside its fields, `{ struct: { rank: Int }, satisfies: ["App.Describable"] }`, and any other type in an extension, keyed by the type, `extensions: { "Bank.Account": { satisfies: ["App.Describable"] } }`. Any document may make one, about a type it declared or about another document's, which is how a document that arrives later gives a type the procedures a contract asks.

**A type the language names is a type the way a declared one is**, and a claim may be about it: `extensions: { Int: { satisfies: ["App.Describable"], procedures: { describe: … } } }`, backed by its member `describe`.

**A claim written where a struct is declared, or under an extension keyed by a type's bare name, is about every value of the type.** A list and a dictionary are named bare `Array` and `Dictionary`: every list is an instance of `Array` whatever it holds, and a claim about `Array` is a claim about every list, one about `Dictionary` about every dictionary, so a declaration backing it takes one whatever it holds, a dictionary under whatever keys, `Dictionary<some K: Hashable, Any>`: a claim backed by one taking `Array<Int>` or `Dictionary<String, Any>` alone does not hold, and **refuses at the build**, at the claim. A list written as bytes is an instance of `Array` as every list is.

**A struct taking type parameters named bare is the same**: a claim about it is about every value of it whatever it is applied to, each parameter one no call fills, held to the bounds the struct declares, so a declaration backing it takes `Box<some T>`, and one taking `Box<Int>` alone does not hold.

**A claim is about a type.** An Optional is one, written by its `?` under *heads* below. `Any` and `Never` are types no value is an instance of by name, `Procedure` and a procedure type name a structure and no type, and `Self` names a type only inside a contract's procedures, so a claim about any of them **refuses at the load**, and a procedure conforms to no contract. A claim about a declared name that is not itself a struct, an alias included, **refuses at the build**: a value of a declared type is an instance of the struct it is, and of no other name. The document declaring an alias gives it nothing at all, and one that does **refuses at the load**.

## Heads

**An extension's key is its head**: a type's name, the type applied to what its brackets hold, `Array<Int>`, `App.Box<some T: Hashable>`, or an Optional, `Int?`. What an extension gives under a head applying its type holds for the values the head takes, the way a parameter written as the head takes an argument. `Array<Int>` takes every list of integers.

**An Optional's head is written by its `?`**, since no head or slot writes the Optional by name: `Int?` takes every reading of `Int?`, `some W?` every Optional, and `(some W: P)?` every Optional of what conforms to `P`.

**Each `some T` a head writes is the head's own type parameter**, held to the contracts written beside it where the head first names it, `some T: Hashable & Standard.Comparable`, so `App.Box<some T: Hashable>` takes every box of something that conforms to `Hashable`.

**A head is held as a parameter's type is**, being a mention of the type it applies: one applying a struct to what its bounds do not hold, or a dictionary to a key that does not conform to `Hashable`, **refuses at the build**, and so does a bound naming what no module declares as a contract. A head that is no type's name, no type applied to what its brackets hold and no Optional, one bounding a type parameter anywhere but where it first names it, and two keys of one document reading as one head **refuse at the load**.

**A claim under a head says the values it takes conform to the contract**: a reading the head takes conforms to it, and one it does not take **refuses at the build** where it is handed.

**A value conforms where it settles into the head.** A value carries no type's arguments, so where a value is what is judged, at a cast, a door and a call a constant folds through, it conforms where it settles into the head, the head's own type parameters filled by what its parts read as, the way a door fits a value to a slot writing the struct. Values meeting at one type parameter of a call or a struct from outside are one type where they are of one struct, each held to the bounds by what it is: a box holding `1` conforms by a claim under `App.Box<Int?>`, and a cast of a value the head does not take is null where it reads `as?`.

**What holds for some of a struct's values is written under a head applying it**, in the document declaring it as in any other, since a struct's declaration gives what every value of it has.

## A claim holds to members

**The build holds the claim to the type's members.** For every procedure the contract asks, it takes the type's member of that name (`Bank.Account`'s `describe`) and holds its signature to the contract's with the type in place of `Self` wherever the contract writes it. A name that stands for a declared struct names that struct's type there, as wherever types are compared, so a declaration may write another name for the struct the contract writes. A declaration that wrote no `returns` returns `Null`, and is held to that.

**Under a head applying the type, a member satisfies the requirement for every value the head takes.** The type there is the type as the head applies it, each of the head's type parameters one no call fills held to its bounds, so one taking `App.Box<Int>` alone does not back a claim under `App.Box<some T: Hashable>`.

**For every type the contract asks**, the build takes the type's type member of that name, under *associated types* below, and reads `Self.Item` as what it gives.

## What a document stands on

**A document stands on** the documents declaring what it names, on the documents those stand on, and on the claims it and they import: a claim imported is the claim, every copy of it the link holds, and not what the documents making it stand on, since the copies are one claim.

**A claim is imported by its pair**, under *a claim among the imports* in [documents](DOCUMENT.md).

**Whether a type conforms to a contract is judged at the build**, against the claims made within what the asking document stands on, the language's among them: a reading of a type no claim there is about, or one the claim's head does not take, conforms to nothing, and **refuses at the build** where it is handed. So what a document builds to is a fact of it and of what it stands on, whatever else the link holds.

**A door and a cast judge what arrives against every claim the link holds**, since what arrives is no reading any one document asked. A fold, which runs at the build, holds a value to the claims within its document's reach, and a cast it folds whose result turns on a type no claim within that reach is about, one that would succeed were the type to conform to the contract, **refuses at the build**, since the run reads every claim the link holds.

**A claim is judged where it is written**, against what its document stands on: a claim missing a procedure, or holding one whose signature does not fit or that does less than the contract asks, **refuses at the build, at the claim**, whether or not anything asks the contract of the type.

**A claim's two names are declared as what it needs of them.** A claim whose type the link declares as a contract, or whose contract it declares as a type, **refuses at the build, at the claim**. One name has one declarer, so no document arriving later makes that right.

**A type conforms to a contract one way.** Two documents claiming one type a contract under heads that take the same values are one claim: a claim holds nothing but the values and the contract, so the second says what the first said, whether it writes the head alike or as `App.Box<some U: Hashable>` beside `App.Box<some T: Hashable>`, through an alias, or as the type applied to its own parameters under its own bounds beside the bare name. Claims across documents under heads taking different values, `Array<Int>` and `Array<String>`, **refuse at the build**. One document says each thing one way, so it claiming one type a contract under a second head, however that head is spelled, **refuses at the load**.

## Members

**What a document gives a type under `procedures` are the type's members**, in the struct's declaration or in an extension. A member is a procedure under its type's name and its own with a dot between them, `Bank.Account.describe`, an Optional's under `Optional`, `Optional.describe`, the spelling a call writes, and it stands among the procedures as any declaration does: a procedure declared under that spelling, or a second member under it, is one name with two declarers, and **refuses at the load** in one document and **at the build** across documents. A member's name holds the grammar [checking](CHECKING.md) gives it.

**A type satisfies a contract's procedure by its member of that name**, given in the claim's document or in one that document stands on. So a claim written in an extension stands on the members a struct's declaration gives, and a claim written in a struct's declaration takes no member from an extension, which stands on the declaration and not the other way round.

**A document gives a struct it declares what it gives every value of it in the declaration**, so an extension of a struct the document declares under its bare name **refuses at the load**, and so does an extension giving nothing, which is a second way to write a document.

**A member takes a value of its type first**, by value or in place. A member is there for the values its head takes, and a call says which by what it hands first, so the member takes that value first. Under a head applying its type it is written as the head is written, its parameters' names and aliases as the head spells them: `App.Box.describe` given under `App.Box<some T: Hashable>` takes `App.Box<some T>` first. Under the type's bare name it takes every value of the type, written by the type's own name: what a claim under the bare name reads `Self` as, `Bank.Account`, `Array<Any>` or `App.Box<some T>`, and one taking only some of them, `Array<Int>` or `App.Box<Any>`, **refuses at the build**, since it is given under a head applying the type. One taking a value of another type first, or nothing, **refuses at the load**: a procedure that takes no value of a type, `Array.make` taking a `String`, is declared under `procedures` with that spelling.

**A member's type parameters the head names are held to the head's bounds** beside its own, so a call handing `App.Box.describe` a box of what does not conform to `Hashable` **refuses at the build**.

**An extension's head is held the way the type a claim is about is held**, whatever the extension gives: one naming a contract, or a declared name that is not itself a struct, an alias included, **refuses at the build** at the extension, and so does one naming what no module declares.

**A procedure spelled like a member and declared among a document's `procedures` is that document's procedure** and nothing more: it is no member, and satisfies no contract's procedure. So what a link declares never decides what an unrelated document may call things, and a document that names no contract builds the same whichever documents stand beside it.

## Associated types

**A contract may ask types as well as procedures**, its associated types. It lists their names under `types`, each one identifier and each once, `{ types: [Item], procedures: { first: { parameters: [Self], returns: "Self.Item" } } }`, and may hold each to contracts beside its name there, `types: ["Item: Hashable"]`, the way a struct holds a type parameter it lists; a name listed twice **refuses at the load**. Its procedures name one as `Self.Item`, the type the type conforming to the contract gives under that name, and one naming a type the contract does not ask **refuses at the load**.

**A type gives one by its type member of that name**, written under `types` beside `procedures` where the document gives the type what it gives it, `types: { Item: "some T" }`, in a struct's declaration or in an extension. Under a head a type member writes the head's own type parameters, in a struct's declaration the struct's, and under a bare head elsewhere none, so one taking the type's parameters is given under a head applying the type.

**A type member's name holds the grammar [checking](CHECKING.md) gives it**, and the type's name and its own with a dot between them, `App.Box.Item`, is its spelling, one type member per spelling: one document giving one type a type member under one name twice, under two heads, **refuses at the load**, and two documents giving it **refuse at the build**, as two declarers of a name do.

**A claim holds where the type gives every type the contract asks**: for each, the type's type member of that name is given in the claim's document or in one it stands on, under a head taking every value the claim's head takes, and its type, read under the claim's head, conforms to what the contract holds it to. A claim that does not **refuses at the build, at the claim**. Two contracts asking one name ask one type member of a type conforming to both.

## The associated types of a type parameter

**`some T.Item` is a type** where a contract bounding a type parameter `T` asks `Item`: the associated type `Item` of `T`, written in a signature, a closure's and a member's included, in a type member, and in what a name a body declares holds.

**A call fills it once it fills `T`**, from what fills `T`: the type member of a type a claim within reach says conforms to the contract, filled by what the type puts in the head the member was given under, or, where a type parameter of the caller fills `T`, the caller's own associated type, `some U.Item`. What the call's arguments read at `some T.Item` is that type, so a declaration taking `some T` and `some T.Item` handed a box of `Int` and a string **refuses at the build**.

**A value of a contract or of `Any` gives no associated type**, being of no one type, so a call filling `T` with one where the signature names `T.Item`, `Self.Item` of a call through the contract included, **refuses at the build**, and what holds no value gives what holds none.

**Inside the declaration an associated type is one type the body does not know**, under *type parameters* above, held to what each contract bounding `T` holds `Item` to and to what the signature's `bounds` say of it under `T.Item`, a slot writing `some T: Lib.Container` beside `bounds: { "T.Item": App.Describable }`. One a call fills from a parameter of the declaration around it is that declaration's own.

**A signature may say an associated type is a type under `sameTypes`**, `sameTypes: { "T.Item": Int }`: a call fills `T` only with what gives that type there, and inside the declaration it is that type. The type may name a type parameter a slot writes or another associated type, `"some U.Item"`, `"Array<some U>"`, which the call reads as it fills the slots, and what fills `T` gives there is held to that type exactly.

**What `sameTypes` may say.** A type parameter no slot writes, and an associated type `sameTypes` names itself or one standing on such, `some T.Item.Key` where it says what `T.Item` is, **refuse at the load**, and so do a key naming a type parameter rather than an associated type, one whose parameter no slot writes, and `sameTypes` written in a closure or a contract's procedure. A type that does not conform to what bounds the associated type **refuses at the build**, where it is written.

**An associated type may stand on another**: where a contract holding `Item` asks `Key`, `some T.Item.Key` is the associated type `Key` of `T.Item`, filled from what fills `T.Item` as that is filled from what fills `T`. An associated type no contract bounding what it stands on asks **refuses at the build** where it is written, and one whose type parameter no parameter of the signature writes, so no call fills it, **refuses at the load**.

**A struct's field and a head write no associated type.** A value carries no type's arguments and what fills a struct's parameters is read off its fields, which an associated type says nothing of, and a head is a type; either **refuses at the load**.

**At a door an associated type is what the type of the value at its parameter gives**, held to what bounds the associated type and to what `sameTypes` says it is, so a value standing at one is held to that type, and one of another, or a type that does not conform to those bounds or is not the type `sameTypes` says, **refuses at the run**.

## What the language declares

**The language declares four names itself**, which stand in every link ahead of its documents: the contract `Hashable` under *a dictionary's key* below, the structs `Failure`, which a catch binds, and `Round`, which a loop binds, under [statements](STATEMENT.md), and the struct `Some`, `{ struct: { wrapped: Any } }`, which holds `null` or a `Some` under [the value model](VALUE.md). A document declaring one of them **refuses at the load**. A mention of one of the first three is that declaration: a slot, a cast and a claim may name any of them, so `extensions: { Round: { satisfies: ["Hashable"] } }` keys a dictionary by `Round`, and a bound and a part joined with `&`, which name contracts, name `Hashable` alone. `Some` is how a value is held and no type a program reads, so a mention of it anywhere **refuses at the load**.

## A dictionary's key

**The language declares one contract, `Hashable`**, which asks no procedures and which the key of every dictionary type conforms to. The language claims it for `Null`, `Bool`, `Int`, `Double`, `String`, `Array` and `Dictionary`, and for every Optional of what conforms to it, under `(some Wrapped: Hashable)?`, and a declared struct conforms to it where a document claims it does: `{ struct: { x: Int }, satisfies: ["Hashable"] }`. Which keys are one key is the value model's sameness, under [the value model](VALUE.md), and no procedure decides it.

**Every dictionary type is keyed so, written or read.** A dictionary type whose key does not conform to `Hashable`, `Any`, a procedure type or a type parameter its bounds do not hold to it among them, **refuses at the build** where it is written, reached or not, and so does a dictionary literal whose keys read as such a type where its place declares no dictionary, since the literal reads as a dictionary keyed by what its keys join to; where the place declares a dictionary, each key is held to the key it declares. Whether a key conforms is judged against the claims within what the document stands on, under *what a document stands on* above.

**A constant's dictionary keeps the key its expression was read as.** A constant's type is its value's, so a dictionary it holds whose keys join to `Any` reads `Any` whole, as two dictionaries keyed apart do, except where the expression it folded from was read as a dictionary type, whose key it takes: folded from a call returning `Dictionary<Hashable, Int>`, a dictionary holding `1` and `"a"` is a value of that type.

## Calling a contract's procedure

**A body calls a contract's procedure by writing the contract's name and the procedure's with a dot between them**: `App.Describable.describe`. That spelling is the contract's declaration of the procedure, and it is a send like any other: a document calling a contract another module declares lists the spelling in `imports`. It names no type's declaration, and what it means is decided by the type that fills `Self` at its first position, so a call writing nothing there **refuses at the build**. What a call hands it and what it returns are the contract's, not any one declaration's.

**The build builds the table and the run reads it.** For every contract, the build gathers every type that conforms to it and lowers one call per type, each against the row that backs it, arguments in that row's own slot order. The build writes the type each position of the procedure reads as at the call, the contract's type parameters, `Self` among them, filled as the call fills them, and each may name a type parameter of the body the call stands in. The run reads those types, each such parameter as the call it runs in filled it, and picks by the name of the first, the type that fills `Self`. A reading of a contract there is read as the type the value standing first holds, and the row takes the value. An Optional's reading is picked by the name `Optional`, whatever value stands first. The row picked is handed what fills its type parameters as its parameters read them off those types, as any call fills them. Nothing is resolved while a program is running.

**A declaration satisfying a contract's procedure is reached through the contract**, which is the spelling that says which contract is meant. Two types satisfying one procedure is the ordinary case. Such a declaration takes exactly the contract's positions and returns what the contract's return type takes: its own type first, then at the contract's positions a parameter taking everything the contract's takes there and taking a place only where the contract hands one, the contract's type parameters standing for types no call fills and the declaration's own filled by what the contract writes at the same positions; the names are its own. One declaring a parameter beyond them, `T?` included, **refuses at the build**, at the claim. The run hands the arguments to the same positions whichever declaration satisfies it.

## Names

**A name is its declared spelling.** The key a document declares a type, contract or procedure under is the whole of its name: `Standard.Math.floored` is declared under that key, and `Wallet.Account` under that one. A mention is a declared spelling, written out, and it means the same declaration wherever it was written, inside the declaring document too. A spelling no module in the link declares **refuses at the build** where it is mentioned.

**A dot is a character of the spelling and nothing more.** The language has no nesting, no scope and no prefix, so what a document chooses to put before a dot is the author's convention, and one document may declare `Wallet.fee` beside `Bank.rate` while another declares `Wallet.rate`.

**There are two namespaces, procedures and types**, and a procedure may be spelled like a type. A contract's procedure stands in the first under its dotted spelling, which names one contract's procedure by the grammar in [checking](CHECKING.md), and a procedure a document declares under that same spelling **refuses at the build**. Types and contracts share the second, and no name in it is both, so a mention reaches whatever declares it: a slot names a type or a contract, and a bound names a contract.

**Every name in the second namespace, declared or mentioned, holds a type's name grammar**, and a type parameter's name its own, under [checking](CHECKING.md): a document declares no type under `Int` and names no type parameter `Int`, a mention spelled `a b` **refuses at the load**, and a mention of `Int` is the type the language names.

## The standard contracts

**The shared `Standard` bundle declares the contracts the standard procedures are bounded by**, `Standard.Numeric`, `Standard.Comparable` and `Standard.Collection`, claims them for the types the language names (`Int` and `Double` are numbers that order, `String` orders and has a count, `Array` and `Dictionary` have a count) and gives those types the members backing those claims, `Int.plus` and the rest, under [the standard vocabulary](VOCABULARY.md). A bundle whose signatures mention them links with `Standard` in the build.

## Cases

What `conformance/` asks about this page, by the name each case's file carries, under the section whose rule each measures.

How a type is written:

- `a-bare-array-refuses`
- `a-bare-dictionary-refuses`
- `a-contract-written-with-brackets-refuses`
- `a-declared-name-is-a-type`
- `a-declared-struct-beside-a-key-no-declaration-writes-refuses`
- `a-dictionary-type-written-with-one-type-refuses`
- `a-procedure-type-listing-a-failure-twice-refuses`
- `a-procedure-type-listing-its-failures-out-of-name-order-refuses`
- `a-procedure-type-without-parentheses-around-its-parameters-refuses`
- `a-procedure-type-writing-throws-takes-a-closure-that-may-fail`
- `a-procedure-type-writing-throws-with-no-failure-refuses`
- `a-procedure-types-return-type-runs-to-the-end-of-its-spelling`
- `a-procedure-value-at-a-slot-writing-a-procedure-type-refuses`
- `a-struct-another-document-declares-applied-to-another-count-refuses`
- `a-struct-applied-to-another-count-of-types-refuses`
- `a-struct-listing-no-type-parameters-applied-to-one-refuses`
- `a-struct-taking-type-parameters-named-without-brackets-refuses`
- `a-type-nested-past-the-bound-refuses`
- `a-type-nested-to-the-bound-is-read`
- `a-type-the-language-names-written-with-brackets-refuses`
- `a-type-written-in-another-spacing-refuses`
- `an-alias-applied-to-a-type-refuses`
- `an-integer-literal-one-way-writes-beside-a-double-is-no-double-refuses`
- `an-optional-procedure-type-is-written-in-parentheses`
- `inout-written-on-a-name-refuses`
- `inout-written-on-returns-refuses`
- `optional-written-with-brackets-refuses`
- `parentheses-around-a-procedure-type-no-question-mark-follows-refuse`
- `parentheses-around-a-type-parameter-written-without-its-bound-refuse`
- `parentheses-around-a-type-that-needs-none-refuse`

Numbers and readings:

- `a-dictionary-literal-reads-an-integer-key-beside-a-double-as-the-double`
- `a-list-holding-a-closure-that-may-fail-where-its-elements-fail-with-nothing-refuses`
- `a-list-of-two-dictionaries-whose-keys-join-to-any-holds-each-as-any-refuses`
- `a-struct-literal-beside-a-declared-struct-at-a-type-parameter-reads-as-that-struct`
- `an-array-of-bytes-and-a-list-of-numbers-at-a-list-of-strings-refuses`
- `an-int-a-name-holds-is-no-double-refuses`
- `an-integer-literal-at-a-double-slot-is-the-double`
- `an-integer-literal-beside-a-double-at-a-bounded-parameter-is-held-to-the-bound-as-the-double`
- `an-integer-literal-between-the-brackets-of-a-dictionary-keyed-by-doubles-is-the-double`
- `an-integer-literal-in-a-struct-beside-a-double-in-one-struct-reads-as-the-double`
- `elements-of-different-types-join-to-any`

What a slot takes, exactly:

- `a-call-of-a-value-read-as-any-refuses`
- `a-cast-between-aliases-of-two-optional-structs-reads-null`
- `a-closure-handed-in-place-failing-otherwise-than-the-slot-refuses`
- `a-closure-parameter-writing-no-type-at-an-associated-type-takes-any-refuses`
- `a-closure-taking-any-stands-where-its-slot-hands-a-contract`
- `a-closure-that-may-fail-where-the-procedure-type-fails-with-nothing-refuses`
- `a-closures-parameter-names-are-not-part-of-its-type`
- `a-dictionary-keyed-by-a-parameter-handed-as-keyed-by-its-optional-marks-its-nones`
- `a-dictionary-of-a-parameter-handed-as-a-dictionary-of-its-optional-marks-its-nones`
- `a-dictionary-of-an-alias-of-any-at-a-dictionary-of-a-contract-refuses`
- `a-double-where-an-int-is-declared-refuses`
- `a-generic-body-returning-its-parameter-as-an-optional-marks-a-none`
- `a-list-of-a-parameter-handed-as-a-list-of-its-optional-marks-its-nones`
- `a-list-of-a-reading-of-any-behind-a-name-handed-beside-a-variable-in-place-refuses`
- `a-list-of-an-alias-of-any-handed-to-a-value-at-a-list-of-a-contract-refuses`
- `a-modifier-in-front-of-an-optional-type-refuses`
- `a-name-of-an-optional-handed-where-its-optional-is-asked-is-its-some`
- `a-parameter-handed-in-place-holding-a-list-of-a-parameter-or-null-takes-null`
- `a-parameter-handed-in-place-holding-a-procedure-of-a-parameter-takes-a-closure-of-it`
- `a-parameter-read-as-a-declared-struct-and-its-alias-keeps-the-name`
- `a-procedure-returning-a-parameter-held-as-returning-its-optional-refuses`
- `a-reading-of-an-optional-of-an-optional-at-its-optional-refuses`
- `a-reading-of-any-at-a-contract-procedure-refuses`
- `a-reading-of-any-beside-an-int-at-a-contract-procedure-refuses`
- `a-reading-of-any-stands-at-an-alias-of-any`
- `a-return-value-read-as-any-where-a-type-is-declared-refuses`
- `a-struct-a-native-procedure-returns-short-of-its-fields-refuses`
- `a-type-parameter-written-optional-takes-a-value-of-the-parameter`
- `a-value-declaring-fewer-parameters-than-its-slot-hands-refuses`
- `a-value-from-outside-is-fitted-to-the-fields-declared`
- `a-value-read-as-any-sent-to-a-closure-held-at-a-procedure-type-refuses`
- `a-value-taking-a-parameter-in-place-at-a-slot-handing-a-value-refuses`
- `a-variable-written-an-alias-and-what-it-stands-for-holds-that-type`
- `an-alias-beside-what-it-stands-for-in-a-list-literal-joins-as-that-type`
- `an-alias-of-a-contract-stands-for-the-contract`
- `an-alias-of-a-struct-conforms-to-the-structs-contracts`
- `an-alias-of-any-another-document-declares-at-a-contract-slot-refuses`
- `an-alias-of-any-at-a-contract-slot-refuses`
- `an-alias-of-any-at-an-optional-contract-slot-refuses`
- `an-entry-handed-a-value-outside-its-declared-type-refuses`
- `an-inout-type-parameter-a-procedure-slot-fills-first-reads-the-value`
- `an-inout-type-parameter-a-variable-fills-first-reads-the-value`
- `an-optional-const-procedure-reads-as-written`
- `an-optional-of-an-optional-tells-its-inner-none-from-its-none`
- `an-optional-read-of-a-field-naming-an-alias-of-an-optional-reads-that-optional`
- `any-written-optional-holds-a-null-as-its-some`
- `never-written-optional-holds-only-its-none`
- `null-written-at-an-optional-of-an-optional-is-its-none`
- `null-written-optional-holds-null-as-its-some`
- `procedures-apart-only-by-an-alias-join-as-one-procedure-type`

A declared struct is nominal:

- `a-cast-of-an-alias-of-an-optional-struct-to-another-struct-refuses`
- `a-cast-of-an-optional-struct-to-another-struct-refuses`
- `a-declared-type-names-itself-in-its-fields`
- `a-dictionary-from-outside-whose-keys-the-door-makes-one-key-refuses`
- `a-dictionary-key-from-outside-under-a-name-no-document-declares-refuses`
- `a-dictionary-key-from-outside-under-an-alias-is-a-value-of-its-struct`
- `a-return-value-from-outside-at-any-under-a-name-no-document-declares-refuses`
- `a-return-value-from-outside-at-any-under-an-alias-is-a-value-of-its-struct`
- `a-return-value-from-outside-at-any-under-its-name-is-held-to-its-struct-refuses`
- `a-struct-arrives-as-an-argument`
- `a-struct-built-where-a-declared-struct-is-read-keeps-its-closure`
- `a-struct-declared-without-its-struct-key-refuses`
- `a-struct-from-outside-at-a-contract-slot-is-fitted-to-its-struct`
- `a-struct-from-outside-short-of-a-field-at-a-contract-slot-refuses`
- `a-struct-from-outside-under-another-name-refuses`
- `a-struct-from-outside-under-its-name-at-any-is-held-to-its-struct-refuses`
- `a-struct-literal-a-name-that-declares-nothing-holds-refuses`
- `a-struct-literal-at-a-type-parameter-nothing-fills-with-a-struct-refuses`
- `a-struct-literal-inside-a-struct-literal-at-a-type-parameter-refuses`
- `a-struct-literal-returned-where-a-declared-struct-is-returned-takes-the-name`
- `a-struct-literal-short-of-a-field-its-struct-declares-refuses`
- `a-struct-literal-written-where-no-declared-struct-is-read-refuses`
- `a-struct-naming-itself-applied-to-a-list-of-its-parameter`
- `a-struct-naming-itself-applied-to-its-parameter`
- `a-struct-type-may-name-a-field-for-a-form`
- `a-struct-under-another-name-refuses`
- `a-struct-written-where-a-type-is-written-refuses`
- `a-value-from-outside-under-a-name-no-document-declares-refuses`
- `a-value-from-outside-under-an-alias-at-any-is-a-value-of-its-struct`
- `an-alias-of-a-declared-struct-gives-a-value-from-outside-the-structs-name`

A struct may take type parameters:

- `a-call-fills-a-type-parameter-through-a-struct-applied-to-it`
- `a-cast-of-a-struct-applied-to-int-to-it-applied-to-string-refuses`
- `a-cast-of-a-struct-to-the-struct-applied-to-what-it-already-is-refuses`
- `a-cast-to-a-struct-applied-to-what-its-fields-do-not-hold-fails`
- `a-cast-to-a-struct-applied-to-what-its-fields-hold`
- `a-constant-of-a-struct-judged-at-any-reads-as-its-fields-joined-refuses`
- `a-constant-of-a-struct-keeps-what-it-was-applied-to-refuses`
- `a-field-of-a-struct-applied-to-int-read-as-string-refuses`
- `a-field-writing-a-bound-refuses`
- `a-field-writing-a-type-parameter-its-struct-does-not-list-refuses`
- `a-generic-procedure-returns-a-struct-applied-to-its-bounded-key`
- `a-list-of-structs-applied-to-a-type-parameter-fills-it`
- `a-module-variable-starting-at-a-struct-applied-to-an-empty-list-refuses`
- `a-procedure-returning-a-struct-of-an-empty-list-stands-at-it-applied-to-a-list-of-int`
- `a-procedure-returns-a-struct-applied-to-its-type-parameter`
- `a-signature-applying-a-struct-to-a-parameter-bounded-as-the-struct-asks`
- `a-signature-applying-a-struct-to-a-parameter-its-bounds-do-not-hold-refuses`
- `a-struct-another-document-declares-with-a-type-parameter-is-applied-here`
- `a-struct-applied-to-a-closure-from-a-call-stands-at-the-procedure-type-it-declares`
- `a-struct-applied-to-a-procedure-failing-nothing-where-it-is-applied-to-one-that-may-fail-refuses`
- `a-struct-applied-to-a-type-its-bound-does-not-take-refuses`
- `a-struct-applied-to-a-type-parameter-handed-in-place-takes-a-write-of-it`
- `a-struct-applied-to-an-isolated-procedure-where-it-is-applied-to-one-saying-nothing-refuses`
- `a-struct-applied-to-int-handed-in-place-is-written-through`
- `a-struct-applied-to-int-where-it-is-applied-to-int-or-null-refuses`
- `a-struct-applied-to-int-where-it-is-applied-to-string-refuses`
- `a-struct-applied-to-itself-reads-the-inner-field`
- `a-struct-applied-to-one-type-is-not-the-struct-applied-to-another-whatever-its-fields-refuses`
- `a-struct-field-holding-a-procedure-of-its-type-parameter-is-called`
- `a-struct-from-outside-at-a-slot-applying-it-to-int-or-null-holds-both`
- `a-struct-from-outside-at-any-holding-what-its-bound-does-not-take-refuses`
- `a-struct-from-outside-at-any-reads-as-its-fields-joined`
- `a-struct-from-outside-under-an-alias-of-a-struct-applied-to-int-is-held-to-int-refuses`
- `a-struct-from-outside-whose-fields-join-to-what-its-bound-does-not-take-refuses`
- `a-struct-holding-a-procedure-of-its-parameter-does-not-stand-applied-to-another-type-refuses`
- `a-struct-holding-an-empty-list-written-into-one-handed-in-place`
- `a-struct-listing-a-type-parameter-twice-refuses`
- `a-struct-listing-no-type-parameters-refuses`
- `a-struct-literal-at-a-generic-struct-applied-to-the-optional-of-a-parameter-promotes-its-field`
- `a-struct-literal-handed-at-a-struct-of-a-type-parameter-fills-it-from-its-fields`
- `a-struct-literal-holding-an-empty-list-beside-an-int-fills-a-call`
- `a-struct-literal-reading-its-type-parameter-two-ways-refuses`
- `a-struct-taking-a-type-parameter-holds-what-its-mention-applies-it-to`
- `a-type-reaching-itself-through-names-alone-refuses`
- `a-var-field-of-a-struct-taking-a-type-parameter-is-written-through`
- `an-alias-coming-back-to-itself-through-a-list-refuses`
- `an-alias-of-a-struct-applied-to-int-reads-as-it`
- `an-entry-returns-a-struct-applied-to-int`
- `reading-one-type-out-of-a-list-of-a-struct-applied-to-two-refuses`
- `two-structs-applied-to-one-type-in-a-list-join-to-it`

Type parameters:

- `a-body-handing-its-own-type-parameter-in-place-to-a-type-refuses`
- `a-body-returning-a-value-for-its-own-type-parameter-refuses`
- `a-body-writing-a-value-into-its-own-type-parameter-refuses`
- `a-bounded-parameter-read-as-string-and-as-any-refuses`
- `a-call-filling-a-parameter-from-a-variable-held-in-place-takes-a-value-of-that-parameter`
- `a-call-filling-a-parameter-from-a-variable-held-in-place-takes-no-other-value-refuses`
- `a-call-filling-a-parameter-from-the-bodys-own-and-a-reading-of-any-refuses`
- `a-cast-of-a-closure-appending-to-a-list-of-its-makers-parameter-fails`
- `a-cast-of-a-closure-over-a-type-parameter-its-making-call-filled-fails`
- `a-cast-of-a-closure-over-a-type-parameter-to-procedure`
- `a-cast-of-a-closure-taking-a-list-of-its-makers-parameter-in-place-fails`
- `a-cast-of-a-closure-taking-its-makers-parameter-by-value-to-one-taking-it-in-place-holds-it`
- `a-cast-of-a-closure-whose-return-value-a-caller-appends-in-place-fails`
- `a-cast-of-a-closure-writing-a-generic-return-type-carried-through-another-fails`
- `a-cast-of-a-closure-writing-a-return-type-read-as-never-fails`
- `a-cast-of-a-closure-writing-a-variable-handed-in-place-fails`
- `a-cast-of-a-closure-writing-where-a-declared-struct-was-filled-fails`
- `a-cast-of-a-setter-a-generic-procedure-made-fails-before-its-getter-reads`
- `a-cast-of-a-struct-holding-a-closure-over-a-type-parameter-reads-the-struct-its-maker-filled`
- `a-closure-a-generic-body-wrote-is-read-as-the-procedure-type-it-is-judged-against`
- `a-closure-a-generic-body-wrote-read-past-its-bounds-is-not-that-type`
- `a-closure-a-generic-body-wrote-taking-a-list-in-place-is-read-as-the-type-it-is-judged-against`
- `a-closure-alone-fills-a-parameter-with-what-it-takes`
- `a-closure-from-a-generic-body-is-the-procedure-type-its-maker-filled`
- `a-closure-parameter-saying-nothing-takes-the-element-the-list-beside-it-fills`
- `a-closure-taking-anything-beside-a-declared-struct-leaves-the-parameter-the-struct`
- `a-closure-taking-int-beside-a-declared-struct-refuses`
- `a-constant-holding-a-closure-from-a-generic-body-is-the-procedure-type-its-maker-filled`
- `a-dictionary-literal-handed-at-a-dictionary-of-a-bounded-parameter-fills-it-by-its-values-refuses`
- `a-dictionary-literal-of-keys-of-two-types-handed-at-a-dictionary-of-a-bounded-key-refuses`
- `a-dictionary-literal-of-values-of-two-types-handed-at-a-dictionary-of-a-bounded-parameter-refuses`
- `a-dictionary-literal-whose-values-do-not-join-handed-at-a-dictionary-of-a-bounded-parameter-refuses`
- `a-generic-body-appending-its-parameter-to-a-list-of-its-optional-promotes-it`
- `a-generic-return-value-of-any-refuses`
- `a-list-literal-of-closures-handed-at-a-bounded-parameter`
- `a-list-literal-of-closures-returning-outside-the-bounds-refuses`
- `a-list-literal-of-names-holding-lists-handed-at-a-bounded-parameter-refuses`
- `a-list-of-a-reading-of-any-handed-beside-a-variable-in-place-refuses`
- `a-literal-of-names-at-a-contract-bound-holds-each-to-its-claim-refuses`
- `a-parameter-declared-where-its-join-would-drop-a-held-type-takes-it`
- `a-parameter-filled-from-a-list-of-any-reads-any-which-a-cast-opens`
- `a-parameter-handed-in-place-handed-on-beside-a-list-of-an-empty-list`
- `a-parameter-handed-in-place-handed-on-beside-an-empty-list`
- `a-parameter-handed-in-place-handed-on-beside-an-empty-list-and-a-list-of-it`
- `a-parameter-handed-in-place-handed-on-beside-dictionaries-of-it-and-of-an-empty-list`
- `a-parameter-handed-in-place-handed-on-to-a-generic-beside-an-empty-list`
- `a-parameter-handed-in-place-holding-a-dictionary-of-a-parameter-takes-a-dictionary-of-it`
- `a-parameter-handed-in-place-holding-a-dictionary-of-lists-of-a-parameter-takes-a-dictionary-of-an-empty-list`
- `a-parameter-handed-in-place-holding-a-list-of-a-parameter-or-null-takes-a-list-of-it`
- `a-parameter-handed-in-place-holding-a-list-of-a-parameter-takes-an-empty-list`
- `a-parameter-handed-in-place-holding-dictionaries-of-a-parameter-takes-dictionaries-of-other-keys-of-it`
- `a-parameter-handed-in-place-holding-dictionaries-of-lists-of-a-parameter-takes-dictionaries-of-an-empty-list-and-of-it`
- `a-parameter-handed-in-place-holding-dictionaries-of-lists-of-a-parameter-takes-dictionaries-of-other-keys`
- `a-parameter-handed-in-place-holding-lists-of-a-parameter-takes-a-list-of-an-empty-list`
- `a-parameter-handed-in-place-holding-lists-of-a-parameter-takes-an-empty-list-beside-a-list-of-it`
- `a-parameter-handed-in-place-holding-optional-dictionaries-of-lists-of-a-parameter-takes-null-and-a-dictionary-of-an-empty-list`
- `a-parameter-handed-in-place-takes-no-reading-of-any-refuses`
- `a-parameter-read-where-its-join-would-change-a-value-refuses`
- `a-parameter-read-where-its-join-would-drop-a-held-type-refuses`
- `a-path-written-from-any-into-a-list-of-a-parameter-refuses`
- `a-procedure-a-call-filled-from-a-declared-struct-takes-no-int-refuses`
- `a-row-of-readings-of-any-appended-to-a-table-of-strings-refuses`
- `a-struct-literal-in-a-list-beside-a-list-of-another-struct-at-a-type-parameter-refuses`
- `a-struct-literal-in-a-list-handed-first-beside-a-list-of-another-struct-at-a-type-parameter-refuses`
- `a-type-parameter-read-as-any-and-as-a-type-holds-any`
- `a-type-parameter-read-loosely-and-tightly-holds-the-loose-reading`
- `a-type-parameter-read-two-ways-refuses`
- `a-type-parameter-two-procedures-take-as-int-and-as-anything-is-int`
- `a-variable-a-closure-took-written-from-any-refuses`
- `a-variable-a-closure-writes-from-any-refuses`
- `a-variable-a-closure-writes-with-a-value-of-the-parameter`
- `a-variable-handed-in-place-to-a-call-whose-cast-fails-stays-as-it-was`
- `an-empty-list-handed-to-a-generic-returns-a-list-of-any-type`
- `an-integer-literal-where-a-bounded-parameter-stands-refuses`
- `an-optional-cast-of-a-closure-over-a-type-parameter-its-making-call-filled-reads-null`

Bounds:

- `a-bound-beside-a-later-naming-of-a-type-parameter-refuses`
- `a-bound-beside-a-procedure-types-return-type-after-its-parameter-refuses`
- `a-bound-beside-an-associated-type-in-a-slot-refuses`
- `a-bound-naming-a-parameter-no-slot-mentions-refuses`
- `a-bound-naming-a-struct-a-document-declares-refuses`
- `a-bound-naming-a-struct-the-language-declares-refuses`
- `a-bound-naming-a-type-the-language-names-refuses`
- `a-cast-writing-a-bound-refuses`
- `a-closure-inside-a-closure-reads-the-bounds-of-the-procedure-around-them`
- `a-closure-naming-a-type-parameter-its-procedure-does-not-declare-refuses`
- `a-closure-reads-the-bounds-of-the-procedure-around-it`
- `a-closure-writing-bounds-refuses`
- `a-contract-bound-naming-a-type-the-language-names-refuses`
- `a-contract-bound-naming-no-contract-refuses`
- `a-contract-or-null-slot-takes-a-parameter-bounded-by-the-contract-and-another`
- `a-contract-procedure-writing-a-bound-refuses`
- `a-declaration-satisfying-a-contracts-procedure-reading-a-bounded-parameter-beside-any-refuses`
- `a-module-declares-a-contract-a-bound-names`
- `a-reading-of-any-at-a-bounded-parameter-refuses`
- `a-reading-outside-a-bound-refuses`
- `a-same-type-writing-a-bound-refuses`
- `a-some-outside-a-signature-refuses`
- `a-struct-bounded-by-a-struct-a-document-declares-refuses`
- `a-struct-bounded-by-a-type-the-language-names-refuses`
- `a-type-member-writing-a-bound-refuses`
- `a-type-parameter-bounded-under-bounds-refuses`
- `a-type-parameter-only-the-return-type-names-refuses`
- `a-value-conforming-to-one-contract-of-a-bound-naming-two-refuses`
- `an-associated-type-before-its-parameter-names-no-parameter`

Contracts:

- `a-box-of-a-contract-at-a-bounded-parameter-inside-it-refuses`
- `a-box-of-an-optional-fills-a-bounded-parameter-inside-it`
- `a-box-of-an-optional-is-taken-by-a-hashable-head`
- `a-cast-to-a-contract-of-a-reading-of-an-optional-holds-the-optional`
- `a-cast-to-a-contract-of-a-reading-of-an-optional-of-any-holding-a-some-reads-the-type-the-value-is-an-instance-of`
- `a-cast-to-a-contract-of-a-type-parameter-holds-what-the-call-filled-it-with`
- `a-cast-to-a-contract-of-a-type-parameter-the-call-filled-with-any-reads-the-type-the-value-is-an-instance-of`
- `a-claim-about-null-returns-null-where-the-contract-returns-the-optional-of-self`
- `a-claim-about-null-taking-a-list-of-null-where-the-contract-takes-a-list-of-the-optional-of-self-refuses`
- `a-claim-about-null-taking-null-where-the-contract-takes-the-optional-of-self-refuses`
- `a-closure-a-constant-holds-keeps-the-type-a-contract-value-it-captured-holds`
- `a-contract-carries-a-procedure-into-a-generic-body`
- `a-contract-or-null-slot-takes-a-type-conforming-to-the-contract`
- `a-contract-procedure-may-return-self-or-null`
- `a-contract-procedure-may-take-self-or-null`
- `a-contract-procedure-not-taking-self-first-refuses`
- `a-contract-procedure-returning-self-hands-a-struct-back-applied-as-it-came`
- `a-contract-procedure-taking-self-in-place-changes-the-variable-handed`
- `a-contract-procedure-taking-self-in-place-is-handed-a-variable-of-the-contract`
- `a-contract-procedure-taking-the-contract-first-refuses`
- `a-contract-procedure-writing-self-in-place-whole-keeps-the-type-the-variable-holds`
- `a-contract-slot-takes-no-optional-where-both-conform-refuses`
- `a-contract-stands-in-a-closures-parameter`
- `a-contract-stands-in-a-declared-types-field`
- `a-contract-stands-where-a-type-is-written`
- `a-contract-value-at-a-bounded-parameter-a-procedure-type-the-call-returns-writes-refuses`
- `a-contract-value-at-a-bounded-parameter-a-struct-the-call-returns-writes-refuses`
- `a-contract-value-at-a-bounded-parameter-fills-it-with-the-type-it-holds`
- `a-contract-value-at-any-is-its-value`
- `a-contract-value-returned-as-the-self-it-filled-holds-the-type-it-held`
- `a-contract-value-returned-at-the-bounded-parameter-it-filled-holds-the-type-it-held`
- `a-dictionary-keyed-by-a-contract-drops-the-types-its-values-hold-where-they-meet-any`
- `a-dictionary-literal-handed-at-a-dictionary-of-a-contract-holds-each-value-to-its-claim-refuses`
- `a-list-literal-at-a-list-of-a-contract-holds-each-element-as-it-was-read`
- `a-list-of-two-types-handed-where-a-contract-is-asked-is-read-element-by-element-refuses`
- `a-module-variable-declared-as-a-contract-holds-the-type-its-start-was-read-as`
- `a-name-for-an-optional-at-a-contract-no-optional-conforms-to-refuses`
- `a-name-that-is-not-a-contracts-joined-with-and-refuses`
- `a-named-list-at-a-list-of-a-contract-its-elements-do-not-conform-to-refuses`
- `a-none-read-as-a-contract-at-the-optional-of-the-contract-is-its-some`
- `a-slot-of-a-type-takes-no-value-read-as-a-contract-refuses`
- `a-struct-the-language-declares-joined-with-and-refuses`
- `a-type-no-claim-names-at-a-contract-asking-no-procedures-refuses`
- `a-type-no-claim-names-in-a-closures-contract-parameter-refuses`
- `a-type-not-conforming-to-the-contract-at-a-contract-or-null-slot-refuses`
- `a-type-parameter-named-self-refuses`
- `a-value-of-a-bounded-parameter-at-an-optional-of-its-contract-is-its-some`
- `a-value-of-a-contract-at-two-self-positions-refuses`
- `a-value-of-a-contract-inside-a-dictionary-at-a-bounded-parameter-refuses`
- `a-value-of-a-contract-inside-a-list-at-a-bounded-parameter-refuses`
- `a-value-of-a-contract-through-an-alias-fills-a-parameter-standing-twice-refuses`
- `a-value-outside-a-contract-in-a-closures-parameter-refuses`
- `a-value-outside-a-contract-standing-as-a-type-refuses`
- `a-value-read-as-a-contract-a-closure-a-native-procedure-calls-returns-holds-the-type-it-was-read-as`
- `a-value-read-as-a-contract-a-native-procedure-hands-back-holds-the-type-it-was-read-as`
- `a-value-read-as-a-contract-reaches-the-row-of-the-type-it-was-read-as`
- `a-value-read-as-a-contract-where-another-is-asked-refuses`
- `an-asking-cast-of-an-optional-to-a-contract-only-its-payload-claims-reads-null`
- `an-optional-at-a-contract-no-optional-conforms-to-refuses`
- `an-optional-of-a-parameter-at-a-contract-no-optional-conforms-to-refuses`
- `an-optional-only-the-optional-of-conforms-at-an-optional-of-the-contract-is-its-some`
- `self-in-a-return-type-is-what-the-call-filled-it-with`
- `self-outside-a-contract-refuses`
- `self-stands-for-the-type-conforming-to-a-contract`
- `what-claims-a-contract-asking-no-procedures-conforms-to-it`

Claims:

- `a-claim-about-a-struct-backed-for-it-applied-to-int-alone-refuses`
- `a-claim-about-a-struct-reads-its-parameters-held-to-the-structs-bounds`
- `a-claim-about-a-struct-taking-a-type-parameter-holds-for-every-value-of-it`
- `a-claim-about-an-alias-another-document-declares-refuses`
- `a-claim-about-an-alias-the-document-declares-refuses`
- `a-claim-about-an-optional-is-reached-through-its-contract`
- `a-claim-about-any-refuses`
- `a-claim-about-array-backed-for-a-list-of-ints-alone-refuses`
- `a-claim-about-never-refuses`
- `a-claim-about-null-holds-for-null`
- `a-claim-about-procedure-refuses`
- `a-claim-about-self-refuses`
- `a-claim-in-one-document-about-a-struct-another-declares-with-a-type-parameter`
- `a-dictionary-handed-through-a-claim-about-dictionary-reads-as-the-dictionary-it-is-refuses`
- `a-dictionary-keyed-by-a-struct-taking-a-type-parameter-claimed-hashable`
- `a-type-no-claim-names-refuses`
- `a-type-the-language-names-conforms-to-a-contract`

Heads:

- `a-bounded-head-takes-a-box-of-a-box-through-its-own-claim`
- `a-box-of-a-box-of-what-is-not-hashable-is-not-taken-by-a-bounded-head-refuses`
- `a-box-of-null-from-outside-is-taken-by-a-hashable-head`
- `a-cast-to-a-contract-holds-a-value-to-the-head-it-settles-into`
- `a-cast-to-a-contract-of-a-value-the-head-of-its-claim-does-not-take-reads-null`
- `a-cast-to-a-contract-reads-a-value-by-the-head-of-its-claim`
- `a-cast-to-a-contract-settles-a-box-of-a-box-through-its-own-claim`
- `a-claim-of-hashable-for-an-optional-beside-the-languages-refuses`
- `a-claim-under-a-head-another-document-makes-is-imported-and-holds`
- `a-claim-under-a-head-applying-a-list-to-int-holds-for-a-list-of-ints`
- `a-claim-under-a-head-bounding-its-parameter-holds-for-a-value-it-takes`
- `a-constant-folded-through-a-claim-under-a-head-holds-the-value-to-the-head`
- `a-dictionary-keyed-by-a-struct-its-conditional-claim-does-not-take-refuses`
- `a-dictionary-keyed-by-a-struct-its-conditional-claim-takes`
- `a-generic-body-handing-a-value-its-bounds-do-not-put-under-a-head-refuses`
- `a-generic-body-handing-a-value-its-bounds-put-under-a-head`
- `a-head-applies-a-struct-to-a-procedure-type`
- `a-head-applying-a-struct-to-a-parameter-its-bounds-do-not-hold-refuses`
- `a-head-bounding-a-type-parameter-where-it-is-named-again-refuses`
- `a-head-bounding-by-what-no-module-declares-as-a-contract-refuses`
- `a-head-bounds-a-type-parameter-inside-a-procedure-type`
- `a-head-writes-an-optional-procedure-type-in-parentheses`
- `a-head-writes-the-optional-of-a-bounded-type-parameter-in-parentheses`
- `a-list-of-strings-outside-a-head-applying-a-list-to-int-refuses`
- `a-member-under-a-head-is-called-for-a-value-the-head-takes`
- `a-struct-from-outside-holds-its-bounded-field-to-the-head-of-its-claim`
- `a-struct-of-two-parameters-not-taken-at-its-first-parameter-refuses`
- `a-value-from-outside-at-a-bounded-parameter-is-held-to-the-head-of-its-claim`
- `a-value-outside-a-head-another-document-claims-refuses`
- `a-value-outside-a-head-bounding-its-parameter-refuses`
- `an-extension-of-a-struct-the-document-declares-under-a-head-applying-it`
- `an-optional-cast-to-a-contract-of-a-box-of-a-box-of-what-is-not-hashable-reads-null`
- `an-optional-conforms-where-its-payload-does-under-its-head`
- `an-optional-whose-payload-does-not-conform-under-its-head-refuses`
- `two-extension-keys-reading-as-one-head-refuse`
- `values-from-outside-meeting-at-a-bounded-parameter-are-one-type-where-they-are-of-one-struct`

A claim holds to members:

- `a-claim-returning-another-type-for-self-item-key-refuses`
- `a-claim-returning-another-type-for-self-or-null-refuses`
- `a-declaration-satisfying-a-contracts-procedure-failing-with-what-the-contract-does-not-name-refuses`
- `a-declaration-satisfying-a-contracts-procedure-may-write-another-name-for-the-struct-the-contract-names`
- `a-declaration-satisfying-a-contracts-procedure-takes-the-claimed-type-wherever-the-contract-writes-self-refuses`
- `a-declaration-satisfying-a-contracts-procedure-with-another-return-type-refuses`
- `a-member-backing-a-claim-under-a-head-for-less-than-the-head-takes-refuses`
- `a-type-satisfies-a-contract-procedure-writing-an-associated-type-of-an-associated-type`

What a document stands on:

- `a-cast-at-the-run-reads-every-claim-of-the-link`
- `a-claim-a-document-two-steps-down-makes`
- `a-claim-another-document-makes-is-imported-and-holds`
- `a-claim-for-a-type-that-misses-a-procedure-refuses`
- `a-claim-in-a-document-the-program-names-nothing-of-refuses`
- `a-claim-naming-a-contract-where-the-type-belongs-refuses`
- `a-claim-naming-a-type-where-a-contract-belongs-refuses`
- `a-claim-two-documents-make-holds-for-a-document-standing-on-the-second`
- `a-copy-of-a-claim-that-does-not-hold-beside-one-that-does-refuses`
- `a-dictionary-key-claimed-only-beneath-an-imported-claim-refuses`
- `a-document-claiming-one-contract-for-a-type-under-two-heads-refuses`
- `a-null-cast-to-a-contract-is-held-to-the-claims-about-null`
- `a-type-member-is-read-through-an-imported-claim`
- `a-value-cast-from-any-to-a-contract-dispatches-by-the-type-it-is`
- `a-value-cast-from-any-to-a-contract-it-does-not-conform-to-fails`
- `an-unasked-claim-that-does-not-hold-refuses`
- `two-documents-claiming-one-contract-for-a-type-under-two-heads-refuse`
- `two-documents-claiming-one-contract-under-heads-taking-the-same-values-are-one-claim`
- `two-documents-claiming-one-contract-under-one-head-are-one-claim`
- `two-documents-claiming-one-pair-are-one-claim`

Members:

- `a-claim-whose-member-a-document-it-does-not-stand-on-gives-refuses`
- `a-declaration-no-claim-names-is-its-documents-own-procedure`
- `a-member-and-a-procedure-under-one-spelling-refuse`
- `a-member-is-called-by-its-types-name-and-its-own`
- `a-member-named-with-a-dot-refuses`
- `a-member-taking-no-value-of-its-type-first-refuses`
- `a-member-under-a-bare-name-bounding-its-parameter-refuses`
- `a-member-under-a-bare-name-taking-a-struct-applied-to-any-refuses`
- `a-member-under-a-bare-name-taking-some-of-its-values-refuses`
- `a-member-under-a-head-called-outside-its-bounds-refuses`
- `a-member-under-a-head-may-restate-the-heads-bounds`
- `a-member-under-a-head-taking-another-type-first-refuses`
- `a-procedure-spelled-like-a-member-backing-a-claim-refuses`
- `an-extension-giving-a-contract-members-refuses`
- `an-extension-giving-another-documents-alias-members-refuses`
- `an-extension-of-a-name-nothing-declares-refuses`
- `an-extension-of-a-struct-the-document-declares-refuses`
- `an-extension-writing-nothing-refuses`
- `two-documents-giving-one-type-one-member-refuse`

Associated types:

- `a-claim-under-a-bare-name-giving-an-item-nothing-holds-to-the-contracts-bound-refuses`
- `a-claim-whose-type-gives-no-type-the-contract-asks-refuses`
- `a-contract-asking-a-type-named-with-a-dot-refuses`
- `a-contract-listing-a-type-twice-refuses`
- `a-contract-procedure-naming-a-type-the-contract-does-not-ask-refuses`
- `a-struct-bounding-its-parameter-gives-an-item-the-contract-bounds`
- `a-type-member-given-outside-the-claims-reach-refuses`
- `a-type-member-given-twice-in-one-document-refuses`
- `a-type-member-given-twice-refuses`
- `a-type-member-named-with-a-dot-refuses`
- `a-type-member-outside-what-the-contract-holds-it-to-refuses`
- `a-type-member-under-a-bare-head-writing-a-parameter-refuses`
- `a-type-member-under-a-head-taking-fewer-values-than-the-claim-refuses`
- `an-optional-gives-the-associated-type-its-claim-gives`
- `two-contracts-asking-one-name-are-satisfied-by-one-type-member`

The associated types of a type parameter:

- `a-bound-on-an-associated-type-carries-a-call-through-another-contract`
- `a-call-fills-an-associated-type-only-a-cast-in-the-body-names`
- `a-call-fills-an-associated-type-only-a-closures-cast-names`
- `a-call-fills-an-associated-type-only-a-reading-in-the-body-reaches`
- `a-call-holds-a-list-at-a-list-of-an-associated-type-to-what-the-type-gives-refuses`
- `a-call-through-a-contract-of-a-value-of-it-reading-an-associated-type-refuses`
- `a-call-through-a-contract-reads-the-associated-type-of-the-value-it-hands`
- `a-call-through-a-contract-takes-no-null-where-the-type-gives-int-refuses`
- `a-caller-not-bounding-an-associated-type-refuses`
- `a-callers-bound-on-an-associated-type-carries-into-a-call`
- `a-callers-same-type-carries-into-a-call`
- `a-claim-about-a-list-gives-its-element-as-an-associated-type`
- `a-closure-handed-at-an-associated-type-takes-what-the-claim-gives`
- `a-closure-returning-an-associated-type-two-steps-from-its-parameter`
- `a-closure-taking-another-type-at-an-associated-type-refuses`
- `a-closure-writes-the-associated-type-of-the-procedure-around-it`
- `a-closure-writing-same-types-refuses`
- `a-constant-folds-through-an-associated-type`
- `a-contract-procedure-writing-same-types-refuses`
- `a-declaration-returning-an-associated-type-two-steps-from-its-parameter`
- `a-dictionary-keyed-by-an-associated-type-the-contract-holds-hashable`
- `a-door-holds-a-derived-associated-type-to-hashable-refuses`
- `a-door-holds-a-derived-associated-type-to-its-bound-refuses`
- `a-door-holds-a-list-at-a-list-of-an-associated-type-to-what-the-type-gives-refuses`
- `a-door-holds-a-same-type-of-a-generic-entry-refuses`
- `a-door-holds-a-value-at-an-associated-type-to-what-its-parameter-gives`
- `a-door-holds-an-associated-type-of-an-associated-type-to-the-head-refuses`
- `a-door-reads-a-same-type-naming-an-applied-struct`
- `a-door-takes-no-value-at-an-associated-type-of-another-type-refuses`
- `a-generic-body-hands-no-optional-value-where-an-associated-type-is-asked-refuses`
- `a-generic-call-takes-no-double-where-the-type-gives-int-refuses`
- `a-generic-call-takes-no-null-where-the-type-gives-int-refuses`
- `a-generic-call-takes-no-optional-variable-in-place-of-int-refuses`
- `a-head-writing-an-associated-type-refuses`
- `a-same-type-holds-an-associated-type-to-a-type`
- `a-same-type-naming-an-associated-type-it-says-is-a-type-refuses`
- `a-same-type-not-conforming-to-what-holds-the-associated-type-refuses`
- `a-same-type-of-a-type-parameter-refuses`
- `a-same-type-of-an-associated-type-standing-on-another`
- `a-same-type-takes-no-type-giving-another-refuses`
- `a-same-type-writing-a-type-parameter-no-slot-writes-refuses`
- `a-struct-field-writing-an-associated-type-refuses`
- `a-struct-from-outside-under-an-alias-of-an-applied-struct-fills-an-associated-type`
- `a-struct-of-two-parameters-gives-two-associated-types`
- `a-type-member-may-be-an-associated-type-of-its-heads-parameter`
- `a-value-of-a-contract-gives-no-associated-type-refuses`
- `an-associated-type-a-call-fills-from-the-callers-parameter-is-the-callers`
- `an-associated-type-is-one-type-the-body-does-not-know-refuses`
- `an-associated-type-may-stand-on-another`
- `an-associated-type-no-contract-bounding-its-parameter-asks-refuses`
- `an-associated-type-of-a-type-parameter-is-what-the-type-filling-it-gives`
- `an-associated-type-read-at-a-type-is-that-type-refuses`
- `an-associated-type-standing-on-one-no-contract-asks-it-of-refuses`
- `an-associated-type-whose-parameter-no-parameter-writes-refuses`
- `an-associated-type-writing-an-empty-member-refuses`
- `an-empty-list-fills-the-base-with-never-and-the-associated-type-takes-nothing-refuses`
- `an-optional-associated-type-bounded-hashable-fills-a-list`
- `an-optional-fills-no-associated-type-no-claim-about-it-gives-refuses`
- `two-associated-types-said-one-type-are-returned-as-one`
- `two-associated-types-said-the-same-giving-a-type-and-its-optional-refuse`
- `two-associated-types-said-the-same-giving-two-types-refuse`

What the language declares:

- `a-claim-about-a-struct-the-language-declares-keys-a-dictionary-by-it`
- `a-mention-of-some-refuses`
- `a-type-declared-under-a-name-the-language-declares-refuses`

A dictionary's key:

- `a-constant-of-keys-of-two-types-folded-from-a-call-returning-any-reads-any-refuses`
- `a-constant-of-keys-of-two-types-folded-from-a-hashable-keyed-dictionary`
- `a-dictionary-keyed-by-a-declared-struct-claimed-hashable`
- `a-dictionary-keyed-by-a-declared-struct-no-document-claims-hashable-refuses`
- `a-dictionary-keyed-by-a-struct-taking-a-type-parameter-no-document-claims-hashable-refuses`
- `a-dictionary-keyed-by-a-type-parameter-bounded-by-hashable`
- `a-dictionary-keyed-by-a-type-parameter-no-bound-holds-refuses`
- `a-dictionary-keyed-by-an-optional-holds-null-as-a-key`
- `a-dictionary-keyed-by-any-refuses`
- `a-dictionary-keyed-by-lists-finds-a-list-by-its-elements`
- `a-dictionary-literal-keyed-by-a-closure-refuses`
- `a-dictionary-literal-of-keys-of-two-types-written-where-a-hashable-keyed-dictionary-is-declared`
- `a-dictionary-literal-whose-keys-read-as-any-handed-through-a-contract-refuses`
- `a-dictionary-literal-whose-keys-read-as-any-refuses`
- `a-struct-bounding-its-key-parameter-holds-a-dictionary`
- `a-struct-keying-a-dictionary-by-an-unbounded-parameter-refuses`

Calling a contract's procedure:

- `a-call-through-a-contract-handed-a-name-hands-the-row-the-value-held`
- `a-call-through-a-contract-handed-a-variable-in-place-hands-the-row-the-value-held`
- `a-call-through-a-contract-with-nothing-first-refuses`
- `a-contract-procedure-names-what-it-may-fail-with`
- `a-declaration-satisfying-a-contracts-procedure-fills-its-own-parameter-with-the-contracts`
- `a-declaration-satisfying-a-contracts-procedure-may-fill-a-bounded-parameter-with-what-the-bound-takes`
- `a-declaration-satisfying-a-contracts-procedure-may-return-a-contract-where-it-promises-it-or-null`
- `a-declaration-satisfying-a-contracts-procedure-may-return-a-type-conforming-to-it-where-it-promises-it-or-null`
- `a-declaration-satisfying-a-contracts-procedure-may-return-an-alias-of-a-struct-conforming-to-it`
- `a-declaration-satisfying-a-contracts-procedure-may-return-an-alias-of-what-it-promises`
- `a-declaration-satisfying-a-contracts-procedure-may-return-another-contract-and-the-contract-where-it-promises-it-or-null`
- `a-declaration-satisfying-a-contracts-procedure-may-take-a-contract-or-null-where-it-writes-the-contract`
- `a-declaration-satisfying-a-contracts-procedure-may-take-a-value-where-it-hands-a-place`
- `a-declaration-satisfying-a-contracts-procedure-may-take-a-wider-type`
- `a-declaration-satisfying-a-contracts-procedure-may-take-any-where-it-writes-a-contract`
- `a-declaration-satisfying-a-contracts-procedure-may-take-anything-where-it-writes-a-parameter`
- `a-declaration-satisfying-a-contracts-procedure-names-its-parameters-its-own-way`
- `a-declaration-satisfying-a-contracts-procedure-returning-any-may-return-its-parameter`
- `a-declaration-satisfying-a-contracts-procedure-taking-in-place-where-it-hands-a-value-refuses`
- `a-declaration-satisfying-a-contracts-procedure-with-a-bounded-parameter-where-it-writes-a-parameter-refuses`
- `a-declaration-satisfying-a-contracts-procedure-with-a-bounded-parameter-where-it-writes-what-the-bound-refuses-refuses`
- `a-declaration-satisfying-a-contracts-procedure-with-a-contract-where-it-returns-another-refuses`
- `a-declaration-satisfying-a-contracts-procedure-with-a-type-not-conforming-to-it-where-it-promises-it-or-null-refuses`
- `a-declaration-satisfying-a-contracts-procedure-with-a-type-where-it-writes-a-contract-refuses`
- `a-declaration-satisfying-a-contracts-procedure-with-a-type-where-it-writes-a-parameter-refuses`
- `a-declaration-satisfying-a-contracts-procedure-with-an-optional-where-it-returns-a-contract-refuses`
- `a-declaration-satisfying-a-contracts-procedure-with-another-contract-where-it-writes-a-contract-refuses`
- `a-declaration-satisfying-a-contracts-procedure-with-any-where-it-asks-string-refuses`
- `a-declaration-satisfying-a-contracts-procedure-with-its-own-parameter-for-a-type-refuses`
- `a-declaration-taking-a-contracts-parameters-in-another-order-refuses`
- `a-declaration-taking-a-parameter-beyond-its-contracts-refuses`
- `a-generic-body-calls-through-a-contract-by-what-filled-its-parameter`
- `a-generic-body-filled-with-an-optional-reaches-the-optionals-row`
- `a-procedure-calling-itself-with-a-list-of-its-parameter-reaches-each-row`
- `a-row-picked-through-a-contract-fills-its-own-parameter-at-the-position-the-contract-reads`

Names:

- `a-bare-contract-name-refuses`
- `a-bare-name-for-another-modules-procedure-refuses`
- `a-bound-names-a-contract-another-document-declares`
- `a-contract-declared-twice-refuses`
- `a-contract-declared-under-a-spelling-that-is-no-name-refuses`
- `a-contract-is-named-by-its-qualified-spelling`
- `a-contract-procedure-named-with-a-dot-refuses`
- `a-name-declared-as-both-a-type-and-a-contract-refuses`
- `a-parameter-naming-a-type-nothing-declares-refuses`
- `a-procedure-declared-under-a-contracts-procedure-spelling-refuses`
- `a-type-declared-under-a-name-the-language-gives-refuses`
- `a-type-declared-under-a-word-a-type-spelling-writes-refuses`
- `a-type-declared-under-throws-refuses`
- `a-type-mention-that-is-no-name-refuses`
- `a-type-parameter-named-for-a-type-the-language-names-refuses`
