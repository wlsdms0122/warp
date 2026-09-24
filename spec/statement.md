# Statements

What a body is made of. A statement binds a name to an expression, and a
**construct** is the only thing that runs a body. Everything a program does in
a particular order is decided here; what it does it *with* is
[the standard vocabulary](vocabulary.md).

## A statement

A record carrying **at most one** naming key and its expression under
**`value`**: `{ let "x" value { call {…} } }`, `{ value { loop {…} } }`. A
construct sits inside `value` under its own key, and that is the one place a
construct key is read. Anywhere else, in an argument, an element of
an array or a record, a construct's key is a field name like any other, and the
record carrying it is data.

The naming key says what the statement does to its name:

| key | means |
|---|---|
| `let` | fixes the name. Written once, never again |
| `var` | introduces a name that may be written again |
| `set` | writes a path headed by a variable: one a `var` declared earlier, a module variable, or an `inout` parameter. `set "p.x"` and `set "people[0].name"` write into what the head holds |

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
  round), `attempt` (its failure). Written nameless, they bind nothing: a
  loop with no name has no round to read and an attempt with no name has no
  failure to read, and each runs the same otherwise.
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
it holds, under *what a variable reads as* in [checking](checking.md); a write to a module variable
or to an `inout` parameter has to fit the type the box holds and retypes
nothing. At the run the value is computed first, and then the box is rewritten
once, so nothing observes the box halfway. An index written as a name (`xs[i]`)
is read where the write stands and must be an int; the write lands on that one
position.

**A `var` may stand alone.** A statement that is only `{ var "name" }`, with no
`value`, introduces the name with nothing in it yet, and a name holding nothing
holds null. It is the declaration a conditional's arms write into; what the name
reads as afterwards is under *what a variable reads as* in [checking](checking.md). The other two
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
[expressions](expression.md).

## The constructs

**`call`**. A procedure called, by its spelling or as a value:

| key | takes | required |
|---|---|---|
| `procedure` | a string names the declaration called, resolved at the build. Any other expression is a value the run calls, and a value no procedure could be **refuses at the build**, and so does one whose reading says it may be null: null is not called through, the way it is not read through, at the build where the text shows it and at the run otherwise. Text is never a value a call could take, so the two readings never meet | yes |
| `arguments` | list of expressions, by position: the first fills the first parameter, and so on, one for each parameter, under *one calling convention* in [procedures](procedure.md) | no |

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
loop is still speaking. The `while` condition, the `body`, and the `result`. A
loop written nameless binds no round: a `break` or `continue` naming no loop
still ends it, and one naming a loop passes through it.
The condition reads the state before the round it would start, so `round.index`
there is how many rounds have finished. What a loop answers is its `result`
read in what the last round that *finished* left behind; a round cut short
contributed nothing. A loop naming no result answers nothing.

A loop carries no budget of its own. Bounding one is the author's to write. A
counter in the condition and a procedure past the bound say it exactly, and
stopping one is the receiver's **cancellation**, under [running](running.md). A kernel
budget would promise neither side anything it could rely on: the author can
already say it, and the receiver could not trust a bound the author chose.

Walking a collection is this construct too, and there is no second one for it.
The round is read against the material's count and the element is read at that
index, so what a walk needs beyond a loop is `std.collection.count`, a
comparison and an index. All three are already there, and none of them is
grammar.

There is no concurrency construct either. Running things at once is
**vocabulary**. `std.concurrent`, under [the standard vocabulary](vocabulary.md), because a closure is already the one
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
no `result` to answer. **refuses at the load**: it would swallow a failure into
null without a trace. A rescue over a body that cannot fail, one the build derives no
failure for, **refuses at the build** for the other half of the same reason: it
is a body no run reaches. A refusal at the run is not a failure and does not
make a body one that can fail, under [running](running.md). This
is the one exception to a block's optional `result`, and the failure is the
reason. The statement's own name binds the failure **while the rescue runs**,
an attempt written nameless binds none, and what a name binds is a **record
declared `{ record: { type: string, message: string, details: dictionary<any> } }`**. `type` names what happened (`aborted`,
`concurrent_failed`), `message` is text for a person, and `details` is what the
failing procedure carried. Every failure holds all three by construction: a
runtime assembles the payload from what a failure declares, so no procedure can
hand over one without them and there is nothing here for a run to check.

The envelope is this specification's; what rides in `details` is the procedure's
own. `concurrent_failed` puts `failures` there: every piece's failure, keyed by
the piece, a record's by its key and an array's by its index written `[0]`,
and each is the envelope that piece raised, so a rescue reads a piece's own
`type`, `message` and `details` through it.

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
way it derives constness and isolation, and the types a failure names itself by
(`aborted`, `cast_refused`) are what it derives: a body fails with what its
plain casts fail with (`cast_refused`, the one failure the runtime itself
raises; `as?` reads the same mismatch as null and raises nothing), with what
the declarations it calls fail with, and with whatever its rescues fail with,
the body under a rescue being caught. Calling a value leaves the
question open, since nothing before the run says which value.

