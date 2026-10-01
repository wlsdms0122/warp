# The standard vocabulary

The procedures every implementation brings, what each answers, and which of them an implementation has to write in native code rather than take from `lib/std`. This is the layer a program does its work in: the language has no arithmetic, no comparison and no collections of its own, and a program that is granted none of these can compute nothing.

Seven bundles, each taken with what it depends on, so a host grants what its programs have use for and no more. What a bundle depends on is what its written half sends and what its signatures mention, and the written half's `imports` is the list. `std` is the shared ground: it declares no procedures, only the memberships and the type the other bundles' signatures mention, so every bundle below links with `std` in the link. Beyond that, `std.math` stands alone; `std.logic` links with `std.collection` and `std.math`; `std.collection` with `std.logic` and `std.math`; `std.concurrent` with `std.collection` and `std.math`; `std.text` with `std.collection`, `std.control`, `std.logic` and `std.math`; `std.control` stands alone. Two bundles that send to each other are not a cycle, because a bundle is not a module, below:

| module | procedures |
|---|---|
| `std` | None. It declares the memberships `std.Numeric`, `std.Comparable` and `std.Collection`, and the type `std.byte = int(0...255)` |
| `std.logic` | `equal` `notEqual` `not` `and` `or` `select` |
| `std.math` | `plus` `minus` `times` `dividedBy` `remainder` `min` `max` `absolute` `floored` `rounded` `lessThan` `greaterThan` |
| `std.text` | `text` `characters` `contains` `startsWith` `uppercased` `lowercased` `trimmed` `split` `joined` `replacing` `decoded` `encoded` |
| `std.collection` | `append` `count` `contains` `first` `last` `reversed` `appending` `prepending` `gathering` `dropFirst` `dropLast` `sorted` `map` `filter` `reduce` `keys` `values` `setting` |
| `std.control` | `abort`. Declared `returns: never` |
| `std.concurrent` | `all` `first` `map`. Run closures at once. Declares the membership `std.concurrent.Pieces` |

## What an implementation must write

Not all of these. Most are written in Warp, from a small set that cannot be: **builtin**. An implementation writes the builtin procedures in its own language and takes the rest as a Warp module, the way any other module arrives.

| bundle | builtin |
|---|---|
| `std.logic` | `equal` |
| `std.math` | `plus` `minus` `times` `dividedBy` `remainder` `lessThan` `floored` `rounded` |
| `std.text` | `text` `joined` `characters` `uppercased` `lowercased` `encoded` `decoded` `trimmed` |
| `std.collection` | `count` `appending` `gathering` `keys` `setting` |
| `std.control` | `abort` |
| `std.concurrent` | `all` `first` |

Twenty-five, beside the memberships and the `std.byte` type `std` declares. What makes one builtin is that the language cannot express it: arithmetic and ordering are the machine's, case mapping and encoding carry Unicode's tables with them, running at once is the host's scheduler, `appending` is the only way an array grows, and `gathering` the only way an answer keeps the spelling its collection arrived in. Everything else is written from those.

A procedure being derivable is not a claim that it is unimportant, and a document cannot tell the two apart: `greaterThan` is `lessThan` with its sides swapped, and both are called the same way. An implementation that wants its own `greaterThan` declares one under that name in a module it lays in the link **in place of** the written one, and the link takes it: one name has one declarer, and which body stands behind it is the host's, which is what every name outside the builtin set is open to.

One of these is builtin for a reason that is not the set it removes. `trimmed` names that set, and a body written from `characters` still could not answer it: `characters` answers characters, and whether a character is whitespace is a question about the code points inside it.

**A bundle is not a module.** A module is compiled against the modules standing before it, so the modules of a link have to have an order, and two that send to each other have none. What a bundle declares for its host to answer has no body and so waits for nothing; what it writes in Warp sends to whatever it needs. An implementation that lands both halves of a bundle in one module holds the builtin half to the written half's order, and two bundles whose written halves lean on each other then have no order at all: `std.logic` walks, so it sends `std.collection.count`, and a collection procedure comparing two elements sends `std.logic.equal`. Landing them apart is how the same set of procedures links, and it is what an implementation weighs when it writes a procedure in Warp rather than in its own language.

**The signatures, exactly.** A second implementation writes these; it must not have to guess them. The *parameters* column lists them in the order a row writes them, which is the position a call hands each argument at. A slot typed `const procedure` takes only a procedure that answers without running.

*std.logic*

