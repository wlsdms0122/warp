# What an implementation checks, and when

Which stage answers which refusal. This page is a list rather than a rule, and the list is the contract: two implementations can agree on every answer a program gives and still not be the same language, if one of them refuses a program the other runs or refuses it later.

A program is read, checked and built before any of it runs, the arms nobody takes included. All of the following are answered while nothing has happened yet. At `load`, since a document answers them alone: the leaves (`break`/`continue` having a loop, nothing following one), every name in normal form C and holding the grammar of where it is written, a procedure's `access` being one of its three values, a closure writing no `access`, no bound and no `sameTypes`, a bound standing only where a name is introduced (beside the first `some T` a signature's slots write, in a struct's `typeParameters`, in a contract's `types`, in a head) and a key of a signature's `bounds` naming an associated type, a literal writing no struct's name, a construct written only as a statement's value, an operand, a constant and a variable's start calling no value, constants naming no cycle, every `set` writing a path headed by a variable and through no optional step, what stands between a path's brackets being a whole number, a text or a path, a contract's procedure taking `Self` first, writing no bound and no `sameTypes` and naming as `Self.Item` only a type its contract asks, a same type keyed by an associated type, naming no associated type `sameTypes` also names and no type parameter no slot writes, one document giving a type one type member under a name once, no declared name that is no struct coming back to itself, and where `inout`, `var`, `Self`, a type parameter and an associated type are written, the type parameter an associated type stands on being one a parameter writes. The rest at `build`, since each is judged against a signature or another document. What the grammar pages refuse as form (a type spelled wrong, a rescue answering nothing, a leave with nothing to leave) is `load` too, and those pages say so where the form is written. The stage is the rule's: a call that misfits a declaration in its own document refuses at `build` all the same.

