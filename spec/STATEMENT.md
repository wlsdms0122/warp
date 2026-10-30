# Statements

What a body is made of. A statement binds a name to an expression, and a **construct** is the only thing that runs a body. Everything a program does in a particular order is decided here; what it does it *with* is [the standard vocabulary](VOCABULARY.md).

## A statement

A dictionary carrying **at most one** naming key and its expression under **`value`**: `{ let: x, value: { call: … } }`, `{ value: { loop: … } }`. A construct sits inside `value` under its own key, and that is the one place a construct key is read. A construct key anywhere else is not a construct: a bare mapping in an operand, such as an argument or an element of an array, is read as an expression form and **refuses at the load**, and under `struct` the key is a field name like any other.

The naming key says what the statement does to its name:

| key | means |
|---|---|
| `let` | fixes the name. Written once, never again |
| `var` | introduces a name that may be written again |
| `set` | writes a path headed by a variable: one a `var` declared earlier, a module variable, or an `inout` parameter. `set "p.x"` and `set "people[0].name"` write into what the head holds |

**A name may say what it holds**, under **`type`**, written the way a parameter's type is: `{ let: x, type: Double, value: 1 }`. The declaration is what the name holds, and the build works out a reading only where the name declares none. What the statement was given has to fit the declaration, and a declaration naming a type nothing declares **refuses at the build**. One naming a type parameter of the procedure the body is written in reads it as the call filled it, under [types](TYPE.md), and one naming any other type parameter **refuses at the load**.

A declaration is a slot like a parameter's, so **what the name takes is judged against it** the way an argument is: an integer literal written where it declares a `Double` is the `Double` it names, a struct literal written where it declares a struct is judged field by field and takes the name, a value whose type the build does not know stands where *what a slot takes, exactly* in [types](TYPE.md) says, and any other value is held as it came.

A `set` reaches a name something else declared and a statement with no naming key introduces none, so `type` beside either **refuses at the load**. So does `type` on a statement whose construct binds the name itself. A `loop`'s round, a `try`'s failure and an `unwrap`'s payload are the construct's to say.

A declared name is fixed at what it says: a write into a declared `var` is held to the declaration and does not retype it, the way a write into a module variable or an `inout` parameter is. This is what lets a name be handed to an `inout` slot, which asks for the same type the name is. A name whose reading the build worked out is that reading, and a name that says what it holds is what it says.

A statement with no naming key, `{ value: … }`, runs its expression and binds nothing. The result is dropped, which is how an effect is asked for on its own. Three families step out of this freedom, in different directions:

- The constructs that bind **through** the statement's name, `loop` (its round), `try` (its failure) and `unwrap` (its payload). The name they bind through is one the statement introduces, with `let`: nothing writes it, so one introduced with `var` **refuses at the load**, and so does a `set` of one. Written nameless they bind nothing: a loop with no name has no round to read, a try with no name has no failure to read and an unwrap with no name has no payload to read, and each runs and leaves the same otherwise.
- The leaving constructs (`return`, `break`, `continue`) take **no** naming key at all: such a statement never finishes, so its name could never bind, and a key that promises a binding that cannot happen **refuses**. The same rule reaches a **call**: a statement whose call returns `Never`, as its callee's `returns` declares, binds nothing and takes no name. Held at the **build**, because only the build knows what a call returns, where the leaves the text shows are held at the load.
- A **`conditional`** takes no naming key either, for the other reason: it finishes, but it has no value, under **`conditional`** below. A `loop`, a `try` and an `unwrap` written with a `then` have no value either, an `unwrap` written with none has its payload, and the name of each is its round's, its failure's or its payload's alone, one that does not finish included.

