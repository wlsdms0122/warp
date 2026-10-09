# Expressions

What is read rather than run. A literal, a name, a path through one, a cast, a record, an array, a call and a closure written where a value is wanted. The line between this page and [statements](statement.md) is the line an operand stands on: a construct runs a body and is refused here.

A scalar is itself, a literal. A string is always literal text; nothing inside it is ever re-parsed. An array is an array of expressions. A mapping is an expression by its **one key**, and that key is one of these:

| form | means |
|---|---|
| `{ ref: a.b[0] }` | a name, resolved in the scope that reads it |
| `{ record: { … } }` | a record, its fields each an expression. A field may be called anything, `ref` and `value` included |
| `{ call: <call> }` | a call where a value is wanted; same grammar as the `call` construct |
| `{ closure: <procedure> }` | a procedure written where a value is wanted; same grammar as a procedure |
| `{ as: { of: <value>, type: <type> } }` | read the value as that type. The door onto what `Any` declares nothing about |
| `{ as?: { of: <value>, type: <type> } }` | the same, reading a mismatch as null rather than refusing; the answer is `T?` |

A mapping with another key, or with more than one, **refuses at the load**. A key names a form and never a field, so no field name is reserved.

A path is a name, then `.name` for a field and `[…]` for an index. A `[` left open, or a `]` that closes none, **refuses at the load**.

A **cast** names the type a value is read as. The type is written the way any type is: a name, or the mapping a record or a signature is written as. From the cast on, the reading *is* that type, so every dot after it is judged against it; the run is left the one question the build cannot answer, which is what actually arrived, and it answers it by judging the value against the type, leaving nothing out. A cast is how a value read as `Any`, as a contract, or along a path a call decides reaches a slot of a type, since the build does not know which type it is. A plain `as` **fails at the run** with `cast_refused` when the value is not that type. It is a failure like any other, so an `attempt` catches it, and `as?` reads that mismatch as null, which is the author saying they expected it.

A cast that names the type the reading already **is** refuses at the build, the way a needless `?.` does: the claim says nothing. The test is sameness, not admission: a reading of `Int?` cast to `Int` names something the types leave open, and only the run can say whether it holds. A cast to a declared record name is one of the places a name is written: reading a nameless record as `Account` attaches the name, so it is never a cast of what the reading already is, and only a reading that is already `Account` makes it one, at whatever depth the name stands and under whatever alias of `Account` either side writes. A cast writes a name and never takes one away: a reading under one declared record cast to another, to an inline record type or to `Dictionary<T>` names a type no value it reads is, null and an empty list or map aside where both take one, and **refuses at the build**, and so does a cast to a record type of other fields than the reading's, since a record type is exactly its fields. A cast reads a value and is no place a literal is written into: a whole literal in its operand, at any depth, is the `Int` it is, so `{ x: 1 } as { x: Double }` names a type no value is both and **refuses at the build**, and `[1] as Array<Double>` builds, the empty list being a value of both, and fails at the run. A cast onto `Any`, `Never` or a type parameter refuses for the other half of the same reason: those name no type to read. A type parameter written anywhere inside a cast's type (`Array<some T>`) **refuses at the load** as it does on a name saying what it holds: nothing in a body fills one, so there is no type there to judge what arrives against.

A cast between a reading and a type **no value is both** refuses at the build too: it could not succeed on any run, so `as` would refuse every time and `as?` would answer null every time, a null that says nothing about the value.

A cast that names a type nothing declares **refuses at the build**, wherever it is written, by the rule every type spelling is held to. `as?` reads a value that is not the named type as null; it does not read a name that names nothing as null, because that is the declaration being wrong rather than the value.

A construct's key, `conditional` or `loop`, is read under a statement's `value` and nowhere else, under [statements](statement.md).

**A dot reads a name and nothing else.** Every `ref` path is judged where names resolve, and the judgement is written into the image; the value that arrives at run time has no say in it. A procedure is sent with a written `call`, which spells the declaration it means. Segment by segment:

