# What an implementation checks, and when

Which stage answers which refusal. This page is a list rather than a rule,
and the list is the contract: two implementations can agree on every answer a
program gives and still not be the same language, if one of them refuses a
program the other runs or refuses it later.

A program is read, checked and built before any of it runs. Including the
arms nobody takes. All of the following are answered while nothing has
happened yet. The first, the leaves (`break`/`continue` having a loop, nothing
following one), the names in normal form C and a procedure's `access` being one
of its three words are answered at `load`, since a document answers them alone; the rest at `build`, since each is judged against
a signature or another document. What the grammar pages refuse as shape, a
type spelled wrong, a rescue answering nothing, a leave with nothing to leave,
is `load` too, and those pages say so where the shape is written. The stage is
the rule's: a call that misfits a declaration in its own document refuses at
`build` all the same.

- every `ref` resolves to a parameter, a constant, a module variable, a
  statement written before it, a binding the construct holding it opened (a
  loop's round, an iteration's element, an attempt's failure), or a path
  through them;
- every procedure sent is declared by some module in the link, exactly once;
- a claim backed by a declaration that does less than the contract asked,
  running where it asked `const` or touching a shared name where it asked
  `isolated`, does not hold, under *what answers without running* in
  [procedures](procedure.md);
- every procedure sent from another document is not `private`, and a claim
  backed by a `private` declaration does not hold, under *who may name a
  declaration* in [procedures](procedure.md); a `private` declaration takes
  no spelling, so the rule above it counts none;
- every call fits the declaration it reaches: arguments by name, receiver,
  and answer, with type parameters bound as [types](type.md) says and every
  bound judged against its constraint's membership;
- every declared type names a type that exists;
- a condition answers a `bool`. A `conditional`'s `when` and a `loop`'s
  `while`, held where they are written, and `any` passing the way it
  passes any other slot;
- every candidate a parameter's `enum` lists is written in a value's one
  spelling, the one the declared type's own values wear. A dead candidate
  no call could ever match refuses, the empty and the all-dead list being
  the plainest cases. A range's bounds admit something, and a `default` is
  a value the parameter itself admits. `type`, range and `enum` together;
- a slot declared `const` takes only a procedure that answers without running,
  under *what answers without running* in [procedures](procedure.md); a slot
  declared `isolated` takes
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
  parameter naming such a type says `consuming` or `borrowing`, a parameter
  naming no such type says neither, and what a body borrowed it does not give
  away;
- every `set` writes a path headed by a variable, through fields declared
  `var` where the type is a declared type, and what it writes fits what the
  path reaches; a write into a module variable or an `inout` parameter fits
  what the box holds;
- every `inout` parameter is handed a variable's path a write may take; two
  parameters handed paths under one head hold one box two ways, under
  [procedures](procedure.md), and nothing keeps them apart;
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
- a statement that never finishes. A syntactic leave, or a call whose answer
  reads `never`, declared under `returns` or read off a body that never
  finishes. Takes no name, and nothing follows it;
- every name the program writes as a value. A statement's, a binding's (a
  loop's round, an iteration's element, an attempt's failure), a parameter's,
  each segment of a `ref`. Is **written**, and is **normal form C**, compared
  as bytes. Record *keys* hold this line at the encodings; these are the names
  that live in string values, and this is where they hold it. One name has one
  byte spelling, so a declaration and a reference can only meet by being the
  same bytes. `é` written two ways is a refusal, not two names. Nothing
  written is no name: a declaration is called something, and a reference
  writes something, and neither is done by writing nothing.

The `imports` list is deliberately not on this list. It is held at `load`,
as [README](README.md) says, because a caller decides from it before any of
this runs.

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

**What a refusal names.** A refusal at `load` or `build` about one spot in a
document names that spot: the document's identity and the steps from its root
to the field, which is a place as [objects](object.md) lay one out, and never
the file the document was authored in. A refusal that is a fact about the
whole link and no spot in it names no place, since it has none. The sentence beside the place is the implementation's: a case
says the stage and reads nothing else.

## Cases

What `conformance/` asks about this page, by the name each case's file carries.

- `a-declaration-is-named-by-its-whole-spelling`
- `a-name-not-in-normal-form-c-is-refused`
- `a-procedure-may-be-spelled-like-a-type`
- `a-procedure-nobody-declares-refuses-at-build`
- `a-procedure-two-modules-declare-refuses`
- `an-untaken-arm-is-checked-too`
