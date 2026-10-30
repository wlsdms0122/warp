# Expressions

What is read rather than run. A literal, a name, a path through one, a cast, a struct, a dictionary, an array, a call and a closure written where a value is wanted. The line between this page and [statements](STATEMENT.md) is the line an operand stands on: a construct runs a body and is refused here.

A scalar is itself, a literal. A string is always literal text; nothing inside it is ever re-parsed. An array is an array of expressions. A mapping is an expression by its **one key**, and that key is one of these:

| form | means |
|---|---|
| `{ ref: a.b[0] }` | a name, resolved in the scope that reads it |
| `{ struct: { … } }` | a struct of the declared struct the place it is written into reads, under *a declared struct is nominal* in [types](TYPE.md), its fields each an expression, made in the order of their names. A field may be called anything, `ref` and `value` included |
| `{ dictionary: [[<key>, <value>], …] }` | a dictionary, its entries each a list of two expressions, a key and a value. The entries are made in the order written, so a key written twice holds the later value. The keys join to one type and the values to another, the way a list literal's elements do, an empty one holding `Never` at both; written where a dictionary type is declared, every key and value is held to it part by part. An entry that is not a list of two **refuses at the load** |
| `{ call: <call> }` | a call where a value is wanted, under *calls* in [statements](STATEMENT.md) |
| `{ closure: <procedure> }` | a procedure written where a value is wanted; same grammar as a procedure, without `access`, a bound and `sameTypes`: nothing names a closure, and its `some T` is the `T` of the procedure it is written in, which says what bounds it and what its associated types are. A closure writing any of them, a bound beside a `some T` included, **refuses at the load** |
| `{ as: { of: <value>, type: <type> } }` | read the value as that type: how a value the build could not type, one read as `Any` or as a contract, is held to one |
| `{ as?: { of: <value>, type: <type> } }` | the same, reading a mismatch as the none rather than failing; the result is exactly `T?`, so a match is its some, and a match that is `null` or a `Some` is a `Some` holding it |

A mapping with another key, or with more than one, **refuses at the load**. A key names a form and never a field, so no field name is reserved.

A path is a name, then `.name` for a field and `[…]` for what a list or a dictionary holds. Between the brackets stands an integer literal, written in decimal with no leading zero and a `-` only below zero, a string between double quotes, or a path of its own, and nothing around it; inside the quotes `\"` is a quote, `\\` a backslash and every other character itself, so each string has one spelling. A `[` left open, a `]` that closes none, a string left open, or a backslash before anything but a quote or a backslash **refuses at the load**, and so does a path spelled any other way, `a[01]`, `a[+1]` or `a[ 1 ]`, as a second spelling of one path.

A **cast** names the type a value is read as. The type is written the way any type is, as a string. From the cast on, the reading *is* that type, so every dot after it is judged against it; the run is left the one question the build cannot decide, which is what actually arrived, and it decides it by judging the value against the type, leaving nothing out. A cast is how a value read as `Any` or as a contract reaches a slot of a type, since the build does not know which type it is. A plain `as` **fails at the run** with `cast_refused` when the value is not that type. It is a failure like any other, so a `try` catches it, and `as?` reads that mismatch as the none, which is the author saying they expected it. A cast takes no level off an Optional: a `Some` holding `null` is no value of `Int?`, so cast to `Int?` it fails.

