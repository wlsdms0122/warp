# The standard vocabulary

The procedures every implementation brings, what each answers, and which of them an implementation has to write in its own language rather than take from `lib/standard`. This is the layer a program does its work in: the language has no arithmetic, no comparison and no collections of its own, and a program that is granted none of these can compute nothing.

Seven bundles, each taken with what it depends on, so a host grants what its programs have use for and no more. What a bundle depends on is what its written half sends and what its signatures mention, and the written half's `imports` is the list. `Standard` is the shared ground: the contracts `Standard.Numeric`, `Standard.Comparable` and `Standard.Collection`, the claims putting the types the language names under them, and the procedures answering those claims. Every bundle below links with `Standard` in the link, and a document calling a contract's procedure stands behind it, so what answers the call stands before the document does. A contract and a bundle may share a spelling: `Standard.Collection.count` is the contract `Standard.Collection`'s procedure, declared by `Standard`, and the bundle `Standard.Collection` is the bundle whose procedures the table lists in its row. Beyond that, `Standard.Math`, `Standard.Logic` and `Standard.Control` stand alone; `Standard.Collection` links with `Standard.Logic`; `Standard.Concurrent` with `Standard.Collection`; `Standard.Text` with `Standard.Collection`, `Standard.Control` and `Standard.Logic`. Two bundles that send to each other are not a cycle, because a bundle is not a module, below:

| module | procedures |
|---|---|
| `Standard` | The contracts below, answered for the types the language names: `Int.plus` `Int.minus` `Int.times` `Int.dividedBy` `Int.remainder` `Int.lessThan`, the same six for `Double`, `String.lessThan`, and `Array.count` `Dictionary.count` `String.count` |
| `Standard.Logic` | `equal` `notEqual` `not` `and` `or` `select` `tryAnd` `tryOr` `trySelect` |
| `Standard.Math` | `min` `max` `absolute` `floored` `rounded` `greaterThan` |
| `Standard.Text` | `text` `characters` `contains` `startsWith` `uppercased` `lowercased` `trimmed` `split` `joined` `replacing` `decoded` `encoded` |
| `Standard.Collection` | `append` `contains` `first` `last` `reversed` `appending` `prepending` `gathering` `dropFirst` `dropLast` `sorted` `map` `filter` `reduce` `tryMap` `tryFilter` `tryReduce` `keys` `values` `setting` |
| `Standard.Control` | `abort`. Declared `returns: Never` |
| `Standard.Concurrent` | `all` `allKeyed` `first` `firstKeyed` `map`. Run closures at once |

## What an implementation must write

Not all of these. Most are written in Warp, from a small set that cannot be: **builtin**. An implementation writes the builtin procedures in its own language and takes the rest as a Warp module, the way any other module arrives.

| bundle | builtin |
|---|---|
| `Standard` | every member it gives: arithmetic, ordering and counting for each type it claims a contract for |
| `Standard.Logic` | `equal` |
| `Standard.Math` | `floored` `rounded` |
| `Standard.Text` | `text` `joined` `characters` `uppercased` `lowercased` `encoded` `decoded` `trimmed` |
| `Standard.Collection` | `appending` `gathering` `keys` `setting` |
| `Standard.Control` | `abort` |
| `Standard.Concurrent` | `all` `allKeyed` `first` `firstKeyed` |

Thirty-six, beside the contracts `Standard` declares. What makes one builtin is that the language cannot express it: arithmetic, ordering and counting are the machine's, written once for each type answering the contract that asks them, case mapping and encoding carry Unicode's tables with them, running at once is the host's scheduler, `appending` is the only way an array grows, and `gathering` the only way an answer keeps the spelling its collection arrived in. Everything else is written from those.

`greaterThan` is `lessThan` with its sides swapped, and both are called the same way.

One of these is builtin for a reason that is not the set it removes. `trimmed` names that set, and a body written from `characters` still could not answer it: `characters` answers characters, and whether a character is whitespace is a question about the code points inside it.

