# Expressions

What is read rather than run. A literal, a name, a path through one, a cast, a struct, a map, an array, a call and a closure written where a value is wanted. The line between this page and [statements](statement.md) is the line an operand stands on: a construct runs a body and is refused here.

A scalar is itself, a literal. A string is always literal text; nothing inside it is ever re-parsed. An array is an array of expressions. A mapping is an expression by its **one key**, and that key is one of these:

| form | means |
|---|---|
| `{ ref: a.b[0] }` | a name, resolved in the scope that reads it |
| `{ struct: { … } }` | a struct of the declared struct the place it is written into reads, under *a declared struct is nominal* in [types](type.md), its fields each an expression, made in the order of their names. A field may be called anything, `ref` and `value` included |
| `{ dictionary: [[<key>, <value>], …] }` | a map, its entries each a list of two expressions, a key and a value. The entries are made in the order written, so a key written twice holds the later value. The keys join to one type and the values to another, the way a list literal's elements do, an empty one holding `Never` at both; written where a map type is declared, every key and value is held to it part by part. An entry that is not a list of two **refuses at the load** |
| `{ call: <call> }` | a call where a value is wanted; same grammar as the `call` construct |
| `{ closure: <procedure> }` | a procedure written where a value is wanted; same grammar as a procedure, without `access`, a bound and `sameTypes`: nothing names a closure, and its `some T` is the `T` of the procedure it is written in, which says what bounds it and what its associated types are. A closure writing any of them, a bound beside a `some T` included, **refuses at the load** |
| `{ as: { of: <value>, type: <type> } }` | read the value as that type: how a value the build could not type, one read as `Any` or as a contract, is held to one |
| `{ as?: { of: <value>, type: <type> } }` | the same, reading a mismatch as null rather than failing; the answer is `T?` |

A mapping with another key, or with more than one, **refuses at the load**. A key names a form and never a field, so no field name is reserved.

A path is a name, then `.name` for a field and `[…]` for what a list or a map holds. Between the brackets stands a whole number, written in decimal with no leading zero and a `-` only below zero, a text between double quotes, or a path of its own, and nothing around it; inside the quotes `\"` is a quote, `\\` a backslash and every other character itself, so each text has one spelling. A `[` left open, a `]` that closes none, a text left open, or a backslash before anything but a quote or a backslash **refuses at the load**, and so does a path spelled any other way, `a[01]`, `a[+1]`, `a[ 1 ]` or `a[${i}]`, as a second spelling of one path.

A **cast** names the type a value is read as. The type is written the way any type is, as a string. From the cast on, the reading *is* that type, so every dot after it is judged against it; the run is left the one question the build cannot answer, which is what actually arrived, and it answers it by judging the value against the type, leaving nothing out. A cast is how a value read as `Any` or as a contract reaches a slot of a type, since the build does not know which type it is. A plain `as` **fails at the run** with `cast_refused` when the value is not that type. It is a failure like any other, so an `attempt` catches it, and `as?` reads that mismatch as null, which is the author saying they expected it.

A cast whose operand, read on its own, already **is** the type it names refuses at the build, the way a needless `?.` does: the claim says nothing. The test is sameness, not admission: a reading of `Int?` cast to `Int` names something the types leave open, and only the run can say whether it holds. The type a cast names is a place a literal in its operand is written into, as a slot is, under [types](type.md): a struct literal there is read as the declared struct the type names, and a whole literal as the fraction it names where the type declares a `Double`, at every depth, so `[1] as Array<Double>` answers `[1.0]`. On its own a literal is read as written, and a struct literal as no struct at all, so a cast that is a literal's place is needless only where the literal already is the type, as `1 as Int` is. A cast writes no name onto a value and never takes one away: a declared struct shares its values with itself alone, so a reading of one cast to another declared struct or to a map, and a reading of a map cast to a declared struct, each name a type no value they read is, null aside where both take it, and **refuse at the build**, and a map arriving where a cast reads a declared struct from a reading of `Any` or of a contract is no value of it, so the cast fails with `cast_refused` and `as?` reads it as null. A cast onto `Any` or `Never` refuses at the build for the other half of the same reason: those name no type to read. A type parameter written anywhere inside a cast's type (`Array<some T>`) **refuses at the load** as it does on a name saying what it holds: nothing in a body fills one, so there is no type there to judge what arrives against.

A cast that names a type nothing declares **refuses at the build**, wherever it is written, by the rule every type spelling is held to. `as?` reads a value that is not the named type as null; it does not read a name that names nothing as null, because that is the declaration being wrong rather than the value.

A construct's key, `conditional` or `loop`, is read under a statement's `value` and nowhere else, under [statements](statement.md).

**A dot reads a name and nothing else.** Every `ref` path is judged where names resolve, and the judgement is written into the image; the value that arrives at run time has no say in it. A procedure is sent with a written `call`, which spells the declaration it means. Segment by segment:

- On a **struct type**, a dot reads the field the type declares. A field it does not declare **refuses at the build**, `?.` or not. The type rules the field out, and no spelling reads past that. A procedure on a struct is written as a call. A struct type says which fields there are, and a value fits it only with exactly them, so there is nothing else to reach.
- On a type that has no fields (`String`, `Int`, `Double`, `Bool`, a list, a map, a procedure), a dot **refuses at the build**: there is no name there to read. The procedure by that spelling is reached by writing the call, and what a list or a map holds through brackets.
- On **`Any`**, a dot or an index **refuses at the build**. Nothing is declared here, so there is nothing for the reading to be judged against, and a dot nothing declares is the one thing a run would have to decide for itself. The type is read by naming it: `{ as: { of: <value>, type: <type> } }` says what the author expects, and every dot after it is judged against that.
- On a **type parameter** (`some T`), or an associated type, a dot or an index **refuses at the build** as on `Any`. The parameter is one type the body does not know, so nothing is declared here for a reading to be judged against. What a type gives is asked through a contract it answers, under [types](type.md).
- **Null is not read through.** A segment reading a null, or one whose reading says it may be (`T?`), **refuses**: at the build where the text shows it, at the run otherwise. `?.` is the one spelling that expects absence on a name: it reads the null as null for the whole path, and the path's own reading is nullable for the same reason. `?[` is that same mark on brackets. On a list what it expects absent is the **list itself**, never an element; on a map it is the map or the entry.
- An **index past the end refuses at the run**. The array is there and says how long it is, so a reading that misses it read the length wrong. `?[` does not change this: it is `?.`'s mark on an index. It expects the **array's** absence, not the element's, so `items?[0]` reads a null array as null for the whole path, and still refuses past the end of one that arrived. Digits between the brackets are a whole number however many there are, and never a name, so one past what an `Int` holds **refuses at the load**. On a list a whole number below zero is no position: one written or settled between the brackets **refuses at the build**, and one the run reads refuses at the run as a position past the end does.
- A `?.` or `?[` that could not have read past anything (on a struct's declared field, on an array the type says is there) **refuses at the build**, the way a `?` that says nothing new refuses on a type spelling. The claim of absence has to be one the types leave open.
- The **head of a path takes no mark**. A head is a name a scope holds, and there is nothing before it to read past: a name that answers nothing is a reading gone wrong, not an absence a mark can expect. `?.name` and `?[i]` written first in a path **refuse at the load**, wherever the path is judged, and whether it was written as text or built as segments.

**A constant-headed path**, one whose head names a constant of its document rather than a name a body introduced under that spelling, is judged first like any path: the constant's settled value is its declared type, so an absent field or a needless `?.` refuses by the same rules, and the path reads as the type its place in that type has: a field its own, and an element or an entry the list's or map's one element type, which joins every element's, so `k[0]` of `[1, "s"]` reads `Any`. A procedure the value holds, whole or as a field, reads as the procedure type its expression was judged at, the constness, isolation and failing its signature declares included. A call of it is judged by the parameters and answer that type writes. Then it folds at the build to the value it read, except where an index on it is a reference the run reads (`digits[ch]`, `ch` a parameter): there the run reads the constant's value past the index the way it reads any name, by the rules above. What a constant may settle from is under *what a constant settles from* in [procedures](procedure.md), and a body **its own document** declares is not among them: such a body is itself still being resolved beside the constants it may read, so a constant that runs one would be a cycle with no start, and it refuses at the build. Settling asks the procedures this specification names, which the host answers, so a link answers them before any of the program runs.

**Brackets read what a list or a map holds** at the value between them, judged against what is indexed: on a list it stands where an `Int` is read, a position, and on a map where the map's key type is read, a key. So `d[3]` on `Dictionary<Int, String>` reads the entry under `3`, `d["a"]` on `Dictionary<String, Int>` the entry under `"a"`, and `d[k]` the entry under what `k` holds; a key finds the entry under the key that is the same value, under [values](value.md). A value written there is a literal, read as that place reads it under [types](type.md), and one of another type than is read there **refuses at the build**, and so does a path there reading another type, a fraction or a value read as `Any` included. A path between the brackets is a path of its own, judged as one even where the outer walk stops, and one level deeper than the path around it, the levels counting on from the containers around the path's string against the bound a document's nesting has under [encoding](encoding.md), so a path past it **refuses at the load**; past a type parameter what it reads is judged at the run against what arrived, as a dot there is: a list refuses what is no position, and a map holds no entry under a key of another type. Brackets on any other type, a declared struct among them, **refuse at the build**: a struct's fields are its type's, read by a dot. An entry the map does not hold refuses at the run, and `?[` reads it as null. A constant written between the brackets settles at the build to the value it reads and is judged at the type it holds, as a path there is.

## Cases

What `conformance/` asks about this page, by the name each case's file carries.

- `a-backslash-before-what-it-does-not-escape-refuses`
- `a-bracket-that-closes-nothing-in-a-path-is-refused`
- `a-cast-from-any-to-a-struct-naming-itself-answers`
- `a-cast-naming-a-type-nothing-declares-refuses`
- `a-cast-naming-what-the-reading-already-is-refuses`
- `a-cast-of-a-map-to-a-declared-struct-refuses`
- `a-cast-of-a-struct-under-another-name-fails`
- `a-cast-onto-a-type-parameter-refuses`
- `a-cast-onto-any-refuses`
- `a-cast-onto-never-refuses`
- `a-cast-opens-what-any-declares-nothing-about`
- `a-cast-that-does-not-match-fails`
- `a-cast-to-a-dictionary-of-a-type-parameter-refuses`
- `a-cast-to-a-list-of-a-type-parameter-refuses`
- `a-cast-to-a-list-of-an-alias-of-the-struct-a-list-holds-refuses`
- `a-cast-to-a-procedure-type-answering-an-alias-of-what-it-answers-refuses`
- `a-cast-writes-a-whole-literal-it-reads-as-the-fraction-its-type-names-answers`
- `a-closure-answers-what-it-declared`
- `a-closure-reads-a-variable-through-its-box`
- `a-closure-write-keeps-the-captured-type`
- `a-closure-writes-what-it-captured`
- `a-closure-writing-access-refuses`
- `a-constant-between-the-brackets-settles-to-a-key-of-its-type`
- `a-constant-closure-called-with-another-count-refuses`
- `a-constant-closure-called-with-another-type-refuses`
- `a-constant-closure-stands-in-a-const-slot`
- `a-constant-closure-taking-a-parameter-in-place-is-handed-a-variable`
- `a-constant-list-hands-an-element-on-at-its-element-type-refuses`
- `a-constant-read-at-an-index-the-run-reads`
- `a-constant-settled-from-an-answer-of-any-reads-its-fields`
- `a-constant-struct-hands-a-field-on-at-its-own-type`
- `a-constant-that-runs-a-body-of-its-own-document-refuses`
- `a-dictionary-is-read-by-a-key-the-run-reads`
- `a-dictionary-read-at-a-constant-key-reads-the-entry`
- `a-dot-on-a-map-refuses`
- `a-dot-on-a-type-parameter-refuses`
- `a-dot-on-a-type-with-no-fields-is-refused`
- `a-dot-on-any-is-refused`
- `a-dot-through-a-null-the-text-shows-refuses`
- `a-key-reference-of-another-type-than-the-key-refuses`
- `a-key-reference-read-as-any-refuses`
- `a-key-written-between-the-brackets-of-another-type-than-the-key-refuses`
- `a-map-keyed-by-whole-numbers-reads-a-key-between-the-brackets`
- `a-map-keyed-by-whole-numbers-reads-a-key-the-run-reads`
- `a-map-literal-makes-its-entries-in-order`
- `a-map-literal-writing-a-key-the-run-reads-twice-holds-the-later-value`
- `a-map-literal-written-where-a-map-is-declared-is-held-part-by-part-refuses`
- `a-mapping-with-no-tag-refuses`
- `a-mapping-with-two-form-keys-refuses`
- `a-marked-head-is-refused`
- `a-path-headed-by-a-name-under-a-constants-spelling-reads-the-name`
- `a-path-nested-past-the-bound-refuses`
- `a-path-nested-to-the-bound-is-read`
- `a-path-reads-through-what-a-name-holds`
- `a-quoted-key-holds-what-a-path-is-spelled-with`
- `a-quoted-text-between-the-brackets-reads-an-entry`
- `a-read-at-a-constant-index-below-zero-refuses`
- `a-read-at-an-index-below-zero-refuses`
- `a-struct-field-may-carry-a-tags-name`
- `a-struct-literal-a-cast-reads-is-the-struct-the-cast-names-answers`
- `a-struct-literals-fields-are-made-in-the-order-of-their-names`
- `a-struct-read-by-a-key-the-run-reads-refuses`
- `a-text-left-open-between-the-brackets-refuses`
- `a-whole-number-below-zero-is-a-key-of-a-map`
- `a-write-at-a-constant-index-below-zero-refuses`
- `a-write-at-an-index-below-zero-refuses`
- `an-absent-dictionary-entry-refuses`
- `an-element-of-a-constant-list-reads-as-its-element-type-refuses`
- `an-element-of-a-constant-struct-field-reads-as-its-element-type-refuses`
- `an-empty-map-literal-is-a-map-of-any-types`
- `an-index-into-a-type-parameter-refuses`
- `an-index-into-any-is-refused`
- `an-index-past-the-end-refuses`
- `an-index-past-what-an-int-holds-refuses`
- `an-index-read-by-a-name-under-a-constants-spelling-reads-the-name`
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
- `the-empty-text-is-a-key`
- `the-optional-bracket-answers-null-for-the-null`
- `the-optional-bracket-on-an-array-that-is-there-is-refused`
- `the-optional-bracket-reads-through-a-nullable`
- `the-optional-bracket-still-refuses-past-the-end`
- `the-optional-dot-reads-through-a-nullable`
