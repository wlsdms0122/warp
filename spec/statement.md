# Statements

What a body is made of. A statement binds a name to an expression, and a **construct** is the only thing that runs a body. Everything a program does in a particular order is decided here; what it does it *with* is [the standard vocabulary](vocabulary.md).

## A statement

A map carrying **at most one** naming key and its expression under **`value`**: `{ let "x" value { call {…} } }`, `{ value { loop {…} } }`. A construct sits inside `value` under its own key, and that is the one place a construct key is read. A construct key anywhere else is not a construct: a bare mapping in an operand, such as an argument or an element of an array, is read as an expression form and **refuses at the load**, and under `record` the key is a field name like any other.

The naming key says what the statement does to its name:

| key | means |
|---|---|
| `let` | fixes the name. Written once, never again |
| `var` | introduces a name that may be written again |
| `set` | writes a path headed by a variable: one a `var` declared earlier, a module variable, or an `inout` parameter. `set "p.x"` and `set "people[0].name"` write into what the head holds |

**A name may say what it holds**, under **`type`**, written the way a parameter's type is: `{ let "x" type "Double" value 1 }`. The declaration is what the name holds, and the build works out a reading only where the name declares none. What the statement was given has to fit the declaration, and a declaration naming a type nothing declares **refuses at the build**, and one naming a type parameter **at the load**: what fills a parameter is a call filling the slot that names it, and a name inside a body is no such slot.

A declaration is a slot like a parameter's, so **what the name takes is judged against it** the way an argument is: a whole literal written where it declares a `Double` is the fraction it names, a record literal written where it declares a record is judged field by field and takes the name, a value whose type the build does not know stands where *what a slot takes, exactly* in [types](type.md) says, and any other value is held as it came.

A `set` reaches a name something else declared and a statement with no naming key introduces none, so `type` beside either **refuses at the load**. So does `type` on a statement whose construct binds the name itself. A `loop`'s round and an `attempt`'s failure are the construct's to say.

A declared name is fixed at what it says: a write into a declared `var` is held to the declaration and does not retype it, the way a write into a module variable or an `inout` parameter is. This is what lets a name be handed to an `inout` slot, which asks for the same type the name is. A name whose reading the build worked out is that reading, and a name that says what it holds is what it says.

A statement with no naming key, `{ value … }`, runs its expression and binds nothing. The answer is dropped, which is how an effect is asked for on its own. Three families step out of this freedom, in different directions:

- The constructs that bind **through** the statement's name, `loop` (its round) and `attempt` (its failure). The name they bind through is one the statement introduces, with `let` or `var`. Written nameless, or under a `set`, which introduces none, they bind nothing: a loop with no name has no round to read and an attempt with no name has no failure to read, and each runs the same otherwise.
- The leaving constructs (`return`, `break`, `continue`) take **no** naming key at all: such a statement never finishes, so its name could never bind, and a key that promises a binding that cannot happen **refuses**. The same rule reaches a **call**: a statement whose call answers `Never`, declared under `returns` or read off a body that never finishes, binds nothing and takes no name. Held at the **build**, because only the build knows what a call answers, where the leaves the text shows are held at the load.
- A **`conditional`** takes no naming key either, for the other reason: it finishes, but it answers nothing, under **`conditional`** below.

**What a write reaches.** A `set` names a path, and the head of the path is the variable written. A segment after the head written optional (`?.`, `?[`) **refuses at the load**, because a write reads no absence. Every segment after the head is judged at the **build** against the type the walk has reached: a field of a type declared in `types` is passed through only when the declaration wrote it `var`; an entry of a map and an element of a list are passed through as they are, and an entry the map does not hold yet is made by the write that lands on it, while a write passing through one **refuses at the run**, as a read of one does; `Any` and a nullable type are not written into. What is written has to fit the type the path reaches, and is judged against it, so a box that said what it holds holds a value of its declaration after a write as it did after its declaration, and a box that said nothing holds what the build reads the path as. A write to a whole local variable retypes it unless the variable declared what it holds, under *what a variable reads as* in [checking](checking.md). A variable a closure captured, or a call handed in place, holds from there on the type it read as there, and a later write has to fit it, since the closure or the callee reads and writes the box as that type. Two ways that took one variable as different types **refuse at the build** where they meet, since what each took goes on writing its own type; two names for one declared record are one type. A way meets the others where its leave lands. A write to a module variable or to an `inout` parameter has to fit the type the box holds and retypes nothing. At the run the value is computed first, and then the box is rewritten once, so nothing observes the box halfway, and the path reaches what the names hold once the value has run, the head and the names it indexes with included. What stands between the brackets is judged as a read's is, under [expressions](expression.md), and a path there is read where the write stands: the write lands on that one position of a list, or on that entry of a map, made where the map does not hold it yet.