**A bundle is not a module.** A module is compiled against the modules standing before it, so the modules of a link have to have an order, and two that send to each other have none. What a bundle declares for its host to answer has no body and so waits for nothing; what it writes in Warp sends to whatever it needs. So a bundle links as two modules, its builtin half standing before every written half, and the same set of procedures links whatever the written halves send.

**The signatures, exactly.** A second implementation writes these; it must not have to guess them. The *parameters* column lists them in the order a row writes them, which is the position a call hands each argument at. A slot of a `const` procedure type takes only a procedure that answers without running. What each procedure declares of itself is part of its signature: every one answers without running (`const`), touches no name another body could touch at once (`isolated`) and fails with nothing, except where its section says otherwise.

**A procedure that takes procedures does what they do, and its name says which.** A procedure a `Standard.Collection` or `Standard.Logic` row takes answers without running and touches nothing, its type written `const isolated`, and it fails with nothing, so the row declares the same of itself. Where a caller would hand one that may fail, the row has a twin named `try` and then its own name with the first letter upper-cased, `map` and `tryMap`, whose slot is the row's with `throws` written into it, so the procedure it takes may fail with anything, and which declares `failing: anything`. The two are two procedures under two names: a call reads the one it names and nothing chooses between them, so a front end writes the one whose slot takes what it hands, and one that cannot tell writes the `try` one. A front end may show the two to a person under one name, and what a document writes is the one it chose.

*Standard.Logic*

| procedure | parameters | answers |
|---|---|---|
| `equal`, `notEqual` | `lhs: Any`, `rhs: Any` | `Bool` |
| `not` | `value: Bool` | `Bool` |
| `and`, `or`, `tryAnd`, `tryOr` | `conditions`. A list of procedures taking nothing, each answering `Bool`, so one answering anything else **refuses at the build** where it is handed | `Bool`. Over nothing, `and` and `tryAnd` answer `true` and `or` and `tryOr` answer `false`: no side decided the answer, so the chain's own answer stands |
| `select`, `trySelect` | `condition: Bool`, `then`, `else`. Procedures taking nothing, each answering `some Answer` | `some Answer` |

`tryAnd`, `tryOr` and `trySelect` declare `failing: anything`, the sides they are handed failing as they may.

`and` and `or` take procedures precisely so they need not run them all: the sides are read in order and the procedure stops at the first side that decides the answer. The first false, the first true. What follows the stop is never evaluated. `select` takes them for the same reason and asks exactly one, so a side that would refuse is never a refusal of the side that was chosen. `equal` and `notEqual` answer by the value model's one sameness, and `not` turns a `Bool` around.

**`select` is how an operand chooses.** A `conditional` answers nothing, under [statements](statement.md), and an operand is read rather than run, so choosing among values inside one is a procedure here rather than grammar. The two sides answer one type, worked out from the call the way any type parameter is.

*Standard*

The contracts, each procedure answering without running and touching nothing, and failing with nothing. A call writes the contract's spelling, `Standard.Numeric.plus`, and the run picks the declaration answering it by the type of the first argument: `Int.plus` for whole numbers, `Double.plus` for fractions.

| contract | procedure | parameters | answers |
|---|---|---|---|
| `Standard.Numeric` | `plus`, `minus`, `times`, `remainder` | `lhs: Self`, `rhs: Self` | `Self` |
| `Standard.Numeric` | `dividedBy` | `lhs: Self`, `rhs: Self` | `Double` |
| `Standard.Comparable` | `lessThan` | `lhs: Self`, `rhs: Self` | `Bool` |
| `Standard.Collection` | `count` | `collection: Self` | `Int` |

| type | claims |
|---|---|
| `Int`, `Double` | `Standard.Comparable`, `Standard.Numeric` |
| `String` | `Standard.Collection`, `Standard.Comparable` |
| `Array`, `Dictionary` | `Standard.Collection` |

`count` reads a list's elements, bytes included, a map's entries, and text's characters as a person reads them. A declared struct is an instance of its own name, so `count` takes one only where a document claims `Standard.Collection` for it.

*Standard.Math*