A cast whose operand, read on its own, already **is** the type it names refuses at the build, the way a needless `?.` does: the claim says nothing. So does a cast to a type that takes what its operand reads and takes the reading, or any part of it, an Optional's payload, a list's element or a dictionary's key or value at any depth, as an Optional's some: the reading stands there by promotion, and a name declared at that type says it, so `x as Int??` of an `x` read as `Int?` refuses, and so does `xs as Array<Int??>` of an `xs` read as `Array<Int?>`. The test is sameness, not admission: a reading of `Int?` cast to `Int` names something the types leave open, and only the run can say whether it holds. The type a cast names is a place a literal in its operand is written into, as a slot is, under [types](TYPE.md): a struct literal there is read as the declared struct the type names, and an integer literal as the `Double` it names where the type declares a `Double`, at every depth, so `[1] as Array<Double>` is `[1.0]`. On its own a literal is read as written, and a struct literal as no struct at all, so a cast that is a literal's place is needless only where the literal, read as written, already is the type or stands there by promotion, as `1 as Int` and `[1] as Array<Int?>` do. A cast writes no name onto a value and never takes one away: a declared struct shares its values with itself alone, so a reading of one cast to another declared struct or to a dictionary, and a reading of a dictionary cast to a declared struct, each name a type no value they read is, and **refuse at the build**. Between the Optionals of two declared structs the none is a value of both, so such a cast stands, and `as?` reads a value of the other as the none. A dictionary arriving where a cast reads a declared struct from a reading of `Any` or of a contract is no value of it, so the cast fails with `cast_refused` and `as?` reads it as the none. A cast onto `Any` or `Never` refuses at the build for the other half of the same reason: those name no type to read. A type parameter of the procedure the cast stands in, written anywhere inside its type (`Array<some T>`), reads as the call filled it, as it does on a name saying what it holds, so the run judges what arrives against the type the call filled; one the procedure does not declare **refuses at the load**.

A cast that names a type nothing declares **refuses at the build**, wherever it is written, by the rule every type spelling is held to. `as?` reads a value that is not the named type as null; it does not read a name that names nothing as null, because that is the declaration being wrong rather than the value.

A construct's key is read under a statement's `value` and nowhere else, under [statements](STATEMENT.md).

**A dot reads a name and nothing else.** Every `ref` path is judged where names resolve, and the judgement is written into the image; the value that arrives at run time has no say in it. A procedure is sent with a written `call`, which spells the declaration it means. Segment by segment:

- On a **struct type**, a dot reads the field the type declares. A field it does not declare **refuses at the build**, `?.` or not. The type rules the field out, and no spelling reads past that. A procedure on a struct is written as a call. A struct type says which fields there are, and a value fits it only with exactly them, so there is nothing else to reach.
- On a type that has no fields (`String`, `Int`, `Double`, `Bool`, a list, a dictionary, a procedure), a dot **refuses at the build**: there is no name there to read. The procedure by that spelling is reached by writing the call, and what a list or a dictionary holds through brackets.
- On **`Any`**, a dot or an index **refuses at the build**. Nothing is declared here, so there is nothing for the reading to be judged against, and a dot nothing declares is the one thing a run would have to decide for itself. The type is read by naming it: `{ as: { of: <value>, type: <type> } }` says what the author expects, and every dot after it is judged against that.
- On a **type parameter** (`some T`), or an associated type, a dot or an index **refuses at the build** as on `Any`. The parameter is one type the body does not know, so nothing is declared here for a reading to be judged against. What a type gives is asked through a contract it conforms to, under [types](TYPE.md).
- **Null is not read through.** A segment reading a null, or one whose reading is an Optional (`T?`), **refuses**: at the build where the text shows it, at the run otherwise. `?.` is the one spelling that expects absence on a name: it reads past every level of an Optional, and reads a none at any level as null for the whole path. A path whose last step reads an Optional reads that Optional, and one whose last step reads no Optional reads its Optional; where that last reading is no Optional and may hold a none, the value the path finds is the Optional's some unless a marked step met a none, so `o?.v` on a field read as `Any` is `Some` holding `null` where the field holds a none, and the none where `o` is absent. `?[` is that same mark on brackets. On a list what it expects absent is the **list itself**, never an element; on a dictionary it is the dictionary or the entry, and the step reads the entry as the Optional of the dictionary's value type exactly, and that Optional is what the path's last step reads: the none where the dictionary holds no entry, and the entry's some where it does, so on `Dictionary<String, Int?>` an absent key reads `null` and a present `null` reads `Some` holding it.
- An **index past the end refuses at the run**. The array is there and says how long it is, so a reading that misses it read the length wrong. `?[` does not change this: it is `?.`'s mark on an index. It expects the **array's** absence, not the element's, so `items?[0]` reads the none of `items` as null for the whole path, and refuses past the end of one that arrived. Digits between the brackets are an integer however many there are, and never a name, so one past what an `Int` holds **refuses at the load**. On a list an integer below zero is no position: one written or folded between the brackets **refuses at the build**, and one the run reads refuses at the run as a position past the end does.
- A `?.` or `?[` that could not have read past anything (on a struct's declared field, on an array the type says is there) **refuses at the build**. The claim of absence has to be one the types leave open.
- The **head of a path takes no mark**. A head is a name a scope holds, and there is nothing before it to read past: a name that names nothing is a reading gone wrong, not an absence a mark can expect. `?.name` and `?[i]` written first in a path **refuse at the load**, wherever the path is judged, and whether it was written as text or built as segments.

**A constant-headed path**, one whose head names a constant of its document rather than a name a body introduced under that spelling, is judged first like any path: the constant's type is its folded value's, so an absent field or a needless `?.` refuses by the same rules, and the path reads as the type its place in that type has: a field its own, and an element or an entry the list's or dictionary's one element type, which joins every element's, so `k[0]` of `[1, "s"]` reads `Any`. A procedure the value holds, whole or as a field, reads as the procedure type its expression was judged at, the constness, isolation and failing its signature declares included. A call of it is judged by the parameters and return type that type writes. Then it folds at the build to the value it read, except where an index on it is a reference the run reads (`digits[ch]`, `ch` a parameter): there the run reads the constant's value past the index the way it reads any name, by the rules above. What a constant may fold from is under *what a constant folds from* in [procedures](PROCEDURE.md), and a body **its own document** declares is not among them: such a body is itself still being resolved beside the constants it may read, so a constant that runs one would be a cycle with no start, and it refuses at the build. Folding asks the procedures this specification names, which every implementation brings, the builtin ones as native procedures and the rest written in Warp in `lib/standard`, so a link provides them before any of the program runs.

**Brackets read what a list or a dictionary holds** at the value between them, judged against what is indexed: on a list it stands where an `Int` is read, a position, and on a dictionary where the dictionary's key type is read, a key. So `d[3]` on `Dictionary<Int, String>` reads the entry under `3`, `d["a"]` on `Dictionary<String, Int>` the entry under `"a"`, and `d[k]` the entry under what `k` holds; a key finds the entry under the key that is the same value, under [values](VALUE.md). A value written there is a literal, read as that place reads it under [types](TYPE.md), and one of another type than is read there **refuses at the build**, and so does a path there reading another type, a `Double`, a value read as `Any` and a type parameter included: a type parameter stands only between the brackets of a dictionary keyed by that same parameter. A path between the brackets is a path of its own, judged as one even where the outer walk stops, and one level deeper than the path around it, the levels counting on from the containers around the path's string against the bound a document's nesting has under [encoding](ENCODING.md), so a path past it **refuses at the load**. Brackets on any other type, a declared struct among them, **refuse at the build**: a struct's fields are its type's, read by a dot. An entry the dictionary does not hold refuses at the run, and `?[` reads it as the none. A constant written between the brackets folds at the build to the value it reads and is judged at the type it holds, as a path there is.

## Cases

What `conformance/` asks about this page, by the name each case's file carries.

- `a-backslash-before-what-it-does-not-escape-refuses`
- `a-bracket-that-closes-nothing-in-a-path-refuses`
- `a-cast-from-any-to-a-struct-naming-itself`
- `a-cast-naming-a-type-nothing-declares-refuses`
- `a-cast-naming-what-the-reading-already-is-refuses`
- `a-cast-of-a-dictionary-to-a-declared-struct-refuses`
- `a-cast-of-a-dictionary-to-a-dictionary-of-the-optional-of-its-value-refuses`
- `a-cast-of-a-list-literal-to-a-list-of-the-optional-of-its-element-refuses`
- `a-cast-of-a-list-to-a-list-of-the-optional-of-its-element-refuses`
- `a-cast-of-a-struct-under-another-name-fails`
- `a-cast-onto-any-refuses`
- `a-cast-onto-never-refuses`
- `a-cast-opens-what-any-declares-nothing-about`
- `a-cast-that-does-not-match-fails`
- `a-cast-to-a-list-of-a-type-parameter-fails-where-what-arrives-is-not-what-the-call-filled`
- `a-cast-to-a-list-of-a-type-parameter-reads-it-as-the-call-filled-it`
- `a-cast-to-a-list-of-an-alias-of-the-struct-a-list-holds-refuses`
- `a-cast-to-a-procedure-type-returning-an-alias-of-what-it-returns-refuses`
- `a-cast-to-an-associated-type-reads-it-as-the-call-filled-it`
- `a-cast-to-an-optional-does-not-take-a-level-off-fails`
- `a-cast-to-an-optional-of-what-its-operand-reads-refuses`
- `a-cast-writes-an-integer-literal-it-reads-as-the-double-its-type-names`
- `a-closure-reads-a-variable-through-its-box`
- `a-closure-writes-what-it-captured`
- `a-closure-writing-access-refuses`
- `a-closures-return-value-its-returns-does-not-take-refuses`
- `a-closures-write-of-another-type-into-what-it-captured-refuses`
- `a-constant-between-the-brackets-folds-to-a-key-of-its-type`
- `a-constant-closure-called-with-another-count-refuses`
- `a-constant-closure-called-with-another-type-refuses`
- `a-constant-closure-stands-in-a-const-slot`
- `a-constant-closure-taking-a-parameter-in-place-is-handed-a-variable`
- `a-constant-folded-from-a-call-returning-any-reads-its-fields`
- `a-constant-list-hands-an-element-on-at-its-element-type-refuses`
- `a-constant-read-at-an-index-the-run-reads`
- `a-constant-struct-hands-a-field-on-at-its-own-type`
- `a-constant-that-runs-a-body-of-its-own-document-refuses`
- `a-dictionary-is-read-by-a-key-the-run-reads`
- `a-dictionary-keyed-by-ints-reads-a-key-between-the-brackets`
- `a-dictionary-keyed-by-ints-reads-a-key-the-run-reads`
- `a-dictionary-literal-entry-of-one-expression-refuses`
- `a-dictionary-literal-entry-of-three-expressions-refuses`
- `a-dictionary-literal-entry-that-is-not-a-list-refuses`
- `a-dictionary-literal-makes-its-entries-in-order`
- `a-dictionary-literal-writing-a-key-the-run-reads-twice-holds-the-later-value`
- `a-dictionary-literal-written-where-a-dictionary-is-declared-is-held-part-by-part-refuses`
- `a-dictionary-read-at-a-constant-key-reads-the-entry`
- `a-dot-on-a-dictionary-refuses`
- `a-dot-on-a-type-parameter-refuses`
- `a-dot-on-a-type-with-no-fields-refuses`
- `a-dot-on-any-refuses`
- `a-dot-through-a-null-the-text-shows-refuses`
- `a-key-read-as-the-type-parameter-a-dictionary-is-keyed-by-reads-its-entry`
- `a-key-reference-of-another-type-than-the-key-refuses`
- `a-key-reference-read-as-any-refuses`
- `a-key-written-between-the-brackets-of-another-type-than-the-key-refuses`
- `a-mapping-with-no-tag-refuses`
- `a-mapping-with-two-form-keys-refuses`
- `a-marked-head-refuses`
- `a-none-held-as-any-cast-to-an-optional-is-its-none`
- `a-path-headed-by-a-name-under-a-constants-spelling-reads-the-name`
- `a-path-nested-past-the-bound-refuses`
- `a-path-nested-to-the-bound-is-read`
- `a-path-reads-through-what-a-name-holds`
- `a-quoted-key-holds-what-a-path-is-spelled-with`
- `a-quoted-string-between-the-brackets-reads-an-entry`
- `a-read-at-a-constant-index-below-zero-refuses`
- `a-read-at-an-index-below-zero-refuses`
- `a-some-of-a-none-held-as-any-cast-to-a-contract-reaches-the-optionals-row`
- `a-some-of-a-none-held-as-any-cast-to-an-optional-of-an-optional-holds`
- `a-string-left-open-between-the-brackets-refuses`
- `a-struct-field-may-carry-a-tags-name`
- `a-struct-literal-a-cast-reads-is-the-struct-the-cast-names`
- `a-struct-literals-fields-are-made-in-the-order-of-their-names`
- `a-struct-read-by-a-key-the-run-reads-refuses`
- `a-write-at-a-constant-index-below-zero-refuses`
- `a-write-at-an-index-below-zero-refuses`
- `a-zero-between-the-brackets-written-with-a-minus-refuses`
- `an-absent-dictionary-entry-refuses`
- `an-asking-cast-to-a-list-of-an-associated-type-reads-it-as-the-call-filled-it`
- `an-asking-cast-to-an-associated-type-reads-it-as-the-call-filled-it`
- `an-asking-cast-to-an-optional-tells-a-mismatch-from-a-none`
- `an-asking-cast-to-null-reads-a-match-as-its-some`
- `an-element-of-a-constant-list-reads-as-its-element-type-refuses`
- `an-element-of-a-constant-struct-field-reads-as-its-element-type-refuses`
- `an-empty-dictionary-literal-is-a-dictionary-of-any-types`
- `an-index-into-a-type-parameter-refuses`
- `an-index-into-any-refuses`
- `an-index-past-the-end-refuses`
- `an-index-past-what-an-int-holds-refuses`
- `an-index-read-by-a-name-under-a-constants-spelling-reads-the-name`
- `an-index-reference-read-as-a-double-refuses`
- `an-index-reference-read-as-a-type-parameter-refuses`
- `an-index-reference-read-as-any-refuses`
- `an-index-reference-read-as-string-refuses`
- `an-int-below-zero-is-a-key-of-a-dictionary`
- `an-integer-between-the-brackets-with-a-leading-zero-refuses`
- `an-integer-between-the-brackets-written-with-a-plus-refuses`
- `an-optional-bracket-reads-an-absent-entry-as-null`
- `an-optional-dot-ending-at-a-field-that-may-hold-a-none-reads-it-as-its-some`
- `an-optional-dot-on-a-field-that-is-there-refuses`
- `an-optional-dot-reads-past-every-level`
- `an-optional-segment-reads-absence-as-null`
- `an-unclosed-bracket-in-a-path-refuses`
- `an-undeclared-field-refuses`
- `indexing-an-optional-without-the-optional-bracket-refuses`
- `null-asked-as-an-optional-is-its-inner-none`
- `reading-an-optional-without-the-optional-dot-refuses`
- `the-asking-cast-reads-a-mismatch-as-null`
- `the-asking-cast-reads-another-name-as-null`
- `the-empty-string-is-a-key`
- `the-optional-bracket-on-an-array-that-is-there-refuses`
- `the-optional-bracket-past-the-end-refuses`
- `the-optional-bracket-reads-null-for-the-null`
- `the-optional-bracket-reads-through-an-optional`
- `the-optional-bracket-tells-an-absent-entry-from-a-none-it-holds`
- `the-optional-dot-reads-through-an-optional`
- `white-space-around-what-the-brackets-hold-refuses`