**A `var` may stand alone.** A statement that is only `{ var "name" }`, with no `value`, introduces the name with nothing in it yet, and a name holding nothing holds null. It is the declaration a conditional's arms write into; what the name reads as afterwards is under *what a variable reads as* in [checking](checking.md). The other two spellings say something about a value, so they still require one, and one written without it **refuses at the load**.

**Where a name may be introduced.** No name introduced in a body, at any depth, takes the spelling of a constant or a variable its document declares, or of a parameter of the procedure it is written in, a closure's included: each **refuses at the load**, and so does a parameter taking a constant's or a variable's spelling. Within one body a name is introduced once, and a second `let` or `var` of it **refuses at the load**. A name declared inside a `block`, a `conditional` arm, a `loop`'s round, an `attempt`'s body or rescue, or a closure's body is read from the statement after it to the end of that body, its `result` included, and nowhere after, so two bodies side by side may each introduce it. Such a body may introduce a name a body around it already introduced, and inside it the name is the new one, with a box of its own: the outer box keeps what it held, and a `set` of that spelling writes the inner name, which **refuses at the load** where a `let` fixed it. A closure's parameter is such a name too.

**One name, several askers.** A statement's name names the statement, and every reader of it reads that one fact: an expression reads the value the statement bound; a body inside a binding construct reads the construct's own binding under it (`round.index`, `tried.message`); a `break` or `continue` names the loop statement it ends. These are not three names sharing a spelling. They are one name, asked three questions, and which question applies is fixed by where the asker stands. What keeps the readings from colliding is scope, stated per construct: a loop's round is readable in its condition, body and result; an attempt's name binds the failure only while the rescue runs, so the binding reading and the value reading are never live at the same place.

The construct keys, each detailed below and each written inside `value`: `call`, `conditional`, `loop`, `attempt`, `block`, `return`, `break`, `continue`. `value` holding anything else holds an expression, under [expressions](expression.md).

## Blocks

A block is `{ body: <statements>, result: <expression> }`, both optional. A block answers what its `result` names, and nothing if it names nothing.

## The constructs

**`call`**. A procedure called, by its spelling or as a value:

| key | takes | required |
|---|---|---|
| `procedure` | a string names the declaration called, resolved at the build. Any other expression is a value the run calls, and a value no procedure could be **refuses at the build**, and so does one whose reading says it may be null: null is not called through, the way it is not read through, at the build where the text shows it and at the run otherwise. Text is never a value a call could take, so the two readings never meet | yes |
| `arguments` | list of expressions, by position: the first fills the first parameter, and so on, one for each parameter, under *one calling convention* in [procedures](procedure.md) | no |

A body a procedure is to run travels as a **closure argument**, like any other value.

**`conditional`**

| key | takes | required |
|---|---|---|
| `when` | expression. Must answer a bool | yes |
| `then` | statements | yes |
| `else` | statements | no |

A conditional is a statement: it **answers nothing**, and it **takes no name**. The condition chooses a way through the body. An arm is statements alone, with no `result` slot, because there is nowhere for a result to go. What an arm keeps it writes to an outer variable with `set`, and a value leaves the procedure through `return`. Both arms are checked whether or not they are taken.

**`loop`**

| key | takes | required |
|---|---|---|
| `while` | expression. Runs another round while true | yes |
| `body` | statements | yes |
| `result` | expression | no |

The loop's own statement name binds the round it is on, a `Round`, a record the language declares as `{ record: { index: Int } }`, readable everywhere the loop is still speaking: the `while` condition, the `body` and the `result`. A loop written nameless binds no round: a `break` or `continue` naming no loop still ends it, and one naming a loop passes through it. The condition reads the state before the round it would start, so `round.index` there is how many rounds have finished, and the `result` reads the round the loop ended on: the one a `break` left, or the one the condition declined to start. What a loop answers is its `result` read in what the last round that *finished* left behind; a round cut short contributed nothing. A loop naming no result answers nothing.

Bounding a loop is the author's to write, with a counter in its condition, and stopping one is the host's **cancellation**, under [running](running.md).

