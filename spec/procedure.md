# Procedures

What a declaration says about itself, and what saying it permits. Four things: the form of a declaration, the one whose code the host answers, what answering without running means and where that claim is spent, and what a parameter takes.

## A procedure

| key | takes | required |
|---|---|---|
| `description` | string | no |
| `access` | `public`, `internal` or `private`: who may name the declaration, under *who may name a declaration* below. `internal` when absent | no |
| `parameters` | list of parameters, in the order the declaration writes them, which is the order every call hands its arguments in | no |
| `returns` | type. When absent, what a call answers is read off the body | no |
| `bounds` | record: type parameter → the names of constraints and contracts, one or several joined with `&`; refuses when it names a parameter no slot mentions | no |
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

A declaration that writes nothing is `internal`: what a document declares is the program's, and only what says so is the host's. A run starts from a `public` declaration and from no other: the host names one when it starts the run, and naming one that is `internal` or `private` **refuses at the run**, before anything runs, the way naming one nothing declares does. A call standing in one document that reaches a `private` declaration of another **refuses at the build**, at the call, and so does a procedure the host answers whose declared sends reach one. A `private` declaration takes no spelling from the link: its own document reaches it, and two documents may each declare one under one spelling, where two declarations any other document could name **refuse** under [checking](checking.md). A `private` declaration backs no claim: a contract is how a document that never names a declaration calls it, so a claim it would answer does not hold, and is refused where the pair is leaned on the way a claim nothing backs is. A procedure the host answers declared `private` in a module the host assembled with no document **refuses where the module is made**: `private` names a document, and there is none. `access` written as any other value **refuses at the load**.

A constant and a module variable are the document's own and write no `access`, under [documents](document.md): a name is a scope question, and another document reaches either only through a procedure declared beside it.

A declaration's `access` travels with it: an object writes it on the row, under [objects](object.md), and a document compiled against another reads it there. Nothing else about a declaration moves with it. What it takes and answers, and what it sends, are judged the same whoever may name it.

## A procedure the host answers

A procedure the host answers is not written in a document. A declaration in a document with no `body` and no `result` is a procedure that answers nothing. The host's procedure arrives at the link in a module the host assembled in its own language, declared there under its spelling with what a body's text would have shown: its signature, the **procedures it sends**, because there is no text to read them off, whether it **touches** a name another body could touch at the same time, what it may **fail** with, and whether it **answers without running**, because what it keeps and what it reaches in the host language is outside any document. A call reaches one of these the way it reaches any other declaration, and is judged against the signature the same way.

**Its sends are held to the rest of what it said.** They are declared beside the signature, so the build reads them. A procedure declaring it answers without running and sending one that answers only by running **refuses at the build**, and so does one declaring it touches nothing shared and sending one that does. Neither is something a host language can catch. What a procedure may fail with is not held this way, because a host language can catch: declaring it fails nothing while sending one that fails is describing itself rather than contradicting itself.

**Nothing else about the host's code is checked.** A procedure that reaches outside the run and says it does not has broken its contract, and the defect belongs to whoever put it in the link rather than to the program that called it, which is where its claim about what it touches is taken too. A host that wants the claim closed closes it by having nothing to hand such a procedure that reaches outside, where it assembles the link.

**Note.** A link holds the code, not the text it was written as, and no reading of a built procedure says whether it asked the clock.

**What a runtime hands one is where the claim is kept.** A procedure that answers without running is handed what its call wrote, a way to send the procedures it declared, and a way to call a procedure it was handed. One that reaches outside is handed those and three more: what a parameter handed in place holds, a way to write it, and whatever the host keeps beside the program. Those three are what the first kind is refused, so a runtime hands the two kinds different ways in rather than one way and a flag.

## What answers without running

Some of what a program writes is **read** and some of it is **run**. A literal, a name, a record, an index, a cast: reading those is what the language does to data. A **construct** runs a body, and it is the only thing that does. That line is what an operand stands on, under *what it permits* below; it is not what this section is about.

