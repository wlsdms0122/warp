# Procedures

What a declaration says about itself, and what saying it lets a caller do.
Four things: the shape of a declaration, the one whose code the host answers,
what answering without running means and where that claim is spent, and what a
parameter takes.

## A procedure

| key | takes | required |
|---|---|---|
| `description` | string | no |
| `parameters` | record: name → parameter | no |
| `receiver` | string. The name of the parameter a call fills by writing a receiver in front | no |
| `returns` | type. When absent, what a call answers is read off the body | no |
| `bounds` | record: type parameter → constraint name; refuses when it names a parameter no slot mentions | no |
| `body` | statements | no |
| `result` | expression. What the procedure answers | no |

A procedure answers what `result` names, and nothing if it names nothing. The
value of the last statement is never the answer.

## A procedure the host answers

A declaration with **no body** is answered by the host. The document says what
it is called, what it takes and what it answers; the code arrives at the link,
in a module the receiver put there. A call reaches one of these the way it
reaches any other declaration, and is judged against the signature the same way.

What a body's text would have shown, such a procedure says instead. It says the
**procedures it sends**, because there is no text to read them off. It says
whether it **touches** a name another body could touch at the same time, what it
may **fail** with, and whether it **answers without running**, because what it
keeps and what it reaches in the host language is outside the document
altogether.

**Its sends are held to the rest of what it said.** They are in the document, so
the build reads them. A procedure declaring it answers without running and
sending one that answers only by running **refuses at the build**, and so does
one declaring it touches nothing shared and sending one that does. Neither is
something a host language can catch. What a procedure may fail with is not held
this way, because a host language can catch: declaring it fails nothing while
sending one that fails is describing itself rather than contradicting itself.

**Nothing else about the host's code is checked, and nothing else can be.** A
link holds the code, not the text it was written as, and there is no reading of
a built procedure that says whether it asked the clock. So a procedure that
reaches outside the run and says it does not has broken its contract, and the
defect belongs to whoever put it in the link rather than to the program that
called it, which is where the word about what it touches is taken too. A
receiver that wants the claim closed closes it by having nothing to hand such a
procedure that reaches outside, where it assembles the link.

**What a runtime hands one is where the claim is kept.** A procedure that
answers without running is handed what its call wrote, a way to send the
procedures it declared, and a way to call a procedure it was handed. One that
reaches outside is handed those and three more: what a parameter handed in place
holds, a way to write it, and whatever the receiver keeps beside the program.
Those three are what the first kind is refused, so a runtime hands the two kinds
different ways in rather than one way and a flag.

## What answers without running

Some of what a program writes is **read** and some of it is **run**. A literal,
a name, a record, an index, a cast: reading those is what the language does to
data. A **construct** runs a body, and it is the only thing that does. That
line is what an operand stands on, under *what it permits* below; it is not
what this section is about.

A procedure **answers without running** when nothing it reaches stands outside
the run it was handed:

- it reads no module variable and writes none, since what one of those holds is
  the run's rather than the text's;
- it calls a value (`apply`) only through a name a slot declared
  `const procedure`. That is the one place something before the run says what
  the value answers; on any other name nothing does. The claim is the slot's
  and so it stands wherever the name is read, a closure that **captured** the
  name included;
- and every procedure it sends answers without running.

A construct reaches nothing on its own. Which part of a `conditional`, `loop`,
`attempt` or `block` runs is decided inside the body, so one of them is read
exactly as far as the parts it holds are, and the same goes for `return`,
`break` and `continue`. A name the body introduces is the body's own: a `let`
and a `var` both make one, neither leaves the body, and so declaring either
says nothing about what the body reaches.

