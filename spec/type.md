# Types

What a name may stand for, and what a slot takes. A type is judged at the
build against the declarations the grammar read; what a type *admits* is asked
of a value at a boundary, which is sometimes the build and sometimes the run.
Reads [the value model](value.md). Read by procedures, statements and
expressions, each of which writes a slot.

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
| `const <procedure type>` | a procedure that answers without running, under *what answers without running* |
| `isolated <procedure type>` | a procedure that touches no name another body could touch at once; `const isolated procedure` says both, and the reader takes the two in either order |
| `inout <type>` | a parameter handed a variable in place; written on a parameter's type and nowhere else |
| `{ linear: <type> }` | a type whose values are handed on exactly once; written on a type in `types` and nowhere else, and every slot naming that type carries it |
| `consuming <type>` / `borrowing <type>` | what a parameter does with a value handed on once: takes the obligation, or reads and leaves it. Written on a parameter's type and nowhere else |
| `var <type>` | a field a path may write through; written on a field of a type declared in `types` and nowhere else |
| `Task` (any declared name) | the type a module declares under that name, or a value of the membership it declares under that name |
| `some T` | a type parameter: worked out from the call, same reading everywhere it appears; bounded when the signature's `bounds` names it |
| `Describable` (a declared contract's name) | a value of whatever type satisfies the contract. Nothing ties one slot's to another's |
| `Describable & Comparable` | a value of whatever type satisfies every contract and belongs to every membership named; the names in either order, and each a contract's or a membership's |
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
slot asking `isolated` takes what the build derived as isolated. Answering
without running is a separate claim and does not stand in for it.

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
name takes only what the constraint admits. A bound may name several, joined
with `&`: `bounds: { T: Comparable & Describable }` holds `T` to what every one
of them admits or asks. The signature owns the bound. A slot names the
parameter and never the membership, so one bound is one claim however many
slots mention the name, and there is no inline union for the membership to leak
out through. A constraint is a **declared membership**. A module binds a
name to the types it admits, the way it declares a type. A slot may also declare
one as its type, and what stands there is a value of one of the members, which
is how the language says **A or B**: the set is declared once under a name, and
no slot writes an inline union. The judgment is made twice, once per surface: at
the **build**, a reading provably outside the membership refuses. Two booleans
meeting `lessThan` never run, and a reading the text says nothing about (`any`)
passes; at the **boundary**, the value that actually arrived is judged against
the membership, so what travelled in through `any` is refused where it arrives.
`bounds` naming a parameter no slot mentions refuses at the read. Only the declaring procedure writes `bounds`. A
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

A contract's name stands where a type is written, and so does `A & B`: the
slot takes a value of whatever type satisfies every contract and belongs to
every membership named. It is a type parameter with no name, so nothing ties
one slot's reading to another's, and a call fills nothing. A name declared as
neither a membership nor a contract joined with `&` **refuses at the build**.

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

## Cases

What `conformance/` asks about this page, by the name each case's file carries.

- `a-bare-constraint-name-refuses-at-the-build`
- `a-bound-may-name-several-and-holds-to-every-one`
- `a-contract-stands-where-a-type-is-written`
- `a-value-outside-a-contract-standing-as-a-type-refuses-at-the-build`
- `a-name-that-is-not-a-bound-joined-with-and-refuses-at-the-build`
- `a-body-cannot-answer-what-it-borrowed`
- `a-borrowing-slot-reads-and-leaves-the-obligation`
- `a-byte-is-a-whole-number-a-range-refines`
- `a-constant-outside-a-range-refuses-at-the-build`
- `a-constraint-is-named-by-its-qualified-spelling`
- `a-contract-carries-a-procedure-into-a-generic-body`
- `a-declared-name-is-a-type`
- `a-declared-range-refuses-what-is-outside-it`
- `a-fraction-is-not-a-whole-number`
- `a-fraction-range-widens-a-whole-number-into-itself`
- `a-handle-already-given-away-is-not-read-again`
- `a-membership-stands-as-a-type`
- `a-named-record-arrives-as-an-argument`
- `a-procedure-answering-its-receivers-own-elements-keeps-the-spelling`
- `a-range-judges-a-runtime-value-at-the-boundary`
- `a-range-that-admits-nothing-refuses-at-the-build`
- `a-range-whose-bounds-meet-on-an-excluded-edge-admits-nothing`
- `a-range-written-with-the-other-kinds-bounds-refuses`
- `a-reading-outside-a-constraint-refuses-at-the-build`
- `a-record-settles-to-the-fields-declared`
- `a-record-takes-the-name-of-the-slot-it-settles-into`
- `a-record-under-another-name-refuses-at-the-build`
- `a-record-under-another-name-refuses-at-the-run`
- `a-slot-naming-a-type-handed-on-once-says-what-it-does`
- `a-type-parameter-read-two-ways-is-refused`
- `a-type-that-misses-a-procedure-does-not-answer-the-contract`
- `a-value-handed-on-once-does-not-go-into-a-list`
- `a-value-handed-on-once-does-not-go-into-a-list-unbound`
- `a-value-handed-on-once-is-ended-by-a-host-procedure`
- `a-value-handed-on-once-is-handed-on`
- `a-value-handed-on-once-that-is-dropped-refuses`
- `a-value-outside-a-declared-type-refuses-at-the-boundary`
- `a-whole-and-a-fraction-meet-exactly`
- `a-whole-fraction-stays-a-fraction`
- `a-whole-number-is-a-fraction`
- `an-answer-read-through-any-is-settled-at-the-run`
- `an-array-slot-that-changes-a-byte-reads-them-out`
- `an-inline-record-slot-takes-a-named-record`
- `an-undeclared-field-refuses-at-the-build`
- `bytes-cross-an-array-slot-in-their-own-spelling`
- `elements-of-different-kinds-join-to-any`
- `the-far-bound-of-a-range-may-be-left-outside`
- `what-a-membership-does-not-admit-refuses`
- `what-was-read-out-of-a-parameter-is-not-the-parameter`