A procedure **answers without running** when nothing it reaches stands outside the run it was handed:

- it reads no module variable and writes no name it does not own: a module variable, a name a closure captured, or a parameter handed in place, whether written by `set` or handed in place to a call. What such a name holds is the run's rather than the text's, and a name the body introduces or a parameter it holds outright is its own;
- it calls a value only through a name a slot declared `const procedure`. That is the one place something before the run says what the value answers; on any other name nothing does. The claim is the slot's and so it stands wherever the name is read, a closure that **captured** the name included;
- and every procedure it sends answers without running.

A construct reaches nothing on its own. Which part of a `conditional`, `loop`, `attempt` or `block` runs is decided inside the body, so one of them is read exactly as far as the parts it holds are, and the same goes for `return`, `break` and `continue`. A name the body introduces is the body's own: a `let` and a `var` both make one, neither leaves the body, and so declaring either says nothing about what the body reaches.

The build works this out over every declaration at once. It starts with all of them and strikes out whatever reaches something struck, so two procedures that call each other settle together rather than each waiting on the other. A procedure with **no body** says it about itself instead, and the sends it declared are held to what it said, under *a procedure the host answers* above. A closure literal is judged by the same rule, and the answer travels with the closure as a value, so a slot reads it wherever the value arrives. What it captured it is judged with: a name the enclosing scope held under a slot that said `const procedure` is one the closure may call, which is what lets a body build a closure per element and hand the lot to `std.concurrent.all`. A variable that declared it holds one is such a name too, since every write into it is held to the declaration; a variable that declared nothing may be retyped after the capture and says nothing the closure can hold on to. **Isolation reads a captured name the same way**, through a slot that said `isolated procedure`.

**What it permits.** Three places, and they are what the claim is for:

- a **constant** and a **module variable** settle at the **build**, from these procedures alone, and from a narrower set of them still, under *what a constant settles from* below;
- a slot may **ask** for one, writing `const procedure`. That is how `std.logic.and` takes sides it may decline to read and how `std.collection.filter` takes a predicate that cannot reach the world;
- an **operand** may call one (a call's arguments, a `conditional`'s `when`, a `loop`'s `while`). Each of those is read rather than run, so an operand calling anything else **refuses at the build**, and so does one calling a value.

A call through a contract reaches whichever declaration the value turns out to be, so what it reads as is what the contract asked of every one of them. A contract's procedure writing `const` answers without running and one writing `isolated` touches no name another body could touch at once, the way a slot asks the same of a procedure with `const procedure` and `isolated procedure`; a call through such a procedure stands wherever a call to a declaration that does stands, an operand and a `const` body among them, and a claim backed by a declaration that does less than the contract asked **does not hold**, and is refused where the pair is leaned on. A contract's procedure writing neither may run, so a call through it is no operand and a body sending it is not `const`.

Choosing among values in an operand is a procedure, `std.logic.select`, under [the standard vocabulary](vocabulary.md).

**What a constant settles from.** Answering without running is what lets a procedure be run at the build. It does not settle *which* run's answer that is. A procedure reaches nothing outside the run it was handed and still answers one thing in one run and another in the next: a host brings a procedure that reads the device it is on, and every run of it inside a run agrees.

What a constant settles to is written into the compiled document, and a compiled document outlives the run that made it. It is kept, it is read again, and it may be made on one machine and read on another. So a constant settles from what answers the same wherever that document is read, which is two things and not three:

- a **body** in another document of the link, since the document it is written in is what the compiled document is made from. A body the constant's own document declares is still being resolved beside it, under *a constant-headed path* in [expressions](expression.md);
- a procedure this specification **names**, under *what an implementation must write* in [the standard vocabulary](vocabulary.md), since every conforming implementation answers it alike.

Settling one **refuses at the build** where it reaches a procedure the host brought, whether the constant called it or called a body that does. A **slot** asking `const procedure` and an **operand** are untouched: both are read while the program runs, and neither writes anything down.

**A host that wants the build to settle a value of its own writes a document.** A body in another document of the link is what a constant settles from, so a host bakes a value in by laying in a document that declares a procedure answering it, and a constant elsewhere calls that procedure. The document is a document like any other: it has an identity, that identity stands among what a compiled document was built against, under *identity and dependencies* in [objects](object.md), and a value that moved is a build that moves with it. What the rule above turns away is a procedure in the host's own language, whose answer no document carries; a value written in a document is carried whole.

What settles at the build, a constant or a variable's start, settles to a value. A body run at the build may answer a closure holding a variable of that run, and settling to one **refuses at the build** as well: the run is over when the build is, and a compiled document carries no box of it.

## A parameter

Written as a record, one per entry of `parameters`:

| key | takes | required |
|---|---|---|
| `name` | string. The name the body reads the argument by | yes |
| `type` | type | no; absent means `any` |
| `enum` | array of strings, each a value's one spelling. The values this parameter admits | no |
| `description` | string | no |

The name is the declaration's own, and a closure literal's names are its own the same way. A procedure type carries the types in position order and no names, under [types](type.md), so two closures naming their parameters differently are one type where the types agree. Two parameters under one name **refuse at the load**.

`enum` is judged wherever an argument is settled against the parameter: at the **build** for a constant argument, at the run's boundary otherwise. The declaration itself is judged at the **build**, wherever the parameter is written, nested signatures included, because a declaration may lean on a declared type name, and only the build resolves those: an `enum` listing a candidate the declared type does not admit **refuses**. An argument meets the candidates **settled**, after the slot widened a whole number to the fraction it names, and a number meets one by worth: `1` handed to a `double` slot listing `1.0` is admitted. A dead candidate is a member no settled value could ever match, whether live ones stand beside it or not, the empty set being the plainest case. A candidate is written in a value's **one spelling**, the one the slot's own values wear: `007`, `+1`, and `1e0` are second spellings of values that already have one, and `1` on a `double` slot is the int's spelling, which no fraction ever wears. Each of these is a dead candidate, because no settled value wears their spelling.

**One calling convention.** Lowering puts every parameter in a slot, in the declaration's order, and every call hands its arguments **by position**: a `call` to a declaration, a `call` of a value, a procedure handing values to a closure it was given, and a procedure the host answers sending one it declared. A call hands exactly as many arguments as the callee takes. Any other count **refuses**, at the build where the callee is known and at the run otherwise, and so does an argument the parameter at its position refuses. Writing an argument is giving it: an argument holding null was given, and a slot whose type admits one takes it, `any`, a `T?`, a type parameter, which stands for what arrived and settles nothing.

**A parameter handed in place.** A parameter typed `inout T` takes no value: it takes a variable. The argument is `{ ref: <path> }`, and all of this is held at the **build**:

- the path's head is a variable where the call stands. A fixed name, a literal and a call's answer each **refuse**;
- the path is one a write may take, under *what a write reaches* in [statements](statement.md);
- the variable's declared type is the same type as the parameter's, all the way in. Nothing settles here, because nothing is handed over: the body reads and writes the caller's own box, so a variable of another type would be written values it was not declared to hold.

Inside the body the parameter is a variable, and `set` writes it. The parameter holds the caller's box through the path it was handed: a read finds what the path holds now, and each write lands in the box as it is made. One box reached two ways, by a parameter and by a name or by two parameters, is still one box, so a write through either is seen through the other at once. A call that fails after writing has written, the same as a variable written before a failure. A body that writes through one does not answer without running, by the rule that such a body writes no name.

A variable is handed in place only by a call a body writes. A run hands its entry values and a procedure the host answers hands what it sends values, so an entry taking a parameter in place **refuses at the run** before anything runs, and a procedure the host answers declaring a send to one **refuses at the build**.

## Cases

What `conformance/` asks about this page, by the name each case's file carries.

- `a-body-reading-a-module-variable-does-not-answer-without-running`
- `a-body-that-branches-answers-without-running`
- `a-body-that-loops-answers-without-running`
- `a-call-of-a-value-hands-its-arguments-by-position`
- `a-call-of-a-value-of-another-count-refuses`
- `a-call-of-a-value-short-of-what-it-takes-refuses`
- `a-call-of-another-count-refuses`
- `a-call-short-of-what-the-callee-takes-refuses`
- `a-call-that-fails-after-writing-has-written`
- `a-candidate-meets-a-number-by-worth`
- `a-candidate-on-a-slot-bounded-by-numbers-meets-either-kind`
- `a-closure-carries-what-a-captured-slot-said`
- `a-closure-that-writes-what-it-captured-is-not-const`
- `a-const-slot-refuses-a-closure-that-calls-what-runs`
- `a-const-slot-takes-a-closure-that-calls-a-const-slot`
- `a-const-slot-takes-a-closure-that-calls-a-host-procedure`
- `a-constant-argument-its-parameter-does-not-take-refuses`
- `a-constant-argument-outside-enum-refuses`
- `a-constant-cannot-settle-from-a-procedure-the-host-brought`
- `a-constant-cannot-settle-from-what-runs`
- `a-constant-handed-to-a-called-value-outside-its-range-refuses`
- `a-constant-sent-through-a-contract-outside-its-range-refuses`
- `a-constant-settles-from-a-body-of-another-document`
- `a-contract-asking-const-lets-its-call-stand-in-a-const-slot`
- `a-contract-asking-isolated-lets-its-call-stand-in-an-isolated-slot`
- `a-contract-call-that-may-run-is-no-operand`
- `a-declaration-that-runs-backs-no-const-contract`
- `a-dictionary-entry-handed-in-place-is-read-by-the-callee`
- `a-fixed-name-is-not-handed-in-place`
- `a-name-declared-inside-a-nested-closure-does-not-cover-a-captured-one`
- `a-native-procedure-is-handed-a-path-indexed-with-a-name`
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
- `a-procedure-that-writes-in-place-does-not-answer-without-running`
- `a-required-argument-left-out-refuses`
- `a-value-is-not-handed-in-place`
- `a-value-is-not-handed-in-place-through-a-contract`
- `a-value-under-a-slot-saying-only-procedure-is-not-const`
- `a-variable-a-body-declares-is-its-own`
- `a-variable-declared-const-procedure-carries-that-into-a-capture`
- `a-variable-handed-in-place-is-written-by-the-callee`
- `a-variable-of-another-type-is-not-handed-in-place`
- `a-variable-that-declares-nothing-gives-a-capture-no-claim`
- `a-whole-number-candidate-on-a-fraction-slot-is-dead`
- `an-access-naming-no-scope-refuses`
- `an-answer-must-fit-what-was-declared`
- `an-answer-nobody-wrote-is-read-off-the-body`
- `an-answer-that-may-be-null-refuses-a-declaration-that-may-not`
- `an-answer-worked-out-from-itself-says-nothing`
- `an-argument-outside-enum-refuses-at-the-boundary`
- `an-argument-through-any-is-held-to-its-parameter`
- `an-effect-in-a-condition-refuses`
- `an-effect-in-a-contract-calls-operand-refuses`
- `an-effect-in-an-operand-refuses`
- `an-effectful-closure-where-const-is-asked-refuses`
- `an-entry-taking-a-parameter-in-place-refuses`
- `an-enum-candidate-written-as-a-number-refuses`
- `an-enum-no-candidate-of-which-fits-refuses`
- `an-enum-that-admits-nothing-refuses`
- `an-enum-with-a-dead-candidate-refuses`
- `an-internal-entry-refuses`
- `an-internal-procedure-is-named-from-another-document`
- `an-isolated-closure-writes-its-own-variables`
- `an-operand-calling-a-value-refuses`
- `arguments-are-settled-at-the-boundary`
- `body-answers-only-what-it-declares`
- `null-is-an-argument-a-document-can-write`
- `two-documents-may-each-declare-a-private-name`
- `two-paths-under-one-head-are-handed-in-place-to-one-call`