The build works this out over every declaration at once. It starts with all of
them and strikes out whatever reaches something struck, so two procedures that
call each other settle together rather than each waiting on the other. A
procedure with **no body** says it about itself instead, and the sends it
declared are held to what it said, under *a procedure the host answers* above.
A closure literal is judged by the same rule, and the answer travels with the
closure as a value, so a slot reads it wherever the value arrives. What it
captured it is judged with: a name the enclosing scope held under a slot that
said `const procedure` is one the closure may apply, which is what lets a body
build a closure per element and hand the lot to `std.concurrent.all`.
**Isolation reads a captured name the same way**, through a slot that said
`isolated procedure`.

**What it permits.** Three places, and they are what the claim is for:

- a **constant** and a **module variable** settle at the **build**, from these
  procedures alone, and from a narrower set of them still, under *what a
  constant settles from* below;
- a slot may **ask** for one, writing `const procedure`. That is how
  `std.logic.and` takes sides it may decline to read and how
  `std.collection.filter` takes a predicate that cannot reach the world;
- an **operand** may call one. A call's arguments and the receiver written in
  front, a `conditional`'s `when`, a `loop`'s `while`. Each of those is read
  rather than run, so an operand calling anything else **refuses at the
  build**, and so does one calling a value.

Choosing among values is a procedure here rather than a construct, because an
operand is read rather than run and a construct is not one. `std.logic.select`,
under the vocabulary.

**What a constant settles from.** Answering without running is what lets a
procedure be run at the build. It does not settle *which* run's answer that is.
A procedure reaches nothing outside the run it was handed and still answers one
thing in one run and another in the next: a caller brings a procedure that
reads the device it is on, and every run of it inside a run agrees.

What a constant settles to is written into the compiled document, and a
compiled document outlives the run that made it. It is kept, it is read again,
and it may be made on one machine and read on another. So a constant settles
from what answers the same wherever that document is read, which is two things
and not three:

- a **body** in the link, since the document it is written in is what the
  compiled document is made from;
- a procedure this specification **names**, under *what an implementation must
  write* in [the standard vocabulary](vocabulary.md), since every conforming
  implementation answers it alike.

Settling one **refuses at the build** where it reaches a procedure a caller
brought, whether the constant called it or called a body that does. A **slot**
asking `const procedure` and an **operand** are untouched: both are read while
the program runs, and neither writes anything down.

## A parameter

Written as a bare string. Its type, or as a record:

| key | takes | required |
|---|---|---|
| `type` | type | no; absent means `any` |
| `enum` | array. The values this parameter admits | no |
| `default` | the value used when the argument is absent | no |
| `description` | string | no |

`enum` is judged wherever an argument is settled against the parameter: at the
**build** for a constant argument, at the run's boundary otherwise. The
declaration itself is judged at the **build**, wherever the parameter is
written. Nested signatures included, because a declaration may lean on a
declared type name, and only the build resolves those: a `enum` listing a
candidate the declared type does not admit **refuses**. A dead candidate is a
member no call could ever match, whether live ones stand beside it or not, the
empty set being the plainest case. A candidate is written in a value's **one
spelling**. The spelling a document itself writes: `007`, `+1`, and `1e0` are
second spellings of values that already have one, and `1` on a `double` slot is
the int's spelling, which no fraction ever wears. Each of these is a dead
candidate, because the boundary compares an arriving value's own spelling and
would never produce theirs. The same judgement refuses a `default` the parameter
itself would refuse, by its `type` or its own `enum`. A `default` written as
`null` is the value the body receives, so it needs a type that admits null.
`any`, `null`, or a nullable `T?`, which is what lets a typed parameter say
"this, or leave it out". A taken default arrives **settled**, exactly as a
passed argument does. A parameter without a `default` is required. Except that a
`T?` parameter's null is one of its values, so it may be left out and omission
reads as that null; the call check and the boundary both answer this one
question the same way. There is no third axis of optionality.