| procedure | parameters | answers |
|---|---|---|
| `equal`, `notEqual` | `lhs: any`, `rhs: any` | `bool` |
| `not` | `value: bool` | `bool` |
| `and`, `or` | `conditions: array<const procedure>`, each declared as taking nothing and answering `bool`, so one answering anything else **refuses at the build** where it is handed | `bool`. Over nothing, `and` answers `true` and `or` answers `false`: no side settled the answer, so the chain's own answer stands |
| `select` | `condition: bool`, `then`, `else`. `const` procedures taking nothing, each answering `some Answer` | `some Answer` |

`and` and `or` take procedures precisely so they need not run them all: the sides are read in order and the procedure stops at the first side that settles the answer. The first false, the first true. What follows the stop is never evaluated. `select` takes them for the same reason and asks exactly one, so a side that would refuse is never a refusal of the side that was chosen. `equal` and `notEqual` answer by the value model's one sameness, and `not` turns a `bool` around.

**`select` is how an operand chooses.** A `conditional` answers nothing and takes no name, and an operand is read rather than run, so choosing among values inside one is a procedure here rather than grammar. The two sides answer one type, worked out from the call the way any type parameter is.

*std.math*

| procedure | parameters | answers |
|---|---|---|
| `plus`, `minus`, `times`, `remainder` | `lhs: some N`, `rhs: some N` | `some N`. Bounds `N: std.Numeric` |
| `min`, `max` | `lhs: some T`, `rhs: some T` | `some T`. Bounds `T: std.Comparable` |
| `dividedBy` | `lhs: some N`, `rhs: some N` | `double`. Bounds `N: std.Numeric` |
| `absolute` | `number: some N` | `some N`. Bounds `N: std.Numeric` |
| `floored`, `rounded` | `number: some N` | `int`. Bounds `N: std.Numeric` |
| `lessThan`, `greaterThan` | `lhs: some T`, `rhs: some T` | `bool`. Bounds `T: std.Comparable` |

`min` and `max` answer one of the two as it arrived. On a tie, where the two order the same, `min` answers `lhs` and `max` answers `rhs`, so `min(1, 1.0)` is `1` and `max(1, 1.0)` is `1.0`.

`floored` goes to the nearest whole toward the smaller side, below zero too: `-2.1` floors to `-3`. `rounded` goes to the nearest whole, and away from zero at the exact halfway: `2.5` rounds to `3`, `-2.5` to `-3`. `absolute` drops the sign and keeps the kind it was given. Each of these answers an `int` only when an int holds the answer. The int's edge refuses at the run, as the edge rules below require.

*std.text*

| procedure | parameters | answers |
|---|---|---|
| `text` | `value: any` | `string` |
| `contains` | `text: string`, `other: string` | `bool` |
| `startsWith` | `text: string`, `prefix: string` | `bool` |
| `uppercased`, `lowercased`, `trimmed` | `text: string` | `string` |
| `characters` | `text: string` | `array<string>` |
| `split` | `text: string`, `separator: string` | `array<string>` |
| `joined` | `strings: array<string>`, `separator: string`, written between each two | `string` |
| `decoded` | `bytes: array<std.byte>`, `encoding: string`, enum `["utf8"]` | `string`. **refuses at the run** when the bytes are not text in that encoding |
| `encoded` | `text: string`, `encoding: string`, enum `["utf8"]` | `array<std.byte>` |
| `replacing` | `text: string`, `target: string`, `replacement: string` | `string` |

`characters` answers the text as an array of its characters, each one a string of its own, counted the way `count` counts. Answered for the whole text rather than read one at a time: a character is an extended grapheme cluster, so where the tenth one starts is only known by walking the nine in front of it, and a body reading them in order would pay that walk every round.

**Two bundles declare `contains`, and they ask different questions.** `std.collection.contains` asks whether an array holds an element; `std.text.contains` asks whether a string holds another string inside it. They are two procedures because a string is not an array here: it has a `count` but no elements to read by position, since where the tenth character starts is only known by walking the nine in front of it. A program that wants a string's characters as a collection asks `characters` for them.

`uppercased` and `lowercased` apply Unicode's full default case mapping and no locale's tailoring: `ß` uppercases to `SS`, a capital sigma ending a word lowercases to the final `ς`, and `i` uppercases to `I` on every machine, whatever its locale says about a dotted `i`.