Walking a collection is this construct too: the round is read against the material's count and the element is read at that index, so what a walk needs beyond a loop is `Standard.Collection.count`, a comparison and an index.

Running things at once is **vocabulary**: `Standard.Concurrent`, under [the standard vocabulary](vocabulary.md).

**Note.** A closure is the one body that is safe to run beside another, and "takes closures" is a thing a signature can say. A loop's body writes the enclosing names, which no signature can say. So a walk whose rounds write outward or lean on the round before is a loop, and one where each element's work stands alone is a procedure (`Standard.Collection.map`, `filter`, `Standard.Concurrent.map`), which is what lets the concurrent `map` run it at once.

**`attempt`**

| key | takes | required |
|---|---|---|
| `body` | statements | yes |
| `result` | expression | no |
| `rescue` | block. Runs if the body fails | yes |

A rescue catches failure (what the world did), not leaving (what the program said). A rescue with nothing in it, no statement to run for effect and no `result` to answer, **refuses at the load**: it would swallow a failure into null without a trace. A rescue over a body that cannot fail, one the build derives no failure for, **refuses at the build** for the other half of the same reason: it is a body no run reaches. A refusal at the run is not a failure and does not make a body one that can fail, under [running](running.md). This is the one exception to a block's optional `result`, and the failure is the reason. The statement's own name binds the failure **while the rescue runs**, an attempt written nameless binds none, and what a name binds is a **`Failure`**, a record the language declares as `{ record: { type: String, message: String, details: Dictionary<String, Any> } }`, under [types](type.md). `type` names what happened (`aborted`, `concurrent_failed`), `message` is text for a person, and `details` is what the failing procedure carried. Every failure holds all three by construction: a runtime assembles the payload from what a failure declares, so no procedure can hand over one without them.

The envelope is this specification's; what rides in `details` is the procedure's own. `concurrent_failed` puts `failures` there: every piece's failure under the piece's key, a map's piece under the key it stood under and an array's under its position, an `Int`, and each is the envelope that piece raised, so a rescue reads a piece's own `type`, `message` and `details` through it.

```
{ ref "failed.details[\"failures\"]" }
```

`cast_refused` has no procedure behind it, so this specification names its `details` too: **`expected`**, the type the cast reads as, so a cast to an alias names what the alias stands for, and **`actual`**, the type the value is an instance of, both as text: `expected` in the type's string spelling, a procedure type, whose signature has none, spelled as what stands in front of it and `Procedure` (`const Procedure`), and `actual` by the type's name. Both halves, because what was asked for is readable from the program and what turned up is not.

```
{ ref "failed.details[\"actual\"]" }
```

`details` holds `Any`, so a value read out of it is read as anything until a type is named for it. A field the envelope does not name is not reached by a dot on the failure itself: `failed.failures` **refuses at the build**, and what `details` holds is read through brackets, `failed.details["failures"]`.

**What a body may fail with is known before it runs.** The build derives it the way it derives constness and isolation, and the types a failure names itself by (`aborted`, `cast_refused`) are what it derives: a body fails with what its plain casts fail with (`cast_refused`, the one failure the runtime itself raises; `as?` reads the same mismatch as null and raises nothing), with what the declarations it calls fail with, and with whatever its rescues fail with, the body under a rescue being caught. Calling a value leaves the question open, since nothing before the run says which value.

A procedure the host answers says what it may fail with, the way it says whether it is isolated. **A procedure that says nothing fails nothing**, which is right for the many procedures that throw only at an author mistake, and a procedure that can fail says so. `Standard.Control.abort` says `aborted`; `Standard.Concurrent` says `concurrent_failed`, every piece's failure being gathered into that one. A piece that refuses at the run refuses the whole run instead, under [running](running.md), and the failures beside it are not gathered. A procedure that fails and does not say so has broken its contract, the same way one that holds state and calls itself isolated has.

**`block`**. A body written as a statement, and nothing more: the bare member of the same family as a `conditional` arm or a `loop` round, with the condition left off. Like any statement it *may* take a name, and its name binds what its `result` answers. A block runs here, once, in the same flow, which the text shows, since no expression can carry a block away; so a block may `set` the enclosing variables, exactly as a `conditional` or `loop` body may.

**`return`**. Answer the enclosing procedure from here. Takes an expression, or nothing (`return null`) to answer nothing. The answer must fit what the procedure declared.