**Writing a key is giving it.** What a call wrote and what it left out are two
different texts, and the boundary reads them as two different things. An
argument holding null was given, and a slot whose type admits one takes it:
`any`, a `T?`, a type parameter, which stands for what arrived and settles
nothing. Omission is the key not being written at all, and that is what a
`default` answers and what a required slot refuses. This is one convention
wherever a call is made. A document's `call`, an `apply`, a procedure handing
values to a closure it was given: each settles against the declaration the same
way, and a name the declaration does not have refuses in all of them. The
receiver written in front of the dot is given the same way: it fills the
parameter the declaration names as its `receiver`, and is held to what that
parameter declares, null included.

**A parameter handed in place.** A parameter typed `inout T` takes no value:
it takes a variable. The argument is `{ ref: <path> }`, and all of this is
held at the **build**:

- the path's head is a variable where the call stands. A fixed name, a
  literal and a call's answer each **refuse**;
- the path is one a write may take, under *what a write reaches* in [statements](statement.md);
- the variable's declared type is the same type as the parameter's, all the
  way in. Nothing settles here, because nothing is handed over: the body reads
  and writes the caller's own box, so a variable of another type would be
  written values it was not declared to hold.

Inside the body the parameter is a variable, and `set` writes it. The
parameter holds the caller's box through the path it was handed: a read finds
what the path holds now, and each write lands in the box as it is made. One
box reached two ways, by a parameter and by a name or by two parameters, is
still one box, so a write through either is seen through the other at once. A
call that fails after writing has written, the same as a variable written
before a failure. A body that writes through one does not answer without
running, by the rule that such a body writes no name.

## Cases

What `conformance/` asks about this page, by the name each case's file carries.

- `a-const-slot-refuses-a-closure-that-calls-what-runs`
- `a-const-slot-takes-a-closure-that-applies-a-const-slot`
- `a-const-slot-takes-a-closure-that-calls-a-host-procedure`
- `a-constant-argument-is-checked-before-running`
- `a-constant-argument-outside-enum-refuses-at-build`
- `a-constant-cannot-settle-from-a-procedure-a-caller-brought`
- `a-constant-cannot-settle-from-what-runs`
- `a-default-outside-its-enum-refuses-at-build`
- `a-default-outside-its-type-refuses-at-build`
- `a-enum-no-candidate-of-which-fits-refuses-at-build`
- `a-enum-that-admits-nothing-refuses-at-build`
- `a-enum-with-a-dead-candidate-refuses-at-build`
- `a-fixed-name-is-not-handed-in-place`
- `a-native-procedure-is-handed-a-path-indexed-with-a-name`
- `a-null-default-needs-a-type-that-admits-null`
- `a-nullable-parameter-defaults-to-null`
- `a-path-handed-in-place-is-written-through`
- `a-piece-that-writes-what-it-captured-refuses-at-the-build`
- `a-procedure-that-can-fail-says-so`
- `a-receiver-is-held-to-its-parameter-at-the-run`
- `a-receiver-written-for-one-that-declares-none-refuses`
- `a-required-argument-left-out-refuses`
- `a-value-is-not-handed-in-place`
- `a-variable-handed-in-place-is-written-by-the-callee`
- `an-answer-must-fit-what-was-declared`
- `an-answer-nobody-wrote-is-read-off-the-body`
- `an-answer-that-may-be-null-refuses-a-declaration-that-may-not`
- `an-answer-worked-out-from-itself-says-nothing`
- `an-argument-outside-enum-refuses-at-the-boundary`
- `an-effect-in-a-condition-refuses-at-the-build`
- `an-effect-in-a-contract-calls-operand-refuses`
- `an-effect-in-an-operand-refuses-at-the-build`
- `an-effectful-closure-where-const-is-asked-refuses`
- `an-isolated-closure-writes-its-own-variables`
- `an-omitted-argument-arrives-as-the-settled-default`
- `arguments-are-settled-at-the-boundary`
- `body-answers-only-what-it-declares`
- `null-is-an-argument-a-document-can-write`
- `two-paths-under-one-head-are-handed-in-place-to-one-call`
