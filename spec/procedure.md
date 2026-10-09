# Procedures

What a declaration says about itself, and what saying it permits. Four things: the form of a declaration, the one whose code the host answers, what answering without running means and where that claim is spent, and what a parameter takes.

## A procedure

| key | takes | required |
|---|---|---|
| `description` | string | no |
| `access` | `public`, `internal` or `private`: who may name the declaration, under *who may name a declaration* below. `internal` when absent | no |
| `parameters` | list of parameters, in the order the declaration writes them, which is the order every call hands its arguments in | no |
| `returns` | type. When absent, what a call answers is read off the body | no |
| `bounds` | record: type parameter → the names of contracts, one or several joined with `&`; one naming a parameter no slot mentions **refuses at the load**, under [types](type.md) | no |
| `body` | statements | no |
| `result` | expression. What the procedure answers | no |

A procedure answers what `result` names, and nothing if it names nothing. The value of the last statement is never the answer.

## Who may name a declaration

A declaration is named from inside its scope and refused from outside it. Three scopes, and `access` says which:

| `access` | named from |
|---|---|
| `private` | the document that declares it |
| `internal` | every document in the link |
| `public` | the link, and the host that assembled it |

A declaration that writes nothing is `internal`: what a document declares is the program's, and only what says so is the host's. A run starts from a `public` declaration and from no other: the host names one when it starts the run, and naming one that is `internal` or `private` **refuses at the run**, before anything runs, the way naming one nothing declares does. A call standing in one document that reaches a `private` declaration of another **refuses at the build**, at the call, and so does a procedure the host answers whose declared sends reach one. A `private` declaration takes no spelling from the link: its own document reaches it, and two documents may each declare one under one spelling, where two declarations any other document could name **refuse** under [checking](checking.md). A `private` declaration backs no claim: a contract is how a document that never names a declaration calls it, so a claim it would answer does not hold, and is refused where the pair is leaned on the way a claim nothing backs is. A procedure the host answers declared `private` in a module the host assembled with no document **refuses at the load**: `private` names a document, and there is none. `access` written as any other value **refuses at the load**.

A constant and a module variable are the document's own and write no `access`, under [documents](document.md): a name is a scope question, and another document reaches either only through a procedure declared beside it.

A declaration's `access` travels with it: an object writes it on the row, under [objects](object.md), and a document compiled against another reads it there. Nothing else about a declaration moves with it. What it takes and answers, and what it sends, are judged the same whoever may name it.

## A procedure the host answers

A procedure the host answers is not written in a document. A declaration in a document with no `body` and no `result` is a procedure that answers nothing. The host's procedure arrives at the link in a module the host assembled in its own language, declared there under its spelling with what a body's text would have shown: its signature, the **procedures it sends**, because there is no text to read them off, whether it **touches** a name another body could touch at the same time, what it may **fail** with, and whether it **answers without running**, because what it keeps and what it reaches in the host language is outside any document. A call reaches one of these the way it reaches any other declaration, and is judged against the signature the same way.

**Its sends are held to the rest of what it said.** They are declared beside the signature, so the build reads them. A send names the declaration it reaches, so a send naming a contract's procedure **refuses at the build**: which declaration answers one is a call's first argument to say, and a send has no call to read it from. A procedure declaring it answers without running and sending one that answers only by running **refuses at the build**, and so does one declaring it touches nothing shared and sending one that does.

**Nothing else about a procedure the host answers is checked.** One that reaches outside the run and says it does not has broken its contract, and the defect belongs to whoever put it in the link rather than to the program that called it, which is where its claim about what it touches is taken too.

**Note.** A link holds the code, not the text it was written as, and no reading of a built procedure says whether it asked the clock.

**What a runtime hands one is where the claim is kept.** A procedure that answers without running is handed what its call wrote, a way to send the procedures it declared, and a way to call a procedure it was handed. One that reaches outside is handed those and three more: what a parameter handed in place holds, a way to write it, and whatever the host keeps beside the program. Those three are what the first kind is refused.

## What answers without running

Some of what a program writes is **read** and some of it is **run**. A literal, a name, a record, an index, a cast: reading those is what the language does to data. A **construct** runs a body, and it is the only thing that does. That line is what an operand stands on, under *what it permits* below; it is not what this section is about.

A procedure **answers without running** when nothing it reaches stands outside the run it was handed:

