# The Warp specification

Warp is a language, and this is where the language is. The directories beside
this one hold implementations of it; nothing they do adds to the language, and
the work of these pages is to owe them nothing. The last section says where
that is still not true.

This describes **Warp 0.1.0**. Nothing has shipped: no document exists anywhere
this specification does not control, and the numbers below start moving at the
first release.

This document is written the way a protocol is written: it says what a
conforming implementation **must** do, field by field and byte by byte, and the
cases under `conformance/` are the same statements as data. An implementation is
a thing you can be *wrong at*.

## What Warp is

A runtime compiler: a front end, an IR and a runtime, composed so that any front
end works with any runtime. Where an ordinary language goes source to build to
machine code, Warp is the half in front of that, and what it answers with is a
language again. This specification is that language. Turning it into machine
code belongs to the toolchain that built the runtime.

What the language is *for*, and every property below that follows from it:

A language for programs that arrive after the program running them was built.

A compiled application cannot run code it did not ship with. Handed a source
file at run time it has no compiler, and on the platforms this exists for it may
not acquire one, so the only way a decision reaches a running program without
rebuilding and re-shipping it is for something inside to read that decision and
carry it out. Warp is what that something reads.

Everything else follows from *arrive*:

- **The program comes from elsewhere**, so the receiving side cannot assume it
  was checked. Checking is the receiver's job, not a favour the sender did.
- **The program crosses machines as bytes**, so there is a document format, and
  the two ends have to agree about what the bytes say.
- **The sender and the receiver may be different implementations**. A server in
  one language, two applications in two others, so agreement cannot mean "the
  same code".
- **The program is not trusted**, so what it can do is bounded by something the
  receiver controls.

What bounds it is the vocabulary. A program does exactly what the procedures in
its link let it do, and every procedure past the ones this specification spells
is one the receiver put there. The language checks what a program *sends*; what
answering a procedure means is the host's. So a receiver draws its line once,
where it assembles the modules, and a module of native procedures it takes in
reaches whatever host code reaches there. That is the same decision as taking in
a library, and it is not one a document can make.

## The pieces

```
what a person writes        YAML, a syntax of your own, …   front ends. Many, replaceable
        ↓
the document                one format, this specification  ← what travels
        ↓  as bytes         binary / text                   encodings of the document
        ↓
the constructs              this specification              what a program is made of
        ↓
a runtime                   Swift, Kotlin, …                implementations. Many, replaceable
```

- A **front end** turns what a person wrote into a document. Its input syntax
  and its shorthands are its own; its output is this specification's. A front
  end owes nothing to any runtime and never produces anything runnable.
- The **document** is a program written down: a tree of data whose keys and
  slots this specification fixes. It is the only thing that crosses machines.
- An **encoding** is bytes for that tree. Two are specified below; a document
  is the same document in either of them.
- A **runtime** reads documents, checks, links and runs them, and brings the
  host's vocabulary. How it holds a program in memory is its own business.

## Conformance language

**must / must not** are requirements. **refuses** means the implementation
raises an error naming what was wrong and produces nothing else. No partial
value, no best guess, no reading what it recognised and skipping the rest.

Refusals happen at one of three stages, and the stage is part of the behaviour:

1. **Reading**. The bytes or the tree are not a document.
2. **Building**. The document is a document, and the program it writes is not
   sound: a name resolves nowhere, a call does not fit the declaration it
   reaches, a procedure no module provides. Nothing has run yet.
3. **Running**. The program was sound and the world disagreed: division by
   zero, overflow, a failure a procedure raised.

Two implementations that run the same programs identically and disagree about
which programs to refuse, or *where*. Are not the same language. A refusal at
the run where another implementation refuses at the build means something
already happened, and what already happened cannot be taken back.

The cases under `conformance/` name the stages **`load`**, **`build`** and
**`run`**. `load` is reading plus the half of the checking a document answers
alone. A document is checked as it is loaded, and to a caller the two are one
refusal surface; `build` is everything that needs the other documents.
Procedures, declared type names, signatures; `run` is running. So a `ref` that
resolves nowhere in its own document refuses at `load`, and a procedure no
module declares refuses at `build`.

Building is compiling and linking, the way it is anywhere else. Compiling
settles what each document says on its own, against the interfaces of the
documents it reaches. Linking lays the compiled documents down together and
answers what only the list can answer, such as which type answers which
contract. Which of the two refused is not part of the stage, because nothing
has run either way.

## The value model

A program computes over eight kinds of data, plus one value that is not data:

| kind | writes as | notes |
|---|---|---|
| null | `null` | |
| bool | `true` / `false` | |
| int | `1`, `-3` | signed, 64-bit; overflow **refuses**, it does not wrap |
| double | `1.0`, `1e2` | IEEE-754 binary64; a document cannot carry infinity or NaN |
| string | `"hi"` | Unicode text |
| bytes | `x"6869"` | `array<byte>` in a compact spelling. `byte` being `int(0...255)`, declared by `std`; what a carrying form carries when the payload is not text |
| array | `[ … ]` | ordered |
| record | `{ … }`, or `Name { … }` | unordered fields, names unique; may carry the **name** of the declared type it settled to |
| procedure |. | code with what it captured; exists only at run time, never in a document |

**A record's name.** A record made by a literal, answered by a native procedure
or read from a document has no name. It takes one the first time it settles into
a slot declaring a type whose structure is a record: an argument, a default, an
answer, a cast. From then on it carries that name wherever it goes, under
*Types* below.

**When two values are the same:**

- A whole number and a fraction of the same size are the same value. Numbers
are compared by what they are worth, not by which of the two they are. exactly,
at **every** size: `9007199254740993` (2^53 + 1) is neither equal to nor below
`9007199254740992.0`, however binary64 would round it, and ordering and `sorted`
read the same worth equality does.
- A fraction that is not a number is not equal to itself. There is one such
  value, no way to write it down, and the standard vocabulary never answers
  one. Arithmetic with no finite answer refuses instead, so it arises only
  from a host's own procedure.
- Bytes are the same when their bytes are, in order. Bytes are not text: no
  encoding is assumed, so no Unicode rule applies. Beside an **array**, worth
  unifies the way it does across numeric width: `x"6869"` and `[104, 105]`
  are worth the same. One collection of the same whole numbers in the same
  order, spelled two ways, and stay two values, the way `1` and `1.0` do.
- Arrays are the same when their elements are, in order.
- Records are the same when they hold the same field names bound to the same
  values and the same type name, or none. A record has no order, so order is
  not part of the answer; the name is part of what a record holds, so an
  `Account` and a `Vault` with the same fields are two values.
- Null is the same as null.
- **Text is counted and compared as a person reads it**: by extended grapheme
  cluster, under Unicode canonical equivalence. A letter written as a letter
  and the same letter written as letter-plus-combining-mark are one character
  and are equal; `"é"` is `"é"` whichever way its bytes spell it, and its
  `count` is 1. An implementation whose platform strings compare by code unit
  must not expose that comparison here.

## Types

A type is written as a string, or as a record for the two forms a string
cannot say:

| written | means |
|---|---|
| `null` `bool` `int` `double` `string` `bytes` | the scalar kinds |
| `number` | whole or fraction. The two numeric kinds and nothing else |
| `any` | anything |
| `never` | never answers. The type `std.control.abort` declares, and what makes a leaving call checkable |
| `array` / `dictionary` | a list / map of anything |
| `array<T>` / `dictionary<T>` | a list / map of `T` |
| `procedure` | some procedure, signature unsaid |
| `pure <procedure type>` | a procedure that answers without running, under *what answers without running* |
| `isolated <procedure type>` | a procedure that touches no name another body could touch at once; `pure isolated procedure` says both, and the reader takes the two in either order |
| `inout <type>` | a parameter handed a variable in place; written on a parameter's type and nowhere else |
| `{ linear: <type> }` | a type whose values are handed on exactly once; written on a type in `types` and nowhere else, and every slot naming that type carries it |
| `consuming <type>` / `borrowing <type>` | what a parameter does with a value handed on once: takes the obligation, or reads and leaves it. Written on a parameter's type and nowhere else |
| `var <type>` | a field a path may write through; written on a field of a type declared in `types` and nowhere else |
| `Task` (any declared name) | the type a module declares under that name, or a value of the membership it declares under that name |
| `some T` | a type parameter: worked out from the call, same reading everywhere it appears; bounded when the signature's `bounds` names it |
| `int(0...255)`, `double(0.0..<1.0)` | a number the slot admits only inside the range. The kind written out, either bound optional but not both, and `..<` leaving the far bound outside |
| `int?` (any string spelling and `?`) | the declared type or null. The one union written inline, and it is null-only. Any other is declared as a membership and named |
| `{ title: string, done: bool }` | a record type, written as the record it describes; structural, and it names nothing |
| `{ procedure: { parameters: …, returns: … } }` | a procedure type, written as the signature it takes |

Acceptance is one-way where the kinds nest: `double` accepts an `int` (a whole
number widens to a fraction; the reverse **refuses**), `number` accepts both and
nothing else, `any` accepts everything.

**A declared record is nominal.** A type declared in `types` whose structure is
a record is a name as well as a structure. When a nameless record settles into a
slot declaring the type, it settles to the declared structure and takes the
name; a record already under that name is settled again and keeps it; a record
under another name **refuses** at the slot, whatever its structure: at the
**build** where the build can see the name, at the **run** where the value
arrived through `any`, and `as?` reads it as null. Two declared records of one
structure under two names are two types, and a value fits only its own. A
declared name whose structure is not a record, an alias such as `byte`, attaches
no name. An inline record type and `dictionary<T>` are structural: a named
record fits them by structure, and what settles there is built on the slot's own
layout, which has no name. `any` declares nothing, so a value passes it as it
is, name included.

`inout` and `var` stand in front of the whole type, `?` included: `inout int?`
is a nullable handed in place. They say something about the slot and nothing
about the value, so what fits the slot is judged by the type after the
procedure. Writing either where it is not allowed **refuses** at the build. A
slot asking `isolated` takes what the build derived as isolated. Purity is a
separate claim and does not stand in for it.

**What a slot takes, exactly.** Where a value meets a declaration. An
argument, a taken default, an answer, and a write into a box that said what it
holds. The settlement is one rule per type:

- `any` passes the value through untouched, null and procedures included.
  Nothing settles, because nothing was declared.
- A **record type** says which fields there are. A value carrying at least
  them fits, and what settles is built on the declared fields: each is settled
  against its type, and a field the declaration never named is not carried
  past it. To keep names the declaration does not have, declare
  `dictionary<T>`, where the names are the value's own.
- A **declared name** whose structure is not a record is an alias: settling
  resolves the name and judges by what it stands for. One whose structure is
  a record is nominal, under *a declared record is nominal* above.
- A **nullable** (`T?`) passes null through and settles anything else against
  the declared half. `T?` takes `T`, null and `T?`; a `T?` reading does not
  fit a plain `T` slot. The `?` is written once, on the whole spelling, and
  only where it says something new: `int??`, `null?`, `any?`, `never?` and
  `some T?` each **refuse at the read**. A type with no string spelling. A
  record. Has no `?` to trail; a nullable record is reached through a
  declared name (`Task?`).
- The numeric edge is value-independent: `int` refuses every fraction, `2.0`
  included. Taking the whole ones would make fitting depend on the value
  rather than the type. `double` takes a whole number and settles it to the
  fraction it names; the widening is binary64's, so digits past 2^53 round as
  binary64 rounds. `number` passes either kind as itself. Settling to one of
  them would be the declaration picking, and it declined to.