**What a write reaches.** A `set` names a path, and the head of the path is the variable written. A segment after the head written optional (`?.`, `?[`) **refuses at the load**, because a write reads no absence. Every segment after the head is judged at the **build** against the type the walk has reached: a field of a type declared in `types` is passed through only when the declaration wrote it `var`; an entry of a dictionary and an element of a list are passed through as they are, and an entry the dictionary does not hold yet is made by the write that lands on it, while a write passing through one **refuses at the run**, as a read of one does; `Any` and an Optional are not written into. What is written has to fit the type the path reaches, and is judged against it, so a box that said what it holds holds a value of its declaration after a write as it did after its declaration, and a box that said nothing holds what the build reads the path as. A write to a whole local variable retypes it unless the variable declared what it holds, under *what a variable reads as* in [checking](CHECKING.md). A variable a closure captured, or a call handed in place, holds from there on the type it read as there, and a later write has to fit it, since the closure or the callee reads and writes the box as that type. Two ways that took one variable as different types **refuse at the build** where they meet, since what each took goes on writing its own type; two names for one declared struct are one type. A way meets the others where its leave lands. A write to a module variable or to an `inout` parameter has to fit the type the box holds and retypes nothing. At the run the value is computed first, and then the box is rewritten once, so nothing observes the box halfway, and the path reaches what the names hold once the value has run, the head and the names it indexes with included. What stands between the brackets is judged as a read's is, under [expressions](EXPRESSION.md), and a path there is read where the write stands: the write lands on that one position of a list, or on that entry of a dictionary, made where the dictionary does not hold it yet.

**A `var` may stand alone.** A statement that is only `{ var: name }`, with no `value`, introduces the name with nothing in it yet, and a name holding nothing holds null. Written with `value: null` it says what the bare `var` says a second way, and **refuses at the load**. It is the declaration a conditional's arms write into; what the name reads as afterwards is under *what a variable reads as* in [checking](CHECKING.md). The other two spellings say something about a value, so they still require one, and one written without it **refuses at the load**.

**Where a name may be introduced.** A body introduces a name once, and a second `let` or `var` of it **refuses at the load**. A procedure's parameters stand in a scope around its body, and a closure's around the closure's body, so a body may introduce one of its own parameters again. A name declared inside a `conditional` arm, a `loop`'s round, a `try`'s body or catch, an `unwrap`'s `then` or `else`, or a closure's body is read from the statement after it to the end of that body, and nowhere after, so two bodies side by side may each introduce it. A body may introduce any name it sees: a constant or a variable its document declares, a parameter of the procedure it is written in, or a name a body around it introduced. From the statement after it the name is the new one, with a box of its own: the outer name keeps what it held, a parameter handed in place keeps the caller's variable, and a `set` of that spelling writes the inner name, which **refuses at the load** where a `let` fixed it. A procedure's body stands inside its document, so a parameter may take a constant's or a variable's spelling, and a closure's parameter may take any name around the closure.

