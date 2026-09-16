# Expressions

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
| `{ format:, with: }` | reserved: a front-end spelling, under [the document format](document.md); **refuses** in a document |

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
value it read. What a constant may settle from is under *what a constant
settles from* in [procedures](procedure.md), and a body **its own document**
declares is not among them: such a body is itself still being resolved beside
the constants it may read, so a constant that runs one would be a circle with
no start, and it refuses at the build. Settling asks native procedures, so a
link answers them before any of the program runs. An index written as a
reference (`items[i]`) is a path of its own, judged wherever the outer walk
stops: a
reference that provably is not a whole number refuses at the build, and one that
names nothing refuses at the run.

The same brackets read a **dictionary** by a key the run settles (`held[name]`),
which is what walking one is for: `keys` answers the names and this reads the
entry under one. What stands between the brackets is judged where an index is,
and has to be able to be a string. An entry that is not there refuses at the run
the way a written key does, and `?[` reads it as null. A record takes no such
reading: its fields are the type's, so a name the run settles has nothing there
to be judged against.

## Blocks

A block is `{ body: <statements>, result: <expression> }`, both optional. A
block answers what its `result` names, and nothing if it names nothing.