- every `ref` resolves to a parameter, a constant, a module variable, a statement written before it, a binding the construct holding it opened (a loop's round, an attempt's failure), or a path through them;
- every procedure sent is declared by some module in the link, exactly once;
- a build holds each document once, so one handed to it twice, the same identity a second time, **refuses**, even when everything it declares is `private`;
- the documents of a link stand in an order where what each one sends, and every type it names, is declared before it, since what a document says is read against those: the types its sends answer with, what its bodies reach, what its constants settle from. Two documents that each need the other have no such order and **refuse**, as the pair and not as a spot in either;
- a claim backed by a declaration that does less than the contract asked, running where it asked `const`, touching a shared name where it asked `isolated`, or failing with what the contract does not name, does not hold, under *what answers without running* in [procedures](procedure.md); a claim about a declared name that is not itself a struct, an alias included, refuses, under [types](type.md);
- every procedure sent from another document is not `private`, and a claim backed by a `private` declaration does not hold, under *who may name a declaration* in [procedures](procedure.md); a `private` declaration takes no spelling, so the rule above it counts none;
- every call fits the declaration it reaches: how many arguments, each at its position, and the answer, with type parameters filled as [types](type.md) says and every bound judged against the contracts it names;
- every declared type names a type that exists;
- every map type is keyed by a type that answers `Hashable`, under *a map's key* in [types](type.md);
- a condition (a `conditional`'s `when`, a `loop`'s `while`) answers a `Bool`, held where it is written as any slot of a type is, under *what a slot takes, exactly* in [types](type.md);
- what stands between brackets reads `Int` on a list and the map's key type on a map, under [expressions](expression.md);
- a call of a value reaches one whose type writes its parameters; one whose type writes none (`Procedure`, `Any`, a type parameter, a contract) is called only through a cast, under [procedures](procedure.md);
- inside a generic body every place reading its own type parameter takes only a value of it, under [types](type.md);
- a slot declared `const` takes only a procedure that answers without running, under *what answers without running* in [procedures](procedure.md); a slot declared `isolated` takes only a procedure declared isolated;
- a body declared `const` answers without running, one declared `isolated` touches nothing shared, and a body fails with no more than its declaration names, a closure literal's body included, under [procedures](procedure.md) and [statements](statement.md);
- a parameter bounded by a contract, and a slot naming one, takes only a value of a type a document within what the asking document stands on says answers it, and every claim is backed where it is written: each procedure the contract asks has the type's member of that name behind it, given within what the claim's document stands on, held to what the contract wrote, and each type the contract asks has the type's type member of that name behind it, given there under a head taking every value the claim's head takes and answering what the contract holds the type to;
- an associated type is one a contract bounding what it stands on asks, a contract's bound names a declared contract, a value of a contract, of what may be null or `Any` fills no type parameter whose associated type the signature names, and the type a same type says answers what holds the associated type, under [types](type.md);
- a value of a contract or of what may be null fills a bounded type parameter only where that parameter stands alone at one position, under [types](type.md);
- every `set` writes through fields declared `var` where the type is a declared type, and what it writes fits what the path reaches; a write into a module variable or an `inout` parameter fits what the box holds;
- every `inout` parameter is handed a variable's path a write may take; two parameters handed paths under one head hold one box two ways, under [procedures](procedure.md), and nothing keeps them apart;
- what a closure writes into a variable it captured fits what the capturing body holds;
- a struct type fits only a value of exactly it: a value read under one declared struct name fits no slot declaring another, nor `Dictionary<String, T>`, and a map fits no declared struct; a struct literal is read as the declared struct of the place it is written into, judged field by field and taking the name, and one written where no declared struct is read refuses;
- a constant is the type it was declared as;
- what `return` carries fits the declaration;
- a statement whose call answers `Never`, as its callee's `returns` declares, never finishes: it takes no name, and nothing follows it;
- every name the program writes is **written**, and is **normal form C**, compared as bytes: one name has one byte spelling, so a declaration and a reference can only meet by being the same bytes, `é` written two ways is a refusal, not two names, and nothing written is no name, since a declaration is called something and a reference writes something. A struct's field names hold this line at the encodings, and the names a program writes hold it here;
- every name holds the grammar of where it is written, and one that does not **refuses at the load** where it is written. A **type's name** is what a type or a contract a module declares is called: identifiers joined by dots, an identifier being ASCII letters, digits and `_` and not beginning with a digit, since a dot is a character of a type's name, and none begins `Self.`, which writes an associated type of `Self`. A **type parameter's name** is the `T` of `some T`, a name a struct's `typeParameters` lists and the part of a key of `bounds` before its first dot: one identifier. Neither is a word the language writes itself: a name it gives its own types (`Any`, `Never`, `Null`, `Bool`, `Int`, `Double`, `String`, `Array`, `Dictionary`, `Procedure`, `Self`) or what it declares itself (`Hashable`, `Failure`, `Round`), a word a type's spelling writes (`some`, `const`, `isolated`, `inout`, `var`, `throws`), or `null`, `true` or `false`. A **mention** of a type or a contract in a slot or a cast, and a struct's name, is a type's name or a name the language declares, which is that declaration and no document's. A **contract** a bound, a part joined with `&` or a claim names is a type's name or `Hashable`, so a type the language names or a struct it declares written there refuses at the load. The **type an extension or a claim is about** is a mention or a type the language names a value an instance of (`Null`, `Bool`, `Int`, `Double`, `String`, `Array`, `Dictionary`), which is that type; what a head applies it to is written as a mention is, and the `T` of a head's `some T` and of its bounds is a type parameter's name. A **value's name** is what a constant, a module variable, a statement, a loop's round, an attempt's failure, a parameter, a contract's procedure's included, and a field of a struct type are called: a name a path reads back as one name. A path is written with `.`, `[`, `]` and `?`, so a value's name holding one, or white space at either end, any character Unicode counts as white space or a line break, is one no `ref` or `set` reaches, and there a dot is a step. A **contract's procedure** is named by one identifier, since a call writes the contract's name, a dot and the procedure's name, and a dot in the procedure's name would make one spelling two contracts' procedures. A **member** is named by one identifier for the same reason, after its type's name, and so is a **type member**, the type a contract asks under `types` and a type gives under its own: `some T.Item` writes it after the type parameter's name and a dot, and a key of `bounds` or `sameTypes` writing an associated type is its label: what it stands on, a type parameter's name or another associated type's label, a dot, and its name. A procedure a document declares under `procedures` is held to no grammar but being written.

`imports` is held at `load`, under *the imports list* in [documents](document.md), because a host decides from it before any of this runs.

**What a variable reads as.** A name a statement fixed reads as what that statement bound, and a variable reads as what the ways through the text could have left in it. The checking follows the flow the running takes:

- a name that **declared** what it holds reads as that declaration, and no write changes it. What is written is held to the declaration instead, a list, map or struct literal part by part along what the declaration asks of each part (every element of a list, every key and value of a map, each field a struct names), an empty list holding no element, so `[[], [1]]` written where `Array<Array<String>>` is declared refuses at the build, and so does `[1, "s"]` where `Array<Int>` is. Every slot a value is written into holds it that way: a name's start value or a later write, a parameter of a call or of a called value, and a declared answer, from a result or from a `return`. An attempt writes what its body answers and what its rescue answers, each held on its own as a write on that way would be;
- a variable a closure captured or a call handed in place is held to the type it read as there, under *what a write reaches* in [statements](statement.md), and a write into it is judged against that type and leaves it reading it, since the taker may write any value of it later;
- an **unconditional** write retypes any other variable: after `set x` at the top of the flow, `x` reads as what was written, whatever it held before;
- a write only **some** ways make (one arm of a conditional, a loop's round, an attempt's body) joins with what the name held. Null beside a value reads `T?`: after `var x` and a conditional whose one arm sets an int, `x` reads `Int?`, because the run either took the arm or did not. Two readings join part by part, a whole literal beside a fraction among them, under [types](type.md). This join is not the variable's own rule: it reads wherever two readings of one slot meet (an attempt's body beside its rescue, an array literal's elements), so an attempt whose rescue answers nothing reads `T?` too, and `[1, null]` reads `Array<Int?>`;
- a write **both** arms make is unconditional again, whichever arm ran, the write happened, and an arm that **leaves** contributes nothing: no run comes back from it, so the ways that finish are the only ways a reading after the conditional can stand on. `var x` with one arm setting an int and the other returning reads `Int` afterwards, plain;
- what an arm **declares** (`let`, `var`) stays its own. Declarations die with the block, and only the box a `set` writes outlives it.

Reading does not decide everything: whether a number will be zero when something divides by it is found out by running, under [running](running.md).

**What a refusal names.** A refusal at `load` or `build` about one spot in a document names that spot: the document's identity and the steps from its root to the field, which is a place as [objects](object.md) lay one out, and never the file the document was authored in. A refusal that is a fact about the whole link and no spot in it names no place, since it has none. The sentence beside the place is the implementation's: a case says the stage and reads nothing else.

## Cases

What `conformance/` asks about this page, by the name each case's file carries.

- `a-break-from-a-rescue-carries-what-the-body-did-before-failing`
- `a-declaration-is-named-by-its-whole-spelling`
- `a-document-sending-a-contract-procedure-stands-before-a-later-one`
- `a-failure-in-a-loop-condition-carries-the-rounds-before-it`
- `a-failure-in-a-loop-round-carries-the-rounds-before-it`
- `a-list-holding-a-struct-of-more-fields-than-a-struct-type-refuses`
- `a-list-literal-a-declared-name-starts-with-is-read-position-by-position-refuses`
- `a-list-literal-a-result-answers-is-read-position-by-position-refuses`
- `a-list-literal-a-return-answers-is-read-position-by-position-refuses`
- `a-list-literal-handed-to-a-call-is-read-part-by-part-refuses`
- `a-list-literal-handed-to-a-called-value-is-read-position-by-position-refuses`
- `a-list-literal-of-an-empty-list-and-text-is-taken-by-every-slot`
- `a-list-literal-of-other-types-written-into-a-list-refuses`
- `a-list-literal-written-into-a-declared-variable-is-read-position-by-position-refuses`
- `a-list-of-structs-handed-to-a-call-is-read-field-by-field-refuses`
- `a-module-variable-name-no-path-reads-refuses`
- `a-name-not-in-normal-form-c-is-refused`
- `a-procedure-may-be-spelled-like-a-type`
- `a-procedure-nobody-declares-refuses`
- `a-procedure-only-an-untaken-arm-sends-is-still-needed`
- `a-procedure-two-modules-declare-refuses`
- `a-reference-to-a-statement-written-later-refuses`
- `a-statement-name-no-path-reads-refuses`
- `a-struct-type-field-no-path-reads-refuses`
- `a-type-named-beginning-self-refuses`
- `a-value-name-ending-in-a-line-break-refuses`
- `a-write-a-called-value-answers-in-a-loop-reads-what-its-slot-wrote`
- `a-write-a-loop-round-makes-reads-back-nullable`
- `a-write-an-attempt-body-makes-reads-back-nullable`
- `a-write-both-arms-make-retypes-the-variable`
- `a-write-only-one-arm-makes-reads-back-nullable`
- `an-arm-that-leaves-keeps-the-other-write-definite`
- `an-array-literal-joins-its-elements`
- `an-attempt-joins-its-body-with-its-rescue`
- `an-attempt-whose-rescue-answers-a-list-literal-of-other-elements-refuses`
- `an-attempt-whose-ways-both-fit-a-slot-answers`
- `an-attempt-written-into-a-slot-holds-each-way-on-its-own-refuses`
- `an-empty-name-refuses`
- `an-untaken-arm-is-checked-too`
- `inout-written-outside-a-parameter-refuses`
- `one-document-handed-twice-refuses`
- `two-documents-that-need-each-other-refuse`
- `var-written-outside-a-declared-field-refuses`