- A **range** (`int(0...255)`, `double(0.0..<1.0)`) is a slot's condition on a
  number, not a kind: the value is an `int` or a `double`, and the bounds are
  judged where a value is settled, the way `enum` is. At the **build** for a
  constant argument or a default, at the **boundary** for what only the run
  can see.
  - **The kind is written out**, because a bound is a value of the kind it
    bounds: `int(0...255)` writes whole numbers and `double(0.0...1.0)`
    fractions, each in that kind's one spelling. `int(0.0...)` and
    `double(0...)` both **refuse at the read**. Neither range can be written
    with the other's bounds. A fraction range takes a whole number the one way
    the language widens (a `2` arriving at `double(0.0...5.0)` settles as
    `2.0`); nothing narrows.
  - **The far bound may be left outside.** `a...b` holds it, `a..<b` does not
   . The half-open interval a position below a length is written against, and
    for a fraction the one nothing can spell by moving a bound. The near bound
    is always inside, which is the convention every half-open interval is
    already read by; there is one spelling per range because of it. `..<` with
    nothing after it **refuses at the read**. It says the far bound is
    outside, and there is no far bound.
  - Before the run, acceptance reads a range as the kind under it on either
    side. Only what is provably outside is refused early, and a reading's
    worth is not knowable, so a call handing a declared `int` to an
    `int(0...255)` slot builds and the boundary judges. Two ranges are both the
    text's fact, so bounds that cannot overlap are refused early, across kinds
    as well as within one.
  - Either bound may be open (`int(0...)`, `int(...255)`); neither may be
    (`int(...)` says nothing and **refuses at the read**), and a range whose
    bounds admit nothing. `int(9...1)`, or `int(5..<5)` where the far bound
    is excluded and the near one stands on it. Is a slot no call could fit,
    **refused at the build** where the declaration wrote it, exactly as an
    empty `enum` is. A whole bound must be a number an `int` holds, and a
    padded or signed spelling (`int(007...)`, `int(+1...)`) or a bound past
    the procedure both **refuse at the read**, each named as what it is.
  - A module gives a range a name the way it names any type: `std` declares
    `byte = int(0...255)`, and there is no separate byte kind.
  - A bound is written as the value it is, so a fraction bound is a fraction's
    one spelling. A host may assemble a range bounded by an infinity. It
    orders like any other bound, and the build takes it, but no document
    spells one, so **writing that range out refuses**, the way every type a
    document cannot say does, rather than coming back as something a reader
    would reject.

`never` is a real type and fits **every** slot, by never arriving: an expression
typed `never` may be written where any value is expected. A conditional arm that
leaves, an argument that aborts, and evaluating it ends the evaluation it is
inside. The statement rules (no name, nothing follows) are statement rules; in
expression position there is nothing extra to say, because nothing after the
expression is reached at all.

**Type parameters.** A declaration may leave a type parameter and let the call
fill it: a procedure taking `array<some T>` and a `some T` answers what it was
given. A parameter read twice must be read the same both ways. Two readings
where one accepts the other settle on the looser; two readings that do not fit
are **refused**. Appending a whole number to a list of text is a parameter read
as text and as a number, and there is no answer that is both. It must be a
refusal rather than a silent widening to `any`: widening there is the checking
announcing it has stopped, in the one place it had just found what it was
looking for.

**Constraints.** A type parameter may be bounded: a signature declares `bounds:
{ T: Comparable }` once, its slots write `some T`, and every occurrence of the
name takes only what the constraint admits. The signature owns the bound. A slot
names the parameter and never the membership, so one bound is one claim however
many slots mention the name, and there is no inline union for the membership to
leak out through. A constraint is a **declared membership**. A module binds a
name to the types it admits, the way it declares a type. A slot may also declare
one as its type, and what stands there is a value of one of the members, which
is how the language says **A or B**: the set is declared once under a name, and
no slot writes an inline union. The judgment is made twice, once per surface: at
the **build**, a reading provably outside the membership refuses. Two booleans
meeting `lessThan` never run, and a reading the text says nothing about (`any`)
passes; at the **boundary**, the value that actually arrived is judged against
the membership, so what travelled in through `any` is refused where it arrives.
One name takes one constraint: two claims binding one parameter to different
constraints refuse at the build, and `bounds` naming a parameter no slot
mentions refuses at the read. Only the declaring procedure writes `bounds`. A
procedure *type* nested in a slot carries none, because its parameters are the
declaring signature's own slots and the declaring signature owns their bounds. A
constraint nobody declares, a constraint declared twice under one spelling, one
admitting nothing, and a name declared as both a type and a constraint all
**refuse at the build**. A member is a **concrete type**: `some`, `any` and
`never` in member position refuse at the build. Each says nothing a membership
could hold. And a type parameter lives in a signature: a declared type writing
`some` outside a procedure signature refuses at the build, because nothing there
is filled by a call.

**Handed on once.** A type written `linear` says the values of it are given
away: to a procedure, or as a body's answer. A body holding one hands it on **on
every way through, once**, and the build says so before anything runs. That is
what "this resource is closed exactly once" comes to, and it is the one claim
here that is about a value's whole life rather than about its type.

The mark is written on the declaration, so the obligation rides with the name:
a slot naming the type has it, and nothing can take it off. Writing `linear`
anywhere else **refuses at the build**, and so does carrying such a type inside
another type (a list, a record, another declaration): what follows the value is
the name holding it, and nothing follows one into a type.

**A slot naming such a type says what it does with it.** Two marks, written on
a parameter's type the way `inout` is, and a parameter that names the type and
writes neither **refuses at the build**:

| written | means |
|---|---|
| `consuming <type>` | the obligation moves to this slot. The caller's name is empty afterwards, and this body owes the value from here |
| `borrowing <type>` | the obligation stays where it was. This body reads the value and the caller still owes it |

Either is written on a slot that **names the type**, because the name is what
the build follows the value by. On `some T` it **refuses**: what fills a type
parameter is the call's, so a body that took the obligation there would have no
name to carry it on and the proof would end at that slot.

**A membership is one when every member is,** and `some T` bounded by one is
what every member of it is. A membership that admits a value handed on once
beside one that is not **refuses where it is declared**: a value of it would
carry an obligation on some readings and not on others, and which it was is
exactly what a membership does not say.

**A declaration whose body answers one writes `returns`.** What a declaration
answers is read off its body where nobody wrote it, and the mark is not
something a reading keeps, so a caller binding that answer would take an
obligation nothing told it about. It **refuses at the build**, by the result
and by every `return` that carries a value alike.

**A reading that may answer nothing does not take one.** `as?` onto a type
handed on once **refuses**, and so does writing `?` on one: what such a value
needs is a name holding it on every way through, and a `?` says there is a way
through where nothing is there.

**A closure is a procedure, and its body is held to all of this.** It is walked
the way a declaration's body is, seeded with what the closure itself was handed:
a closure that opens one and reaches its end still holding it is refused exactly
as a declaration would be. What it runs an unfixed number of times is the
*capture*, and a name the closure declared is its own.

**What such a body may not do is answer one.** A procedure type whose `returns`
is handed on once **refuses**, closure literals included, and a body that wrote
no `returns` is held to the same rule by what the walk finds: the rule turns
neither on whether a key was typed nor on how the answer was written. Nothing
reads inside a body that travels as a value, so what one handed back would
arrive with nothing to say it is owed. A declaration is not held to this: what
it answers lands on the name its caller binds.

Silence read as taking is what hid the second one: a procedure that only wanted
to look at a handle had no way to say so, and every slot that touched one took
it. So silence refuses rather than defaulting. Writing either where nothing is
handed on once **refuses** too, the way a `?` that says nothing new does: both
say what a slot does with an obligation, and there is none.

**No lifetime rides with a borrow.** The language has no references, so what a
slot was handed is a value of its own and cannot outlive what it was read from.
A borrow is the one sentence above and nothing more.

What a body may do with one:

- hand it to a slot that says `consuming`, which ends the obligation here;
- hand it to a slot that says `borrowing`, which ends nothing: the body still
  holds it and still owes it;
- answer it, which hands it to the caller, who owes it from there;
- read a part of it (`handle.name`), which hands nothing on.

What a body may do with one it **borrowed**: read it, read a part of it, bind
it to another name, and pass it to another slot that borrows. That is all.
Writing the name anywhere a value leaves by refuses, wrapping it in a list or a
record included: that carries the whole value out rather than reading a part of
it.

What **refuses at the build**:

- reaching the end of a body still holding one;
- handing one on a second time;
- handing one on in one arm of a conditional and not the other, since what a
  body holds afterwards would depend on which arm ran. An arm that **returns**
  is not one of those arms: no run comes back from it, so what the body holds
  afterwards stands on the arms that finish. An arm that `break`s is one of
  them, and is held to the same rule: the run comes back out of the loop still
  holding what the arm held;
- handing one on inside a loop round, inside an `attempt`, in a call of a value
  (`apply`), or capturing one in a closure. Each of those runs no fixed number
  of times, or fails somewhere the text does not show, so "exactly once" is not
  something the text says. Leaving is not one of these unless it leaves the
  procedure: a `break` leaves the construct and a `continue` ends the round, and
  what the body was holding it holds still on the other side of either;
- writing over a name still holding one;
- writing one into a **list or a record**, whether it is a name still holding
  one, a value nothing holds yet, or what a cast, a block or an `attempt` hands
  out. What follows the value is the name, and a name does not follow it into a
  type, so the obligation would be neither handed on nor still held;
- handing a borrowed one to a slot that says `consuming`, or answering it, or
  keeping it in a box. Each gives away what this body never took, and a box
  outlives the call that lent the value.

Only a procedure with **no body** ends the obligation. A body that takes one has
to hand it on like any other, so the chain runs out at a native procedure, which
is right: what a resource is lives outside the document, and only the side that
made it can close it.

Nothing about this survives lowering. It is proven at the build and there is
nothing left for a run to keep.

**Contracts.** A membership says which types a name admits. A contract says
which **procedures** a value answers, which is the other half of "what may stand
here" and the half a list cannot give: the types that answer a procedure are
open, and new ones arrive with new documents. A module declares one the way it
declares a type: a name bound to the procedures, each written as a signature
with no receiver, because the receiver is whatever satisfies the contract.

A type **satisfies** a contract when a document says it does. The document
writes the claim under `satisfies`, keyed by the type: `satisfies: {
"bank.Account": ["app.Describable"] }`. Any document may make one, about a type
it declared or about another document's, which is how a document that arrives
later gives a type the procedures a contract asks.

The build holds the claim to the declarations behind it. For every procedure the
contract asks, it takes the declaration named for the type and that procedure
(`bank.Account` and `describe` give `bank.Account.describe`) and holds its
signature to the contract's with the receiver filled in by the type.

Whether a type answers a contract is therefore a fact of the whole list, and a
claim may be written in a document the one leaning on it never names. A document
handing a type where a contract is asked is not judged where it is compiled: the
pair leaves the compile unresolved, the way a procedure the document sends and
does not declare leaves it, and **refuses at the call that leaned on it** where
the build cannot answer. A claim missing a procedure, or holding one whose
signature does not fit, puts its type under no contract and its reason is what
that refusal says.

A claim whose two names the list declares as something other than what the
claim needs of them **refuses at the claim**: a contract where the type
belongs, a type where the contract belongs, or a membership in either place.
One name has one declarer, so no document arriving later makes that right. A
name the list declares as nothing at all waits with the rest.

Two documents claiming one pair are one claim: a claim holds nothing but the
pair, so the second says what the first said.

A declaration named for a type and a procedure that no claim names is that
document's procedure and nothing else. So what a link declares never decides
what an unrelated document may call things, and a document that names no
contract builds the same whichever documents stand beside it.

A contract asking no procedures refuses, since every type would satisfy it. A
name is a type or a membership or a contract and never two of them.

A signature bounds a type parameter by a contract the way it bounds one by a
membership: `bounds: { T: app.Describable }`, and the slots write `some T`. A
value reaching such a slot is judged twice, once per surface, the way a
membership's is: at the **build** a reading provably outside refuses, and at the
**boundary** the value that arrived is judged by the name it wears.

A body calls a contract's procedure by writing the contract's name and the
procedure's with a dot between them: `app.Describable.describe`. That spelling
names no declaration, and what it means is settled by the value it is sent to,
so it is written with a receiver in front and refuses without one. What a call
hands it and what it answers are the contract's, not any one declaration's.

**The build builds the table and the run reads it.** For every contract, the
build gathers every type that satisfies it and lowers one call per type, each
against the row that answers, arguments in that row's own slot order. The run
reads the name the value wears and picks. Nothing is resolved while a program
is running.