| procedure | parameters | answers |
|---|---|---|
| `min`, `max` | `lhs: some T`, `rhs: some T` | `some T`. Bounds `T: Standard.Comparable` |
| `absolute` | `number: some N` | `some N`. Bounds `N: Standard.Comparable & Standard.Numeric` |
| `floored`, `rounded` | `number: Double` | `Int` |
| `greaterThan` | `lhs: some T`, `rhs: some T` | `Bool`. Bounds `T: Standard.Comparable` |

`min` and `max` answer one of the two as it arrived. On a tie, where the two order the same, `min` answers `lhs` and `max` answers `rhs`, so `min(0.0, -0.0)` is `0.0` and `max(0.0, -0.0)` is `-0.0`.

`floored` goes to the nearest whole toward the smaller side, below zero too: `-2.1` floors to `-3`. `rounded` goes to the nearest whole, and away from zero at the exact halfway: `2.5` rounds to `3`, `-2.5` to `-3`. `floored` and `rounded` answer an `Int`, and only where an int holds the answer. `absolute` drops the sign and keeps the type it was given. The int's edge refuses at the run, as the edge rules below require.

*Standard.Text*

| procedure | parameters | answers |
|---|---|---|
| `text` | `value: Any` | `String` |
| `contains` | `text: String`, `other: String` | `Bool` |
| `startsWith` | `text: String`, `prefix: String` | `Bool` |
| `uppercased`, `lowercased`, `trimmed` | `text: String` | `String` |
| `characters` | `text: String` | `Array<String>` |
| `split` | `text: String`, `separator: String` | `Array<String>` |
| `joined` | `strings: Array<String>`, `separator: String`, written between each two | `String` |
| `decoded` | `bytes: Array<Int>`, `encoding: String` | `String`. **refuses at the run** when an element is no byte (a whole number from 0 to 255), the encoding is not one it has, or the bytes are not text in it |
| `encoded` | `text: String`, `encoding: String` | `Array<Int>`. **refuses at the run** when the encoding is not one it has |
| `replacing` | `text: String`, `target: String`, `replacement: String` | `String` |

`characters` answers the text as an array of its characters, each one a string of its own, counted the way `count` counts. Answered for the whole text rather than read one at a time: a character is an extended grapheme cluster, so where the tenth one starts is only known by walking the nine in front of it, and a body reading them in order would pay that walk every round.

**Two bundles declare `contains`, and they ask different questions.** `Standard.Collection.contains` asks whether an array holds an element; `Standard.Text.contains` asks whether a string holds another string inside it. They are two procedures because a string is not an array here: it has a `count` but no elements to read by position, since where the tenth character starts is only known by walking the nine in front of it. A program that wants a string's characters as a collection asks `characters` for them.

`uppercased` and `lowercased` apply Unicode's full default case mapping and no locale's tailoring: `ß` uppercases to `SS`, a capital sigma ending a word lowercases to the final `ς`, and `i` uppercases to `I` on every machine, whatever its locale says about a dotted `i`.

`trimmed` removes the whitespace at either end and nothing from the middle. A character goes only if **every one of its code points** has Unicode's `White_Space` property, and nothing a platform adds to that set is whitespace here. Both halves of that rule are load-bearing: `\r\n` is one character and two code points, both of them `White_Space`, so it goes; a space carrying a combining mark is also one character and two code points, and the mark is not `White_Space`, so it stays where it was written. A zero-width space is not whitespace in Unicode and so is not trimmed, however a platform's own set answers.

`replacing` rewrites every occurrence, not only the first. `joined` over an array with nothing in it answers the empty text, whatever the separator: there is nothing to put between. `split` keeps the empty pieces a separator at either end leaves, since dropping them would be an opinion about the text rather than a reading of it. `split` fails on a separator holding no characters and `replacing` on a target holding none, since either would match everywhere and consume nothing. The failure is `aborted`, which each declares, so an attempt around either catches it. The procedures that read text, `contains` and `startsWith` included, read as a person reads, under the value model's canonical equivalence.