A native procedure says what it may fail with, the way it says whether it is
isolated. **A procedure that says nothing fails nothing**, which is right for
the many procedures that throw only at an author mistake, and a procedure that
can fail says so. `std.control.abort` says `aborted`; `std.concurrent` says
`concurrent_failed`, every piece's failure being gathered into that one. A
piece that refuses at the run refuses the whole run instead, under
[running](running.md), and the failures beside it are not gathered. A procedure that fails and does not say so has broken its contract, the
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
loop. Both **refuse at the load** when nothing encloses them: a closure runs
away from where it was written, so the loops around the writing are
not around the running, and neither crosses into a procedure written inside
another.

Nothing may be written after a `return`, `break` or `continue` in the same body:
it would never run, and the name it would bind would never bind. The same holds
after a call whose answer reads `never`, declared under `returns` or read off a
body that never finishes, at the build. The rule reaches
through structure, because the fact does: a `conditional` both of whose arms
leave never finishes either, so nothing may follow it. Held at the **load**,
since the arms are text. A construct that can finish. A conditional with no
`else`, a loop, an `attempt` (its rescue may finish normally). Is not a leave,
however its bodies end.

There is no `abort` construct. Failing on purpose is a procedure.
`std.control.abort`, under [the standard vocabulary](vocabulary.md), because a signature can say everything checking it
needs: `returns: never` is the whole fact, and a thing is grammar only when
checking it would need to understand more than a signature can say.

## Cases

What `conformance/` asks about this page, by the name each case's file carries.

- `a-block-writes-the-flow-it-is-in`
- `a-break-does-not-excuse-the-arm-it-leaves-from`
- `a-call-that-fails-after-writing-has-written`
- `a-condition-that-is-not-a-bool-refuses`
- `a-conditional-both-of-whose-arms-leave-ends-the-body`
- `a-conditional-writes-the-flow-it-is-in`
- `a-construct-key-outside-a-statement-is-a-field-name`
- `a-declared-name-is-not-retyped-by-a-write`
- `a-declining-conditional-writes-nothing`
- `a-duplicate-statement-name-refuses`
- `a-failure-field-the-declaration-does-not-name-is-refused`
- `a-field-a-path-writes-through-is-declared-var`
- `a-fixed-name-cannot-be-written`
- `a-loop-condition-that-is-not-a-bool-refuses`
- `a-loop-reads-how-many-rounds-passed`
- `a-loop-result-reads-the-last-finished-round`
- `a-loop-takes-no-budget`
- `a-loop-written-nameless-binds-no-round`
- `a-name-on-a-conditional-is-refused`
- `a-name-on-what-never-finishes-is-refused`
- `a-name-says-what-it-holds`
- `a-name-that-says-nothing-is-what-the-build-worked-out`
- `a-name-the-module-bound-is-not-introduced-again`
- `a-named-block-binds-its-result`
- `a-named-step-arrives-where-the-walk-arrives`
- `a-rescue-over-a-body-that-cannot-fail-refuses`
- `a-rescue-reads-a-pieces-own-failure`
- `a-rescue-reads-the-failure-it-caught`
- `a-rescue-reads-what-a-cast-refused`
- `a-rescue-reads-what-a-failure-carried`
- `a-rescue-that-answers-nothing-answers-null`
- `a-rescue-that-produces-nothing-refuses`
- `a-return-is-held-to-the-declaration`
- `a-statement-saying-two-things-refuses`
- `a-statement-with-no-name-still-runs`
- `a-var-field-lets-a-path-through`
- `a-walk-is-a-loop-over-the-count`
- `a-write-both-arms-make-retypes-the-variable`
- `a-write-indexes-with-a-name`
- `a-write-makes-an-entry-of-a-dictionary`
- `a-write-only-one-arm-makes-reads-back-nullable`
- `a-write-reaches-into-what-a-variable-holds`
- `a-write-through-an-element-keeps-the-others`
- `an-arm-that-leaves-holds-nothing-afterwards`
- `an-arm-that-leaves-keeps-the-other-write-definite`
- `an-attempt-catches-a-cast-that-did-not-match`
- `an-attempt-joins-its-body-with-its-rescue`
- `an-attempt-written-nameless-binds-no-failure`
- `break-ends-the-loop`
- `calling-a-value-bounded-to-numbers-refuses`
- `calling-a-value-no-procedure-could-be-refuses`
- `calling-a-value-read-as-a-nullable-number-refuses`
- `calling-a-value-that-may-be-null-refuses`
- `continue-skips-a-round`
- `leaving-answers-from-the-middle`
- `leaving-is-not-failing`
- `leaving-needs-something-to-leave`
- `nothing-runs-after-leaving`
- `nothing-runs-after-what-never-finishes`
- `return-inside-a-closure-answers-the-closure`
- `type-beside-set-refuses`
- `what-is-written-fits-the-type-the-path-reaches`
- `what-nobody-wrote-is-not-readable`
- `writing-a-name-never-declared-refuses`