**`break`**. End a loop. **`continue`**. End the round and go on to the next. Each takes a loop's statement name, or nothing for the nearest enclosing loop. Both **refuse at the load** when nothing encloses them: a closure runs away from where it was written, so the loops around the writing are not around the running, and neither crosses into a procedure written inside another.

Nothing may be written after a `return`, `break` or `continue` in the same body: it would never run, and the name it would bind would never bind. The same holds after a call whose answer reads `Never`, declared under `returns` or read off a body that never finishes, at the build. The rule reaches through structure, because the fact does: a `conditional` both of whose arms leave never finishes either, so nothing may follow it. Held at the **load**, since the arms are text. A construct that can finish (a conditional with no `else`, a loop, an `attempt`, whose rescue may finish normally) is not a leave, however its bodies end.

Failing on purpose is a procedure, `Standard.Control.abort` under [the standard vocabulary](vocabulary.md), declared `returns: Never`: the signature says everything checking it needs.

## Cases

What `conformance/` asks about this page, by the name each case's file carries.

- `a-block-writes-the-flow-it-is-in`
- `a-body-ending-in-a-call-answering-an-alias-of-never-answers-as-declared`
- `a-closure-a-constant-holds-does-not-take-a-variables-name`
- `a-closure-does-not-leave-what-wrote-it`
- `a-closure-in-a-loop-condition-holds-what-it-takes-for-the-body`
- `a-closure-parameter-may-take-the-spelling-of-a-name-around-it`
- `a-closure-whose-body-shadows-a-variable-takes-nothing-of-it`
- `a-condition-read-as-any-refuses`
- `a-condition-that-is-not-a-bool-refuses`
- `a-conditional-both-of-whose-arms-leave-ends-the-body`
- `a-conditional-writes-the-flow-it-is-in`
- `a-construct-key-in-an-argument-refuses`
- `a-construct-key-outside-a-statement-is-a-field-name`
- `a-declared-name-is-not-retyped-by-a-write`
- `a-declared-type-naming-a-type-parameter-refuses`
- `a-declared-type-nothing-declares-refuses`
- `a-declining-conditional-writes-nothing`
- `a-duplicate-statement-name-refuses`
- `a-failure-field-the-declaration-does-not-name-is-refused`
- `a-field-a-path-writes-through-is-declared-var`
- `a-fixed-name-cannot-be-written`
- `a-let-without-a-value-refuses`
- `a-list-pieces-failure-is-under-its-position`
- `a-loop-binds-a-round-the-language-declares`
- `a-loop-condition-that-is-not-a-bool-refuses`
- `a-loop-reads-how-many-rounds-passed`
- `a-loop-result-reads-a-body-name-as-the-last-finished-round-left-it`
- `a-loop-result-reads-the-last-finished-round`
- `a-loop-takes-no-budget`
- `a-loop-under-a-set-binds-no-round`
- `a-loop-written-nameless-binds-no-round`
- `a-loops-name-reads-its-round-inside-the-loop`
- `a-name-a-block-declares-is-not-read-after-it`
- `a-name-a-round-declares-is-not-read-after-the-loop`
- `a-name-an-arm-declares-is-not-read-after-it`
- `a-name-declared-again-inside-an-arm-is-a-new-name`
- `a-name-introduced-again-in-a-nested-block-is-a-new-name`
- `a-name-on-a-body-that-never-comes-back-refuses`
- `a-name-on-a-call-answering-an-alias-of-never-is-refused`
- `a-name-on-a-call-of-a-declared-procedure-type-answering-an-alias-of-never-is-refused`
- `a-name-on-a-conditional-is-refused`
- `a-name-on-a-return-refuses`
- `a-name-on-what-never-finishes-is-refused`
- `a-name-says-what-it-holds`
- `a-name-that-says-nothing-is-what-the-build-worked-out`
- `a-name-the-module-bound-is-not-introduced-again`
- `a-named-block-binds-its-result`
- `a-parameter-does-not-take-a-name-the-module-bound`
- `a-parameter-is-not-introduced-again-in-a-nested-body`
- `a-parameter-is-not-introduced-again-inside-a-closure`
- `a-procedure-that-can-fail-says-so`
- `a-record-literal-written-into-an-entry-of-a-declared-dictionary-takes-the-name-answers`
- `a-record-literal-written-through-a-field-without-var-refuses`
- `a-rescue-binds-a-failure-the-language-declares`
- `a-rescue-over-a-body-that-cannot-fail-refuses`
- `a-rescue-reads-a-cast-to-a-procedure-type-as-procedure`
- `a-rescue-reads-a-pieces-own-failure`
- `a-rescue-reads-the-failure-it-caught`
- `a-rescue-reads-the-type-a-cast-to-an-alias-reads-as`
- `a-rescue-reads-what-a-cast-refused`
- `a-rescue-reads-what-a-failure-carried`
- `a-rescue-that-answers-nothing-answers-null`
- `a-rescue-that-produces-nothing-refuses`
- `a-result-after-leaving-refuses`
- `a-result-after-what-never-finishes-refuses`
- `a-return-is-held-to-the-declaration`
- `a-set-without-a-value-refuses`
- `a-statement-saying-two-things-refuses`
- `a-statement-with-no-name-still-runs`
- `a-taken-variable-a-loop-writes-is-read-after-it-as-written`
- `a-var-field-lets-a-path-through`
- `a-variable-a-closure-captured-is-not-retyped-after`
- `a-walk-is-a-loop-over-the-count`
- `a-way-ending-in-a-call-answering-an-alias-of-never-contributes-nothing`
- `a-way-that-leaves-is-not-met-by-the-ways-that-go-on`
- `a-way-that-returns-from-a-loop-is-not-met-after-it`
- `a-way-that-returns-from-an-attempt-is-not-met-after-it`
- `a-write-at-a-constant-key-writes-the-entry`
- `a-write-at-a-constant-position-writes-the-element`
- `a-write-index-that-is-not-a-whole-number-refuses`
- `a-write-indexes-with-a-name`
- `a-write-into-an-element-of-bytes-lands-on-that-element-answers`
- `a-write-into-an-entry-of-a-declared-dictionary-is-judged-against-its-entry-type-refuses`
- `a-write-into-an-inout-parameter-is-judged-against-its-type-refuses`
- `a-write-makes-an-entry-of-a-dictionary`
- `a-write-reaches-into-what-a-variable-holds`
- `a-write-through-an-element-keeps-the-others`
- `a-write-through-an-entry-the-map-does-not-hold-refuses`
- `a-write-through-an-optional-segment-refuses`
- `a-write-through-any-refuses`
- `a-write-to-a-taken-variable-lands-in-every-round`
- `a-write-to-a-taken-variable-reads-as-the-type-it-is-held-to`
- `a-write-to-a-variable-handed-in-place-lands-in-every-round`
- `a-write-under-a-key-a-name-holds-writes-the-entry`
- `a-write-under-a-whole-number-key-makes-the-entry`
- `a-write-whose-value-rewrites-its-head-lands-where-the-head-then-holds-answers`
- `an-attempt-body-reads-the-variable-its-statement-name-shadows`
- `an-attempt-catches-a-cast-that-did-not-match`
- `an-attempt-under-a-set-binds-no-failure`
- `an-attempt-without-a-rescue-refuses`
- `an-attempt-written-nameless-binds-no-failure`
- `an-attempts-name-reads-the-failure-inside-its-rescue`
- `an-inner-constant-of-an-outer-name-is-not-written`
- `break-ends-the-loop`
- `calling-a-value-bounded-to-numbers-refuses`
- `calling-a-value-no-procedure-could-be-refuses`
- `calling-a-value-read-as-a-nullable-number-refuses`
- `calling-a-value-that-may-be-null-refuses`
- `continue-skips-a-round`
- `leaving-answers-from-the-middle`
- `leaving-is-not-failing`
- `leaving-needs-something-to-leave`
- `nothing-runs-after-a-call-answering-an-alias-of-never`
- `nothing-runs-after-leaving`
- `nothing-runs-after-what-never-finishes`
- `return-inside-a-closure-answers-the-closure`
- `sibling-blocks-may-each-introduce-one-name`
- `two-breaks-taking-a-variable-as-different-types-refuse`
- `two-ways-taking-a-variable-as-a-type-and-its-nullable-refuse`
- `two-ways-taking-a-variable-as-a-type-parameter-and-a-type-refuse`
- `two-ways-taking-a-variable-as-different-types-refuse-where-they-meet`
- `two-ways-taking-a-variable-under-two-names-of-one-record-stand`
- `type-beside-set-refuses`
- `type-on-a-statement-binding-a-loop-refuses`
- `type-on-a-statement-with-no-name-refuses`
- `what-is-written-fits-the-type-the-path-reaches`
- `what-nobody-wrote-is-not-readable`
- `writing-a-name-never-declared-refuses`