A declaration answering a contract's procedure is reached **through the
contract**, which is the spelling that says which contract is meant. Two types
answering one procedure is the ordinary case.

**A name is its declared spelling.** The key a document declares a type,
constraint or procedure under is the whole of its name: `std.math.plus` is
declared under that key, and `wallet.Account` under that one. A mention is a
declared spelling, written out, and it means the same declaration wherever it
was written, inside the declaring document too. A dot is a character of the
spelling and nothing more: the language has no nesting, no scope and no
prefix, so what a document chooses to put before a dot is the author's
convention, and one document may declare `wallet.fee` beside `bank.rate` while
another declares `wallet.rate`. A spelling no module in the link declares
**refuses at the build** where it is mentioned. There are two namespaces,
procedures and types, and a procedure may be spelled like a type. Types,
memberships and contracts share the second, and no name in it is two of them,
so a mention reaches whatever declares it: a slot names a type or a membership,
and a bound names a membership or a contract.

The shared `std` module (the foundation bundle) declares the memberships the
standard procedures are bounded by: `Numeric` admits `int` and `double`;
`Comparable` admits `int`, `double` and `string`. A bundle whose signatures
mention them. `std.math`, `std.collection`. Links only with `std` in the
build, which is the one dependency the standard bundles have.

## The document format

A document is one record. Every record below is **closed**: a key not named
here **refuses**. Every slot marked *expression*, *block*, *statements* or
*type* takes the grammar of that name.

### The module

| key | takes | required |
|---|---|---|
| `warp` | int. The language version this document is written for | yes |
| `imports` | array of strings. Every procedure the program calls and does not declare | yes, and empty where the program uses none |
| `description` | string | no |
| `types` | record: name → type | no |
| `constraints` | record: name → array of types the name admits | no |
| `contracts` | record: name → record: procedure → `{ parameters?, returns? }` | no |
| `satisfies` | record: type name → array of contract names that type answers | no |
| `const` | record: name → expression | no |
| `var` | record: name → expression; a variable every procedure beside it may read and write | no |
| `procedures` | record: name → procedure | yes, and not empty |

**A module variable.** Its start is written like a constant and settles the same
way: at the **build**, from native procedures alone, beside the constants and
reading them. Its type is the type of that settled value, and every write into
it is settled against that type. It is private to the document like a constant,
read by the same spelling (`ref`), and written by a `set` in a procedure the
document declares, or through a parameter such a procedure hands it to in place;
another document reaches it only through such a procedure. A name is a constant
or a variable, not both: one declared under both keys **refuses** at the load.
Every run starts each variable at its settled value, so two runs of one image
never see each other.

**The version.** Every document says it, and one that does not **refuses**. As
not a document rather than as a malformed one. A reader that filled in a default
would be answering, on the sender's behalf, the one question that has to be
answerable from the bytes alone; and a file of some other kind entirely would
get as far as having its keys judged. Nobody writes the number by hand anyway. A
front end computes it, so a document without one did not come from one.

The current version is **1**; the earliest that ever existed is **1**.
Pre-release, so the two ends of the reading range are one number. A reader must
refuse a document written for a later version than it implements, before judging
the document's keys. A later version may add keys, and checking the keys first
would turn "I am too old for this" into "this is malformed". A document claiming
a version below the earliest **refuses**. The number goes up when anything
portable changes what an existing program *means*: a type added, a type read
differently, a checking rule moved, a standard procedure answering differently.
It does not move when a procedure is *added*, since a program that does not call
it cannot tell, and one that does is refused by name.

What each version was:

| version | what moved |
|---|---|
| 1 | the language as specified here |

An implementation implements the **current** version only. An older document is
read, and held to the current rules. A program that leaned on what moved is
*refused with the reason named*, not quietly run to a different answer, and
that refusal being explicable is what the number buys. Forward compatibility is
not available to anyone: what a reader can do about a version it has never
heard of is refuse, and the point of the number is that it can.

**The imports list.** What the program *sends* and does not itself declare. From
procedure bodies and from constants alike, each by the spelling it is sent by,
which is its declared spelling: `std.math.plus`, never `plus`. A native
procedure's sends are in it too. What a body sends is read off its text; a
procedure implemented in the host language has no text a reader could read, so
the procedure declares the procedures it sends and those count the same. A
module whose native procedures send things its list never mentioned would
understate what the module does, which is the one thing this list may not do.
The list is that set exactly, not a bound around it: **reading refuses** a
document whose list disagrees with what its program sends, in either direction.
A stage-1 refusal, and it can be, since what a program sends is a fact of its
text alone. The list is read before the program and a caller grants from it, so
a list saying less would be trusted and wrong, and a list saying more asks for a
grant the program has no use for.

**A module asks and does not carry.** What the list names is supplied by
whatever else stands in the link, and a module that shipped its own copy of a
bundle it uses would put that bundle's declarations in the link twice, which
the build refuses by the rule that one name has one declarer. Which modules
are in a link is decided where the link is assembled, the same way a program's
libraries are chosen where the program is built rather than by each library in
it. The same holds for the types and memberships a signature mentions, which
the list does not name: a module declares against a vocabulary and expects to
be linked beside whatever declares it.

A document says it, and one that does not **refuses**. The way one that does
not say its version does. Silence is not a claim a caller can act on: the list
is read before the program and a grant is decided from it, so a reader with no
list cannot tell a program that touches nothing from one that touches
everything, and the empty list is what says the first. Nobody writes it by
hand. It is computed from the program the way the version is filled in by
whatever produced the document, and the canonical writer always writes it.

It is refused after the types are read and not before them. A missing list is
the least specific thing that can be wrong with a document, and refusing for it
first would make it the only thing an author ever heard about. That ordering is
an implementation's to choose, though, which is why every case in the suite
writes the list, including the ones whose programs will not read at all. A case
with two things wrong with it is a case any reader passes for the wrong
reason.

### A procedure

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

### A procedure the host answers

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

### What answers without running

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
  `pure procedure`. That is the one place something before the run says what
  the value answers; on any other name nothing does;
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
closure as a value, so a slot reads it wherever the value arrives.

**What it permits.** Three places, and they are what the claim is for:

- a **constant** and a **module variable** settle at the **build**, from these
  procedures alone;
- a slot may **ask** for one, writing `pure procedure`. That is how
  `std.logic.and` takes sides it may decline to read and how
  `std.collection.filter` takes a predicate that cannot reach the world;
- an **operand** may call one. A call's arguments and the receiver written in
  front, a `conditional`'s `when`, a `loop`'s `while`. Each of those is read
  rather than run, so an operand calling anything else **refuses at the
  build**, and so does one calling a value.

Choosing among values is a procedure here rather than a construct, because an
operand is read rather than run and a construct is not one. `std.logic.select`,
under the vocabulary.

### A parameter

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
way, and a name the declaration does not have refuses in all of them.

**A parameter handed in place.** A parameter typed `inout T` takes no value:
it takes a variable. The argument is `{ ref: <path> }`, and all of this is
held at the **build**:

- the path's head is a variable where the call stands. A fixed name, a
  literal and a call's answer each **refuse**;
- the path is one a write may take, under *what a write reaches* below;
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

### A statement

A record carrying **at most one** naming key and its expression under
**`value`**: `{ let "x" value { call {…} } }`, `{ value { loop {…} } }`. A
construct sits inside `value` under its own key, and that is the one place a
construct key is read; a construct written as an operand (an argument, a
receiver, an element of an array or a record) **refuses**.

The naming key says what the statement does to its name:

| key | means |
|---|---|
| `let` | fixes the name. Written once, never again |
| `var` | introduces a name that may be written again |
| `set` | writes a path headed by a variable: one a `var` declared earlier, or a module variable. `set "p.x"` and `set "people[0].name"` write into what the head holds |

**A name may say what it holds**, under **`type`**, written the way a
parameter's type is: `{ let "x" type "double" value 1 }`. The declaration is
what the name holds, and the build works out a reading only where the name
declares none. What the statement was given has to fit the declaration, and a
declaration naming a type nothing declares **refuses at the build**, as does one
naming a type parameter: what fills a parameter is a call filling the slot that
names it, and a name inside a body is no such slot.

A declaration is a boundary like a parameter's, so **what the name takes is
settled against it** the way an argument is: a whole number given to a `double`
is held as a fraction, a value outside a declared range **refuses at the run**,
and a record settles to the declared layout.

A `set` reaches a name something else declared and a statement with no naming
key introduces none, so `type` beside either **refuses at the load**. So does
`type` on a statement whose construct binds the name itself. A `loop`'s round
and an `attempt`'s failure are the construct's to say.

A declared name is fixed at what it says: a write into a declared `var` is held
to the declaration and does not retype it, the way a write into a module
variable or an `inout` parameter is. This is what lets a name be handed to an
`inout` slot, which asks for the same type the name is. A name whose reading
the build worked out is that reading, and a name that says what it holds is what
it says.

A statement with no naming key, `{ value … }`, runs its expression and binds
nothing. The answer is dropped, which is how an effect is asked for on its
own. Three
families step out of this freedom, in different directions:

- The constructs that bind **through** the statement's name. `loop` (its
  round), `attempt` (its failure). **require** one. With no name there is
  nothing for the body to read those bindings under, and a reader that
  invented a name would have invented a real name somewhere. Writing one
  nameless **refuses**.
- The leaving constructs (`return`, `break`, `continue`) take **no** naming
  key at all: such a statement never finishes, so its name could never bind,
  and a key that promises a binding that cannot happen **refuses**. The same
  rule reaches a **call**: a statement whose procedure declares `returns: never`
  binds nothing and takes no name. Held at the **build**, because only the
  build knows the signature, where the leaves the text shows are held at the
  load.
- A **`conditional`** takes no naming key either, for the other reason: it
  finishes, but it answers nothing and binds nothing inside. A condition
  chooses a way through the body, not a value. What an arm keeps it writes to
  an outer variable with `set`, and a value leaves through `return`.

**What a write reaches.** A `set` names a path, and the head of the path is the
variable written. Every segment after the head is judged at the **build**
against the type the walk has reached: a field of a type declared in `types` is
passed through only when the declaration wrote it `var`; a field of an inline
record type, an entry of a `dictionary<T>`, and an element of an array are
passed through as they are, and a `dictionary<T>` entry the value does not hold
yet is made by the write; `any` and a nullable type are not written into, and
an optional segment (`?.`, `?[`) is not written through, because a write reads
no absence. What is written has to fit the type the path reaches, and is
settled against it, so a box that said what it holds is laid out the way its
declaration says after a write as it was after its declaration. A path that
reaches no declared type settles nothing and the value stands as it was handed.
A write to a whole local variable retypes it unless the variable declared what
it holds, under *what a variable reads as* below; a write to a module variable
or to an `inout` parameter has to fit the type the box holds and retypes
nothing. At the run the value is computed first, and then the box is rewritten
once, so nothing observes the box halfway. An index written as a name (`xs[i]`)
is read where the write stands and must be an int; the write lands on that one
position.

**A `var` may stand alone.** A statement that is only `{ var "name" }`, with no
`value`, introduces the name with nothing in it yet, and a name holding nothing
holds null. It is the declaration a conditional's arms write into; what the name
reads as afterwards is under *what a variable reads as*, below. The other two
spellings say something about a value, so they still require one.

**One name, several askers.** A statement's name names the statement, and every
reader of it reads that one fact: an expression reads the value the statement
bound; a body inside a binding construct reads the construct's own binding under
it (`round.index`, `tried.message`); a `break` or `continue` names the loop
statement it ends. These are not three names sharing a spelling. They are one
name, asked three questions, and which question applies is fixed by where the
asker stands. What keeps the readings from colliding is scope, stated per
construct: a loop's round is readable in its condition, body and result; an
attempt's name binds the failure only while the rescue runs, so the binding
reading and the value reading are never live at the same place.

The construct keys, each detailed below and each written inside `value`:
`call`, `conditional`, `loop`, `attempt`, `block`, `return`, `break`,
`continue`. `value` holding anything else holds an expression, under
*Expressions* below.

### Statements: the constructs

**`call`**. A message:

| key | takes | required |
|---|---|---|
| `procedure` | string. The procedure sent | yes |
| `of` | expression. The receiver | no |
| `arguments` | record: name → expression | no |

A body a procedure is to run travels as a **closure argument**, like any other
value. There is no second channel for bodies: one kind of thing crosses into a
procedure, and it is the isolated one.

**`conditional`**

| key | takes | required |
|---|---|---|
| `when` | expression. Must answer a bool | yes |
| `then` | statements | yes |
| `else` | statements | no |

A conditional is a statement: it **answers nothing**, and it **takes no name**.
The condition chooses a way through the body. An arm is statements alone, with
no `result` slot, because there is nowhere for a result to go. What an arm keeps
it writes to an outer variable with `set`, and a value leaves the procedure
through `return`. Both arms are checked whether or not they are taken.

**`loop`**

| key | takes | required |
|---|---|---|
| `while` | expression. Runs another round while true | yes |
| `body` | statements | yes |
| `result` | expression | no |

The loop's own statement name binds the round it is on, readable everywhere the
loop is still speaking. The `while` condition, the `body`, and the `result`.
The condition reads the state before the round it would start, so `round.index`
there is how many rounds have finished. What a loop answers is its `result`
read in what the last round that *finished* left behind; a round cut short
contributed nothing. A loop naming no result answers nothing.

A loop carries no budget of its own. Bounding one is the author's to write. A
counter in the condition and a procedure past the bound say it exactly, and
stopping one is the receiver's **cancellation**, under Running below. A kernel
budget would promise neither side anything it could rely on: the author can
already say it, and the receiver could not trust a bound the author chose.

Walking a collection is this construct too, and there is no second one for it.
The round is read against the material's count and the element is read at that
index, so what a walk needs beyond a loop is `std.collection.count`, a
comparison and an index. All three are already there, and none of them is
grammar.

There is no concurrency construct either. Running things at once is
**vocabulary**. `std.concurrent`, below, because a closure is already the one
body that is safe to run beside another, and "takes closures" is a thing a
signature can say. A loop is grammar for the opposite reason: its body writes
the enclosing names, and that is exactly what no signature can say. That is also
the line between the two ways to walk. Reach for a loop when a round writes
outward or leans on the round before it, and for a procedure.
`std.collection.map`, `filter`, `std.concurrent.map`. When each element's work
stands alone, which is what lets the concurrent `map` run it at once.

**`attempt`**

| key | takes | required |
|---|---|---|
| `body` | statements | yes |
| `result` | expression | no |
| `rescue` | block. Runs if the body fails | yes |

A rescue catches failure. What the world did. It does not catch leaving. What
the program said. A rescue with nothing in it. No statement to run for effect,
no `result` to answer. **refuses at the check**: it would swallow a failure into
null without a trace. A rescue over a body that cannot fail **refuses at the
build** for the other half of the same reason: it is a body no run reaches. This
is the one exception to a block's optional `result`, and the failure is the
reason. The statement's own name binds the failure **while the rescue runs**,
and what it binds is a **record declared `{ type: string, message: string,
details: dictionary<any> }`**. `type` names what happened (`aborted`,
`concurrent_failed`), `message` is text for a person, and `details` is what the
failing procedure carried. Every failure holds all three by construction: a
runtime assembles the payload from what a failure declares, so no procedure can
hand over one without them and there is nothing here for a run to check.

The envelope is this specification's; what rides in `details` is the procedure's
own. `concurrent_failed` puts `failures` there, every piece's reason keyed by
the piece.

```
{ ref "failed.details.failures" }
```

`cast_refused` has no procedure behind it, so this specification names its
`details` too: **`expected`**, the type the cast wrote, and **`actual`**, the
kind the value arrived as, both as text. Both halves, because what was asked for
is readable from the program and what turned up is not.

```
{ ref "failed.details.actual" }
```

`details` holds `any`, so a value read out of it is read as anything until a
type is named for it. A field the envelope does not name is not reached by a
dot on the failure itself: `failed.failures` names nothing.

A failure is data the moment a rescue holds it, which is why no ninth kind
exists for it.

**What a body may fail with is known before it runs.** The build derives it the
way it derives purity and isolation, and the types a failure names itself by
(`aborted`, `cast_refused`) are what it derives: a body fails with what its
plain casts fail with (`cast_refused`, the one failure the runtime itself
raises; `as?` reads the same mismatch as null and raises nothing), with what
the declarations it calls fail with, and with whatever its rescues fail with,
the body under a rescue being caught. Calling a value (`apply`) leaves the
question open, since nothing before the run says which value.

A native procedure says what it may fail with, the way it says whether it is
isolated. **A procedure that says nothing fails nothing**, which is right for
the many procedures that throw only at an author mistake, and a procedure that
can fail says so. `std.control.abort` says `aborted`; `std.concurrent` says
`concurrent_failed`, every piece's recoverable failure being gathered into that
one. A procedure that fails and does not say so has broken its contract, the
same way one that holds state and calls itself isolated has.

**`block`**. A body written as a statement, and nothing more: the bare member of
the same family as a `conditional` arm or a `loop` round, with the condition
left off. Like any statement it *may* take a name, and its name binds what its
`result` answers. Because a block runs here, once, in the same flow. A fact the
text shows, since no expression can carry a block away. A block may `set` the
enclosing variables, exactly as a `conditional` or `loop` body may. A fence for
names, not a door to elsewhere. (See *two kinds of body*, under Concurrency.)

**`return`**. Answer the enclosing procedure from here. Takes an expression,
or nothing (`return:` with null) to answer nothing. The answer must fit what
the procedure declared.

**`break`**. End a loop. **`continue`**. End the round and go on to the
next. Each takes a loop's statement name, or nothing for the nearest enclosing
loop. Both **refuse at the check** when nothing encloses them: a closure runs
away from where it was written, so the loops around the writing are
not around the running, and neither crosses into a procedure written inside
another.

Nothing may be written after a `return`, `break` or `continue` in the same body:
it would never run, and the name it would bind would never bind. The same holds
after a call whose procedure declares `never`, at the build. The rule reaches
through structure, because the fact does: a `conditional` both of whose arms
leave never finishes either, so nothing may follow it. Held at the **load**,
since the arms are text. A construct that can finish. A conditional with no
`else`, a loop, an `attempt` (its rescue may finish normally). Is not a leave,
however its bodies end.

There is no `abort` construct. Failing on purpose is a procedure.
`std.control.abort`, below, because a signature can say everything checking it
needs: `returns: never` is the whole fact, and a thing is grammar only when
checking it would need to understand more than a signature can say.

### Expressions

A scalar is itself. A literal. A string is always literal text; nothing inside
it is ever re-parsed. An array is an array of expressions. A record is a record
of expressions. **unless** it carries one of the form keys:

| form | means |
|---|---|
| `{ ref: a.b[0] }` | a name, resolved in the consuming scope; the record must have no other key |
| `{ value: <data> }` | the escape: exactly this data, as a literal, even if it looks like a form |
| `{ call: <message> }` | a message where a value is wanted; same grammar as the `call` construct |
| `{ closure: <procedure> }` | a procedure written where a value is wanted; same grammar as a procedure |
| `{ as: <type>, of: <value> }` | read the value as that type. The door onto what `any` declares nothing about |
| `{ as?: <type>, of: <value> }` | the same, reading a mismatch as null rather than refusing; the answer is `T?` |
| `{ format:, with: }` | reserved: a front-end spelling (below); **refuses** in a document |

A **cast** names the type a value is read as. The type is written the way any
type is. A name, or the mapping a record or a signature is written as. From
the cast on, the reading *is* that type, so every dot after it is judged
against it; the run is left the one question the build cannot answer, which is
what actually arrived, and it answers it at the same boundary a parameter's
argument passes through. A plain `as` **refuses at the run** when the value is
not that type. A failure like any other, so an `attempt` catches it, and
`as?` reads that mismatch as null, which is the author saying they expected it.

A cast that names the type the reading already **is** refuses at the build, the
way a needless `?.` does: the claim says nothing. Sameness, not admission. A
reading of `int` cast to `int(0...10)` names something the types do not prove,
and only the run can say whether it holds. A cast to a declared record name is
the settling written out: reading a nameless record as `Account` attaches the
name, so it is never a cast of what the reading already is, and only a reading
that is already `Account` makes it one. A cast onto `any`, `never` or a type
parameter refuses for the other half of the same reason: those name no type to
read.

A cast between a reading and a type **no value is both** refuses at the build
too: it could not succeed on any run, so `as` would refuse every time and `as?`
would answer null every time. A null that says nothing about the value. Two
ranges are read here the way acceptance reads them: `int(0...5) as int(10...15)`
names a value no run produces, so it is refused where it is written. So is a
reading under one declared record name cast to another: a `Vault` is never an
`Account`.

A cast that names a type nothing declares **refuses at the build**, wherever it
is written. The rule every type spelling is held to. `as?` reads a value that
is not the named type as null; it does not read a name that names nothing as
null, because that is the declaration being wrong rather than the value.

The form keys are fixed. A record that carries one as plain data must be
quoted with `{ value: … }`. Quotation is a fact about the document, not about
the expression it writes. A construct key under a statement's `value` is read
as its construct; under any other `value` it is a field.

**A dot reads a name and nothing else.** Every `ref` path is judged where names
resolve, and the judgment is written into the image; the value that arrives at
run time has no say in it. A procedure is sent with a written `call`, which
spells the declaration it means. Segment by segment:

- On a **record type**, a dot reads the field the type declares. A field it does
  not declare **refuses at the build**, `?.` or not. The type proved the
  absence, and no spelling reads past a proof. A procedure on a record is
  written as a call. A record type says which fields there are, so there is
  nothing else to reach: data that arrived under other names was not carried
  past the declaration. To read names a declaration does not have, take
  `dictionary<any>`.
- On a **dictionary**, a dot reads an entry; which names are there is the run's
  fact. An absent entry **refuses at the run**, unless the segment is
  written `?.`, which reads it as null.
- On a kind that has no fields. Text, numbers, arrays, bytes, booleans,
  procedures. A dot **refuses at the build**: there is no name there to read,
  and the procedure by that spelling is reached by writing the call.
- On **`any`**, a dot, or an index. **refuses at the build**. Nothing is
  declared here, so there is nothing for the reading to be judged against, and a
  dot no declaration proves is the one thing a run would have to decide for
  itself. The type is read by naming it: `{ as: <type>, of: <value> }` says
  what the author expects, and every dot after it is judged against that.
- On a **type parameter** (`some T`), whose type is the call's fact, a dot
**reads data**: the type is declared, at the call rather than here, so the
segments stand as written and what the call filled in answers them. What the dot
reaches is a type the call decides too. Dots go on standing after it. but it is
**not the parameter**: `of` is the type the call filled in and `of.a` is a
field of that type, which is a different unknown, and it carries none of the
parameter's bound. So a name holding `of` on one way through and `of.a` on
another holds neither, and one holding `of.a` twice holds one type. Which field
of which parameter a walk reached is all that decides this. So `of.a` and
`of?.a` are one field read twice. A mark says what is expected of the *value*
and says nothing about where the walk landed. A name given to a step along the
way arrives where the unbroken walk arrives (`held` holding `of.a`, then
`held.b`, is `of.a.b`), and two parameters written `some T` hold one type, so
the same field of either is the same field.
- **Null is not read through.** A segment whose receiver is null, or whose
  reading says it may be (`T?`). **refuses**: at the build where the text
  shows it, at the run otherwise. `?.` is the one spelling that expects
  absence on a name: it reads the null (or the absent entry) as null for the
  whole path, and the path's own reading is nullable for the same reason.
  `?[` is that same mark on an index, and what it expects absent is the
  **array itself**. Never an element.
- An **index past the end refuses at the run**. The array is there and says
  how long it is, so a reading that misses it read the length wrong. `?[` does
  not change this: it is `?.`'s mark on an index. It expects the **array's**
  absence, not the element's, so `items?[0]` reads a null array as null for
  the whole path, and still refuses past the end of one that arrived.
- A `?.` or `?[` that could not have read past anything. On a record's
  declared field, on an array the type proves is there. **refuses at the
  build**, the way a `?` that says nothing new refuses on a type spelling. The
  claim of absence has to be one the types leave open.