- On a **record type**, a dot reads the field the type declares. A field it does not declare **refuses at the build**, `?.` or not. The type rules the field out, and no spelling reads past that. A procedure on a record is written as a call. A record type says which fields there are, and a value fits it only with exactly them, so there is nothing else to reach. To read names a declaration does not have, take `Dictionary<Any>`.
- On a **dictionary**, a dot reads an entry; which names are there is the run's fact. An absent entry **refuses at the run**, unless the segment is written `?.`, which reads it as null.
- On a kind that has no fields (text, numbers, arrays, bytes, booleans, procedures), a dot **refuses at the build**: there is no name there to read, and the procedure by that spelling is reached by writing the call.
- On **`Any`**, a dot or an index **refuses at the build**. Nothing is declared here, so there is nothing for the reading to be judged against, and a dot nothing declares is the one thing a run would have to decide for itself. The type is read by naming it: `{ as: { of: <value>, type: <type> } }` says what the author expects, and every dot after it is judged against that.
- On a **type parameter** (`some T`), whose type is the call's fact, a dot **reads data**: the type is declared, at the call rather than here, so the segments stand as written and what the call filled in answers them. What the dot reaches is a type the call decides too. Dots go on standing after it, but it is **not the parameter**: `item` is the type the call filled in and `item.a` is a field of that type, which is a different unknown, and it carries none of the parameter's bound. So a name holding `item` on one way through and `item.a` on another holds neither, and one holding `item.a` twice holds one type. Which field of which parameter a walk reached is all that decides this. So `item.a` and `item?.a` are one field read twice. A mark says what is expected of the *value* and says nothing about where the walk landed. A name given to a step along the way arrives where the unbroken walk arrives (`held` holding `item.a`, then `held.b`, is `item.a.b`), and two parameters written `some T` hold one type, so the same field of either is the same field.
- **Null is not read through.** A segment reading a null, or one whose reading says it may be (`T?`), **refuses**: at the build where the text shows it, at the run otherwise. `?.` is the one spelling that expects absence on a name: it reads the null (or the absent entry) as null for the whole path, and the path's own reading is nullable for the same reason. `?[` is that same mark on an index. On an array what it expects absent is the **array itself**, never an element; on a dictionary it is the entry, as `?.` does.
- An **index past the end refuses at the run**. The array is there and says how long it is, so a reading that misses it read the length wrong. `?[` does not change this: it is `?.`'s mark on an index. It expects the **array's** absence, not the element's, so `items?[0]` reads a null array as null for the whole path, and still refuses past the end of one that arrived.
- A `?.` or `?[` that could not have read past anything (on a record's declared field, on an array the type says is there) **refuses at the build**, the way a `?` that says nothing new refuses on a type spelling. The claim of absence has to be one the types leave open.
- The **head of a path takes no mark**. A head is a name a scope holds, and there is nothing before it to read past: a name that answers nothing is a reading gone wrong, not an absence a mark can expect. `?.name` and `?[i]` written first in a path **refuse**, wherever the path is judged, and whether it was written as text or built as segments.

**A constant-headed path** is judged first like any path: the constant's settled value is its declared type, so an absent field or a needless `?.` refuses by the same rules. A procedure that value holds reads as the type its place in the value has: whole or as a field, the procedure type its expression was judged at, the constness and isolation the build derived for it included; as an element or an entry, the list's or map's one element type, which joins every element's. A call of it is judged by the parameters and answer that type writes. Then it folds at the build to the value it read, except where an index on it is a reference the run settles (`digits[ch]`, `ch` a parameter): the build binds the constant's value in the body before its first statement, and the run reads past it the way it reads any name, by the rules above. What a constant may settle from is under *what a constant settles from* in [procedures](procedure.md), and a body **its own document** declares is not among them: such a body is itself still being resolved beside the constants it may read, so a constant that runs one would be a cycle with no start, and it refuses at the build. Settling asks procedures the host answers, so a link answers them before any of the program runs. An index written as a reference (`items[i]`) is a path of its own, judged wherever the outer walk stops: it stands where an `Int` is read, so a reference reading anything else, a fraction or a value read as `Any` included, refuses at the build.

The same brackets read a **dictionary** by a key the run settles (`held[name]`), which is what walking one is for: `keys` answers the names and this reads the entry under one. What stands between the brackets is judged where an index is, and stands where a `String` is read: one reading anything else **refuses at the build**. An entry that is not there refuses at the run the way a written key does, and `?[` reads it as null. A constant written between the brackets settles at the build, a whole number to a position and text to a key, and text that is not a name **refuses at the build**. A whole number below zero is no position: one written between the brackets **refuses at the load**, and a constant settling to one **refuses at the build**. A record takes no such reading: its fields are the type's, so a name the run settles has nothing there to be judged against, and the reading **refuses at the build**.

## Cases

What `conformance/` asks about this page, by the name each case's file carries.

- `a-bracket-that-closes-nothing-in-a-path-is-refused`
- `a-cast-names-the-record-it-reads`
- `a-cast-naming-a-type-nothing-declares-refuses`
- `a-cast-naming-what-the-reading-already-is-refuses`
- `a-cast-of-a-declared-record-to-a-record-of-its-fields-refuses`
- `a-cast-of-a-list-of-nameless-records-to-a-list-of-a-declared-record-names-them`
- `a-cast-of-a-nameless-field-to-a-field-of-a-declared-record-names-it`
- `a-cast-of-a-nameless-record-to-a-declared-record-of-its-fields-names-it-answers`
- `a-cast-of-a-record-literal-names-the-nameless-record-it-holds-answers`
- `a-cast-of-a-record-literal-reads-a-whole-number-in-it-as-an-int-refuses`
- `a-cast-of-a-record-under-another-name-fails`
- `a-cast-of-a-recursive-alias-to-what-it-names-refuses`
- `a-cast-onto-a-type-parameter-refuses`
- `a-cast-onto-any-refuses`
- `a-cast-onto-never-refuses`
- `a-cast-opens-what-any-declares-nothing-about`
- `a-cast-that-does-not-match-fails`
- `a-cast-to-a-dictionary-of-a-type-parameter-refuses`
- `a-cast-to-a-list-of-a-type-parameter-refuses`
- `a-cast-to-a-list-of-an-alias-of-the-record-a-list-holds-refuses`
- `a-cast-to-a-map-of-a-declared-record-names-each-entry`
- `a-cast-to-a-procedure-type-answering-an-alias-of-what-it-answers-refuses`
- `a-closure-answers-what-it-declared`
- `a-closure-reads-a-variable-through-its-box`
- `a-closure-write-keeps-the-captured-type`
- `a-closure-writes-what-it-captured`
- `a-constant-closure-called-with-another-count-refuses`
- `a-constant-closure-called-with-another-type-refuses`
- `a-constant-closure-stands-in-a-const-slot`
- `a-constant-closure-taking-a-parameter-in-place-is-handed-a-variable`
- `a-constant-list-hands-an-element-on-at-its-element-type-refuses`
- `a-constant-read-at-an-index-the-run-settles`
- `a-constant-record-hands-a-field-on-at-its-own-type`
- `a-constant-settled-from-an-answer-of-any-reads-its-fields`
- `a-constant-that-runs-a-body-of-its-own-document-refuses`
- `a-dictionary-is-read-by-a-key-the-run-settles`
- `a-dictionary-key-that-is-not-text-refuses`
- `a-dictionary-read-at-a-constant-key-reads-the-entry`
- `a-dot-on-a-type-with-no-fields-is-refused`
- `a-dot-on-any-is-refused`
- `a-dot-through-a-null-the-text-shows-refuses`
- `a-key-reference-read-as-any-refuses`
- `a-mapping-with-no-tag-refuses`
- `a-mapping-with-two-form-keys-refuses`
- `a-mark-does-not-split-the-field-it-reached`
- `a-marked-head-is-refused`
- `a-named-step-arrives-where-the-walk-arrives`
- `a-path-reads-through-what-a-name-holds`
- `a-read-at-a-constant-index-below-zero-refuses`
- `a-read-at-a-constant-key-that-is-not-a-name-refuses`
- `a-read-at-an-index-below-zero-refuses`
- `a-record-field-may-carry-a-tags-name`
- `a-record-read-by-a-key-the-run-settles-refuses`
- `a-write-at-a-constant-index-below-zero-refuses`
- `a-write-at-an-index-below-zero-refuses`
- `an-absent-dictionary-entry-refuses`
- `an-asking-cast-of-a-declared-record-read-as-any-to-an-inline-record-reads-null`
- `an-index-into-any-is-refused`
- `an-index-past-the-end-refuses`
- `an-index-reference-read-as-a-fraction-refuses`
- `an-index-reference-read-as-any-refuses`
- `an-index-reference-read-as-text-refuses`
- `an-optional-bracket-reads-an-absent-entry-as-null`
- `an-optional-cast-to-a-list-of-a-type-parameter-refuses`
- `an-optional-dot-on-a-field-that-is-there-refuses`
- `an-optional-segment-reads-absence-as-null`
- `an-unclosed-bracket-in-a-path-is-refused`
- `an-undeclared-field-refuses`
- `indexing-what-may-be-null-takes-the-optional-bracket`
- `reading-what-may-be-null-takes-the-optional-dot`
- `the-asking-cast-reads-a-mismatch-as-null`
- `the-asking-cast-reads-another-name-as-null`
- `the-optional-bracket-answers-null-for-the-null`
- `the-optional-bracket-on-an-array-that-is-there-is-refused`
- `the-optional-bracket-reads-through-a-nullable`
- `the-optional-bracket-still-refuses-past-the-end`
- `the-optional-dot-reads-through-a-nullable`
- `two-parameters-of-one-type-parameter-hold-one-type`
