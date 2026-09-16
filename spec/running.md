# Running

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
way it works out constness:

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
  variable a closure captured), hands none of those in place, calls a value
  (`apply`) only through a name a slot declared `isolated procedure`, and calls
  only isolated declarations. The slot's word is what says an applied value
  writes only its own names, the same way `const procedure` is what says an
  applied value answers without running, and a closure carries the word for a
  name it captured. The build starts every body
  isolated and strikes them until nothing more is struck, and judges every
  closure literal by the same rule. A closure value carries the constness and
  isolation the build derived, and a slot asking for either reads them wherever
  the value arrives, through `any` or an undeclared field included.
- **A native procedure says whether it is isolated, and is taken at its word for
  what it does itself.** The build reads what a body writes and calls; what a
  procedure keeps in the host language is outside the document, so the procedure
  declares it. A procedure that declares nothing is isolated, and one that holds
  state between calls declares otherwise, which strikes every body that reaches
  it. `const` does not answer this: a procedure can answer without running and
  still answer from a box two callers share. What the build does hold this claim
  to is what the procedure sends, under *a procedure the host answers* in [procedures](procedure.md).
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

## Cases

What `conformance/` asks about this page, by the name each case's file carries.

- `concurrency-is-granted-vocabulary`