`text` spells a value in its own spelling, which is the type's and not a document's. A string is its own characters, unquoted; a number, a bool and `null` are the spelling a document writes; bytes are `x` and their hex digits. A container it spells on **one line**: an array's elements between `[` and `]`, a map's entries between `{` and `}` as the key, spelled the way any value inside a container is, a colon and the value, a struct its fields the same, each field's name bare as its struct's name is, with its name and a space before the brace, a map's entries in the **key order** `keys` answers them in and a struct's fields by name ascending, elements or entries joined by commas with no space, and an empty one `[]` or `{}`. Inside a container `null` is `null`, and a string, bytes or a procedure is quoted: between double quotes, with `"`, `\`, a newline, a carriage return and a tab escaped as `\"`, `\\`, `\n`, `\r` and `\t`, any other character below `0x20` as `\u` and four hex digits, and everything else as itself, so `text` of `[x"6869"]` is `["x\"6869\""]` and of `[1, 2]` is `[1,2]`: a value's spelling does not change with how deep it sits. What no document carries answers in the language's own markers, never a host formatter's: a procedure is `<procedure>`, so `text` of a list holding one is `["<procedure>"]`. This is what `text` is for: a person reading a value. A carrier that has to give the value *back* is a different question, and one with no compact spelling writes bytes as what they are: an array of `Int`.

*Standard.Collection*

| procedure | parameters | answers |
|---|---|---|
| `append` | `array: inout Array<some Element>`, `element: some Element` | `null`, having written the element onto the end of the array the variable holds, in place |
| `contains` | `array: Array<some Element>`, `element: some Element` | `Bool` |
| `first`, `last` | `array: Array<some Element>` | `some Element`. Over nothing there is no element to answer, and the read of one **refuses at the run**, the way any index past the end does |
| `reversed`, `dropFirst`, `dropLast` | `array: Array<some Element>` | `Array<some Element>` |
| `sorted` | `array: Array<some Element>` | `Array<some Element>`, every element once, in order where `lessThan` is a strict order. Bounds `Element: Standard.Comparable` |
| `appending`, `prepending` | `array: Array<some Element>`, `element: some Element` | `Array<some Element>` |
| `gathering` | `array: Array<some Element>`, `positions: Array<Int>`. Where to read, in the order to read it | `Array<some Element>`, the collection's own, in the collection's spelling. A position the collection does not hold refuses at the run |
| `map`, `tryMap` | `array: Array<some Element>`, `transform`. A procedure handed the item, answering `some Answer` | `Array<some Answer>` |
| `filter`, `tryFilter` | `array: Array<some Element>`, `isIncluded`. A procedure handed the item, answering `Bool` | `Array<some Element>` |
| `reduce`, `tryReduce` | `array: Array<some Element>`, `initialResult: some Carried`, `nextPartialResult`. A procedure handed the carried value, then the item, answering `some Carried` | `some Carried` |
| `keys` | `dictionary: Dictionary<some Key, Any>` | `Array<some Key>`, the keys the map holds, in its key order. Bounds `Key: Hashable` |
| `values` | `dictionary: Dictionary<some Key, some Entry>` | `Array<some Entry>`, what the map holds, in its key order. Bounds `Key: Hashable` |
| `setting` | `dictionary: Dictionary<some Key, some Value>`, `key: some Key`, `value: some Value` | `Dictionary<some Key, some Value>`, the map with the entry under the key written. The map's keys and the key read as one type, and its entries and the value as another, so two types there that neither takes **refuse at the build**. Bounds `Key: Hashable` |

`tryMap`, `tryFilter` and `tryReduce` declare `failing: anything`, for the reason `tryAnd` does. `append` writes the caller's variable, so it is not `const`.

`gathering` is how a procedure answers a collection's own elements. It says which by position, and the answer comes back in the spelling the collection arrived in: bytes rearranged are bytes. This is the whole of what `reversed`, `dropFirst`, `dropLast`, `filter` and `sorted` add to a walk, and it is the reason those are written in Warp rather than asked of an implementation. A body that read the elements out and put them back would answer an array of numbers, because an array it started empty has no spelling to keep. The standard name for reading one collection at another's positions is a **gather**.

*Standard.Control*

| procedure | parameters | answers |
|---|---|---|
| `abort` | `message: Any`. What the failure says. Null says `aborted` | `Never` |

*Standard.Concurrent*

| procedure | parameters | answers |
|---|---|---|
| `all` | `pieces`. A list of `isolated` procedures taking nothing, each answering `some Answer` | `Array<some Answer>`, each piece's answer in the pieces' order |
| `allKeyed` | `pieces`. A map of `isolated` procedures taking nothing under keys of `some Key`, each answering `some Answer` | `Dictionary<some Key, some Answer>`, each piece's answer under its key. Bounds `Key: Hashable` |
| `first` | `pieces`. A list of `isolated` procedures taking nothing, each answering `some Answer` | `some Answer` |
| `firstKeyed` | `pieces`. A map of `isolated` procedures taking nothing under keys of `some Key`, each answering `some Answer` | `some Answer`. Bounds `Key: Hashable` |
| `map` | `array: Array<some Element>`, `transform`. `isolated` procedure, handed the item, then its index, answering `some Answer` | `Array<some Answer>` |

**`Standard.Concurrent`**. Running closures at once. `all` takes a list of closures, runs every one, and answers every answer in the list's order; `allKeyed` takes a map of closures under keys, and answers each answer under its key. A failure fails the whole procedure with `concurrent_failed`, whose `details` hold `failures`: every piece's failure under the piece's key, a map's piece under the key it stood under and a list's under its position, an `Int`, and each is the envelope that piece raised, so a rescue reads a piece's own `type`, `message` and `details` through it. `first` and `firstKeyed` take the same and answer the first success, asking the rest to stop; which piece wins is the one timing fact this language admits. A piece that refuses at the run before one succeeds ends the race the way a success does, and refuses the whole run. What a piece does once the rest are asked to stop is not reported. `map` takes a collection and one closure, calls it once per element, handing it the element and then its index, and answers in the collection's order. These are procedures rather than grammar because a closure is already the safe unit of concurrent work, and being procedures makes concurrency a permission: what a host does not link, a program cannot do. Each procedure its rows take may fail with anything, its type writing `throws`. Each runs what it is handed, so none is `const`, and each declares `failing: [concurrent_failed]`.

The names are plain ones with the module carrying the context. A call site spells the module, so `Standard.Collection.first` and `Standard.Concurrent.first` are two names, and a link carrying both bundles holds both: every `first` and every `map`, the sequential ones included, is written with its bundle, and concurrency shows at the call site.

What the checking sees: `map` declares its types the way the sequential one does. The collection's `Element` meets the closure's parameter, and the answer's type is the closure's answer, checked at the build. Its `transform` is an `isolated` procedure type taking `some Element` and `Int` and answering `some Answer`, so a closure that writes a captured variable refuses there before anything runs. `all` and `allKeyed` take a list and a map of an `isolated` procedure type answering `some Answer`, and `first` and `firstKeyed` the same, so a piece the build reads as something other than a closure, or as a closure that writes what it captured, refuses at the build; a list or a map literal is held to the slot part by part, so a piece that is not a closure refuses there too, and a list of pieces read as `Any` takes a cast first, the way any value read as `Any` does. Every piece answers the one `Answer` the call fills from them, so `all` answers `Array<some Answer>`, `allKeyed` `Dictionary<some Key, some Answer>` under the keys its pieces stood under, and the two `first`s `some Answer`; pieces answering two types that neither takes fill it with `Any`, joined part by part the way a literal's parts are, and so does a piece written to answer `Any`.

What the procedures hand their closures is one convention, shared with the sequential walks. `Standard.Collection.map`, `filter` and their `try` twins hand over the item, `reduce` and `tryReduce` hand over the carried value then the item, `Standard.Concurrent.map` hands over the item then its index, and a closure written for one of them **declares exactly as many parameters as it is handed, in that order**, under names of its own, whether or not its body goes on to read one. A closure of another count **refuses at the build**, the same as anywhere else a value is called: a walk is not a second calling convention. `Standard.Concurrent.first` run over nothing **refuses at the run**, and so does `firstKeyed` over a map holding nothing, the way `Standard.Collection.first` of nothing is: a procedure that answers exactly one thing has no empty answer. And a `first` or a `firstKeyed` in which nothing succeeds fails the way `all` and `allKeyed` fail: every piece's failure reported under the piece's key, a map's piece under the key it stood under and a list's under its position, an `Int`.

What the vocabulary answers about **bytes**: they are an array of whole numbers from 0 to 255, `Array<Int>`, and `x"6869"` is that array's compact spelling, under [values](value.md). A slot taking bytes is written `Array<Int>`, or any other array the bytes fit. **The spelling is the value's own fact rather than the slot's**: a bytes value stands where `Array<Int>` is declared and crosses it *whole*, because the slot asked for an array and bytes are one. `Array<Double>` takes no byte at all, a byte being a whole number. An element declared as a **bounded** type parameter stands for one type the call filled, so `sorted`, whose element carries `Standard.Comparable`, reads a compact spelling the way `reversed` does. An array of byte worths written out one by one stays as written: the compact spelling is the value's, and no slot puts it on.

An index reads an element out as an `Int`, and so does `some Element` filled by bytes: `first` of bytes answers an `Int`. The collection vocabulary (`count`, `first`, `contains`, `reversed`, `map`, all of it) applies directly. A procedure that answers a collection's **own** elements (`reversed`, `filter`, `sorted`, `dropFirst`, `dropLast`) answers them in the spelling they arrived in, so bytes stay bytes; put something among them that is not a byte (`appending` a `300`) and the answer is the array it now is. A procedure that builds **new** elements does not: `map` answers whatever its procedure answered, which its declaration says by naming a second type parameter for it. Two bytes values do **not** order: `Standard.Comparable` is claimed for numbers and strings, not for `Array`. Reading bytes *as* text is a procedure that names its encoding: `decoded` and `encoded` are the two directions of one mapping (`encoding: "utf8"`, the only encoding they have). `decoded` completes no broken sequence, which would answer a text nobody sent. `encoded` writes the text's code points as they stand and normalises nothing, and `decoded` keeps a byte order mark as the character it is: normalising the one or dropping the other would be an opinion about the text rather than a reading of it. The encodings are this specification's: each is one every implementation writes.

**`abort`**. Fail on purpose, with a message. Declared `returns: Never` and `failing: [aborted]`, which is everything the checking needs: nothing runs after it, and no name binds it. The message is what `message` spells as text. Sent null, the failure says `aborted`. It is a failure like any other, so an `attempt` around it catches it. Leaving is what a rescue does not catch, and this is failing, not leaving.

Behaviour at the edges, where implementations quietly differ, stated as requirements:

- Arithmetic takes two of one type: both sides are `Self` of `Standard.Numeric`, and so is the answer of `plus`, `minus`, `times` and `remainder`. A whole number added to text **refuses at the build**, and so do two pieces of text, because no claim puts text under `Standard.Numeric`.
- Ordering (`lessThan`, `greaterThan`, `sorted`, `min`, `max`) compares two of one type under `Standard.Comparable`, `String` among them. A type no claim puts under it, or a reading whose type the build does not know, refuses at the build, under **Bounds** in [types](type.md).
- Whole-number arithmetic with no whole answer **refuses at the run**. It does not wrap and does not silently widen. The rule covers every standard procedure that answers an `Int` and can miss it: `plus`, `minus`, `times` off the int's edge, `absolute` of the int's own minimum, and `floored`/`rounded` of a fraction whose whole part is past the int. `remainder` is not on the list because its answer always fits. A remainder is smaller in size than its divisor, and the one divisor that trips a machine's division instruction still has one: `-9223372036854775808 remainder -1` answers `0`. These run-stage refusals (overflow, and the zero divisor below) are the program's own defect, not a failure of the work: an `attempt` does **not** catch them, the way it does not catch an index past the end. What a rescue catches is `abort` and a procedure's own failure.
- Fraction arithmetic with no finite answer **refuses at the run**, at the door its answer crosses under [running](running.md): infinity is a value the arithmetic can reach and no document can carry.
- `dividedBy` answers a fraction, whole or not. Division by zero **refuses at the run**. The quotient is binary64's own: a whole operand reads as the fraction nearest it first, and the division rounds once more, so two implementations spell the same quotient bit for bit.
- `remainder` truncates toward zero, for wholes and fractions alike: what is left takes the dividend's sign, so `-7 remainder 3` is `-1`, `7 remainder -3` is `1` and `-5.5 remainder 2.0` is `-1.5`. A zero divisor **refuses at the run**, the same as under `dividedBy`.
- A whole number is no fraction, and a fraction is no whole number, under [types](type.md), which says too where a whole number written as a literal is read as the fraction it names.

What a host brings beyond these (its own procedures, and which of them answer without running) is the host's, and is the boundary to the outside world: a program reaches nothing except by sending a procedure the host declared.

## Cases

What `conformance/` asks about this page, by the name each case's file carries.

- `a-closure-that-may-fail-handed-to-filter-refuses`
- `a-const-body-chooses-a-value-with-select`
- `a-const-map-rewrites-in-order`
- `a-document-gathers-a-collections-own-elements`
- `a-document-writes-a-short-circuiting-connective`
- `a-document-writes-map-over-a-const-slot`
- `a-document-writes-startsWith-over-characters`
- `a-fraction-divided-by-negative-zero-refuses`
- `a-fraction-divided-by-zero-refuses`
- `a-list-holding-no-byte-handed-to-decoded-refuses`
- `a-list-of-pieces-joining-to-any-at-a-fan-out-refuses`
- `a-mapped-procedure-chooses-what-it-answers`
- `a-piece-that-is-not-a-closure-refuses`
- `a-procedure-answering-a-collections-own-elements-keeps-the-spelling`
- `a-quotient-reads-a-whole-operand-as-the-nearest-fraction`
- `a-side-not-saying-it-is-isolated-handed-to-and-refuses`
- `a-space-carrying-a-mark-is-not-trimmed`
- `a-string-holding-another-is-a-text-question`
- `a-string-not-holding-another-answers-false`
- `a-text-procedure-answers-new-text`
- `a-zero-width-space-is-not-whitespace`
- `abort-sent-null-says-aborted`
- `absolute-drops-the-sign-of-negative-zero`
- `absolute-floored-and-rounded-answer-a-whole`
- `absolute-of-the-minimum-refuses`
- `all-keyed-answers-under-keys-of-any-type`
- `an-encoding-a-procedure-does-not-have-refuses`
- `an-isolated-body-filters-through-a-closure-that-fails-with-nothing`
- `an-operand-of-and-that-answers-no-bool-refuses`
- `and-over-nothing-answers-true`
- `append-writes-the-array-in-place`
- `arithmetic-answers-the-type-it-was-given`
- `arithmetic-divide-by-zero-refuses`
- `arithmetic-divides-to-a-fraction`
- `arithmetic-on-a-value-it-does-not-take-refuses`
- `arithmetic-on-two-pieces-of-text-refuses`
- `arithmetic-overflow-refuses`
- `arithmetic-reads-a-whole-literal-beside-a-fraction-as-the-fraction`
- `bytes-at-a-list-of-fractions-refuse`
- `bytes-cross-an-array-slot-in-their-own-spelling`
- `case-mapping-takes-no-locale`
- `characters-answers-grapheme-clusters`
- `comparing-bytes-for-order-refuses`
- `concurrent-map-offers-item-and-index`
- `concurrent-map-over-nothing-answers-nothing`
- `contains-asks-a-collection`
- `count-of-a-declared-struct-no-claim-names-refuses`
- `count-of-a-number-refuses`
- `count-of-bytes-is-their-length`
- `decoded-keeps-a-byte-order-mark`
- `decoded-reads-bytes-as-text-in-a-named-encoding`
- `decoded-reads-bytes-written-one-by-one`
- `decoding-what-is-not-utf8-text-refuses`
- `dropping-an-end-answers-the-rest`
- `encoded-writes-text-as-bytes-in-a-named-encoding`
- `encoded-writes-the-code-points-as-they-stand`
- `first-and-last-read-the-ends`
- `first-answers-the-first-success`
- `first-in-which-nothing-succeeds-fails-with-every-piece`
- `first-keyed-over-nothing-refuses`
- `first-over-a-piece-that-refuses-before-one-succeeds-refuses`
- `first-over-nothing-refuses`
- `floored-past-the-int-refuses`
- `fraction-arithmetic-with-no-finite-answer-refuses`
- `gathering-past-the-end-refuses`
- `gathering-reads-positions-written-as-bytes`
- `greater-than-mirrors-less-than`
- `indexing-bytes-answers-a-whole-number`
- `joined-over-nothing-answers-empty-text`
- `keys-answer-a-maps-own-keys-in-the-key-order`
- `keys-answer-in-canonical-order`
- `keys-of-a-map-keyed-by-hashable-refuses`
- `lowercased-ends-a-word-with-final-sigma`
- `lowercased-folds-the-case`
- `map-answers-in-the-collections-order`
- `map-over-a-closure-not-declaring-isolated-refuses`
- `max-answers-rhs-on-a-tie`
- `min-and-max-pick-an-end`
- `min-answers-lhs-on-a-tie`
- `minus-and-times-compose-as-written`
- `minus-off-the-ints-edge-refuses`
- `not-and-notequal-say-the-opposite`
- `or-does-not-ask-past-the-first-yes`
- `or-over-nothing-answers-false`
- `ordering-compares-two-of-one-type`
- `overflow-inside-an-attempt-refuses`
- `prepending-writes-the-front`
- `reduce-folds-in-order`
- `remainder-at-the-ints-minimum-answers`
- `remainder-by-zero-refuses`
- `remainder-is-what-whole-division-leaves`
- `remainder-takes-the-sign-of-the-dividend`
- `replacing-nothing-fails`
- `replacing-swaps-every-occurrence`
- `reversed-turns-the-order-around`
- `rounded-past-the-int-refuses`
- `setting-a-key-of-another-type-than-the-maps-refuses`
- `setting-answers-a-new-map`
- `setting-writes-a-key-of-the-maps-own-type`
- `sorted-answers-every-element-where-less-than-is-not-strict`
- `sorted-orders-what-it-was-given`
- `sorting-the-unorderable-refuses`
- `split-cuts-and-joined-writes`
- `split-keeps-the-empty-pieces`
- `split-on-nothing-fails`
- `starts-with-reads-the-head`
- `text-counts-as-a-person-reads`
- `text-of-a-list-holding-a-procedure-quotes-its-marker`
- `text-of-a-procedure-spells-a-marker`
- `text-of-null-spells-null`
- `text-spells-a-maps-key-as-the-value-it-is`
- `text-spells-a-struct-on-one-line`
- `text-spells-bytes-the-way-a-document-writes-them`
- `the-side-select-does-not-choose-goes-unasked`
- `times-off-the-ints-edge-refuses`
- `trimming-takes-unicode-whitespace-from-both-ends`
- `tryAnd-fails-with-what-its-side-fails-with`
- `tryAnd-over-nothing-answers-true`
- `tryFilter-fails-with-what-its-closure-fails-with`
- `tryMap-fails-with-what-its-closure-fails-with`
- `tryOr-fails-with-what-its-side-fails-with`
- `tryOr-over-nothing-answers-false`
- `tryReduce-fails-with-what-its-closure-fails-with`
- `trySelect-fails-with-what-the-chosen-side-fails-with`
- `uppercased-uses-unicode-full-case-mapping`
- `values-answer-in-canonical-order`
- `values-of-a-map-keyed-by-whole-numbers-answer-in-the-key-order`