- The **head of a path takes no mark**. A head is a name a scope holds, and
  there is nothing before it to read past: a name that answers nothing is a
  reading gone wrong, not an absence a mark can expect. `?.name` and `?[i]`
  written first in a path **refuse**. Wherever the path is judged, and
  whether it was written as text or built as segments.

A constant-headed path never reaches a run: it is judged first like any path.
The constant's settled value is its declared type, so an absent field or a
needless `?.` refuses by the same rules, and then folds at the build to the
value it read. A constant settles from **native procedures alone**: a procedure
with a written body is itself still being resolved beside the constants it may
read, so a constant that runs one would be a circle with no start, and it
refuses at the build. Settling asks those procedures, so a link answers native
procedures before any of the program runs. An index written as a reference
(`items[i]`) is a path of its own, judged wherever the outer walk stops: a
reference that provably is not a whole number refuses at the build, and one that
names nothing refuses at the run.

The same brackets read a **dictionary** by a key the run settles (`held[name]`),
which is what walking one is for: `keys` answers the names and this reads the
entry under one. What stands between the brackets is judged where an index is,
and has to be able to be a string. An entry that is not there refuses at the run
the way a written key does, and `?[` reads it as null. A record takes no such
reading: its fields are the type's, so a name the run settles has nothing there
to be judged against.

### Blocks

A block is `{ body: <statements>, result: <expression> }`, both optional. A
block answers what its `result` names, and nothing if it names nothing.

## Spellings are not part of the document

A front end may offer shorthands. Operator keys like `is:` in a condition
slot, a `{ format:, with: }` template. That stand in for types the language
already has. They are the front end's own: it spends them before the document
leaves, and what leaves writes the types themselves.

A reader of documents **refuses** the spelled keys rather than reading them as
data. The reserved set is exactly `format` and `with`. An operator key like
`is:` lives inside a condition slot a front end owns and can never reach a
document, so it needs no reservation. The two stay reserved whether or not any
notation offers them. A document that writes one was written *for* a spelled
notation, and reading it as a record that happens to have those fields would
be running a program nobody wrote.

## What an implementation checks, and when

A program is read, checked and built before any of it runs. Including the
arms nobody takes. All of the following are answered while nothing has
happened yet:

- every `ref` resolves to a parameter, a constant, a statement written before
  it, or a path through them;
- every procedure sent is declared by some module in the link, exactly once;
- every call fits the declaration it reaches: arguments by name, receiver,
  and answer, with type parameters bound as above and every bound judged
  against its constraint's membership;
- every declared type names a type that exists;
- a condition answers a `bool`. A `conditional`'s `when` and a `loop`'s
  `while`, held where they are written, and `any` passing the way it
  passes any other slot;
- every candidate a parameter's `enum` lists is written in a value's one
  spelling, the one the declared type's own values wear. A dead candidate
  no call could ever match refuses, the empty and the all-dead list being
  the plainest cases. A range's bounds admit something, and a `default` is
  a value the parameter itself admits. `type`, range and `enum` together;
- a slot declared `pure` takes only a procedure that answers without running,
  under *what answers without running* above; a slot declared `isolated` takes
  only a procedure the build derived as isolated;
- a slot declaring a membership takes what the membership admits, and a value
  of a membership stands only where every one of its members would. A cast
  tells the members apart, and a cast onto a type the membership never holds
  refuses the way any impossible cast does;
- a parameter bounded by a contract takes only a type some document says
  answers it, and every claim is backed: each procedure the contract asks has a
  declaration named for the type and the procedure, held to what the contract
  wrote;
- every value of a type written `linear` is handed on exactly once on every way
  through the body holding it, and to a slot that says `consuming`; every
  parameter naming such a type says `consuming` or `borrowing`, and what a body
  borrowed it does not give away;
- every `set` writes a path headed by a variable, through fields declared
  `var` where the type is a declared type, and what it writes fits what the
  path reaches; a write into a module variable or an `inout` parameter fits
  what the box holds;
- every `inout` parameter is handed a variable's path a write may take, and
  no call hands one variable to two parameters;
- `inout` is written only on a parameter's type, and `var` only on a field of
  a declared type;
- what a closure writes into a variable it captured fits what the capturing
  body holds;
- a value read under one declared record name fits no slot declaring another;
  a nameless record reaching such a slot is judged by type and takes the name
  at the run, and a named record arriving through `any` is judged by name at
  the run;
- a constant is the type it was declared as;
- `break`/`continue` have a loop, `return` fits the declaration, nothing
  follows any of them;
- a statement that never finishes. A syntactic leave, or a call whose procedure
  declares `never`. Takes no name, and nothing follows it;
- every name the program writes as a value. A statement's, a binding's (a
  loop's round, an iteration's element, an attempt's failure), a parameter's,
  each segment of a `ref`. Is **written**, and is **normal form C**, compared
  as bytes. Record *keys* hold this line at the encodings; these are the names
  that live in string values, and this is where they hold it. One name has one
  byte spelling, so a declaration and a reference can only meet by being the
  same bytes. `é` written two ways is a refusal, not two names. Nothing
  written is no name: a declaration is called something, and a reference
  writes something, and neither is done by writing nothing.

The `imports` list is deliberately not on this list. It is held at *reading*,
above, because a caller decides from it before any of this runs.

**What a variable reads as.** A name a statement fixed reads as what that
statement bound, and a variable reads as what the ways through the text could
have left in it. The checking follows the flow the running takes:

- a name that **declared** what it holds reads as that declaration, and no
  write changes it. What is written is held to the declaration instead;
- an **unconditional** write retypes a name that declared nothing: after `set
  x` at the top of the flow, `x` reads as what was written, whatever it held
  before;
- a write only **some** ways make. One arm of a conditional, a loop's round, an
  attempt's body. Joins with what the name held. Null beside a value reads
  `T?`: after `var x` and a conditional whose one arm sets an int, `x` reads
  `int?`, because the run either took the arm or did not. Two values of
  different kinds join to `any`. Where readings disagree the slot holds
  neither, and a join that guessed would be a refusal an author cannot act
  on. This join is not the variable's own rule: it reads wherever two
  readings of one slot meet. An attempt's body beside its rescue, an array
  literal's elements, so an attempt whose rescue answers nothing reads `T?`
  too, and `[1, null]` reads `array<int?>`;
- a write **both** arms make is unconditional again, whichever arm ran, the
  write happened, and an arm that **leaves** contributes nothing: no run comes
  back from it, so the ways that finish are the only ways a reading after the
  conditional can stand on. `var x` with one arm setting an int and the other
  returning reads `int` afterwards, plain;
- what an arm **declares** (`let`, `var`) stays its own. Declarations die with
  the block, and only the box a `set` writes outlives it.

**This is not a proof and does not pretend to be.** Whether a number will be
zero when something divides by it is not decided by reading. What moved is the
line between "found out by running" and "found out by reading" A long way,
not all the way.

An interpreter that reports a defect on the path you happened to take is
sampling, not checking. A program that arrived has branches nobody ran before
sending it, and the one that matters is the one that only fires in production.
There is no opportunity to find out by trying, because trying *is* production.

## Running

- Statements run in order; each binds its name in the scope of what follows.
- A call's arguments are evaluated in **name order**. Almost nothing can
  observe this. Arguments evaluate without effects, but two arguments that
  would each refuse surface one refusal, and which one is the text's fact,
  not a hash table's.
- `std.collection.keys` and `values` answer in the record's **canonical
  order**. Names ascending. For the same reason: a program that walks them
  gets the same walk on every run.
- A procedure's answer is held to `returns` where both are written. A body and
  the declaration beside it are one document's text, so what the body reads is
  judged at the **build**: a reading the declaration does not take refuses
  there. A reading the text opens to `any`, which is what applying a value
  reaches, stands at the build and is settled at the run's boundary instead. A
  body cannot leak a value its declaration did not admit either way. A
  **constant** answer is a value and not only a type, so it is held to what
  the declaration admits as well, the way a constant argument is. A closure
  literal writes a signature and a body side by side too, and is held the same
  way where it is written.
- **A `returns` nobody wrote is read off the body.** A declaration with no
  `returns` still answers something, and what it answers is what its body
  hands back: the `result` it names, joined with every `return` that carries a
  value out. A call site is judged against that, so a dot on what such a call
  answers stands where the body states a type. The type does not have to be
  written twice.
  - The reading never becomes the declaration. What the author wrote is what a
    document written back out carries and what the boundary settles against; a
    type read off a body is the build's own reading, and reaches exactly as far
    as readings do.
  - It is worked out in the **call graph's order**. Each declaration read
    after everything its answer could come from. Declarations whose answers
    reach one another in a circle, a recursive one included, read as `any`: an
    answer worked out from itself is not one the text states. Writing `returns`
    says more, and removes the circle by saying it.
  - A body no way through comes back from. One that always aborts. Answers
    `never` by this reading, and a statement binding such a call takes no name,
    exactly as one calling a declared `returns: never` does.
- **A run can always be stopped from outside.** Cancellation is observed
between statements and at the entry to every round, including a round with an
empty body. This is the receiver's one lever over consumption, and it is the
whole of the language's promise about time and memory: a program calling only
the standard vocabulary can run forever, and nothing here predicts it. what is
promised is that it can always be told to stop.
- Leaving (`return`/`break`/`continue`) travels out through whatever it is
  inside, and is not a failure: a rescue does not catch it. It does not cross
  a closure's edge: `return` inside a closure answers the closure.

**Concurrency is isolation, and it is granted.** Warp's values are all data,
so the only thing two bodies running at once could contend for is a written
name, or a box a native procedure holds. What may run beside another body is an
**isolated** closure, and which closures are isolated the build works out, the
way it works out purity:

- **Two kinds of body, told apart by where they are written.** Every
  `body`/`block` slot the document grammar has. `block`, a `conditional` arm, a
  `loop` round, an `attempt`'s body and its `rescue`, all of them, present and
  future. Holds a **block**: a body that runs here, in the flow that wrote it,
  and that is visible in the text, because no expression can carry a block away.
  A block may `set` the enclosing variables. The one body that becomes a value
  is the **closure**. A *procedure*, with parameters and a declared answer, and
  a value may cross into a procedure, where no signature can say when, how
  often, or beside what the procedure runs it. So the split is carried by
  spelling rather than worked out by analysis: which of the two a body is, is
  what it is written as. The slot *is* the proof, and there is nothing in
  between: the one channel into a procedure is the isolated one. Not two flavours of one thing,
  either: a block has no parameters because a body that runs where it stands has
  nothing to be handed, and a procedure has them because crossing a boundary is
  exactly when arguments exist.
- What a closure captures is the name as it is: a fixed name's **value**, and
  a variable's **box**. Making a closure runs nothing; a variable set between
  the making and the calling is seen by the call,
  because the box is one thing under one name everywhere it is visible. The
  closure's body is one of those places, so a closure may `set` a variable
  it captured; what it writes has to fit what the capturing body holds, held
  at the **build**, because the capturing body reads the variable as the type
  it gave it.
- **Isolation is derived for a body and declared by a procedure.** A body is
  isolated when it writes no name it did not declare (a module variable, or a
  variable a closure captured), hands none of those in place, calls no value
  (`apply`), and calls only isolated declarations. The build starts every body
  isolated and strikes them until nothing more is struck, and judges every
  closure literal by the same rule. A closure value carries the purity and
  isolation the build derived, and a slot asking for either reads them wherever
  the value arrives, through `any` or an undeclared field included.
- **A native procedure says whether it is isolated, and is taken at its word for
  what it does itself.** The build reads what a body writes and calls; what a
  procedure keeps in the host language is outside the document, so the procedure
  declares it. A procedure that declares nothing is isolated, and one that holds
  state between calls declares otherwise, which strikes every body that reaches
  it. Purity does not answer this: a procedure can answer without running and
  still answer from a box two callers share. What the build does hold this claim
  to is what the procedure sends, under *a procedure the host answers* above.
- **A procedure that runs closures at once asks for isolated ones.**
  `std.concurrent.map` declares its closure `isolated procedure`, and `all` and
  `first` declare their pieces a membership of collections of them, so a
  closure that writes a captured variable **refuses at the build** in all three.
  A piece answers a value; combining is written after the join, where the names
  are sequential again.
- Leaving does not cross the boundary either: `return` inside a closure
  answers the closure, and `break`/`continue` aimed past one **refuse at the
  check**. The ground is the `attempt` distinction. A failure is what the
  *world* did, and the world was always concurrent; leaving is what the
  *program* says, and the program does not get to say two things at once.
- Because a closure is already isolated, running closures at once is a thing
  a **procedure** can be handed. `std.concurrent`, under the vocabulary, and so
  concurrency is a *grant*: a receiver that leaves the bundle out of the link
  has programs that cannot fan out at all. There is no construct to have for
  free.
- What this buys, exactly: **Warp itself writes no race.** Only isolated
  closures run beside each other, and an isolated closure has no writable name
  in common with anything, so no interleaving reaches a name two bodies hold. It
  is not "every answer is deterministic" One thing is timing's on purpose, and
  it is named: which piece `first` answers with. Everything else a join answers
  is the same under every interleaving. `all` waits for every piece, so a rescue
  around a fan-out that lost twice is handed every failure, keyed by the piece
  it came from, whichever finished first.
- **Effects are the world's, and the world is the receiver's.** Two pieces' host
  calls interleave in an order nothing states. Two pieces reaching one host-held
  thing, a file or a counter, is contention the *host's* procedure must defend.
  What the language guarantees is that a procedure holding such a thing declares
  it and the build refuses to run two of its callers at once. A procedure that
  holds state and declares itself isolated has broken its contract, and that is
  the one place the language takes a procedure at its word. A receiver that
  needs an ordered meeting point offers one as a host procedure, where it can
  defend it.

There are no lower-level primitives. No spawn, no locks. On purpose: a
program that arrives is a program nobody can debug a race in.

## The standard vocabulary

Seven bundles, each taken with what it depends on, so a receiver grants what
its programs have use for and no more. A bundle whose procedures are written in
Warp names the ones they call: `std.logic` and `std.collection` walk, so they
send `std.math.lessThan` and link only with `std.math` in the link. `std` is the
shared ground: it declares no procedures, only the constraints the other
bundles' signatures mention, and a bundle mentioning them (`std.math`,
`std.collection`) links only with `std` in the link:

| module | procedures |
|---|---|
| `std` |. Declares the memberships `Numeric` and `Comparable`, and the type `byte = int(0...255)` |
| `std.logic` | `equal` `notEqual` `not` `and` `or` `select` |
| `std.math` | `plus` `minus` `times` `dividedBy` `remainder` `min` `max` `absolute` `floored` `rounded` `lessThan` `greaterThan` |
| `std.text` | `text` `characters` `startsWith` `regex` `uppercased` `lowercased` `trimmed` `split` `joined` `replacing` `decoded` `encoded` |
| `std.collection` | `append` `count` `contains` `first` `last` `reversed` `appending` `prepending` `gathering` `dropFirst` `dropLast` `sorted` `map` `filter` `reduce` `keys` `values` `setting` |
| `std.control` | `abort`. Declared `returns: never` |
| `std.concurrent` | `all` `first` `map`. Run closures at once. Declares the membership `Pieces` |

### What an implementation must write

Not all of these. Most are written in Warp, from a small set that cannot be:
**builtin**. An implementation writes the builtin procedures in its own language
and takes the rest as a Warp module, the way any other module arrives.

| bundle | builtin |
|---|---|
| `std.logic` | `equal` |
| `std.math` | `plus` `minus` `times` `dividedBy` `remainder` `lessThan` `floored` `rounded` |
| `std.text` | `text` `joined` `characters` `uppercased` `lowercased` `encoded` `decoded` `trimmed` |
| `std.collection` | `count` `appending` `gathering` `keys` `setting` |
| `std.control` | `abort` |
| `std.concurrent` | `all` `first` |

Twenty-five, beside the memberships and the `byte` type `std` declares. What
makes one builtin is that the language cannot express it: arithmetic and
ordering are the machine's, case mapping and encoding carry Unicode's tables
with them, running at once is the host's scheduler, `appending` is the only way
an array grows, and `gathering` the only way an answer keeps the spelling its
receiver arrived in. Everything else is written from those.

A procedure being derivable is not a claim that it is unimportant, and a
document cannot tell the two apart: `greaterThan` is `lessThan` with its sides
swapped, and both are called the same way. An implementation that wants its own
`greaterThan` declares one under that name, and the link takes it, which is what
every name outside the builtin set is open to.

One of these is builtin only because something else is missing. `trimmed`
would be written in Warp if anything named the characters it removes; nothing
does, so a body written from `characters` would have to invent the list.

`regex` is the one procedure `std` declares that is in neither set. It cannot be
written in Warp and it is not required of an implementation: what a pattern
means differs between the engines a host would reach for, so a host brings this
one or leaves it out, the way it grants any bundle. A document reaching for it
is asking for something of its host rather than of the language.

**A bundle stands above what it sends to.** The bundles a link lays down have to
have an order to be compiled in, so a bundle whose procedures call another's
cannot be called back: `std.logic` and `std.text` walk, so they send
`std.collection.count`, and `std.collection` reaches neither of them. This is
what an implementation is choosing between when it writes a procedure in Warp
rather than in its own language, and it is why `contains`, which asks one
question of a string and another of an array, is written natively here.

**The signatures, exactly.** A second implementation writes these; it must not
have to guess them. The *receiver* column is the parameter a call fills by
writing a receiver in front (the `of` key in a `call`); everything else is
written by name under `arguments`. A parameter with a `default` may be left out.
A slot typed `pure procedure` takes only a procedure that answers without
running.

*std.logic*

| procedure | receiver | arguments | answers |
|---|---|---|---|
| `equal`, `notEqual` | `of: any = null` | `value: any = null` | `bool` |
| `not` | `of: bool` |. | `bool` |
| `and`, `or` | `of: array<pure procedure>` |. | `bool` |
| `select` | `of: bool` | `then`, `else`. Pure procedures taking nothing, each answering `some Answer` | `some Answer` |

`and` and `or` take procedures precisely so they need not run them all: the
sides are read in order and the procedure stops at the first side that settles
the answer. The first false, the first true. What follows the stop is never
evaluated. `select` takes them for the same reason and asks exactly one, so a
side that would refuse is never a refusal of the side that was chosen. `equal`
and `notEqual` answer by the value model's one sameness, and `not` turns a
`bool` around.

**`select` is how an operand chooses.** A `conditional` answers nothing and
takes no name, and an operand is read rather than run, so choosing among values
inside one is a procedure here rather than grammar. The two sides answer one
type, worked out from the call the way any type parameter is.

*std.math*

| procedure | receiver | arguments | answers |
|---|---|---|---|
| `plus`, `minus`, `times`, `remainder` | `of: some N` | `value: some N` | `some N`. Bounds `N: Numeric` |
| `min`, `max` | `of: some N` | `value: some N` | `some N`. Bounds `N: Comparable` |
| `dividedBy` | `of: some N` | `value: some N` | `double`. Bounds `N: Numeric` |
| `absolute` | `of: some N` |. | `some N`. Bounds `N: Numeric` |
| `floored`, `rounded` | `of: number` |. | `int` |
| `lessThan`, `greaterThan` | `of: some T` | `value: some T` | `bool`. Bounds `T: Comparable` |

`floored` goes to the nearest whole toward the smaller side, below zero too:
`-2.1` floors to `-3`. `rounded` goes to the nearest whole, and away from zero
at the exact halfway: `2.5` rounds to `3`, `-2.5` to `-3`. `absolute` drops
the sign and keeps the kind it was given. Each of these answers an `int` only
when an int holds the answer. The int's edge refuses at the run, as the
edge rules below require.

*std.text*

| procedure | receiver | arguments | answers |
|---|---|---|---|
| `text` | `of: any` |. | `string` |
| `startsWith`, `regex` | `of: string` | `value: string` | `bool` |
| `uppercased`, `lowercased`, `trimmed` | `of: string` |. | `string` |
| `characters` | `of: string` |. | `array<string>` |
| `split` | `of: string` | `value: string` | `array<string>` |
| `joined` | `of: array<string>` | `value: string = ""` | `string` |
| `decoded` | `of: bytes` | `encoding: string = "utf8"`, enum `["utf8"]` | `string`. **refuses at the run** when the bytes are not text in that encoding |
| `encoded` | `of: string` | `encoding: string = "utf8"`, enum `["utf8"]` | `bytes` |
| `replacing` | `of: string` | `value: string`, `with: string` | `string` |

`characters` answers the text as an array of its characters, each one a string
of its own, counted the way `count` counts. Answered for the whole text rather
than read one at a time: a character is an extended grapheme cluster, so where
the tenth one starts is only known by walking the nine in front of it, and a
body reading them in order would pay that walk every round.

`regex` answers whether the pattern matches *anywhere* in the text. A program
asking about the whole anchors the pattern itself (`^…$`). A pattern that does
not compile, written as a constant, refuses before the run the way any constant
argument does. `replacing` rewrites every occurrence, not only the first.
`split` keeps the empty pieces a separator at either end leaves, since dropping
them would be an opinion about the text rather than a reading of it. Both refuse
a separator holding no characters, which would match everywhere and consume
nothing; the refusal is `aborted`, so an attempt around either catches it. The
procedures that read text. `startsWith` included. Read as a person reads, under
the value model's canonical equivalence.

`text` spells a value the way a document writes it. Bytes included, as `x`
and their hex digits. What no document carries answers in the language's own
markers, never a host formatter's: a procedure is `<procedure>`, a host's
non-finite fraction is `<infinity>`, `<-infinity>` or `<not a number>`, and a
container holding one shows whole as `<unencodable>`.

A value's spelling does not change with how deep it sits: `text` of
`[x"6869"]` is `["x\"6869\""]`, the same spelling quoted the way a string in
that position is quoted. This is what `text` is for. A person reading a
value. A carrier that has to give the value *back* is a different question,
and one with no compact spelling writes what `bytes = array<byte>` says
instead: the array.

*std.collection*

| procedure | receiver | arguments | answers |
|---|---|---|---|
| `append` | `to: inout array<some Element>` | `value: some Element` | `null`, having written the element onto the end of the array the variable holds, in place |
| `count` | `of: any` |. | `int` |
| `contains` | `of: any` | `value: any` | `bool` |
| `first`, `last` | `of: array<some Element>` |. | `some Element` |
| `reversed`, `dropFirst`, `dropLast` | `of: array<some Element>` |. | `array<some Element>` |
| `sorted` | `of: array<some Element>` |. | `array<some Element>`. Bounds `Element: Comparable` |
| `appending`, `prepending` | `of: array<some Element>` | `value: some Element` | `array<some Element>` |
| `gathering` | `of: array<some Element>` | `value: array<int>`. Where to read, in the order to read it | `array<some Element>`, the receiver's own, in the receiver's spelling. A position the receiver does not hold refuses at the run |
| `map` | `of: array<some Element>` | `value`. Pure procedure, handed `item`, answering `some Answer` | `array<some Answer>` |
| `filter` | `of: array<some Element>` | `value`. Pure procedure, handed `item`, answering `bool` | `array<some Element>` |
| `reduce` | `of: array<some Element>` | `from: some Carried`; `value`. Pure procedure, handed `carried` and `item`, answering `some Carried` | `some Carried` |
| `keys` | `of: dictionary<any>` |. | `array<string>` |
| `values` | `of: dictionary<some Entry>` |. | `array<some Entry>` |
| `setting` | `of: dictionary<any>` | `key: string`, `value: any` | `dictionary<any>` |

`gathering` is how a procedure answers its receiver's own elements. It says which
by position, and the answer comes back in the spelling the receiver arrived in:
bytes rearranged are bytes. This is the whole of what `reversed`, `dropFirst`,
`dropLast`, `filter` and `sorted` add to a walk, and it is the reason those are
written in Warp rather than asked of an implementation. A body that read the
elements out and put them back would answer an array of numbers, because an
array it started empty has no spelling to keep. The standard name for reading
one collection at another's positions is a **gather**.