- it reads no module variable and writes no name it does not own: a module variable, a name a closure captured, or a parameter handed in place, whether written by `set` or handed in place to a call. What such a name holds is the run's rather than the text's, and a name the body introduces or a parameter it holds outright is its own;
- it calls a value only where a slot declared it a `const` procedure type: the name the slot gave, a fixed name bound to such a name, which follows the declared type it reads, or what a path reaches inside one of those by the type the slot wrote (an element of an array or a dictionary, an entry of a dictionary, a field of a record type). The value was judged against that type when it was handed over, so that is the one place something before the run says what the value answers. A type the build worked out (a closure literal's, a call's answer, a cast's) is a reading rather than a declaration, so a name bound to one carries no claim. The claim is the slot's and so it stands wherever the name is read, a closure that **captured** the name included;
- and every procedure it sends answers without running.

A construct reaches nothing on its own. Which part of a `conditional`, `loop`, `attempt` or `block` runs is decided inside the body, so one of them is read exactly as far as the parts it holds are, and the same goes for `return`, `break` and `continue`. A name the body introduces is the body's own: a `let` and a `var` both make one, neither leaves the body, and so declaring either says nothing about what the body reaches.

The build works this out over every declaration at once. It starts with all of them and strikes out whatever reaches something struck, so two procedures that call each other settle together rather than each waiting on the other. A procedure with **no body** says it about itself instead, and the sends it declared are held to what it said, under *a procedure the host answers* above. A closure literal is judged by the same rule, and the answer travels with the closure as a value, so a slot reads it wherever the value arrives. What it captured it is judged with: a name the enclosing scope held under a slot that said a `const` procedure type is one the closure may call, which is what lets a body build a closure per element and hand the lot to `Standard.Concurrent.all`. A variable that declared it holds one is such a name too, since every write into it is held to the declaration; a variable that declared nothing is held from the capture on to the type it read as there, under *what a write reaches* in [statements](statement.md), and that type is a reading the build worked out, so it says nothing the closure can hold on to. **Isolation reads a captured name the same way**, through a slot that said an `isolated` procedure type.

**What it permits.** Three places, and they are what the claim is for:

- a **constant** and a **module variable** settle at the **build**, from these procedures alone, and from a narrower set of them still, under *what a constant settles from* below;
- a slot may **ask** for one, writing a `const` procedure type. That is how `Standard.Logic.and` takes sides it may decline to read and how `Standard.Collection.filter` takes a predicate that cannot reach the world;
- an **operand** may call one (a call's arguments, a `conditional`'s `when`, a `loop`'s `while`). Each of those is read rather than run, so an operand calling any other declaration **refuses at the build**. An operand, a constant or a variable's start calling a value **refuses at the load**: which procedure a value is, is the run's answer, and the text alone shows the call.

A call through a contract reaches whichever declaration the value turns out to be, so what it reads as is what the contract asked of every one of them. A contract's procedure writing `const` answers without running and one writing `isolated` touches no name another body could touch at once, the way a slot asks the same of a procedure with a `const` and an `isolated` procedure type; a call through such a procedure stands wherever a call to a declaration that does stands, an operand and a `const` body among them, and a claim backed by a declaration that does less than the contract asked **does not hold**, and is refused where the pair is leaned on. A contract's procedure writing neither may run, so a call through it is no operand and a body sending it is not `const`. What a contract's procedure may fail with it names under `failing`, nothing where it names none, and a call through it may fail with that and nothing else, the way a call to a declaration fails with what its body may: a claim backed by a declaration that may fail with more than the contract names does not hold, and is refused where the pair is leaned on.

Choosing among values in an operand is a procedure, `Standard.Logic.select`, under [the standard vocabulary](vocabulary.md).

**What a constant settles from.** Answering without running is what lets a procedure be run at the build. It does not settle *which* run's answer that is. A procedure reaches nothing outside the run it was handed and still answers one thing in one run and another in the next: a host brings a procedure that reads the device it is on, and every run of it inside a run agrees.

What a constant settles to is written into the compiled document, and a compiled document outlives the run that made it. It is kept, it is read again, and it may be made on one machine and read on another. So a constant settles from what answers the same wherever that document is read, which is two things and not three:

- a **body** in another document of the link, since the document it is written in is what the compiled document is made from. A body the constant's own document declares is still being resolved beside it, under *a constant-headed path* in [expressions](expression.md);
- a procedure this specification **names**, under *what an implementation must write* in [the standard vocabulary](vocabulary.md), since every conforming implementation answers it alike.

A call through a contract settles from the declaration a claim names, and which declarations answer a contract is a fact of the whole list. So a constant settles through a contract only where the declaration answering it stands in a document the constant's document stands on, near or far: what it names, and what those name. A constant whose call through a contract reaches a type no such document declares an answer for **refuses at the build**, however the host handed the documents over, and the claim it ran on is still held at the link.

Settling one **refuses at the build** where it reaches a procedure the host brought, whether the constant called it or called a body that does. A **slot** asking a `const` procedure type and an **operand** are untouched: both are read while the program runs, and neither writes anything down.

**A value the build settles is written in a document.** A body in another document of the link is what a constant settles from, so a value baked in is a document declaring a procedure that answers it, which a constant elsewhere calls. The document is a document like any other: it has an identity, that identity stands among what a compiled document was built against, under *identity and dependencies* in [objects](object.md), and a value that moved is a build that moves with it. What the rule above turns away is a procedure in the host's own language, whose answer no document carries; a value written in a document is carried whole.

What settles at the build, a constant or a variable's start, settles to a value. A body run at the build may answer a closure holding a variable of that run, and settling to one **refuses at the build** as well: the run is over when the build is, and a compiled document carries no box of it. Whatever stops one settling, a refusal the standard vocabulary gives at the run or a failure, which nothing there rescues, **refuses at the build** too, whether or not anything reads the constant or the variable.

## A parameter

Written as a record, one per entry of `parameters`:

| key | takes | required |
|---|---|---|
| `name` | string. The name the body reads the argument by | yes |
| `type` | type | no; absent means `Any`, and `Any` written out **refuses at the load**, since leaving it out says it |
| `description` | string | no |

A closure literal that writes no `returns`, written where a procedure type says what it answers, answers that: the place completes its signature, so its body is judged against the answer and a literal it answers is read as the place reads it. Written where nothing completes it, it answers what its body hands back, each way out read as a name holds it, the way a declaration that writes no `returns` does, and the build writes that answer into its signature, so the run reads the closure as the build did. An answer no type spells, what a dot on a value of a type parameter reaches, is one only the body around it can read, so the signature answers `Any` there. A place is every one a literal is written into: a name that says what it holds, a write, an argument to a declaration or to a called value, a body's answer and what a `return` carries, and an element or a field of a list or a record written there, so where a closure is written does not decide whether what it answers is judged at the build. An answer the call fills is no place's to say.

The name is the declaration's own, and a closure literal's names are its own the same way. A procedure type carries the types in position order and no names, under [types](type.md), so two closures naming their parameters differently are one type where the types agree. Two parameters under one name **refuse at the load**.

**One calling convention.** Lowering puts every parameter in a slot, in the declaration's order, and every call hands its arguments **by position**: a `call` to a declaration, a `call` of a value, a procedure handing values to a closure it was given, and a procedure the host answers sending one it declared. A call hands exactly as many arguments as the callee takes. Any other count **refuses**, at the build where the callee is known and at the run otherwise. An argument the parameter at its position does not take **refuses at the build**, and the run judges one only where a value from outside is handed, under [running](running.md). A call through a contract picks its row by the type the first argument is an instance of, and hands the arguments on as they are. In a `call` of a value, a type parameter the slot holding the value names at a position is the body's own, which no call fills and no run can hold a value to, so what stands there is a value of it already, the way a write into a box of it is, and anything else **refuses at the build**. Writing an argument is giving it: an argument holding null was given, and a slot whose type admits one takes it, `Any`, a `T?`, a type parameter, which stands for what arrived.

**A parameter handed in place.** A parameter typed `inout T` takes no value: it takes a variable. The argument is `{ ref: <path> }`, and all of this is held at the **build**:

- the path's head is a variable where the call stands. A fixed name, a literal and a call's answer each **refuse**;
- the path is one a write may take, under *what a write reaches* in [statements](statement.md);
- the variable's type is the same type as the parameter's, all the way in: what it declared, else what it reads as. A variable a closure or a call holds to a type, under *what a write reaches* in [statements](statement.md), is handed only where that type is the parameter's too. Nothing is judged here, because nothing is handed over: the body reads and writes the caller's own box, so a variable of another type would be written values it does not hold.

Inside the body the parameter is a variable, and `set` writes it. The parameter holds the caller's box through the path it was handed: a read finds what the path holds now, and each write lands in the box as it is made. One box reached two ways, by a parameter and by a name or by two parameters, is still one box, so a write through either is seen through the other at once. A call that fails after writing has written, the same as a variable written before a failure. A body that writes through one does not answer without running, by the rule that such a body writes no name. What a procedure the host answers writes through one is a value from outside: it is fitted to the parameter's type and judged against it at the door it comes through, and a value that does not fit **refuses at the run** there.

A variable is handed in place only by a call a body writes: a `call` to a declaration, and a `call` of a value whose type the build reads as a procedure type writing its parameters, at each position that type writes `inout`, held at the **build** to the three rules above; a value whose type writes no parameters (`Procedure`, `Any`, a type parameter, a contract) is called only once a cast says what procedure it is, and a call of one **refuses at the build**. A value standing there whose own parameter takes a value reads what the variable holds. Every other way in hands values: a run hands its entry values, and a procedure the host answers hands values to what it sends and to a procedure it was handed. So an entry taking a parameter in place **refuses at the run** before anything runs; a procedure the host answers declaring a send to one, or a parameter asking for a procedure that takes one, **refuses at the build**; and a value taking one that is handed a value **refuses at the run** before its body runs.

## Cases

What `conformance/` asks about this page, by the name each case's file carries.

- `a-body-reading-a-module-variable-does-not-answer-without-running`
- `a-body-that-branches-answers-without-running`
- `a-body-that-loops-answers-without-running`
- `a-call-of-a-value-hands-in-place-inside-every-construct`
- `a-call-of-a-value-hands-its-arguments-by-position`
- `a-call-of-a-value-indexed-by-a-module-variable-does-not-answer-without-running`
- `a-call-of-a-value-of-another-count-refuses`
- `a-call-of-a-value-read-as-a-contract-refuses`
- `a-call-of-a-value-read-as-a-type-parameter-refuses`
- `a-call-of-a-value-short-of-what-it-takes-refuses`
- `a-call-of-a-value-whose-type-writes-no-parameters-refuses`
- `a-call-of-another-count-refuses`
- `a-call-short-of-what-the-callee-takes-refuses`
- `a-call-that-fails-after-writing-has-written`
- `a-closure-answered-without-returns-reads-a-module-variable-by-running`
- `a-closure-carries-what-a-captured-slot-said`
- `a-closure-literal-a-body-answers-answers-what-its-declaration-answers-refuses`
- `a-closure-literal-a-return-carries-answers-what-its-declaration-answers-refuses`
- `a-closure-literal-a-write-hands-a-box-answers-what-the-box-answers-refuses`
- `a-closure-literal-handed-to-a-called-value-answers-what-the-slot-answers-refuses`
- `a-closure-literal-in-a-list-answers-what-the-element-answers-refuses`
- `a-closure-literal-in-a-list-of-procedures-answering-a-declared-record-names-what-it-answers`
- `a-closure-literal-in-a-record-answers-what-the-field-answers-refuses`
- `a-closure-that-writes-what-it-captured-is-not-const`
- `a-closure-writes-its-own-parameter-in-place-and-no-name-it-shadows`
- `a-closures-parameter-is-not-the-const-procedure-it-shadows`
- `a-const-procedure-read-out-of-a-dictionary-answers-without-running`
- `a-const-procedure-read-out-of-a-dictionary-by-a-dot-answers-without-running`
- `a-const-procedure-read-out-of-a-record-field-answers-without-running`
- `a-const-slot-refuses-a-closure-that-calls-what-runs`
- `a-const-slot-takes-a-closure-that-calls-a-const-slot`
- `a-const-slot-takes-a-closure-that-calls-a-host-procedure`
- `a-constant-cannot-settle-from-a-procedure-the-host-brought`
- `a-constant-cannot-settle-from-what-runs`
- `a-constant-leaning-on-a-claim-of-a-document-it-does-not-stand-on-refuses`
- `a-constant-settles-from-a-body-of-another-document`
- `a-constant-whose-settling-is-refused-refuses-at-the-build`
- `a-contract-asking-const-lets-its-call-stand-in-a-const-slot`
- `a-contract-asking-isolated-lets-its-call-stand-in-an-isolated-slot`
- `a-contract-call-that-may-run-is-no-operand`
- `a-declaration-that-runs-backs-no-const-contract`
- `a-dictionary-entry-handed-in-place-is-read-by-the-callee`
- `a-fixed-name-bound-to-a-calls-answer-gives-a-capture-no-claim`
- `a-fixed-name-bound-to-a-closure-literal-gives-a-capture-no-claim`
- `a-fixed-name-bound-to-a-const-slot-carries-its-claim`
- `a-fixed-name-is-not-handed-in-place`
- `a-fixed-name-is-not-handed-in-place-to-a-called-value`
- `a-list-literal-handed-to-a-called-value-at-a-list-naming-itself-answers`
- `a-literal-argument-its-parameter-does-not-take-refuses`
- `a-loop-reads-a-closure-reading-a-module-variable-as-one-that-runs`
- `a-name-declared-inside-a-nested-closure-does-not-cover-a-captured-one`
- `a-parameter-declared-twice-refuses`
- `a-parameter-handed-in-place-reads-what-the-box-holds-now`
- `a-path-handed-in-place-is-written-through`
- `a-piece-that-writes-what-it-captured-refuses`
- `a-private-declaration-backs-no-claim`
- `a-private-entry-refuses`
- `a-private-name-beside-an-internal-one-reaches-its-own`
- `a-private-name-is-typed-by-its-own-document`
- `a-private-procedure-called-beside-its-declaration-runs`
- `a-private-procedure-called-from-another-document-refuses`
- `a-private-procedure-the-host-brings-is-not-named`
- `a-procedure-handing-a-parameter-in-place-to-a-value-does-not-answer-without-running`
- `a-procedure-that-writes-in-place-does-not-answer-without-running`
- `a-procedure-the-host-answers-is-handed-a-path-indexed-with-a-name`
- `a-procedure-value-cast-to-a-procedure-type-is-called`
- `a-record-literal-a-closure-writes-into-a-captured-variable-takes-the-name-answers`
- `a-record-literal-handed-to-a-called-value-at-a-record-naming-itself-answers`
- `a-record-literal-handed-to-a-called-value-takes-the-name-beside-a-type-parameter-answers`
- `a-record-literal-handed-to-a-called-value-takes-the-name-its-slot-reads-answers`
- `a-required-argument-left-out-refuses`
- `a-slot-handing-a-const-procedure-in-place-is-a-const-slot`
- `a-slot-naming-a-const-procedure-type-is-a-const-slot`
- `a-taken-variable-handed-in-place-as-its-held-type-while-it-reads-another-refuses`
- `a-taken-variable-is-handed-in-place-only-as-the-type-it-is-held-to`
- `a-taken-variable-is-handed-in-place-to-a-value-only-as-the-type-it-is-held-to`
- `a-value-is-not-handed-in-place`
- `a-value-is-not-handed-in-place-through-a-contract`
- `a-value-is-not-handed-in-place-to-a-called-value`
- `a-value-read-as-any-a-called-values-slot-does-not-take-refuses`
- `a-value-read-as-any-handed-to-a-called-value-at-a-type-parameter-of-the-body-refuses`
- `a-value-taking-a-value-reads-the-variable-its-slot-hands-in-place`
- `a-value-under-a-slot-saying-only-procedure-is-not-const`
- `a-variable-a-body-declares-is-its-own`
- `a-variable-declared-const-procedure-carries-that-into-a-capture`
- `a-variable-handed-in-place-is-not-retyped-after`
- `a-variable-handed-in-place-is-written-by-a-called-value`
- `a-variable-handed-in-place-is-written-by-the-callee`
- `a-variable-holding-a-const-procedure-is-not-a-const-slot`
- `a-variable-of-another-type-is-not-handed-in-place`
- `a-variable-of-another-type-is-not-handed-in-place-to-a-called-value`
- `a-variable-that-declares-nothing-gives-a-capture-no-claim`
- `an-access-naming-no-scope-refuses`
- `an-answer-must-fit-what-was-declared`
- `an-answer-nobody-wrote-is-read-off-the-body`
- `an-answer-that-may-be-null-refuses-a-declaration-that-may-not`
- `an-answer-worked-out-from-itself-says-nothing`
- `an-argument-read-as-any-refuses-at-a-typed-parameter`
- `an-effect-in-a-condition-refuses`
- `an-effect-in-a-contract-calls-operand-refuses`
- `an-effect-in-an-operand-refuses`
- `an-effectful-closure-where-const-is-asked-refuses`
- `an-entry-taking-a-parameter-in-place-refuses`
- `an-internal-entry-refuses`
- `an-internal-procedure-is-named-from-another-document`
- `an-isolated-closure-writes-its-own-variables`
- `an-operand-calling-a-value-refuses`
- `arguments-are-judged-at-the-boundary`
- `body-answers-only-what-it-declares`
- `null-is-an-argument-a-document-can-write`
- `two-documents-may-each-declare-a-private-name`
- `two-paths-under-one-head-are-handed-in-place-to-one-call`