`trimmed` removes the whitespace at either end and nothing from the middle. A character goes only if **every one of its code points** has Unicode's `White_Space` property, and nothing a platform adds to that set is whitespace here. Both halves of that rule are load-bearing: `\r\n` is one character and two code points, both of them `White_Space`, so it goes; a space carrying a combining mark is also one character and two code points, and the mark is not `White_Space`, so it stays where it was written. A zero-width space is not whitespace in Unicode and so is not trimmed, however a platform's own set answers.

`replacing` rewrites every occurrence, not only the first. `joined` over an array with nothing in it answers the empty text, whatever the separator: there is nothing to put between. `split` keeps the empty pieces a separator at either end leaves, since dropping them would be an opinion about the text rather than a reading of it. `split` fails on a separator holding no characters and `replacing` on a target holding none, since either would match everywhere and consume nothing. The failure is `aborted`, so an attempt around either catches it. The procedures that read text, `contains` and `startsWith` included, read as a person reads, under the value model's canonical equivalence.

`text` spells a value in its own spelling, which is the type's and not a document's. A string is its own characters, unquoted; a number, a bool and `null` are the spelling a document writes; bytes are `x` and their hex digits. A container it spells on **one line**: an array's elements between `[` and `]`, a dictionary's entries between `{` and `}` as the key quoted, a colon and the value, a named record the same with its name and a space before the brace, entries in **name order** ascending as `keys` answers them, elements or entries joined by commas with no space, and an empty one `[]` or `{}`. Inside a container `null` is `null`, and a string or bytes is quoted: between double quotes, with `"`, `\`, a newline, a carriage return and a tab escaped as `\"`, `\\`, `\n`, `\r` and `\t`, any other character below `0x20` as `\u` and four hex digits, and everything else as itself, so `text` of `[x"6869"]` is `["x\"6869\""]` and of `[1, 2]` is `[1,2]`: a value's spelling does not change with how deep it sits. What no document carries answers in the language's own markers, never a host formatter's: a procedure is `<procedure>`, a host's non-finite fraction is `<infinity>`, `<-infinity>` or `<not a number>`, and a container holding one shows whole as `<unencodable>`. This is what `text` is for: a person reading a value. A carrier that has to give the value *back* is a different question, and one with no compact spelling writes bytes as what they are: an array of `std.byte`.

*std.collection*

| procedure | parameters | answers |
|---|---|---|
| `append` | `array: inout array<some Element>`, `element: some Element` | `null`, having written the element onto the end of the array the variable holds, in place |
| `count` | `collection: std.Collection`. The membership of `string`, `array` and `dictionary`; bytes stand as an array and a record as a dictionary | `int` |
| `contains` | `array: array<some Element>`, `element: some Element` | `bool` |
| `first`, `last` | `array: array<some Element>` | `some Element`. Over nothing there is no element to answer, and the read of one **refuses at the run**, the way any index past the end does |
| `reversed`, `dropFirst`, `dropLast` | `array: array<some Element>` | `array<some Element>` |
| `sorted` | `array: array<some Element>` | `array<some Element>`. Bounds `Element: std.Comparable` |
| `appending`, `prepending` | `array: array<some Element>`, `element: some Element` | `array<some Element>` |
| `gathering` | `array: array<some Element>`, `positions: array<int>`. Where to read, in the order to read it | `array<some Element>`, the collection's own, in the collection's spelling. A position the collection does not hold refuses at the run |
| `map` | `array: array<some Element>`, `transform`. `const` procedure, handed the item, answering `some Answer` | `array<some Answer>` |
| `filter` | `array: array<some Element>`, `isIncluded`. `const` procedure, handed the item, answering `bool` | `array<some Element>` |
| `reduce` | `array: array<some Element>`, `initialResult: some Carried`, `nextPartialResult`. `const` procedure, handed the carried value, then the item, answering `some Carried` | `some Carried` |
| `keys` | `dictionary: dictionary<any>` | `array<string>` |
| `values` | `dictionary: dictionary<some Entry>` | `array<some Entry>` |
| `setting` | `dictionary: dictionary<any>`, `key: string`, `value: any` | `dictionary<any>`. The key becomes a field's name, so a key that is not a name (empty, or not in normal form C) **refuses at the run** |

`gathering` is how a procedure answers a collection's own elements. It says which by position, and the answer comes back in the spelling the collection arrived in: bytes rearranged are bytes. This is the whole of what `reversed`, `dropFirst`, `dropLast`, `filter` and `sorted` add to a walk, and it is the reason those are written in Warp rather than asked of an implementation. A body that read the elements out and put them back would answer an array of numbers, because an array it started empty has no spelling to keep. The standard name for reading one collection at another's positions is a **gather**.

*std.control*

| procedure | parameters | answers |
|---|---|---|
| `abort` | `message: any`. What the failure says. Null says `aborted` | `never` |

*std.concurrent*

| procedure | parameters | answers |
|---|---|---|
| `all`, `first` | `pieces: std.concurrent.Pieces`. The membership of `array<isolated procedure>` and `dictionary<isolated procedure>` | `any` |
| `map` | `array: array<some Element>`, `transform`. `isolated procedure`, handed the item, then its index, answering `some Answer` | `array<some Answer>` |

**`std.concurrent`**. Running closures at once. `all` takes a record or an array of closures, runs every one, and answers every answer. A record's under its keys, an array's in its order; a failure fails the whole procedure with every piece's failure reported, keyed by the piece it came from. `first` takes the same and answers the first success, asking the rest to stop; which piece wins is the one timing fact this language admits. `map` takes a collection and one closure, calls it once per element, handing it the element and then its index, and answers in the collection's order. These are procedures rather than grammar because a closure is already the safe unit of concurrent work, and being procedures makes concurrency a permission: what a host does not link, a program cannot do.

The names are plain ones with the module carrying the context, the way `Array.map` and `TaskGroup.next` lean on their types. A call site spells the module, so `std.collection.first` and `std.concurrent.first` are two names, and a link carrying both bundles holds both: every `first` and every `map`, the sequential ones included, is written with its bundle, and concurrency shows at the call site.

What the checking sees: `map` declares its types the way the sequential one does. The collection's `Element` meets the closure's parameter, and the answer's type is the closure's answer, checked at the build. Its `transform` is an `isolated procedure` taking `item: some Element` and `index: int` and answering `some Answer`, so a closure that writes a captured variable refuses there before anything runs. `all` and `first` take `std.concurrent.Pieces`, the membership of `array<isolated procedure>` and `dictionary<isolated procedure>`, so a piece the build reads as something other than a closure, or as a closure that writes what it captured, refuses at the build; a piece that arrives as `any` (an array literal whose elements join to `any`) is held to the membership at the run, the way any value crossing a slot through `any` is. They answer `any`: the answer is shaped like what went in, and a membership names a set of types rather than tying one of them to another. What a fan-out's answer feeds is checked from `map`, not from these two.

What the procedures hand their closures is one convention, shared with the sequential walks. `std.collection.map` and `filter` hand over the item, `reduce` hands over the carried value then the item, `std.concurrent.map` hands over the item then its index, and a closure written for one of them **declares exactly as many parameters as it is handed, in that order**, under names of its own, whether or not its body goes on to read one. A closure of another count refuses, the same as anywhere else a value is called: a walk is not a second calling convention. `std.concurrent.first` run over nothing is refused, the way `std.collection.first` of nothing is: a procedure that answers exactly one thing has no empty answer. And a `first` in which nothing succeeds fails the way `all` fails: every piece's failure reported, keyed by the piece it came from, a record's by its key and an array's by its index written `[0]`.

What the vocabulary answers about **bytes**: bytes are not a special material. They are an array of small whole numbers, `array<std.byte>`, `std.byte` being the range `int(0...255)` that `std` declares, and `x"6869"` is that array's compact spelling, under [values](value.md). There is no type named for the spelling: a slot is written `array<std.byte>`, or any other array the bytes fit. **The spelling is the value's own fact rather than the slot's**: a bytes value stands where `array<int>` is declared and crosses it *whole*, because the slot asked for an array and bytes are one. There is nothing to settle, and unpacking would spend an element per byte to answer questions like `first` that read one. An `array<…>` slot reads the bytes out one by one only where its element declaration would not leave a byte as it is: `array<double>` changes every one of them, a range narrower than `std.byte` has something to ask of each, and a fraction range (`double(0.0...255.0)`) is both. It widens every byte it takes. An element declared as a **bounded** type parameter asks each value for its membership, and a member of the constraint that takes every byte answers that for all of them at once, so `sorted`, whose element carries `std.Comparable`, reads a compact spelling the way `reversed` does rather than by whether its declaration happened to carry a bound. An array of byte worths written out one by one stays as written: the compact spelling is the value's, and no slot puts it on.

An index reads an element out as a `std.byte`, the range `std` names, and so does `some Element` filled by bytes: `first` of bytes answers a `std.byte`. The collection vocabulary (`count`, `first`, `contains`, `reversed`, `map`, all of it) applies directly. A procedure that answers a collection's **own** elements (`reversed`, `filter`, `sorted`, `dropFirst`, `dropLast`) answers them in the spelling they arrived in, so bytes stay bytes; put something among them that is not a byte (`appending` a `300`) and the answer is the array it now is. A procedure that builds **new** elements does not: `map` answers whatever its procedure answered, which its declaration says by naming a second type parameter for it. Two bytes *values* still do **not** order, for the array reason rather than an opacity one: `std.Comparable` admits numbers and strings among themselves, not collections. Reading bytes *as* text is a procedure that names its encoding: `decoded` and `encoded` are the two directions of one mapping (`encoding: "utf8"`, the only member), and bytes that are not text in that encoding **refuse at the run**. Completing a broken sequence would answer a text nobody sent. `encoded` writes the text's code points as they stand and normalises nothing, and `decoded` keeps a byte order mark as the character it is: normalising the one or dropping the other would be an opinion about the text rather than a reading of it. The list of encodings is this specification's: a member is one every implementation writes, so a host with an encoding of its own declares a procedure of its own rather than widening the list.

**`abort`**. Fail on purpose, with a message. Declared `returns: never`, which is everything the checking needs: nothing runs after it, and no name binds it. The message is what `message` spells as text. Sent null, the failure says `aborted`. It is a failure like any other, so an `attempt` around it catches it. Leaving is what a rescue does not catch, and this is failing, not leaving.

Behaviour at the edges, where implementations quietly differ, stated as requirements:

- Arithmetic takes two of a kind and answers that kind: both sides and the answer are one type parameter, bounded by `std.Numeric`. A whole number added to text **refuses at the build**, and so do two pieces of text, because agreement is not admission.
- Ordering (`lessThan`, `greaterThan`, `sorted`, `min`, `max`) compares two of a kind under `std.Comparable`, and text is a kind. A kind the constraint does not admit refuses at the build where the text says so, and at the boundary where the value arrives through `any`.
- Whole-number arithmetic with no whole answer **refuses at the run**. It does not wrap and does not silently widen. The rule covers every standard procedure that answers an `int` and can miss it: `plus`, `minus`, `times` off the int's edge, `absolute` of the int's own minimum, and `floored`/`rounded` of a fraction whose whole part is past the int. `remainder` is not on the list because its answer always fits. A remainder is smaller in size than its divisor, and the one divisor that trips a machine's division instruction still has one: `-9223372036854775808 remainder -1` answers `0`. These run-stage refusals (overflow, and the zero divisor below) are the program's own defect, not a failure of the work: an `attempt` does **not** catch them, the way it does not catch an index past the end. What a rescue catches is `abort` and a procedure's own failure.
- Fraction arithmetic with no finite answer **refuses at the run** for the same reason: infinity is a value the arithmetic can reach and no document can carry, and a value that exists only until someone writes it down is not an answer.
- `dividedBy` answers a fraction, whole or not. Division by zero **refuses at the run**. The quotient is binary64's own: a whole operand reads as the fraction nearest it first, the same widening every mixed operation performs, and the division rounds once more, so two implementations spell the same quotient bit for bit.
- `remainder` truncates toward zero, for wholes and fractions alike: what is left takes the dividend's sign, so `-7 remainder 3` is `-1`, `7 remainder -3` is `1` and `-5.5 remainder 2.0` is `-1.5`. A zero divisor **refuses at the run**, the same as under `dividedBy`.
- A whole number where a fraction is expected widens; the reverse refuses.

What a host brings beyond these (its own procedures, and which of them answer without running) is the host's, and is the boundary to the outside world: a program reaches nothing except by sending a procedure the host declared.

## Cases

What `conformance/` asks about this page, by the name each case's file carries.

- `a-const-body-chooses-a-value-with-select`
- `a-const-map-rewrites-in-order`
- `a-document-gathers-a-collections-own-elements`
- `a-document-writes-a-short-circuiting-connective`
- `a-document-writes-map-over-a-const-slot`
- `a-document-writes-startsWith-over-characters`
- `a-mapped-procedure-chooses-what-it-answers`
- `a-piece-arriving-through-any-is-held-to-the-membership-at-the-run`
- `a-piece-that-is-not-a-closure-refuses`
- `a-procedure-answering-a-collections-own-elements-keeps-the-spelling`
- `a-quotient-widens-its-operands`
- `a-space-carrying-a-mark-is-not-trimmed`
- `a-string-holding-another-is-a-text-question`
- `a-string-not-holding-another-answers-false`
- `a-text-procedure-answers-new-text`
- `a-zero-width-space-is-not-whitespace`
- `abort-sent-null-says-aborted`
- `absolute-drops-the-sign-of-negative-zero`
- `absolute-floored-and-rounded-answer-a-whole`
- `absolute-of-the-minimum-refuses`
- `an-array-slot-that-changes-a-byte-reads-them-out`
- `an-attempt-does-not-catch-overflow`
- `an-operand-of-and-that-answers-no-bool-refuses`
- `append-writes-the-array-in-place`
- `arithmetic-admits-only-numbers`
- `arithmetic-answers-the-kind-it-was-given`
- `arithmetic-divide-by-zero-refuses`
- `arithmetic-divides-to-a-fraction`
- `arithmetic-is-checked-before-it-runs`
- `arithmetic-overflow-refuses`
- `arithmetic-whole-widens-to-fraction`
- `bytes-cross-an-array-slot-in-their-own-spelling`
- `bytes-do-not-order`
- `case-mapping-takes-no-locale`
- `characters-answers-grapheme-clusters`
- `concurrent-map-offers-item-and-index`
- `concurrent-map-over-nothing-answers-nothing`
- `contains-asks-a-collection`
- `count-asks-a-collection`
- `count-of-a-record-is-its-fields`
- `count-of-bytes-is-their-length`
- `cutting-on-nothing-refuses`
- `decoded-keeps-a-byte-order-mark`
- `decoded-reads-bytes-as-text-in-a-named-encoding`
- `decoded-reads-bytes-written-one-by-one`
- `dropping-an-end-answers-the-rest`
- `encoded-writes-text-as-bytes-in-a-named-encoding`
- `encoded-writes-the-code-points-as-they-stand`
- `first-and-last-read-the-ends`
- `first-answers-the-first-success`
- `first-in-which-nothing-succeeds-fails-with-every-piece`
- `first-over-nothing-refuses`
- `floored-past-the-int-refuses`
- `fraction-arithmetic-with-no-finite-answer-refuses`
- `gathering-past-the-end-refuses`
- `gathering-reads-positions-written-as-bytes`
- `greater-than-mirrors-less-than`
- `indexing-bytes-answers-a-whole-number`
- `joined-over-nothing-answers-empty-text`
- `keys-answer-in-canonical-order`
- `lowercased-ends-a-word-with-final-sigma`
- `lowercased-folds-the-case`
- `map-answers-in-the-collections-order`
- `map-takes-only-an-isolated-closure`
- `max-answers-rhs-on-a-tie`
- `min-and-max-pick-an-end`
- `min-answers-lhs-on-a-tie`
- `minus-and-times-compose-as-written`
- `minus-off-the-ints-edge-refuses`
- `not-and-notequal-say-the-opposite`
- `or-does-not-ask-past-the-first-yes`
- `ordering-compares-two-of-a-kind`
- `prepending-writes-the-front`
- `reduce-folds-in-order`
- `remainder-at-the-ints-minimum-answers`
- `remainder-by-zero-refuses`
- `remainder-is-what-whole-division-leaves`
- `remainder-takes-the-sign-of-the-dividend`
- `replacing-swaps-every-occurrence`
- `reversed-turns-the-order-around`
- `rounded-past-the-int-refuses`
- `setting-answers-a-new-record`
- `setting-refuses-a-key-that-is-not-a-name`
- `sorted-orders-what-it-was-given`
- `sorting-the-unorderable-refuses`
- `split-cuts-and-joined-writes`
- `split-keeps-the-empty-pieces`
- `starts-with-reads-the-head`
- `text-counts-as-a-person-reads`
- `text-of-a-procedure-spells-a-marker`
- `text-of-null-spells-null`
- `text-spells-a-record-on-one-line`
- `text-spells-bytes-the-way-a-document-writes-them`
- `the-side-select-does-not-choose-goes-unasked`
- `times-off-the-ints-edge-refuses`
- `trimming-takes-unicode-whitespace-from-both-ends`
- `uppercased-uses-unicode-full-case-mapping`
- `values-answer-in-canonical-order`
- `what-is-not-utf8-text-refuses-to-decode`