**One name, several askers.** A statement's name names the statement, and every reader of it reads that one fact: an expression reads the value the statement bound; a body inside a binding construct reads the construct's own binding under it (`round.index`, `tried.message`, an unwrap's payload); a `break` or `continue` names the loop statement it ends. These are not three names sharing a spelling. They are one name, asked three questions, and which question applies is fixed by where the asker stands. What keeps the readings from colliding is scope, stated per construct: a loop's round is readable in its condition and body, and its name reads nothing after it; a try's name binds the failure only while the catch runs, and an unwrap's the payload only while `then` runs, or, written with no `then`, from the statement on, so the binding reading and the value reading are never live at the same place. A name a body introduces again is the new one to every asker, a leave included: after a `let` or `var` of a loop's spelling in a body inside the loop, in a catch whose failure takes it and where an unwrap's payload takes it, a `break` or `continue` naming that spelling names no loop around it, and **refuses at the load**.

The construct keys, each detailed below and each written inside `value`: `conditional`, `loop`, `try`, `unwrap`, `return`, `break`, `continue`. `value` holding anything else holds an expression, under [expressions](EXPRESSION.md), a call among them.

## Calls

A call is an expression, `{ call: … }`, written wherever a value is wanted and as a statement's `value`. A procedure called, by its spelling or as a value:

| key | takes | required |
|---|---|---|
| `procedure` | a string names the declaration called, resolved at the build. Any other expression is a value the run calls, and a value no procedure could be **refuses at the build**, and so does one whose reading is an Optional: null is not called through, the way it is not read through, at the build where the text shows it and at the run otherwise. A string is never a value a call could take, so the two readings never meet | yes |
| `arguments` | list of expressions, by position: the first fills the first parameter, and so on, one for each parameter, under *one calling convention* in [procedures](PROCEDURE.md) | no |

A body a procedure is to run travels as a **closure argument**, like any other value.

## The constructs

**`conditional`**

| key | takes | required |
|---|---|---|
| `when` | expression. Must be a `Bool` | yes |
| `then` | statements | yes |
| `else` | statements | no |

A conditional is a statement: it **has no value**, and it **takes no name**. The condition chooses a way through the body. An arm is statements. What an arm keeps it writes to an outer variable with `set`, and a value leaves the procedure through `return`. Both arms are checked whether or not they are taken.

**`loop`**

| key | takes | required |
|---|---|---|
| `while` | expression. Runs another round while true | no |
| `body` | statements | yes |

A loop is a statement: it **has no value**, the way a `conditional` does, and what a round keeps it writes to an outer variable. The loop's own statement name binds the round it is on, a `Round`, a struct the language declares as `{ struct: { index: Int } }`, readable where the loop speaks, the `while` condition and the `body`, and nowhere after the loop. A loop written nameless binds no round: a `break` or `continue` naming no loop still ends it, and one naming a loop passes through it. The condition reads the state before the round it would start, so `round.index` there is how many rounds have finished.

**A loop written with no `while` does not finish.** The text declares it: a round runs after every round, and only a leave reaching past the loop ends it, a `return` or a `break` or `continue` naming a loop further out. A `continue` of it starts the next round, and a `break` that would end it, one naming no loop included, **refuses at the load**. It never finishes, so nothing may follow it, and a body ending in one leaves on every way through it. A loop written with `while` may finish whatever its condition reads: `(while true)` is one, and a `break` ends it.

Bounding a loop is the author's to write, with a counter in its condition, and stopping one is the host's **cancellation**, under [running](RUNNING.md).

Walking a collection is this construct too: the round is read against the material's count and the element is read at that index, so what a walk needs beyond a loop is `Standard.Collection.count`, a comparison and an index.

Running things at once is **vocabulary**: `Standard.Concurrent`, under [the standard vocabulary](VOCABULARY.md).

**Note.** A closure is the one body that is safe to run beside another, and "takes closures" is a thing a signature can say. A loop's body writes the enclosing names, which no signature can say. So a walk whose rounds write outward or lean on the round before is a loop, and one where each element's work stands alone is a procedure (`Standard.Collection.map`, `filter`, `Standard.Concurrent.map`), which is what lets the concurrent `map` run it at once.

**`try`**

| key | takes | required |
|---|---|---|
| `body` | statements | yes |
| `catch` | statements. Runs if the body fails | yes |

A try is a statement: it **has no value**, the way a `conditional` does. Its body and its catch are its two ways through, and what either keeps it writes to an outer variable with `set`. A catch takes failure (what the world did), not leaving (what the program said). A catch with no statement in it **refuses at the load**: it would drop a failure without a trace. A catch over a body that cannot fail, one whose casts and calls say no failure, **refuses at the build** for the other half of the same reason: it is a body no run reaches. A refusal at the run is not a failure and does not make a body one that can fail, under [running](RUNNING.md). The statement's own name binds the failure **while the catch runs** and nowhere after the try, a try written nameless binds none, and what a name binds is a **`Failure`**, a struct the language declares as `{ struct: { type: String, message: String, details: Dictionary<String, Any> } }`, under [types](TYPE.md). `type` names what happened (`aborted`, `concurrent_failed`), `message` is a string for a person, and `details` is what the failing procedure carried. Every failure holds all three by construction: a runtime assembles the payload from what a failure declares, so no procedure can hand over one without them.

The envelope is this specification's; what rides in `details` is the procedure's own, the standard vocabulary's under [the standard vocabulary](VOCABULARY.md).

```
{ ref: "failed.details[\"failures\"]" }
```

`cast_refused` has no procedure behind it, so this specification names its `details` too: **`expected`**, the type the cast reads as, so a cast to an alias names what the alias stands for, and **`actual`**, the type the value is an instance of, both as strings: `expected` in the type's string spelling and `actual` by the type's name. Both halves, because what was asked for is readable from the program and what turned up is not.

```
{ ref: "failed.details[\"actual\"]" }
```

`details` holds `Any`, so a value read out of it is read as anything until a type is named for it. A field the envelope does not name is not reached by a dot on the failure itself: `failed.failures` **refuses at the build**, and what `details` holds is read through brackets, `failed.details["failures"]`.

**What a body may fail with is declared, and known before it runs.** A declaration and a closure literal name it under `failing`, by the types a failure names itself by (`aborted`, `cast_refused`), or say `anything`, and a body failing with more than its declaration names **refuses at the build**. A body fails with what its plain casts fail with (`cast_refused`, the one failure the runtime itself raises; `as?` reads the same mismatch as the none and raises nothing), with what the declarations it calls say they fail with, and with whatever its catches fail with, the body under a catch being caught. Calling a value fails with what the type written for it says it may fail with, by the rule under *a const procedure* in [procedures](PROCEDURE.md), since nothing before the run says which value.

A native procedure says what it may fail with the same way. **A procedure that says nothing fails nothing**, which is right for the many procedures that throw only at an author mistake, and a procedure that can fail says so. `Standard.Control.abort` says `aborted`; `Standard.Concurrent` says `concurrent_failed`, every piece's failure being gathered into that one. A piece that refuses at the run refuses the whole run instead, under [running](RUNNING.md), and the failures beside it are not gathered. A procedure that fails and does not say so has broken its contract, the same way one that holds state and calls itself isolated has.

**`unwrap`**

| key | takes | required |
|---|---|---|
| `of` | expression. Its reading is an Optional | yes |
| `then` | statements. Runs where `of` holds a some | no |
| `else` | statements. Runs where `of` holds the none | no |

An unwrap is a statement, and written with a `then` it **has no value**, the way a `conditional` does. It takes an Optional apart one level, under [types](TYPE.md): where `of` holds `null` it takes the `else` way, and otherwise the `then` way, where the statement's own name binds the **payload** while `then` runs and nowhere after the unwrap. The payload is what a `Some` holds, and any other value itself, and it reads `T` where `of` reads `T?`. An unwrap written nameless binds no payload. The two ways meet past the unwrap as a conditional's arms do, a way not written as the way that wrote nothing. What `of` takes apart is an operand, read rather than run, under [procedures](PROCEDURE.md). An unwrap with neither `then` nor `else` **refuses at the load**, since no way through it reads what it takes apart, and an `of` whose reading is no Optional **refuses at the build**, since it holds no none to take apart.

**An unwrap written with no `then` has the payload past it**, its value, whether or not a name binds it, so a none has no way on: every way through `else` leaves, and an `else` with a way that finishes **refuses at the build**, where a way ending in a call returning `Never` is known. A name, where one is written, holds the payload from the statement after the unwrap to the end of the statements it stands among.

**`return`**. Return from the enclosing procedure here. Takes an expression, or nothing (`{ return: null }`, the text `(return)`) to return nothing. The return value must fit what the procedure declared, and it is the only way a body returns a value, under *a procedure* in [procedures](PROCEDURE.md).

**`break`**. End a loop. **`continue`**. End the round and go on to the next. Each takes nothing for the nearest enclosing loop, or the statement name of a loop further out. A name is for reaching past the nearest: one naming the nearest says what naming none says, and a document says each thing one way, so it **refuses at the load**. Both **refuse at the load** when nothing encloses them: a closure runs away from where it was written, so the loops around the writing are not around the running, and neither crosses into a procedure written inside another.

Nothing may be written after a `return`, `break` or `continue` in the same body: it would never run, and the name it would bind would never bind. The same holds after a call whose callee declares `returns: Never`, at the build. The rule reaches through structure, because the fact does: a `conditional` both of whose arms leave never finishes either, nor does a `try` whose body and catch both leave, nor an `unwrap` whose `then` and `else` both leave, nor a `loop` written with no `while`, so nothing may follow any of them. Held at the **load** where the text shows it, and at the **build** where a way ends in a call returning `Never`. A construct one of whose ways may finish (a conditional with no `else`, a loop written with `while`, a try whose body or catch may finish, an unwrap with no `then` or no `else`) is not a leave, however its other ways end.

Failing on purpose is a procedure, `Standard.Control.abort` under [the standard vocabulary](VOCABULARY.md), declared `returns: Never`: the signature says everything checking it needs.

## Cases

What `conformance/` asks about this page, by the name each case's file carries.

- `a-body-ending-in-a-call-returning-an-alias-of-never-returns-as-declared`
- `a-body-ending-in-a-return-returns-its-value`
- `a-body-failing-beyond-its-declaration-refuses`
- `a-body-introducing-its-parameter-again-reads-the-parameter-in-its-value`
- `a-body-may-introduce-its-parameter-again`
- `a-break-in-a-closure-written-in-a-loop-refuses`
- `a-break-naming-a-loop-a-let-inside-it-hides-refuses`
- `a-break-naming-a-loop-with-no-while-refuses`
- `a-break-naming-an-outer-loop-from-a-loop-with-no-while-ends-the-outer-loop`
- `a-break-naming-an-outer-loop-past-a-named-one-ends-the-outer-loop`
- `a-break-naming-the-nearest-loop-refuses`
- `a-break-outside-a-loop-refuses`
- `a-call-of-a-value-fails-with-what-its-slots-procedure-type-names`
- `a-catch-binds-a-failure-the-language-declares`
- `a-catch-over-a-body-that-cannot-fail-refuses`
- `a-catch-reads-a-cast-to-a-procedure-type-by-its-spelling`
- `a-catch-reads-a-pieces-own-failure`
- `a-catch-reads-the-failure-it-caught`
- `a-catch-reads-the-type-a-cast-to-an-alias-reads-as`
- `a-catch-reads-what-a-cast-refused`
- `a-catch-reads-what-a-failure-carried`
- `a-catch-that-produces-nothing-refuses`
- `a-closure-a-constant-holds-may-introduce-a-variables-spelling`
- `a-closure-body-may-introduce-its-parameter-again`
- `a-closure-failing-beyond-its-signature-refuses`
- `a-closure-may-introduce-a-parameter-of-the-procedure-around-it`
- `a-closure-parameter-may-take-the-spelling-of-a-name-around-it`
- `a-closure-whose-body-shadows-a-variable-takes-nothing-of-it`
- `a-condition-read-as-any-refuses`
- `a-condition-that-is-not-a-bool-refuses`
- `a-conditional-writes-the-flow-it-is-in`
- `a-construct-key-in-an-argument-refuses`
- `a-construct-key-outside-a-statement-is-a-field-name`
- `a-continue-in-a-loop-with-no-while-starts-the-next-round`
- `a-continue-naming-an-outer-loop-past-a-named-one-starts-its-next-round`
- `a-continue-naming-the-nearest-loop-refuses`
- `a-declaration-failing-with-anything-may-fail-with-any-failure`
- `a-declared-type-naming-a-bounded-type-parameter-holds-its-bounds`
- `a-declared-type-naming-a-type-parameter-its-procedure-does-not-declare-refuses`
- `a-declared-type-naming-a-type-parameter-reads-it-as-the-call-filled-it`
- `a-declared-type-nothing-declares-refuses`
- `a-declining-conditional-writes-nothing`
- `a-duplicate-statement-name-refuses`
- `a-failure-field-the-declaration-does-not-name-refuses`
- `a-let-without-a-value-refuses`
- `a-list-pieces-failure-is-under-its-position`
- `a-loop-binds-a-round-the-language-declares`
- `a-loop-condition-that-is-not-a-bool-refuses`
- `a-loop-holding-a-key-other-than-while-and-body-refuses`
- `a-loop-named-with-var-refuses`
- `a-loop-reads-how-many-rounds-passed`
- `a-loop-under-a-set-refuses`
- `a-loop-with-no-while-binds-its-round-under-its-name`
- `a-loop-written-nameless-binds-no-round`
- `a-loops-name-leaves-the-outer-name-after-the-loop`
- `a-loops-name-leaves-the-outer-name-to-what-a-constant-call-reads`
- `a-loops-name-leaves-the-outer-name-to-what-a-failure-check-reads`
- `a-loops-name-leaves-the-outer-variable-to-write-after-the-loop`
- `a-loops-name-reads-its-round-inside-the-loop`
- `a-loops-name-reads-nothing-after-the-loop-refuses`
- `a-name-a-nested-body-introduces-under-a-constants-spelling-is-its-own`
- `a-name-a-round-declares-read-after-the-loop-refuses`
- `a-name-an-arm-declares-read-after-it-refuses`
- `a-name-declared-again-inside-an-arm-is-a-new-name`
- `a-name-introduced-again-in-a-nested-body-is-a-new-name`
- `a-name-on-a-body-that-never-comes-back-refuses`
- `a-name-on-a-call-of-a-declared-procedure-type-returning-an-alias-of-never-refuses`
- `a-name-on-a-call-returning-an-alias-of-never-refuses`
- `a-name-on-a-conditional-refuses`
- `a-name-on-a-return-refuses`
- `a-name-on-what-never-finishes-refuses`
- `a-name-saying-nothing-handed-in-place-at-another-type-refuses`
- `a-name-says-what-it-holds`
- `a-nameless-break-in-a-loop-with-no-while-refuses`
- `a-nameless-unwrap-without-then-whose-else-finishes-refuses`
- `a-parameter-handed-in-place-introduced-again-keeps-the-callers-variable`
- `a-parameter-introduced-again-in-a-nested-body-is-a-new-name`
- `a-parameter-may-take-a-constants-spelling`
- `a-path-writing-through-a-field-not-declared-var-refuses`
- `a-procedure-that-can-fail-says-so`
- `a-return-on-one-way-the-declaration-does-not-take-refuses`
- `a-round-ending-in-continue-goes-on-to-the-next`
- `a-set-of-a-failures-name-refuses`
- `a-set-of-a-rounds-name-refuses`
- `a-set-without-a-value-refuses`
- `a-statement-after-a-call-returning-an-alias-of-never-refuses`
- `a-statement-after-a-conditional-both-of-whose-arms-leave-refuses`
- `a-statement-after-a-loop-with-no-while-refuses`
- `a-statement-after-a-try-both-of-whose-ways-leave-refuses`
- `a-statement-after-a-try-whose-catch-ends-in-a-call-returning-never-refuses`
- `a-statement-after-an-unwrap-both-of-whose-ways-leave-refuses`
- `a-statement-after-leaving-refuses`
- `a-statement-after-what-never-finishes-refuses`
- `a-statement-saying-two-things-refuses`
- `a-statement-with-no-name-still-runs`
- `a-struct-literal-written-into-an-entry-of-a-declared-dictionary-takes-the-name`
- `a-struct-literal-written-through-a-field-without-var-refuses`
- `a-taken-variable-a-loop-writes-returned-where-null-is-not-declared-refuses`
- `a-try-around-a-call-of-a-value-whose-type-fails-with-nothing-refuses`
- `a-try-catches-a-cast-that-did-not-match`
- `a-try-named-with-var-refuses`
- `a-try-under-a-set-refuses`
- `a-try-without-a-catch-refuses`
- `a-try-written-nameless-binds-no-failure`
- `a-trys-name-reads-nothing-after-the-try-refuses`
- `a-trys-name-reads-the-failure-inside-its-catch`
- `a-var-field-lets-a-path-through`
- `a-var-started-at-null-written-out-refuses`
- `a-variable-only-a-trys-body-writes-is-null-after-its-catch`
- `a-walk-is-a-loop-over-the-count`
- `a-way-ending-in-a-call-returning-an-alias-of-never-contributes-nothing`
- `a-way-that-leaves-is-not-met-by-the-ways-that-go-on`
- `a-way-that-returns-from-a-loop-is-not-met-after-it`
- `a-way-that-returns-from-a-try-is-not-met-after-it`
- `a-write-at-a-constant-key-writes-the-entry`
- `a-write-at-a-constant-position-writes-the-element`
- `a-write-index-that-is-not-an-integer-refuses`
- `a-write-indexes-with-a-name`
- `a-write-into-an-element-of-bytes-lands-on-that-element`
- `a-write-into-an-entry-of-a-declared-dictionary-is-judged-against-its-entry-type-refuses`
- `a-write-into-an-inout-parameter-is-judged-against-its-type-refuses`
- `a-write-makes-an-entry-of-a-dictionary`
- `a-write-of-another-type-into-a-declared-name-refuses`
- `a-write-of-another-type-into-a-variable-a-closure-captured-refuses`
- `a-write-of-another-type-into-what-a-loop-conditions-closure-takes-refuses`
- `a-write-of-another-type-into-what-a-try-body-reads-under-its-name-refuses`
- `a-write-of-another-type-through-a-path-refuses`
- `a-write-reaches-into-what-a-variable-holds`
- `a-write-through-an-element-keeps-the-others`
- `a-write-through-an-entry-the-dictionary-does-not-hold-refuses`
- `a-write-through-an-optional-segment-refuses`
- `a-write-through-any-refuses`
- `a-write-to-a-taken-variable-lands-in-every-round`
- `a-write-to-a-taken-variable-reads-as-the-type-it-is-held-to`
- `a-write-to-a-variable-handed-in-place-lands-in-every-round`
- `a-write-under-a-key-a-name-holds-writes-the-entry`
- `a-write-under-an-int-key-makes-the-entry`
- `a-write-whose-value-writes-its-head-lands-where-the-head-then-holds`
- `an-unwrap-binds-the-payload-while-its-then-runs`
- `an-unwrap-named-with-var-refuses`
- `an-unwrap-of-a-none-takes-its-else`
- `an-unwrap-of-an-inner-none-binds-a-none`
- `an-unwrap-of-what-is-no-optional-refuses`
- `an-unwrap-under-a-set-refuses`
- `an-unwrap-with-neither-then-nor-else-refuses`
- `an-unwrap-without-then-binds-after-it`
- `an-unwrap-without-then-under-a-set-refuses`
- `an-unwrap-without-then-whose-else-finishes-refuses`
- `an-unwrap-written-nameless-binds-no-payload`
- `an-unwraps-name-reads-nothing-after-the-unwrap-refuses`
- `break-ends-the-loop`
- `calling-a-value-bounded-to-numbers-refuses`
- `calling-a-value-no-procedure-could-be-refuses`
- `calling-a-value-read-as-an-optional-number-refuses`
- `calling-a-value-that-may-be-null-refuses`
- `continue-skips-a-round`
- `leaving-is-not-failing`
- `reading-what-nobody-wrote-refuses`
- `return-inside-a-closure-returns-from-the-closure`
- `returning-from-the-middle-leaves-early`
- `sibling-bodies-may-each-introduce-one-name`
- `two-breaks-taking-a-variable-as-different-types-refuse`
- `two-ways-taking-a-variable-as-a-type-and-its-optional-refuse`
- `two-ways-taking-a-variable-as-a-type-parameter-and-a-type-refuse`
- `two-ways-taking-a-variable-as-different-types-refuse`
- `two-ways-taking-a-variable-under-two-names-of-one-struct-stand`
- `type-beside-set-refuses`
- `type-on-a-statement-binding-a-loop-refuses`
- `type-on-a-statement-binding-a-try-refuses`
- `type-on-a-statement-binding-an-unwrap-refuses`
- `type-on-a-statement-with-no-name-refuses`
- `writing-a-fixed-name-refuses`
- `writing-a-name-never-declared-refuses`
- `writing-an-inner-constant-spelled-like-an-outer-variable-refuses`
