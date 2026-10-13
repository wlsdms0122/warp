# Types

What a name may stand for, and what a slot takes. A type is judged at the build against the declarations the grammar read; what a type *admits* is asked of a value where it meets a slot, at the build where its reading is known and at the run at a door or a cast. Reads [the value model](value.md). Read by procedures, statements and expressions, each of which writes a slot.

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
| `var <type>` | a field a path may write through; written on a field of a struct a type in `types` declares, and nowhere else |
| `Task` (any declared name) | the type a module declares under that name |
| `Box<Int>` (a declared struct and the types it is applied to) | the struct a module declares under that name with its type parameters read as the types between the brackets, in the order it lists them; another count, a struct that lists none named with brackets and one that lists some named without, **refuse at the build**, where the name resolves, and so do brackets on any other declared name, a contract's or an alias's, and on a name nothing declares. Brackets after a type the language names other than `Array` and `Dictionary` **refuse at the load** |
| `some T` | a type parameter: worked out from the call, same reading everywhere it appears; bounded when the signature's `bounds` names it. In a field of a struct listing it, the type a mention applies the struct to at its position |
| `Self` | the type answering a contract, written in that contract's procedures alone |
| `some T.Item`, `Self.Item` | an associated type: the type the type filling `T` gives under a name a contract bounding `T` asks, and in a contract's procedures the one the type answering the contract gives, under *the associated types of a type parameter* below |
| `Describable` (a declared contract's name) | a value of whatever type satisfies the contract. Nothing ties one slot's to another's |
| `Describable & Standard.Comparable` | a value of whatever type satisfies every contract named; two names or more, in name order, and each a contract's |
| `Int?` (any string spelling and `?`) | the declared type or null |
| `{ procedure: { parameters: [<type>, …], returns: …, failing: [<name>, …] } }` | a procedure type: the types it is called with, in position order, what it answers, and what it may fail with, an array of failure names as a contract's procedure writes it: left out, the procedure may fail with anything, and `[]` says it fails with nothing. No names, since a name is a declaration's and a value is called by position; a mark such as `inout` is written on the type it stands in front of |
| `{ "const procedure": { … } }` | a procedure type with its marks and modifiers on the key, `inout` first, then `const` and `isolated`, the way they stand in front of the string form |
| `{ array: <type> }` / `{ dictionary: { key: <type>, value: <type> } }` | a list / map of a procedure type that writes its signature, which has no string spelling. Where every type inside has a spelling the type is written `Array<T>` or `Dictionary<K, V>`, and the form around it **refuses at the load** |

`Int` and `Double` are two types, and neither takes the other: a value's type is fixed at the build, so a whole number never stands where a fraction is declared, and the reverse **refuses at the build** too. A literal is read as the place it is written into reads it, where a place is a slot, an answer, a name that says what it holds, a write, a list's, a map's or a struct's part there, what stands between a path's brackets, which reads an `Int` on a list and the key type on a map, the type a cast, `as` or `as?`, names, and a type parameter a call fills, read as what the readings of the call's arguments fill it with once they join, which is what the parameter's bounds are held to; a struct literal there fills nothing, and reads as the declared struct the others fill it with. A whole number written as a literal is read as the fraction it names where its place reads a `Double`. Where one value joins what was written beside it, a list literal's elements at every depth and a map literal's keys and its values, a whole literal beside a fraction is the fraction it names too. Anywhere else it is an `Int`, and a name it is bound to holds an `Int`. Two readings of one place join part by part: null beside a value reads as what may be null, two lists join by their elements and two maps by their keys and their values, two maps whose keys join to `Any` reading `Any` whole, since a map's key answers `Hashable`, and two procedures to a procedure that keeps the parameters and answer both write alike, the constness and isolation both carry and what either may fail with; two parts that still differ read `Any`. Where ways that each answer meet, each way out of a body that writes no `returns` and each of an attempt's two ways is a place of its own, so one answering a whole literal beside another answering a fraction reads `Any`, which a slot of a type takes only through a cast. `Any` accepts everything. A slot that takes either kind of number is bounded by the contract `Standard.Numeric`, under [the standard vocabulary](vocabulary.md).

**A declared struct is nominal.** A struct type is written once, as the structure of a type declared in `types`, `{ struct: { title: String, done: Bool } }` under the type's name, its fields under `struct`, each called anything; everywhere else a type names it. It is a name as well as a structure, and a value of it carries the name. A struct type is exact: a declared struct fits a value under its own name and no other, so two declared structs of one structure under two names are two types, and a declared struct and `Dictionary<String, T>` of its fields take nothing of each other. A slot judges a value and hands it on as it came; it does not rebuild one. A struct literal is read, as every literal is, as the place it is written into reads it: the declared struct that place reads. The build judges it there field by field against the declaration, exactly the declared fields, and it takes the struct's name. A struct literal written where no declared struct is read, at `Any`, at a contract, at a type parameter no call fills with a declared struct or at a name that declares nothing, **refuses at the build**. A struct under another name **refuses** at the **build** where the build can see the name and at the **run** at the door it comes through, and where a cast reads a value read as `Any` or as a contract, the cast fails with `cast_refused` and `as?` reads it as null. A declared name whose structure is not a struct, an alias, attaches no name. A value from outside holds a name only as a struct's: at every door, whatever the slot declares, `Any` included, a struct under a name is held to the struct the name declares, fitted to it and judged against it, an alias's name becoming its struct's, and one under a name that declares no struct **refuses at the run**, and so does a map at a declared struct, which takes no map. A map's key is a value, held there as its value is, and two keys of one map that this makes one key, a struct under an alias's name beside one under its struct's or two structs apart only in a field left out, **refuse at the run**: a map value holds its keys in the key order, so neither of the two is the later one. So every struct under a name is a value of that struct. A declared struct may name itself in a field, nullable or as a list's element, so a tree is one declaration.

**A struct may take type parameters.** It lists them in order under `typeParameters`, `{ struct: { item: "some T" }, typeParameters: [T] }`, and may hold each to contracts under `bounds` the way a signature does, `bounds: { K: Hashable }`; a field writes one as `some T`, and a field naming one the struct does not list, a bound naming one, a name listed twice and an empty list each **refuse at the load**. A mention applies the struct to one type per parameter, `Box<Int>`, `Box<some T>` in a signature, and is the struct with each parameter read as the type at its position, so every judgement above asks that of its fields. A type standing at a bounded position answers the contracts its bound names, a type parameter by its own bounds, the way a map's key answers `Hashable`, or **refuses at the build** where the mention is written. A value of one carries the struct's name and its fields, and nothing of what it was applied to, as a list carries no element type. Two mentions of one struct are one type only where they are applied to the same types, what a reading says of one value and no declaration writes read as what is declared: a whole literal as the number it names, `Never` as any type, and a procedure as its positions and answer, the constness, isolation and failing derived for it meeting what is declared: `Box<Int>` does not stand where `Box<Int?>` is declared, though a list of `Int` stands where a list of `Int?` is, two readings applied to different types join to `Any`, and a constant holding one is the struct its expression was judged as, or, judged at `Any`, what its value reads as, its fields' readings joined. A call filling a type parameter walks into what the struct is applied to as into a list's element. A struct literal is read as applied to what its place applies the struct to, and where the place leaves a position to a call, to what the fields standing on that parameter read as, joined as a call's arguments fill a parameter, `Never` where no field reads one, as an empty list's element is. A door and a cast judge a value's fields against the struct applied to what the slot or the cast writes, and an alias's name, `Pair: "Box<Int>"`, against the struct applied to what the alias writes. Where nothing does, at `Any`, a contract or a type parameter, a struct from outside reads as applied to its fields' readings joined, as a list value reads as its elements joined, and a bounded parameter is held to its bounds, which `Any`, what readings of several types join to, answers none: such a value **refuses at the run** at the door. A procedure type that writes its signature has no string spelling, and one standing at a position is reached through a declared name, as a nullable one is. An alias takes no type parameters, and a mention applying one **refuses at the build**: what it stands for may be a struct applied to types, `Pair: "Box<Int>"`. A declared name that is no struct and comes back to itself through what it stands for, through names alone, a `?` or a structure, spells no type and **refuses at the load**: a type that holds itself is a declared struct.

`inout` and `var` stand in front of the whole type, `?` included: `inout Int?` is a nullable handed in place. They stand in front of a string spelling or on the key a procedure type is written under. They say something about the slot and nothing about the value, so what fits the slot is judged by the type after the procedure. Writing either where it is not allowed **refuses at the load**. A slot asking `isolated` takes what the build derived as isolated. Answering without running is a separate claim and does not stand in for it. A value standing in a procedure-typed slot takes exactly the positions the slot's type hands, each accepting what the slot may hand at that position, answers what the slot's `returns` accepts, and fails with no more than the slot's `failing` names where it names anything. What a closure may fail with is read off its body, as its constness is. The names the value's declaration wrote are its own and take no part: one closure fits two slots that name their parameter differently. That is held at the **build** where the value's type is known, and at the **run** where a cast reads a value read as `Any` or as a contract, under *one calling convention* in [procedures](procedure.md).

**What a slot takes, exactly.** Where a value meets a declaration (an argument, an answer, and a write into a box that said what it holds), the judgement is one rule per type:

- `Any` passes the value through untouched, null and procedures included. Nothing is judged, because nothing was declared, beyond what every door holds of a struct's name, under *a declared struct is nominal* above.
- A value read as `Any`, as a contract, or along a path a call decides through a type parameter is of a type the build does not know. It stands where `Any` is declared and where a call fills a type parameter no bound holds, and a value read as a contract stands where a contract it is read as is asked, a bound among them; anywhere else it **refuses at the build**, and a cast says what it is. An empty list or map reads as holding `Never`: it holds no element, so it is a value of a list or a map of any type.
- A **declared struct** says which fields there are, and a struct under its name fits only with exactly them: one short and one over both **refuse**, each field is judged against its type, and the value is held as it came. To hand on fewer fields, write a struct literal of another declared struct; to keep keys a declaration does not name, declare `Dictionary<String, T>`, where the keys are the value's own. The door a value from outside comes through is the one place a value is fitted: a field the declaration never named is left out of a struct under its name there, at whatever depth a struct, a list, a map's key or value or what may be null holds it.
- A **declared name** whose structure is not a struct is an alias, a second spelling of what it stands for: the build reads every mention of it as that type, so it takes, joins and answers wherever that type does. One whose structure is a struct is nominal, under *a declared struct is nominal* above.
- A **nullable** (`T?`) passes null through and judges anything else against the declared half. `T?` takes `T`, null and `T?`; a `T?` reading does not fit a plain `T` slot. The `?` is written once, on the whole spelling, and only where it says something new: `Int??`, `Null?`, `Any?`, `Never?` and `some T?` each **refuse at the load**, and the same `?` behind a declared name standing for one of them **refuses at the build**, where the name resolves. A procedure type that writes its signature has no string spelling and no `?` to trail; a nullable one is reached through a declared name.
- The numeric edge is value-independent: `Int` refuses every fraction, `2.0` included, and `Double` every whole number. A literal read as a fraction names the binary64 fraction nearest it, so digits past 2^53 round as binary64 rounds.

`Never` is a real type and fits **every** slot, by never arriving: an expression typed `Never` may be written where any value is expected, such as an argument that calls `Standard.Control.abort`, and evaluating it ends the evaluation it is inside. The statement rules (no name, nothing follows) are statement rules.

**Type parameters.** A declaration may leave a type parameter and let the call fill it: a procedure taking `Array<some T>` and a `some T` answers what it was given. Inside the declaration the parameter is one type its body does not know, so every place there that reads it takes only a value of it: the answer, a write into a variable of it or into a part of one, a parameter handed in place, and an argument at a slot a call fills from it. A reading of `Any` or of a contract, and a value of a type the bounds hold, is no value of the parameter, and each **refuses at the build**; a call reads the answer as what filled the parameter. A procedure handed to the call is a value, and what it takes at a position is what it accepts there, not a value the call hands: where anything else handed fills a parameter, the procedure is judged against what filled it, by the rule a procedure-typed slot takes a value, and only where nothing else fills it does what the procedure takes fill it, so a closure whose parameter writes no type, handed to `filter` beside a list of `Int`, leaves `Element` `Int`. Two positions of procedures taking it as two types, one of which takes the other, fill it with the one both take: `(Int) -> Int` beside a closure whose parameter writes no type fills it with `Int`. The run does not know what filled it either, so a closure the body wrote that names the parameter in its own signature is, outside the call that made it, a value of no procedure type that writes a signature, and a value of `Procedure`, which writes none: a door handing one in at such a type **refuses at the run**, and a cast reading one as such a type fails with `cast_refused`. A list or map literal written there is judged part by part, each element, key or value against what the slot asks at it, and an empty list holds no element wherever in the literal it stands: `[]` is a value of `Array<some T>`, `[[], [x]]` of `Array<Array<some T>>` where `x` is one of `some T`, and a list of two map literals, one holding `[]` under `a` and one holding `[x]` under `b`, of `Array<Dictionary<String, Array<some T>>>`. A call reads a literal handed to it as one type to fill a parameter, its parts joined part by part, and handed beside such a parameter it is then judged part by part as a write is. A map literal handed where a map of the parameter is declared fills it with what each of its keys and values reads it as where it stands at the parameter, joined part by part as a list's elements are, an empty one holding no entry, and each key and value is held where it stands. Where bounds hold the parameter, only what stands at the parameter in a literal handed there is held to them, what a name the literal holds reads as included, and a closure in the literal is judged as any closure handed to its procedure type is. A parameter read twice must be read the same both ways. Two readings where one accepts the other join to the one that holds both, position by position through lists, dictionaries and what may be null: a reading of `Any` makes its position `Any`, as it does the whole parameter, and elsewhere the looser stands; a reading that leaves, or an empty list's element, holds no value, and a parameter only such readings read is filled with `Never`, so `[]` handed at `Array<some T>` answers a list of any type, and a call answering that parameter alone reads `Never` and takes no name, the way a call of `Standard.Control.abort` does; two readings that do not fit **refuse at the build**, and do not widen to `Any`: two declared structs, or a declared struct and a map, are two types neither of which takes the other. Where bounds hold the parameter, what each argument hands there is held to them before its readings are joined, so a reading among them that does not answer **refuses at the build**, and so does a parameter the readings fill with `Any`, though each answers: a bounded parameter is one type. Appending a whole number to a list of text is a parameter read as text and as a number, and there is no answer that is both.

**Bounds.** A type parameter may be bounded: a signature declares `bounds: { T: Standard.Comparable }` once, its slots write `some T`, and every occurrence of the name takes only what answers the contract the bound names, under **Contracts** below. A bound may name several, joined with `&`: `bounds: { T: Describable & Standard.Comparable }` holds `T` to what answers every one of them. The signature owns the bound. A slot names the parameter and never the bound, so one bound is one claim however many slots mention the name. A bound names contracts and nothing else, and what answers one is whatever type a document claims does, so the set a bound holds a parameter to is open. The judgement is the **build**'s: a reading whose type does not answer the bound refuses (two booleans meeting `lessThan` never run), and so does a reading whose type the build does not know, under *what a slot takes, exactly* above; a cast judges what actually arrived at the **run** by what it reads as: the type it is an instance of, applied to what its parts read as, which is what a head is held to under **Heads** below. `bounds` naming a parameter no slot mentions, itself or through an associated type, refuses at the load, and a key may name an associated type of one, `T.Item`, under *the associated types of a type parameter* below. Only the declaring procedure writes `bounds`, and a closure writes none, under [expressions](expression.md); a head writes its own beside the names it applies, under **Heads** below. A procedure *type* nested in a slot carries none, because its parameters are the declaring signature's own slots and the declaring signature owns their bounds. A closure written in the body reads the same names: its `some T` is the `T` the caller filled, held to the bounds the declaration wrote, so a closure may send what the body around it may, and one writing a `some T` the procedure around it does not declare, or written where no procedure is, **refuses at the load**. A bound naming what no module declares as a contract **refuses at the build**, and one naming a type the language names or a struct the language declares, `Failure`, neither of which is a contract, **refuses at the load**. And a type parameter lives in a signature and is filled by what a call hands, in a struct that lists it and is filled by a mention, or in a head and is filled by what the claim or the member is asked about: a declared type writing `some` for a name it does not list, an alias's included, and a signature naming one in what it answers and at none of its parameters, at any depth of a procedure-typed one included, each **refuse at the load**, because nothing there fills it.

**Contracts.** A contract says which **procedures** a value answers, and which types its type gives, under *associated types* below: the types that answer it are open, and new ones arrive with new documents. A module declares one the way it declares a type: a name bound to the procedures it asks, under `procedures`, each written as a signature whose first parameter is `Self`, the type that answers the contract, since the value standing there is the one the procedure is answered about. `Self` may stand at any of the procedure's positions and in its answer, `Self?` included, and it is that one type wherever it stands: a claim reads it as the type the claim is about, and `Self?` as that type or null, which for a claim about `Null` is `Null` itself, so a declaration backing such a claim writes `Null` there, at a parameter as in its answer, and a call through the contract reads it as one type parameter the contract bounds, filled from the call the way any type parameter is. A contract's procedure taking anything else first **refuses at the load**, the contract's own name included, since that is a value of whichever type answers it, and so does one taking `inout Self` first, since a call through the contract picks the declaration by the value standing there and a place handed in is no value. `Self` written anywhere but a contract's procedures **refuses at the load**, and so does `some Self`.

A contract's name stands where a type is written, and so does `A & B`: the slot takes a value of whatever type satisfies every contract named. This is how the language says **A or B**: each type claims one contract and the slot names it. Either is a type parameter with no name, so nothing ties one slot's reading to another's, and a call fills nothing. A value read as a contract is of a type the build does not know and stands where *what a slot takes, exactly* above says: a value read as `A` does not stand where `B` is asked, and one read as `A & B` stands where either is. A reading of what may be null is a value of the type or of `Null`, so it answers a contract where both do. A type parameter a contract bounds is one type wherever it stands, while a value of a contract is of whichever type answers it and a value of what may be null of the type or `Null`, so either fills one only where the parameter stands alone at one of the procedure's positions: `App.Described.describe` takes one, and a call handing one where the parameter stands twice, `Self` of `lhs` and `rhs` included, or inside a list or a map, **refuses at the build**. A closure literal's parameter is such a slot too, and a call of the value holds what it hands to the contract by the rule a call to a declaration is held by. A name that is not a contract's joined with `&` **refuses at the build**, and a type the language names or a struct the language declares joined with `&` **refuses at the load**.

A type **satisfies** a contract when a document says it does. A document says it where it gives the type what it gives it, under `satisfies`: a struct it declares beside its fields, `{ struct: { rank: Int }, satisfies: ["App.Describable"] }`, and any other type in an extension, keyed by the type, `extensions: { "Bank.Account": { satisfies: ["App.Describable"] } }`. Any document may make one, about a type it declared or about another document's, which is how a document that arrives later gives a type the procedures a contract asks. A type the language names is a type the way a declared one is, and a claim may be about it: `extensions: { Int: { satisfies: ["App.Describable"], procedures: { describe: … } } }`, answered by its member `describe`. A claim written where a struct is declared, or under an extension keyed by a type's bare name, is about every value of the type. A list and a map are named bare `Array` and `Dictionary`: every list is an instance of `Array` whatever it holds, and a claim about `Array` is a claim about every list, one about `Dictionary` about every map, so a declaration answering it takes one whatever it holds, a map under whatever keys, `Dictionary<some K, Any>` with `bounds: { K: Hashable }`: a claim answered by one taking `Array<Int>` or `Dictionary<String, Any>` alone does not hold, and **refuses at the build**, at the claim. A struct taking type parameters named bare is the same, and a claim about it is about every value of it whatever it is applied to, each parameter one no call fills, held to the bounds the struct declares, so a declaration answering it takes `Box<some T>`: one taking `Box<Int>` alone does not hold. A list written as bytes is an instance of `Array` as every list is. `Any` and `Never` are types no value is an instance of by name, `Procedure` and a procedure type name a structure and no type, and `Self` names a type only inside a contract's procedures, so a claim about any of them **refuses at the load**, and a procedure answers no contract. A claim about a declared name that is not itself a struct, an alias included, **refuses at the build**: a value of a declared type is an instance of the struct it is, and of no other name. The document declaring an alias gives it nothing at all, and one that does **refuses at the load**.

**Heads.** An extension's key is its **head**: a type's name, or the type applied to what its brackets hold, `Array<Int>`, `App.Box<some T: Hashable>`. What an extension gives under a head applying its type holds for the values the head takes, the way a parameter written as the head takes an argument. `Array<Int>` takes every list of integers. Each `some T` a head writes is the head's own type parameter, held to the contracts written beside it where the head first names it, `some T: Hashable & Standard.Comparable`, so `App.Box<some T: Hashable>` takes every box of something that answers `Hashable`. A head is a mention of the type it applies and is held as a parameter's type is: one applying a struct to what its bounds do not hold, or a map to a key that does not answer `Hashable`, **refuses at the build**, and so does a bound naming what no module declares as a contract. A head naming no type a value is an instance of, `Int?` among them, one bounding a type parameter anywhere but where it first names it, and two keys of one document reading as one head **refuse at the load**. A claim under a head says the values it takes answer the contract: a reading the head takes answers it, and one it does not take **refuses at the build** where it is handed. A value carries no type's arguments, so where a value is what is judged, at a cast, a door and a call a constant settles through, it answers where it settles into the head, the head's own type parameters filled by what its parts read as, the way a door fits a value to a slot writing the struct, and values meeting at one type parameter of a call or a struct from outside are one type where they are of one struct, each held to the bounds by what it is: a box holding `1` answers a claim under `App.Box<Int?>`, and a cast of a value the head does not take answers null where it reads `as?`. A struct's declaration gives what every value of it has, so what holds for some of its values is written under a head applying it, in the document declaring it as in any other.

The build holds the claim to the type's members. For every procedure the contract asks, it takes the type's member of that name (`Bank.Account`'s `describe`) and holds its signature to the contract's with the type in place of `Self` wherever the contract writes it. Under a head applying the type, that is the type as the head applies it, each of the head's type parameters one no call fills held to its bounds, so a member answering the claim takes every value the head takes: one taking `App.Box<Int>` alone does not answer a claim under `App.Box<some T: Hashable>`. A name that stands for a declared struct names that struct's type there, as wherever types are compared, so a declaration may write another name for the struct the contract writes. A declaration that wrote no `returns` is held by what its body answers, read the way a call site reads it. For every type the contract asks, the build takes the type's type member of that name, under *associated types* below, and reads `Self.Item` as what it gives.

**What a document stands on.** A document stands on the documents declaring what it names, on the documents those stand on, and on the claims it and they import: a claim imported is the claim, every copy of it the link holds, and not what the documents making it stand on, since the copies are one claim. A claim declares no name, so a document reaches one made in a document it names nothing of by writing the pair the claim is about among its `imports`, the type's name and the contract's with a colon and a space between, `"T.Card: App.Describable"`. Whether a type answers a contract is judged at the **build**, against the claims made within what the asking document stands on, the language's among them: a reading of a type no claim there is about, or one the claim's head does not take, answers nothing, and **refuses at the build** where it is handed. So what a document builds to is a fact of it and of what it stands on, whatever else the link holds. A door and a cast judge what arrives against every claim the link holds, since what arrives is no reading any one document asked; a fold, which runs at the build, holds a value to the claims within its document's reach, and a cast it settles whose answer turns on a type no claim within that reach is about, one that would answer were the type to answer the contract, **refuses at the build**, since the run reads every claim the link holds. A claim is judged where it is written, against what its document stands on: a claim missing a procedure, or holding one whose signature does not fit or that does less than the contract asks, **refuses at the build, at the claim**, whether or not anything asks the contract of the type. An import naming a claim the document makes itself or one the language makes **refuses at the load**, and so does one written as neither a name nor a pair, or as a pair whose halves are no type's name and no contract's; one naming a claim no document in the link makes **refuses at the build**, as a name nothing declares does

A claim whose two names the list declares as something other than what the claim needs of them **refuses at the build, at the claim**: a contract where the type belongs, or a type where the contract belongs. One name has one declarer, so no document arriving later makes that right.

A type answers a contract one way. Two documents claiming one type a contract under heads that take the same values are one claim: a claim holds nothing but the values and the contract, so the second says what the first said, whether it writes the head alike or as `App.Box<some U: Hashable>` beside `App.Box<some T: Hashable>`, through an alias, or as the type applied to its own parameters under its own bounds beside the bare name. Claims across documents under heads taking different values, `Array<Int>` and `Array<String>`, **refuse at the build**. One document says each thing one way, so it claiming one type a contract under a second head, however that head is spelled, **refuses at the load**.

**Members.** What a document gives a type under `procedures`, in the struct's declaration or in an extension, are the type's **members**. A member is a procedure under its type's name and its own with a dot between them, `Bank.Account.describe`, the spelling a call writes, and it stands among the procedures as any declaration does: a procedure declared under that spelling, or a second member under it, is one name with two declarers, and **refuses at the load** in one document and **at the build** across documents. A member is named by one identifier, so one named otherwise **refuses at the load**. A type answers a contract's procedure by its member of that name, given in the claim's document or in one that document stands on, so a claim written in an extension stands on the members a struct's declaration gives, and a claim written in a struct's declaration takes no member from an extension, which stands on the declaration and not the other way round. A document gives a struct it declares what it gives every value of it in the declaration, so an extension of a struct the document declares under its bare name **refuses at the load**, and so does an extension giving nothing, which is a second way to write a document. A member given under a head applying its type is there for the values the head takes, and a call says which by the value it hands first, so the member takes that value first, written as the head is written, its parameters' names and aliases as the head spells them: `App.Box.describe` given under `App.Box<some T: Hashable>` takes `App.Box<some T>` first, and one taking anything else first **refuses at the load**. A member taking no value of its type first, `Array.make` taking a `String`, is there for every value, so it is given under the type's bare name. Each type parameter its signature writes that the head names is held to the head's bounds beside its own, so a call handing `App.Box.describe` a box of what does not answer `Hashable` **refuses at the build**. An extension's head is held the way the type a claim is about is held, whatever the extension gives: one naming a contract, or a declared name that is not itself a struct, an alias included, **refuses at the build** at the extension, and so does one naming what no module declares. A procedure spelled like a member and declared among a document's `procedures` is that document's procedure and nothing more: it is no member, and answers no contract. So what a link declares never decides what an unrelated document may call things, and a document that names no contract builds the same whichever documents stand beside it.

A contract may ask no procedures. It is then a mark a claim gives a type, and a type answers it where a document claims it does, as for any contract.

**Associated types.** A contract may ask types as well as procedures, its **associated types**. It lists their names under `types`, each one identifier, `{ types: [Item], procedures: { first: { parameters: [Self], returns: "Self.Item" } } }`, and may hold each to contracts under `bounds` the way a signature holds a type parameter, `bounds: { Item: Hashable }`; a bound naming a type the contract does not ask **refuses at the load**. Its procedures name one as `Self.Item`, the type the type answering the contract gives under that name, and one naming a type the contract does not ask **refuses at the load**. A type gives one by its **type member** of that name, written under `types` beside `procedures` where the document gives the type what it gives it, `types: { Item: "some T" }`, in a struct's declaration or in an extension. Under a head a type member writes the head's own type parameters, in a struct's declaration the struct's, and under a bare head elsewhere none, so one taking the type's parameters is given under a head applying the type. It is named by one identifier, and the type's name and its own with a dot between them, `App.Box.Item`, is its spelling, one type member per spelling: two documents giving one type a type member under one name **refuse at the build**, as two declarers of a name do. A claim holds where, for every type the contract asks, the type's type member of that name is given in the claim's document or in one it stands on, under a head taking every value the claim's head takes, and its type, read under the claim's head, answers what the contract holds it to; a claim that does not **refuses at the build, at the claim**. Two contracts asking one name ask one type member of a type answering both.

**The associated types of a type parameter.** Where a contract bounding a type parameter `T` asks `Item`, `some T.Item` is a type, the associated type `Item` of `T`, written in a signature, a closure's and a member's included, and in a type member. A call fills it once it fills `T`, from what fills `T`: the type member of a type a claim within reach says answers the contract, filled by what the type puts in the head the member was given under, or, where a type parameter of the caller fills `T`, the caller's own member, `some U.Item`. What the call's arguments read at `some T.Item` is that type, so a declaration taking `some T` and `some T.Item` handed a box of `Int` and text **refuses at the build**. A value of a contract, of what may be null, or of `Any` is of no one type and gives no associated type, so a call filling `T` with one where `some T.Item` is written, `Self.Item` of a call through the contract included, **refuses at the build**, and what holds no value gives what holds none. Inside the declaration an associated type is one type the body does not know, under *type parameters* above, held to what each contract bounding `T` holds `Item` to and to what the signature's `bounds` say of it under `T.Item`, `bounds: { T: Lib.Container, "T.Item": App.Describable }`, and one a call fills from a parameter of the declaration around it is that declaration's own. A signature may say an associated type is a type under `sameTypes`, `sameTypes: { "T.Item": Int }`: a call fills `T` only with what gives that type there, and inside the declaration it is that type. The type may name a type parameter or another associated type, `"some U.Item"`, `"Array<some U>"`, which the call reads from what fills `T` as it reads one from an argument, and not one `sameTypes` names itself, which **refuses at the load**, and so do a key naming a type parameter rather than an associated type, one whose parameter no slot writes, and `sameTypes` written in a closure or a contract's procedure; a type that does not answer what holds the associated type **refuses at the build**, where it is written. An associated type stands one step from its parameter, so `some T.Item.Key` names nothing. An associated type no contract bounding its parameter asks **refuses at the build** where it is written, and one whose parameter no parameter of the signature writes, so no call fills it, **refuses at the load**. A struct's field writes no associated type, since a value carries no type's arguments and what fills a struct's parameters is read off its fields, which an associated type says nothing of, and a head writes none, being a type a value is an instance of; either **refuses at the load**. At a door an associated type is what the type of the value at its parameter gives, so a value standing at one is held to that type, and one of another **refuses at the run**.

**What the language declares.** The language declares three names itself, which stand in every link ahead of its documents: the contract `Hashable` below, and the structs `Failure`, which a rescue binds, and `Round`, which a loop binds, under [statements](statement.md). A document declaring one of them **refuses at the load**, and a mention of one is that declaration: a slot, a cast and a claim may name any of the three, so `extensions: { Round: { satisfies: ["Hashable"] } }` keys a map by `Round`, and a bound and a part joined with `&`, which name contracts, name `Hashable` alone.

**A map's key.** The language declares one contract, `Hashable`, which asks no procedures and which the key of every map type answers. The language claims it for `Null`, `Bool`, `Int`, `Double`, `String`, `Array` and `Dictionary`, and a declared struct answers it where a document claims it does: `{ struct: { x: Int }, satisfies: ["Hashable"] }`. Which keys are one key is the value model's sameness, under [the value model](value.md), and no procedure decides it. Every map type is keyed so, written or read: a map type whose key does not answer `Hashable`, `Any`, a procedure type or a type parameter its bounds do not hold to it among them, **refuses at the build** where it is written, reached or not, and so does a map literal whose keys read as such a type where its place declares no map, since the literal reads as a map keyed by what its keys join to; where the place declares a map, each key is held to the key it declares. A constant's type is its value's, so a map it holds whose keys join to `Any` reads `Any` whole, as two maps keyed apart do, except where the expression it settled from was read as a map type, whose key it takes: settled from a call answering `Dictionary<Hashable, Int>`, a map holding `1` and `"a"` is a value of that type. Whether a key answers is judged against the claims within what the document stands on, under the rule above.

A body calls a contract's procedure by writing the contract's name and the procedure's with a dot between them: `App.Describable.describe`. That spelling is the contract's declaration of the procedure, and it is a send like any other: a document calling a contract another module declares lists the spelling in `imports`. It names no type's declaration, and what it means is decided by the value at its first position, so a call writing nothing there **refuses at the build**. What a call hands it and what it answers are the contract's, not any one declaration's.

**The build builds the table and the run reads it.** For every contract, the build gathers every type that satisfies it and lowers one call per type, each against the row that answers, arguments in that row's own slot order. The run reads the type the first argument is an instance of and picks. Nothing is resolved while a program is running.

A declaration answering a contract's procedure is reached **through the contract**, which is the spelling that says which contract is meant. Two types answering one procedure is the ordinary case. Such a declaration takes exactly the contract's positions and answers what the contract's answer takes: its own type first, then **at the contract's positions** a parameter taking everything the contract's takes there and taking a place only where the contract hands one, the contract's type parameters standing for types no call fills and the declaration's own filled by what the contract writes at the same positions; the names are its own. One declaring a parameter beyond them, `T?` included, **refuses at the build**, at the claim. The run hands the arguments to the same positions whichever declaration answers.

**A name is its declared spelling.** The key a document declares a type, contract or procedure under is the whole of its name: `Standard.Math.floored` is declared under that key, and `Wallet.Account` under that one. A mention is a declared spelling, written out, and it means the same declaration wherever it was written, inside the declaring document too. A dot is a character of the spelling and nothing more: the language has no nesting, no scope and no prefix, so what a document chooses to put before a dot is the author's convention, and one document may declare `Wallet.fee` beside `Bank.rate` while another declares `Wallet.rate`. A spelling no module in the link declares **refuses at the build** where it is mentioned. There are two namespaces, procedures and types, and a procedure may be spelled like a type. A contract's procedure stands in the first under its dotted spelling, which names one contract's procedure by the grammar in [checking](checking.md), and a procedure a document declares under that same spelling **refuses at the build**. Types and contracts share the second, and no name in it is both, so a mention reaches whatever declares it: a slot names a type or a contract, and a bound names a contract. Every name in the second, declared or mentioned, holds a type's name grammar, and a type parameter's name its own, under [checking](checking.md): a document declares no type under `Int` and names no type parameter `Int`, a mention spelled `a b` **refuses at the load**, and a mention of `Int` is the type the language names.

The shared `Standard` bundle declares the contracts the standard procedures are bounded by, `Standard.Numeric`, `Standard.Comparable` and `Standard.Collection`, claims them for the types the language names (`Int` and `Double` are numbers that order, `String` orders and has a count, `Array` and `Dictionary` have a count) and gives those types the members answering them, `Int.plus` and the rest, under [the standard vocabulary](vocabulary.md). A bundle whose signatures mention them links with `Standard` in the build.

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
- `a-bound-naming-a-struct-a-document-declares-refuses`
- `a-bound-naming-a-struct-the-language-declares-refuses`
- `a-bound-naming-a-type-the-language-names-refuses`
- `a-bound-on-an-associated-type-carries-a-call-through-another-contract-answers`
- `a-bounded-parameter-read-as-text-and-as-any-refuses`
- `a-call-filling-a-parameter-from-a-variable-held-in-place-takes-a-value-of-that-parameter`
- `a-call-filling-a-parameter-from-a-variable-held-in-place-takes-no-other-value-refuses`
- `a-call-filling-a-parameter-from-the-bodys-own-and-a-reading-of-any-refuses`
- `a-call-fills-a-type-parameter-through-a-struct-applied-to-it-answers`
- `a-call-of-a-value-read-as-any-refuses`
- `a-call-through-a-contract-of-a-value-of-it-reading-an-associated-type-refuses`
- `a-call-through-a-contract-reads-the-associated-type-of-the-value-it-hands-answers`
- `a-call-through-a-contract-with-nothing-first-refuses`
- `a-caller-not-bounding-an-associated-type-refuses`
- `a-callers-bound-on-an-associated-type-carries-into-a-call-answers`
- `a-callers-same-type-carries-into-a-call-answers`
- `a-cast-at-the-run-reads-every-claim-of-the-link`
- `a-cast-between-aliases-of-two-nullable-structs-reads-null-answers`
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
- `a-cast-of-a-closure-writing-where-a-declared-struct-was-filled-fails`
- `a-cast-of-a-nullable-struct-to-another-struct-refuses`
- `a-cast-of-a-setter-a-generic-procedure-made-fails-before-its-getter-reads`
- `a-cast-of-a-struct-applied-to-int-to-it-applied-to-text-refuses`
- `a-cast-of-a-struct-to-the-struct-applied-to-what-it-already-is-refuses`
- `a-cast-of-an-alias-of-a-nullable-struct-to-another-struct-refuses`
- `a-cast-to-a-contract-holds-a-value-to-the-head-it-settles-into`
- `a-cast-to-a-contract-of-a-value-the-head-of-its-claim-does-not-take-answers-null`
- `a-cast-to-a-contract-reads-a-value-by-the-head-of-its-claim-answers`
- `a-cast-to-a-struct-applied-to-what-its-fields-do-not-hold-fails`
- `a-cast-to-a-struct-applied-to-what-its-fields-hold-answers`
- `a-claim-a-document-two-steps-down-makes-answers`
- `a-claim-about-a-list-gives-its-element-as-an-associated-type-answers`
- `a-claim-about-a-struct-answered-for-it-applied-to-int-alone-refuses`
- `a-claim-about-a-struct-reads-its-parameters-held-to-the-structs-bounds-answers`
- `a-claim-about-a-struct-taking-a-type-parameter-holds-for-every-value-of-it-answers`
- `a-claim-about-a-struct-the-language-declares-keys-a-map-by-it-answers`
- `a-claim-about-an-alias-another-document-declares-refuses`
- `a-claim-about-an-alias-the-document-declares-refuses`
- `a-claim-about-any-refuses`
- `a-claim-about-array-answered-for-a-list-of-ints-alone-refuses`
- `a-claim-about-never-refuses`
- `a-claim-about-null-answers-null-where-the-contract-answers-self-or-null`
- `a-claim-about-null-is-answered-for-null`
- `a-claim-about-null-takes-a-list-of-null-where-the-contract-takes-a-list-of-self-or-null`
- `a-claim-about-null-takes-null-where-the-contract-takes-self-or-null`
- `a-claim-about-procedure-refuses`
- `a-claim-about-self-refuses`
- `a-claim-another-document-makes-is-imported-and-answers`
- `a-claim-answering-self-or-null-with-another-type-refuses`
- `a-claim-imported-brings-nothing-its-maker-stands-on`
- `a-claim-in-a-document-the-program-names-nothing-of-refuses`
- `a-claim-in-one-document-about-a-struct-another-declares-with-a-type-parameter-answers`
- `a-claim-naming-a-contract-where-the-type-belongs-refuses`
- `a-claim-naming-a-type-where-a-contract-belongs-refuses`
- `a-claim-that-does-not-hold-refuses-though-nothing-asks-it`
- `a-claim-two-documents-make-answers-a-document-standing-on-the-second`
- `a-claim-under-a-head-another-document-makes-is-imported-and-answers`
- `a-claim-under-a-head-another-document-makes-refuses-a-value-it-does-not-take`
- `a-claim-under-a-head-applying-a-list-to-int-answers-for-a-list-of-ints`
- `a-claim-under-a-head-applying-a-list-to-int-refuses-a-list-of-text`
- `a-claim-under-a-head-bounding-its-parameter-answers-for-a-value-it-takes`
- `a-claim-under-a-head-bounding-its-parameter-refuses-a-value-it-does-not-take`
- `a-claim-whose-member-a-document-it-does-not-stand-on-gives-refuses`
- `a-claim-whose-type-gives-no-type-the-contract-asks-refuses`
- `a-closure-a-generic-body-wrote-is-read-as-the-procedure-type-it-is-judged-against`
- `a-closure-a-generic-body-wrote-read-past-its-bounds-is-not-that-type`
- `a-closure-a-generic-body-wrote-taking-a-list-in-place-is-read-as-the-type-it-is-judged-against`
- `a-closure-alone-fills-a-parameter-with-what-it-takes`
- `a-closure-handed-in-place-fails-with-exactly-what-the-slot-names`
- `a-closure-inside-a-closure-reads-the-bounds-of-the-procedure-around-them`
- `a-closure-naming-a-type-parameter-its-procedure-does-not-declare-refuses`
- `a-closure-parameter-saying-nothing-takes-the-element-the-list-beside-it-fills`
- `a-closure-reads-the-bounds-of-the-procedure-around-it`
- `a-closure-taking-any-stands-where-its-slot-hands-a-contract`
- `a-closure-taking-anything-beside-a-declared-struct-leaves-the-parameter-the-struct`
- `a-closure-taking-int-beside-a-declared-struct-refuses`
- `a-closure-that-may-fail-where-the-procedure-type-fails-with-nothing-refuses`
- `a-closure-writes-the-associated-type-of-the-procedure-around-it-answers`
- `a-closure-writing-bounds-refuses`
- `a-closure-writing-same-types-refuses`
- `a-closures-parameter-names-are-not-part-of-its-type`
- `a-constant-of-a-struct-judged-at-any-reads-as-its-fields-joined-refuses`
- `a-constant-of-a-struct-keeps-what-it-was-applied-to-refuses`
- `a-constant-of-keys-of-two-types-settled-from-a-hashable-keyed-map-answers`
- `a-constant-of-keys-of-two-types-settled-from-an-answer-of-any-reads-any-refuses`
- `a-constant-settled-through-a-claim-under-a-head-holds-the-value-to-the-head`
- `a-constant-settles-through-an-associated-type-answers`
- `a-contract-asking-no-procedures-is-answered-by-what-claims-it`
- `a-contract-asking-no-procedures-refuses-what-no-claim-names`
- `a-contract-bound-naming-a-type-it-does-not-ask-refuses`
- `a-contract-carries-a-procedure-into-a-generic-body`
- `a-contract-declared-twice-refuses`
- `a-contract-declared-under-a-spelling-that-is-no-name-refuses`
- `a-contract-is-named-by-its-qualified-spelling`
- `a-contract-or-null-slot-refuses-a-type-not-answering-the-contract`
- `a-contract-or-null-slot-takes-a-parameter-bounded-by-the-contract-and-another`
- `a-contract-or-null-slot-takes-a-type-answering-the-contract`
- `a-contract-procedure-answering-self-hands-a-struct-back-applied-as-it-came-answers`
- `a-contract-procedure-may-answer-self-or-null`
- `a-contract-procedure-may-take-self-or-null`
- `a-contract-procedure-named-with-a-dot-refuses`
- `a-contract-procedure-names-what-it-may-fail-with`
- `a-contract-procedure-naming-a-type-the-contract-does-not-ask-refuses`
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
- `a-contract-written-with-brackets-refuses`
- `a-copy-of-a-claim-that-does-not-hold-refuses-beside-one-that-does`
- `a-declaration-answering-a-contract-answering-any-may-answer-its-parameter`
- `a-declaration-answering-a-contract-failing-with-what-the-contract-does-not-name-refuses`
- `a-declaration-answering-a-contract-fills-its-own-parameter-with-the-contracts`
- `a-declaration-answering-a-contract-may-answer-a-contract-where-it-promises-it-or-null`
- `a-declaration-answering-a-contract-may-answer-a-type-answering-it-where-it-promises-it-or-null`
- `a-declaration-answering-a-contract-may-answer-an-alias-of-a-struct-answering-it`
- `a-declaration-answering-a-contract-may-answer-an-alias-of-what-it-promises`
- `a-declaration-answering-a-contract-may-answer-another-contract-and-the-contract-where-it-promises-it-or-null`
- `a-declaration-answering-a-contract-may-fill-a-bounded-parameter-with-what-the-bound-takes`
- `a-declaration-answering-a-contract-may-take-a-contract-or-null-where-it-writes-the-contract`
- `a-declaration-answering-a-contract-may-take-a-value-where-it-hands-a-place`
- `a-declaration-answering-a-contract-may-take-a-wider-type`
- `a-declaration-answering-a-contract-may-take-any-where-it-writes-a-contract`
- `a-declaration-answering-a-contract-may-take-anything-where-it-writes-a-parameter`
- `a-declaration-answering-a-contract-may-write-another-name-for-the-struct-the-contract-names`
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
- `a-document-claiming-one-contract-for-a-type-under-two-heads-refuses`
- `a-door-holds-a-value-at-an-associated-type-to-what-its-parameter-gives-answers`
- `a-door-takes-no-value-at-an-associated-type-of-another-type-refuses`
- `a-field-of-a-struct-applied-to-int-read-as-text-refuses`
- `a-field-writing-a-type-parameter-its-struct-does-not-list-refuses`
- `a-fraction-is-not-a-whole-number`
- `a-generic-answer-of-any-refuses`
- `a-generic-body-appends-its-parameter-to-a-list-of-it-or-null`
- `a-generic-body-handing-a-value-its-bounds-do-not-put-under-a-head-refuses`
- `a-generic-body-handing-a-value-its-bounds-put-under-a-head-answers`
- `a-generic-procedure-answers-a-struct-applied-to-its-bounded-key-answers`
- `a-head-applying-a-struct-to-a-parameter-its-bounds-do-not-hold-refuses`
- `a-head-bounding-a-type-parameter-where-it-is-named-again-refuses`
- `a-head-bounding-by-what-no-module-declares-as-a-contract-refuses`
- `a-head-naming-what-may-be-null-refuses`
- `a-head-writing-an-associated-type-refuses`
- `a-list-holding-a-closure-that-may-fail-where-its-elements-fail-with-nothing-refuses`
- `a-list-literal-of-closures-answering-outside-the-bounds-refuses`
- `a-list-literal-of-closures-handed-at-a-bounded-parameter-answers`
- `a-list-literal-of-names-holding-lists-handed-at-a-bounded-parameter-refuses`
- `a-list-of-a-reading-of-any-behind-a-name-handed-beside-a-variable-in-place-refuses`
- `a-list-of-a-reading-of-any-handed-beside-a-variable-in-place-refuses`
- `a-list-of-an-alias-of-any-handed-to-a-value-at-a-list-of-a-contract-refuses`
- `a-list-of-structs-applied-to-a-type-parameter-fills-it-answers`
- `a-list-of-two-maps-whose-keys-join-to-any-holds-each-as-any-refuses`
- `a-list-of-two-types-handed-where-a-contract-is-asked-is-read-element-by-element-refuses`
- `a-literal-of-names-at-a-contract-bound-holds-each-to-its-claim-refuses`
- `a-map-from-outside-whose-keys-the-door-makes-one-key-refuses`
- `a-map-handed-through-a-claim-about-dictionary-reads-as-the-map-it-is-refuses`
- `a-map-key-from-outside-under-a-name-no-document-declares-refuses-at-the-door`
- `a-map-key-from-outside-under-an-alias-is-a-value-of-its-struct-answers`
- `a-map-keyed-by-a-declared-struct-claimed-hashable-answers`
- `a-map-keyed-by-a-declared-struct-no-document-claims-hashable-refuses`
- `a-map-keyed-by-a-struct-taking-a-type-parameter-claimed-hashable-answers`
- `a-map-keyed-by-a-struct-taking-a-type-parameter-no-document-claims-hashable-refuses`
- `a-map-keyed-by-a-type-parameter-bounded-by-hashable-answers`
- `a-map-keyed-by-a-type-parameter-no-bound-holds-refuses`
- `a-map-keyed-by-an-associated-type-the-contract-holds-hashable-answers`
- `a-map-keyed-by-any-refuses`
- `a-map-keyed-by-lists-finds-a-list-by-its-elements`
- `a-map-keyed-by-what-may-be-null-holds-null-as-a-key`
- `a-map-literal-handed-at-a-dictionary-of-a-bounded-parameter-fills-it-by-its-values-refuses`
- `a-map-literal-handed-at-a-dictionary-of-a-contract-holds-each-value-to-its-claim-refuses`
- `a-map-literal-keyed-by-a-closure-refuses`
- `a-map-literal-of-keys-of-two-types-handed-at-a-dictionary-of-a-bounded-key-refuses`
- `a-map-literal-of-keys-of-two-types-written-where-a-hashable-keyed-map-is-declared-answers`
- `a-map-literal-of-values-of-two-types-handed-at-a-dictionary-of-a-bounded-parameter-refuses`
- `a-map-literal-reads-a-whole-key-beside-a-fraction-as-the-fraction`
- `a-map-literal-whose-keys-read-as-any-handed-through-a-contract-refuses`
- `a-map-literal-whose-keys-read-as-any-refuses`
- `a-map-literal-whose-values-do-not-join-handed-at-a-dictionary-of-a-bounded-parameter-refuses`
- `a-map-type-written-with-one-type-refuses`
- `a-member-and-a-procedure-under-one-spelling-refuse`
- `a-member-answering-a-claim-under-a-head-for-less-than-the-head-takes-refuses`
- `a-member-is-called-by-its-types-name-and-its-own`
- `a-member-named-with-a-dot-refuses`
- `a-member-under-a-head-answers-for-a-value-the-head-takes`
- `a-member-under-a-head-may-restate-the-heads-bounds`
- `a-member-under-a-head-takes-the-heads-bounds`
- `a-member-under-a-head-taking-another-type-first-refuses`
- `a-module-declares-a-contract-a-bound-names`
- `a-module-variable-starting-at-a-struct-applied-to-an-empty-list-refuses`
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
- `a-parameter-read-as-a-declared-struct-and-its-alias-keeps-the-name`
- `a-path-written-from-any-into-a-list-of-a-parameter-refuses`
- `a-procedure-a-call-filled-from-a-declared-struct-takes-no-int-refuses`
- `a-procedure-answering-a-struct-of-an-empty-list-stands-at-it-applied-to-a-list-of-int-answers`
- `a-procedure-answers-a-struct-applied-to-its-type-parameter-answers`
- `a-procedure-spelled-like-a-member-answers-no-contract`
- `a-procedure-value-at-a-slot-writing-a-procedure-type-refuses`
- `a-reading-of-any-at-a-bounded-parameter-refuses`
- `a-reading-of-any-at-a-contract-procedure-refuses`
- `a-reading-of-any-beside-a-whole-at-a-contract-procedure-refuses`
- `a-reading-of-any-stands-at-an-alias-of-any`
- `a-reading-outside-a-bound-refuses`
- `a-row-of-readings-of-any-appended-to-a-table-of-text-refuses`
- `a-same-type-holds-an-associated-type-to-a-type-answers`
- `a-same-type-naming-an-associated-type-it-says-is-a-type-refuses`
- `a-same-type-of-a-type-parameter-refuses`
- `a-same-type-takes-no-type-giving-another-refuses`
- `a-signature-applying-a-struct-to-a-parameter-bounded-as-the-struct-asks-answers`
- `a-signature-applying-a-struct-to-a-parameter-its-bounds-do-not-hold-refuses`
- `a-slot-of-a-type-takes-no-value-read-as-a-contract-refuses`
- `a-some-outside-a-signature-refuses`
- `a-struct-a-block-answers-where-a-declared-struct-is-read-takes-the-name`
- `a-struct-a-host-procedure-answers-short-of-its-fields-refuses`
- `a-struct-a-loop-answers-where-a-declared-struct-is-read-takes-the-name`
- `a-struct-another-document-declares-applied-to-another-count-refuses`
- `a-struct-another-document-declares-with-a-type-parameter-is-applied-here-answers`
- `a-struct-applied-to-a-closure-from-a-call-stands-at-the-procedure-type-it-declares-answers`
- `a-struct-applied-to-a-type-its-bound-does-not-take-refuses`
- `a-struct-applied-to-a-type-parameter-handed-in-place-takes-a-write-of-it-answers`
- `a-struct-applied-to-another-count-of-types-refuses`
- `a-struct-applied-to-int-handed-in-place-is-written-through-answers`
- `a-struct-applied-to-int-where-it-is-applied-to-int-or-null-refuses`
- `a-struct-applied-to-int-where-it-is-applied-to-text-refuses`
- `a-struct-applied-to-itself-reads-the-inner-field-answers`
- `a-struct-applied-to-one-type-is-not-the-struct-applied-to-another-whatever-its-fields-refuses`
- `a-struct-arrives-as-an-argument`
- `a-struct-bounded-by-a-struct-a-document-declares-refuses`
- `a-struct-bounded-by-a-type-the-language-names-refuses`
- `a-struct-bounding-a-name-it-does-not-list-refuses`
- `a-struct-bounding-its-key-parameter-holds-a-map-answers`
- `a-struct-built-where-a-declared-struct-is-read-keeps-its-closure`
- `a-struct-declared-without-its-struct-key-refuses`
- `a-struct-field-holding-a-procedure-of-its-type-parameter-is-called-answers`
- `a-struct-field-writing-an-associated-type-refuses`
- `a-struct-from-outside-at-a-contract-slot-is-fitted-to-its-struct`
- `a-struct-from-outside-at-a-slot-applying-it-to-int-or-null-holds-both-answers`
- `a-struct-from-outside-at-any-holding-what-its-bound-does-not-take-refuses`
- `a-struct-from-outside-at-any-reads-as-its-fields-joined-answers`
- `a-struct-from-outside-holds-its-bounded-field-to-the-head-of-its-claim`
- `a-struct-from-outside-short-of-a-field-at-a-contract-slot-refuses`
- `a-struct-from-outside-under-an-alias-of-a-struct-applied-to-int-is-held-to-int-refuses`
- `a-struct-from-outside-under-another-name-refuses-at-the-door`
- `a-struct-from-outside-under-its-name-at-any-is-held-to-its-struct-refuses`
- `a-struct-from-outside-whose-fields-join-to-what-its-bound-does-not-take-refuses`
- `a-struct-holding-a-procedure-of-its-parameter-does-not-stand-applied-to-another-type-refuses`
- `a-struct-holding-an-empty-list-written-into-one-handed-in-place-answers`
- `a-struct-keying-a-map-by-an-unbounded-parameter-refuses`
- `a-struct-listing-no-type-parameters-applied-to-one-refuses`
- `a-struct-listing-no-type-parameters-refuses`
- `a-struct-literal-a-name-that-declares-nothing-holds-refuses`
- `a-struct-literal-answered-where-a-declared-struct-is-answered-takes-the-name`
- `a-struct-literal-at-a-type-parameter-nothing-fills-with-a-struct-refuses`
- `a-struct-literal-beside-a-declared-struct-at-a-type-parameter-reads-as-that-struct-answers`
- `a-struct-literal-handed-at-a-struct-of-a-type-parameter-fills-it-from-its-fields-answers`
- `a-struct-literal-holding-an-empty-list-beside-an-int-fills-a-call-answers`
- `a-struct-literal-in-a-list-beside-a-list-of-another-struct-at-a-type-parameter-refuses`
- `a-struct-literal-in-a-list-handed-first-beside-a-list-of-another-struct-at-a-type-parameter-refuses`
- `a-struct-literal-inside-a-struct-literal-at-a-type-parameter-refuses`
- `a-struct-literal-reading-its-type-parameter-two-ways-refuses`
- `a-struct-literal-short-of-a-field-its-struct-declares-refuses`
- `a-struct-literal-written-where-no-declared-struct-is-read-refuses`
- `a-struct-naming-itself-applied-to-a-list-of-its-parameter-answers`
- `a-struct-naming-itself-applied-to-its-parameter-answers`
- `a-struct-taking-a-type-parameter-holds-what-its-mention-applies-it-to-answers`
- `a-struct-taking-type-parameters-named-without-brackets-refuses`
- `a-struct-the-language-declares-joined-with-and-refuses`
- `a-struct-type-may-name-a-field-for-a-form`
- `a-struct-under-another-name-refuses`
- `a-struct-written-where-a-type-is-written-refuses`
- `a-type-declared-under-a-name-the-language-declares-refuses`
- `a-type-declared-under-a-name-the-language-gives-refuses`
- `a-type-declared-under-a-word-a-type-spelling-writes-refuses`
- `a-type-form-array-of-an-element-with-a-spelling-refuses`
- `a-type-form-beside-other-keys-refuses`
- `a-type-member-given-twice-refuses`
- `a-type-member-is-read-through-an-imported-claim-answers`
- `a-type-member-may-be-an-associated-type-of-its-heads-parameter-answers`
- `a-type-member-outside-what-the-contract-holds-it-to-refuses`
- `a-type-member-under-a-bare-head-writing-a-parameter-refuses`
- `a-type-member-under-a-head-taking-fewer-values-than-the-claim-refuses`
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
- `a-type-the-language-names-written-with-brackets-refuses`
- `a-value-cast-from-any-to-a-contract-answers-by-the-type-it-is`
- `a-value-cast-from-any-to-a-contract-it-does-not-answer-fails`
- `a-value-declares-every-parameter-the-slot-hands`
- `a-value-from-outside-at-a-bounded-parameter-is-held-to-the-head-of-its-claim`
- `a-value-from-outside-is-fitted-to-the-fields-declared`
- `a-value-from-outside-under-a-name-no-document-declares-refuses-at-the-door`
- `a-value-from-outside-under-an-alias-at-any-is-a-value-of-its-struct-answers`
- `a-value-of-a-contract-at-two-self-positions-refuses`
- `a-value-of-a-contract-gives-no-associated-type-refuses`
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
- `a-var-field-of-a-struct-taking-a-type-parameter-is-written-through-answers`
- `a-variable-a-closure-took-written-from-any-refuses`
- `a-variable-a-closure-writes-from-any-refuses`
- `a-variable-a-closure-writes-with-a-value-of-the-parameter-answers`
- `a-variable-handed-in-place-to-a-call-whose-cast-fails-stays-as-it-was`
- `a-variable-written-an-alias-and-what-it-stands-for-holds-that-type`
- `a-whole-literal-an-attempt-answers-beside-a-fraction-is-no-fraction-refuses`
- `a-whole-literal-at-a-fraction-slot-is-the-fraction`
- `a-whole-literal-beside-a-fraction-at-a-bounded-parameter-is-held-to-the-bound-as-the-fraction`
- `a-whole-literal-between-the-brackets-of-a-map-keyed-by-fractions-is-the-fraction`
- `a-whole-literal-in-a-struct-beside-a-fraction-in-one-struct-reads-as-the-fraction-answers`
- `a-whole-literal-where-a-bounded-parameter-stands-refuses`
- `a-whole-number-a-name-holds-is-no-fraction-refuses`
- `an-alias-applied-to-a-type-refuses`
- `an-alias-beside-what-it-stands-for-in-a-list-literal-joins-as-that-type`
- `an-alias-coming-back-to-itself-through-a-list-refuses`
- `an-alias-of-a-contract-answers-the-contract`
- `an-alias-of-a-declared-struct-gives-a-value-from-outside-the-structs-name`
- `an-alias-of-a-struct-answers-the-structs-contracts`
- `an-alias-of-a-struct-applied-to-int-reads-as-it-answers`
- `an-alias-of-any-another-document-declares-at-a-contract-slot-refuses`
- `an-alias-of-any-at-a-contract-slot-refuses`
- `an-alias-of-any-at-a-nullable-contract-slot-refuses`
- `an-answer-from-outside-under-a-name-no-document-declares-where-no-returns-is-written-refuses-at-the-door`
- `an-answer-from-outside-under-an-alias-where-no-returns-is-written-is-a-value-of-its-struct-answers`
- `an-answer-from-outside-under-its-name-where-no-returns-is-written-is-held-to-its-struct-refuses`
- `an-answer-read-as-any-where-a-type-is-declared-refuses`
- `an-array-of-bytes-and-a-list-of-numbers-joins-to-a-list-of-lists`
- `an-associated-type-a-call-fills-from-the-callers-parameter-is-the-callers-answers`
- `an-associated-type-is-one-type-the-body-does-not-know-refuses`
- `an-associated-type-no-contract-bounding-its-parameter-asks-refuses`
- `an-associated-type-of-a-type-parameter-is-what-the-type-filling-it-gives-answers`
- `an-associated-type-read-at-a-type-is-that-type-refuses`
- `an-associated-type-whose-parameter-no-parameter-writes-refuses`
- `an-empty-list-handed-to-a-generic-answers-a-list-of-any-type`
- `an-entry-answers-a-struct-applied-to-int`
- `an-extension-giving-a-contract-members-refuses`
- `an-extension-giving-another-documents-alias-members-refuses`
- `an-extension-of-a-name-nothing-declares-refuses`
- `an-extension-of-a-struct-the-document-declares-refuses`
- `an-extension-of-a-struct-the-document-declares-under-a-head-applying-it-answers`
- `an-extension-writing-nothing-refuses`
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
- `two-associated-types-said-one-type-answer`
- `two-associated-types-said-one-type-take-no-two-types-refuses`
- `two-contracts-asking-one-name-are-answered-by-one-type-member-answers`
- `two-documents-claiming-one-contract-for-a-type-under-two-heads-refuse`
- `two-documents-claiming-one-contract-under-heads-taking-the-same-values-are-one-claim`
- `two-documents-claiming-one-contract-under-one-head-are-one-claim`
- `two-documents-claiming-one-pair-are-one-claim`
- `two-documents-giving-one-type-one-member-refuse`
- `two-structs-applied-to-one-type-in-a-list-join-to-it-answers`
- `two-structs-applied-to-two-types-in-a-list-join-to-anything-refuses`
- `values-from-outside-meeting-at-a-bounded-parameter-are-one-type-where-they-are-of-one-struct`
- `what-was-read-out-of-a-parameter-is-not-the-parameter`