*std.control*

| procedure | receiver | arguments | answers |
|---|---|---|---|
| `abort` | `of: any`. What the refusal says |. | `never` |

*std.concurrent*

| procedure | receiver | arguments | answers |
|---|---|---|---|
| `all`, `first` | `of: Pieces`. The membership of `array<isolated procedure>` and `dictionary<isolated procedure>` |. | `any` |
| `map` | `over: array<some Element>` | `by`. `isolated procedure`, handed `item` and `index`, answering `some Answer` | `array<some Answer>` |

**`std.concurrent`**. Running closures at once. `all` takes a record or an array
of closures, runs every one, and answers every answer. A record's under its
keys, an array's in its order; a failure fails the whole procedure with every
piece's failure reported, keyed by the piece it came from. `first` takes the
same and answers the first success, asking the rest to stop, which piece wins is
the one timing fact this language admits. `map` takes a collection and one
closure, calls it once per element. Each call handed `item` and `index`, and
the closure's own signature says which it reads, and answers in the collection's
order. These are procedures rather than grammar because a closure is already the
safe unit of concurrent work, and being procedures makes concurrency a
permission: what a receiver does not link, a program cannot do.

The names are plain ones with the module carrying the context, the way
`Array.map` and `TaskGroup.next` lean on their types. A call site spells the
module, so `std.collection.first` and `std.concurrent.first` are two names, and
a link carrying both bundles holds both: every `first` and every `map`, the
sequential ones included, is written with its bundle, and concurrency shows at
the call site.

What the checking sees: `map` declares its types the way the sequential one
does. The collection's `Element` meets the closure's parameter, and the
answer's type is the closure's answer, checked at the build. Its `by` is an
`isolated procedure<(item: some Element, index: int) -> some Answer>`, so a
closure that writes a captured variable refuses there before anything runs.
`all` and `first` take `std.concurrent.Pieces`, the membership of
`array<isolated procedure>` and `dictionary<isolated procedure>`, so a piece
that is not a closure and a piece that writes what it captured both refuse at
the build. They answer `any`: the answer is shaped like what went in, and a
membership names a set of types rather than tying one of them to another. What
a fan-out's answer feeds is checked from `map`, not from these two.

What the procedures hand their closures is one convention, shared with the
sequential walks. `std.collection.map` hands over `item`, `reduce` hands over
`carried` and `item`, `std.concurrent.map` hands over `item` and `index`, and a
closure written for one of them **declares every name it is handed**, whether or
not its body goes on to read one. A name the closure does not declare refuses,
the same as anywhere else a call is settled: a walk is not a second calling
convention. `first` run over nothing is refused. A procedure that answers exactly one thing has no
empty answer, and a `first` in which nothing succeeds fails the way `all`
fails: every piece's failure reported, keyed by the piece it came from.

What the vocabulary answers about **bytes**: `bytes = array<byte>`. Bytes are
not a special material. They are the compact spelling of an array of small whole
numbers, `byte` being the range `int(0...255)` that `std` declares. The equation
is read everywhere the types are, and **the spelling is the value's own fact
rather than the slot's**: a bytes value stands where `array<int>` is declared
and crosses it *whole*, because the slot asked for an array and bytes are one.
There is nothing to settle, and unpacking would spend an element per byte to
answer questions like `first` that read one. An `array<…>` slot reads the bytes
out one by one only where its element declaration would not leave a byte as it
is: `array<double>` changes every one of them, a range narrower than `byte` has
something to ask of each, and a fraction range (`double(0.0...255.0)`) is both.
It widens every byte it takes. An element declared as a **bounded** type
parameter asks each value for its membership, and a member of the constraint
that takes every byte answers that for all of them at once, so `sorted`, whose
element carries `Comparable`, reads a compact spelling the way `reversed` does
rather than by whether its declaration happened to carry a bound. An array of
byte worths standing where `bytes` is declared does settle to the compact
spelling. The asymmetry is the declaration's: naming `bytes` names a spelling,
naming `array<…>` names a type bytes already have.

An index reads an element out as the ordinary int it is, and the collection
vocabulary. `count`, `first`, `contains`, `reversed`, `map`, all of it. Applies
directly. A procedure that answers its receiver's **own** elements. `reversed`,
`filter`, `sorted`, `dropFirst`, `dropLast`. Answers them in the spelling they
arrived in, so bytes stay bytes; put something among them that is not a byte
(`appending` a `300`) and the answer is the array it now is. A procedure that
builds **new** elements does not: `map` answers whatever its procedure answered,
which its declaration says by naming a second type parameter for it. Two bytes
*values* still do **not** order, for the array reason rather than an opacity
one: `Comparable` admits numbers and strings among themselves, not collections.
Reading bytes *as* text is a procedure that names its encoding: `decoded` and
`encoded` are the two directions of one mapping (`encoding: "utf8"`, the default
and today the only member), and bytes that are not text in that encoding
**refuse at the run**. Completing a broken sequence would answer a text nobody
sent.

**`abort`**. Fail on purpose, with a message. Declared `returns: never`, which
is everything the checking needs: nothing runs after it, and no name binds it.
The refusal it raises is a failure like any other, so an `attempt` around it
catches it. Leaving is what a rescue does not catch, and this is failing, not
leaving.

Behaviour at the edges. Where implementations quietly differ, so stated as
requirements:

- Arithmetic takes two of a kind and answers that kind: both sides and the
  answer are one type parameter, bounded by `Numeric`. A whole number added to
  text **refuses at the build**, and so do two pieces of text, because
  agreement is not admission.
- Ordering (`lessThan`, `greaterThan`, `sorted`, `min`, `max`) compares two of a
  kind under `Comparable`, and text is a kind. A kind the constraint does not
  admit refuses at the build where the text says so, and at the boundary where
  the value arrives through `any`.
- Whole-number arithmetic with no whole answer **refuses at the run**. It does
  not wrap and does not silently widen. The rule covers every standard
  procedure that answers an `int` and can miss it: `plus`, `minus`, `times` off
  the int's edge, `absolute` of the int's own minimum, and `floored`/`rounded`
  of a fraction whose whole part is past the int. `remainder` is not on the
  list because its answer always fits. A remainder is smaller than its
  divisor, and the one divisor that trips a machine's division instruction
  still has one: `-9223372036854775808 remainder -1` answers `0`. These
  run-stage refusals. Overflow, and the zero divisor below. Are the
  program's own defect, not a failure of the work: an `attempt` does **not**
  catch them, the way it does not catch an index past the end. What a rescue
  catches is `abort` and a procedure's own failure.
- Fraction arithmetic with no finite answer **refuses at the run** for the
  same reason: infinity is a value the arithmetic can reach and no document
  can carry, and a value that exists only until someone writes it down is not
  an answer.
- `dividedBy` answers a fraction, whole or not. Division by zero **refuses at
  the run**. The quotient is binary64's own: a whole operand reads as the
  fraction nearest it first. The same widening every mixed operation
  performs, and the division rounds once more, so two implementations spell
  the same quotient bit for bit.
- A whole number where a fraction is expected widens; the reverse refuses.

What a host brings beyond these. Its own procedures, and which of them answer
without running. Is the host's, and is the boundary to the outside world:
a program reaches nothing except by sending a procedure the receiver declared.

## Encodings

An encoding is bytes for the document tree. Whatever the encoding, three
promises hold:

1. **A whole number and a fraction are told apart.** However the encoding does
   it, `1` and `1.0` must arrive as the values they were. They are one value
   to a program and two byte strings here, so two documents a program cannot
   tell apart may carry two signatures, and that is the intended order: the
   encoding is faithful to what was written, and sameness of worth is the
   value model's, not the bytes'.
2. **The same document is the same bytes, in binary.** Writers are canonical:
record keys are written in one order. **ascending by their UTF-8 bytes**. and
every value has one spelling. This is what makes a document cacheable,
comparable and signable, and the binary reader holds the same line:
non-canonical bytes **refuse**, they are not normalised. Were that reader
forgiving, one document would have many byte spellings again, and what a
signature was checked against could differ from what the reader went on to read.
The text reader is the one that is forgiving, under Warp text below: text is for
people, and the binary is the document.
3. **Nothing but data.** A procedure value has already run far enough to close
   over a scope; no encoding writes one, and refusing every such value rather
   than only the ones that captured nothing is the decision. It costs an
   author nothing and saves every reader a rule about which captures are empty.
   Infinity and NaN are likewise refused on the way out and on the way in.

Every reader also refuses: bytes after the document ends, bytes that end inside
a value, and nesting deeper than **512** containers. The depth is an exact
bound, not a floor. A document 513 deep is not a document anywhere, so a
writer may rely on the refusal. The bound guards whoever walks the tree after
the reader: readers here are obliged to iterate, but everything downstream of
one. Checkers, comparers, hosts. Recurses over values in the ordinary way,
and their stacks must not be the sender's to spend.

**Record keys are NFC.** Unicode writes some characters more than one way. A
letter, or the same letter as letter-plus-combining-mark, and a name that had
several byte spellings would break promise 2 quietly: two fields one name, or
one name sorted to two places. So a key must be in Unicode Normalization Form
C, and a key that is not **refuses**. A key with nothing in it **refuses** for
the same reason a name does: a field is called something. One name, one byte
spelling; the ascending-bytes order is then an order on *names*. ASCII is NFC
already, so a document that never leaves ASCII never meets this rule. String
*values* are data, not names: they travel byte-for-byte as written and are
never normalised.

**A document is read whole.** Streaming and incremental decoding are
deliberately not offered: a program is checked whole before any of it runs, so
nothing downstream could act on a prefix anyway. This buys the budget rule:
lengths claimed inside a document are charged against **one budget. The byte
count of the document itself**. At the cheapest cost a claimed thing could
possibly occupy on the wire, and a claim the budget cannot cover **refuses**
before anything is set aside for it. Nested containers cannot each claim the
whole document, and no document can make a reader hold more than a small
multiple of its own size.

**Compact was the goal that lost.** In a small document most bytes are field
names, and the format leaves them there: a key table would give one document an
inline spelling and a referenced spelling. Promise 2 gone, and schemas are a
meaning the encodings must not learn. Of canonical, self-contained and
compact, the encodings choose the first two; repeated names compress well, and
compression is the transport's job.

An encoding's header carries the *encoding's* format version, distinct from the
document's `warp` key: the one says how the bytes are laid out, the other says
what the program means. A reader refuses bytes laid out by a later format than
it implements, and a format number that never existed.

### Warp binary. `.warp`

The carrying form: what a document travels as. Current format: **1**.

```
"W" "A" "R" "P"  0x01        magic, then the format version
<value>                       exactly one, then end of input
```

Each value is a tag byte, then its payload:

| tag | value | payload |
|---|---|---|
| `0x00` | null |. |
| `0x01` | false |. |
| `0x02` | true |. |
| `0x03` | int | ZigZag, then unsigned LEB128 |
| `0x04` | double | 8 bytes, IEEE-754 binary64, big-endian |
| `0x05` | string | length varint, then that many bytes of UTF-8 |
| `0x06` | array | count varint, then that many values |
| `0x07` | record | count varint, then that many of: key (length varint + UTF-8), value |
| `0x08` | bytes | length varint, then that many raw bytes |
| `0x09` | named record | name (length varint + UTF-8), then count and fields exactly as `0x07` writes them |

- **Varint** is unsigned LEB128: seven bits a byte, low bits first, high bit
says another byte follows. At most 64 bits of payload. The largest zigzagged
value takes exactly ten bytes, the tenth carrying bit 63 alone. so an eleventh
byte, or a tenth-byte bit that would carry past bit 63, **refuses**; overflow is
not wrapped, masked or truncated. A trailing zero group (`0x80 0x00` for zero)
is a longer spelling of the same number and **refuses**. One value, one
spelling.
- **ZigZag** maps signed to unsigned: `(n << 1) ^ (n >> 63)`.
- Record keys are **strictly ascending** by UTF-8 bytes, which refuses a
  shuffle and a duplicate with the same rule: these are bytes the writer would
  not write.
- A claimed length larger than the bytes that remain **refuses** before
  anything is set aside for it.
- Invalid UTF-8 in a string **refuses**.
- A record with no name is `0x07`; only a record carrying a name is `0x09`.

The golden case (also held as a test in each implementation):

```
{ "a": 1, "b": [true, null], "c": "hi", "d": 1.5, "e": x"6a73" }

57 41 52 50 01                    WARP, format 1
07 05                             a record of five
01 61 03 02                       "a": int 1        (zigzag 2)
01 62 06 02 02 00                 "b": [true, null]
01 63 05 02 68 69                 "c": "hi"
01 64 04 3F F8 00 00 00 00 00 00  "d": 1.5
01 65 08 02 6A 73                 "e": two bytes
```

### Warp text. `.warpt`

The readable form: the same document laid out for eyes. **A dump, not a
syntax**. Machines write it, people read it, and nobody composes one by hand;
composing is a front end's job, in a front end's notation. Nothing can be said
here that the document does not hold, which is why there are no comments to
lose on the way back. Current format: **1**.

```
warpt 1
{
  a 1
  b [
    true
    null
  ]
  c "hi"
  d 1.5
  e x"6a73"
}
```

The layout:

- The first line is `warpt`, a space, the format version, a newline.
- A record is `{ key value … }`; an array is `[ value … ]`. No commas, no
  colons. Containers with anything in them take two-space indentation, one
  element or field per line; empty containers are inline as `[]` / `{}`. The
  text ends with one newline.
- A key is written bare when it is an identifier (`[A-Za-z_][A-Za-z0-9_]*`),
  quoted otherwise. In key position a bare token is always a key. `{ null 1 }`
  is a field called null.
- `null`, `true` and `false` are bare keywords. **A number with a point or an
exponent is a fraction; with neither it is whole**. The difference is grammar,
not a reader's guess. A double is spelled as the shortest decimal that reads
back to the same binary64 (a Ryū/Grisu-class rendering), with the point or
exponent always present. Which form those digits take is the document's rule,
not a host library's: writing the value `d.ddd…×10^k`, the point form when `-5 <
k < 16`, otherwise the exponent form, its exponent written `e` with an explicit
sign and at least two digits. `0.0001` but `1e-05`, `1000000000000000.0` but
`1e+16`, so one value keeps one spelling down to its last character. An int is
spelled with no leading zeros and a `-` only when negative.
- A string is double-quoted. Exactly `"` `\` and the five characters with
  short escapes are escaped as `\"` `\\` `\n` `\r` `\t`; every other control
  character (below U+0020) as `\uXXXX` with lowercase hex; **nothing else is
  escaped**, and no character that has a shorter escape may take a longer one.
- Bytes are `x"…"`. Lowercase hex, two digits a byte, no spaces.
- A named record is the name, a space, and the record: `bank.Account {
  balance 1 }`. In value position a bare token followed by `{` is the name; a
  bare token that spells a scalar (`null`, `true`, `false`, a number) is never
  one.

Layout is free on the way in. A reader takes keys in any order, any
whitespace between tokens and any indentation, because a text is written by a
person as often as by a writer. The writer still lays a text out one way,
keys ascending and two spaces an indent, so a text that has been through a
writer is the same bytes everywhere, and that is the form the conformance
cases are kept in. What is not free is the spelling of a value: a fraction
written `1.50` and an escape spelled long **refuse**, since those are two
texts for one value rather than two layouts of one text. Sameness of
documents is the binary's promise, above, and a text makes it by being
written out.

## Conformance

The rules above, as cases that run: `conformance/`. Prose ages against an
implementation that keeps moving, and an implementation is the last thing that
should be asked whether it is correct. These are the questions asked instead.
Data rather than code, so an implementation written in another language runs the
same cases and finds out the same things.

### What a case is

One file, one question: a document, what to run it with, and what should happen.

    test        int. The case format this file is written for
    name        what the case is called
    note        why it exists. The rule it holds an implementation to
    program     a document
    arguments   what the entry procedure is given, if anything; a record
                under a name is written as the text encoding writes one
    vocabulary  the procedures the runner brings, if any
    expect      answers <value>   it runs and answers this, named records
                                  written the same way
                refuses <stage>   it is refused, at load, build or run

A case is **not a document**, and this is the record where that is said out
loud. It is written in the same text. An encoding carries a tree of data and
never learns what a tree means, so there is one of those and not two, but the
document it asks about is nested whole under `program`, and what surrounds it
belongs to the asking.

Each format declares itself, and that is how the two are told apart: a case
says `test`, a document says `warp`, and each is refused by the other's reader
for **what it is** rather than for the keys it happens to carry. The `test`
number moves for the same reason `warp` does and on its own schedule. The day
a case may say something new is not the day a document may.

`expect` holds one of `answers` or `refuses`. One slot, so "one of the two and
exactly one" is the record rather than a rule about two keys that could both be
written or neither.

**`vocabulary` is what the runner brings.** Most of what a document may say
about a procedure the host answers is not something a case can write down: the
code is the host's. So a case writes the part that is in the document, and the
runner builds the rest.

It is written as a **module**, because that is what a receiver takes in: it may
declare `types`, `constraints`, `contracts` and `satisfies` the way any document
does, and it declares the procedures under `procedures`. It does not say `warp`
or `imports`: which version this module is read at is the runner's, and its
declarations send nothing. A case writing either **refuses** as a case. The
module stands in front of the case's own document in the link, so what the host
brings is there to be named. Each procedure is keyed by its name and written the way a
declaration is, with four keys of its own beside it:

    answers     what it answers, whatever it was sent. Default null
    runs        bool. Whether it reaches outside the run. Default false,
                which is a procedure that answers without running
    isolated    bool. Default true
    failing     array of strings. What it may fail with. Default empty

It answers the same thing every time, because a case asks what a declaration
permits rather than what arithmetic does. The names it may declare are `of` and
`value`, in that order, since a procedure the host answers reads its arguments
at fixed places and a case cannot invent a place in another runner.

This is the only way a case reaches the three things answering without running
permits, all of which need a procedure with no body: a constant settling, a
slot asking `pure procedure`, and an operand calling one.

The cases here are `test 2` where they say nothing new and `test 3` where they
ask for a vocabulary: `test 1` spelled the middle stage `link`, and a runner
that reads `build` cannot honour a case that says the other one.

Both kinds matter equally. **An implementation that accepts a program another
refuses has failed in the same way as one that answers differently**, so half of
these say what must *not* run, and where it must stop. The stage is part of the
answer: refusing at run what another implementation refuses at build means
something already happened before the refusal, and what already happened
cannot be taken back, which is most of why this language checks before it runs.

### What a runner does

Read the file, and read `test` before the record, for the reason a document
reads its own version first: a later case may say something this runner has no
name for, and "I am too old for this" is a different answer from "this is not a
case". Then read `program` as a document. Read each entry of `vocabulary` the
same way a declaration is read, and build the host's side of it from the four
keys beside it. If the case expects `refuses`, check that it fails at that stage
and no earlier or later. Otherwise build it against that vocabulary and the
standard bundles, start from the procedure declared under `entry`, run it with
`arguments`, and compare.

The cases are the files named `<name>.test.warpt`, and what else the folder
holds is not the suite's business. A runner that refused to start over an
editor's leftover would be answering "is this folder tidy" with the same red
light as "is this implementation the language", and only the second is a
question about a language.

A runner reaches inside nothing and imports what any caller imports. One that
could see inside its implementation could pass by agreeing with the
implementation rather than with the specification, which is the one thing it
must not do.

### How a case is written

A case may be written by hand, since the text reader takes any layout, or
authored as any document is (a front end, a literal in a host language). Either
way it is run through the writer before it lands in `conformance/`, so every
case sits in the writer's layout and a diff shows what changed rather than who
indented it. An implementation adding cases writes its own dumper anyway. It
is the same writer conformance already requires of it.

So the suite is the first thing a new implementation reads with its own reader,
and the reader is proven before it by the golden cases above. One whose reader
disagrees with the golden bytes cannot trust anything the rest of the suite
tells it.

The extension is `.test.warpt` and not `.warpt`, and both halves are true at
once: the file *is* warpt text, which is why the text reader reads it, and what
it holds is a test rather than a document, which is why nothing that runs
programs will take it. Naming the format outright. A single extension of its
own. Would make a file that is spelled in warpt look like it is not, and every
tool that highlights or formats warpt would have to be told about it twice.

## Known gaps

Written down because a specification that hides what it has not decided is
worse than one that admits it. Each is a place a second implementation would
have to guess, and would be entitled to guess differently.

- **`imports` does not announce type or constraint dependencies.** The list
  gathers what a program *sends*; a document leaning on a constraint another
  module declares. `bounds: { T: Comparable }` with no declaration of its
  own. States that dependency nowhere a caller can read before linking.
  Whether `imports` should widen to carry unresolved type and constraint
  mentions is undecided; until it is, that dependency surfaces only as a build
  refusal.
- **`regex` names no dialect.** The table says the pattern is a string and says
  nothing about what it means, so two hosts reaching for their own engines
  answer the same document differently. That is why it is required of no
  implementation, but naming a dialect would be a better answer than leaving it
  out.
- **`trimmed` does not say what it removes.** The table says it trims and says
  nothing about which characters are whitespace, so two hosts reading their own
  platform's answer trim differently. Naming a set (Unicode's `White_Space` is
  the one to name) would settle that and make the procedure writable in Warp
  from `characters`.
- **The text decision is cheap in Swift and dear elsewhere.** Grapheme-cluster
  counting and canonical equivalence are the platform's gift in Swift and a
  library obligation in most other languages; the decision stands, and the
  cost lands on implementations unevenly.
- **The document grammar above was written from the readers.** Field tables
  transcribed from one implementation carry its blind spots; the first reader
  who implements from these tables alone, and disagrees, is worth more than
  any amount of agreement.
- **The suite covers the constructs and the vocabulary; cancellation is the
  exception.** Every construct, the naming and leaving rules, the envelope, the
  boundary settlements, the concurrency grant and every standard procedure are
  held as cases, but cancellation cannot be a data case at all: it needs a
  caller with a lever, so stopping is held only by tests inside the Swift
  implementation.
- **Two equivalences coexist, and the border is drawn.** Values compare as a
  person reads. `equal`, `contains`, ordering and `count` all read text
  under canonical equivalence, stated under the value model. Where names are
  matched as bytes, held to NFC at the check, so a document cannot declare
  `é` one way and reference it the other. What remains here is only the cost:
  an implementation whose platform compares by code unit owes a library the
  difference.
- **Encodings beyond utf8.** `decoded`/`encoded` name their encoding and
  today name one. Which others join the `enum`, and whether a host may
  extend it. Is undecided; the type of the procedures is not.
- **Where a refusal points is not specified.** A case says the stage a
  document is refused at and nothing about the sentence, so two
  implementations agreeing on every case may still name the place
  differently, or name none. What an author is owed is the whole of the
  question: a refusal that does not say where sends them searching a
  document they did not write by hand. Whether the answer belongs here. A
  path spelled from the document's own keys, so that following it step by
  step lands on what was typed, or stays each implementation's to give, is
  undecided. What is decided is that a place is a fact about the **document**
  and never about the file it was authored in: a front end holds the file,
  and the document is what crossed the wire.
- **How a document is told from another document is decided; where the answer
  belongs is not.** Nothing a document says about itself can do it: what a
  document writes is declarations, and two documents may declare spellings
  under one prefix (a program split across files). A file path cannot do it
  either, since a
  document arrives as bytes and the wire carries no container. What is always
  there is the document itself, so a document is identified by the **digest of
  its canonical binary writing**, and by nothing it says about itself. It is
  derived and never declared: there is no field for it, which is what makes it
  impossible to write down wrongly, and two readers holding one document arrive
  at one answer without having agreed on anything but this paragraph. The
  digest is SHA-256 of the bytes the canonical binary writer produces. The
  same bytes a conforming reader already has to accept exactly, so an
  implementation that has the wire right has this right. What is undecided is
  whether identity belongs in this specification at all or stays a fact each
  implementation works out for itself, since nothing a program *runs* depends
  on it.
