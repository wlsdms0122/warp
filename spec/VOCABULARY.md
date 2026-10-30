# The standard vocabulary

The procedures every implementation brings, what each returns, and which of them an implementation has to write in its own language rather than take from `lib/standard`. This is the layer a program does its work in: the language has no arithmetic, no comparison and no collections of its own, and a program that is granted none of these can compute nothing.

Eight bundles, each taken with what it depends on, so a host grants what its programs have use for and no more. What a bundle depends on is what its written half sends and what its signatures mention, and the written half's `imports` is the list. `Standard` is the shared ground: the contracts `Standard.Numeric`, `Standard.Comparable` and `Standard.Collection`, the claims putting the types the language names under them, and the procedures backing those claims. Every bundle below links with `Standard` in the link, and a document calling a contract's procedure stands behind it, so what the call reaches stands before the document does. A contract and a bundle may share a spelling: `Standard.Collection.count` is the contract `Standard.Collection`'s procedure, declared by `Standard`, and the bundle `Standard.Collection` is the bundle whose procedures the table lists in its row. Beyond that, `Standard.Math`, `Standard.Logic`, `Standard.Optional` and `Standard.Control` stand alone; `Standard.Collection` links with `Standard.Logic`; `Standard.Concurrent` with `Standard.Collection`; `Standard.Text` with `Standard.Collection`, `Standard.Control` and `Standard.Logic`. Two bundles that send to each other are not a cycle, because a bundle is not a module, below:

| bundle | procedures |
|---|---|
| `Standard` | The contracts below, the claims putting the types the language names under them, and the procedures backing those claims: `Int.plus` `Int.minus` `Int.times` `Int.dividedBy` `Int.remainder` `Int.lessThan`, the same six for `Double`, `String.lessThan`, and `Array.count` `Dictionary.count` `String.count` |
| `Standard.Logic` | `equal` `notEqual` `not` `and` `or` `select` `tryAnd` `tryOr` `trySelect` |
| `Standard.Math` | `min` `max` `absolute` `floored` `rounded` `greaterThan` |
| `Standard.Text` | `text` `characters` `contains` `startsWith` `uppercased` `lowercased` `trimmed` `split` `joined` `replacing` `decoded` `encoded` |
| `Standard.Collection` | `append` `contains` `first` `last` `reversed` `appending` `prepending` `gathering` `dropFirst` `dropLast` `sorted` `map` `filter` `reduce` `tryMap` `tryFilter` `tryReduce` `keys` `values` `setting` |
| `Standard.Optional` | `unwrapped` `tryUnwrapped` |
| `Standard.Control` | `abort`. Nothing runs after it |
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

Thirty-six, beside the contracts `Standard` declares. What makes one builtin is that the language cannot express it: arithmetic, ordering and counting are the machine's, written once for each type conforming to the contract that asks them, case mapping and encoding carry Unicode's tables with them, running at once is the host's scheduler, `appending` is the only way an array grows, and `gathering` the only way a return value keeps the spelling its collection arrived in. Everything else is written from those.

`greaterThan` is `lessThan` with its sides swapped, and both are called the same way.

One of these is builtin for a reason that is not the set it removes. `trimmed` names that set, and a body written from `characters` still could not compute it: `characters` returns characters, and whether a character is whitespace is a question about the code points inside it.

**A bundle is not a module.** A module is compiled against the modules standing before it, so the modules of a link have to have an order, and two that send to each other have none. What a bundle declares for its host to implement has no body and so waits for nothing; what it writes in Warp sends to whatever it needs. So a bundle links as two modules, its builtin half standing before every written half, and the same set of procedures links whatever the written halves send. A bundle with nothing builtin, `Standard.Optional`, links as its written half alone.

**The signatures are the standard vocabulary's interface**, [`lib/standard/interface/standard.interface.warpt`](../lib/standard/interface/standard.interface.warpt), under *an interface* in [the text](TEXT.md). It declares every contract, claim and procedure this page names, builtin or written in Warp alike, and it is the authority for each one's parameters and their order, what each parameter and the procedure return, the bounds, and whether the procedure is `const`, touches no name another body could touch at once (`isolated`) and what it fails with. An implementation brings a standard vocabulary that declares exactly it, and a front end writes calls against it. This page says what each procedure does: the *parameters* column names a parameter to say of it what its type does not.

**A procedure that takes procedures runs them, and its name says whether they may fail.** Where a caller would hand a `Standard.Collection`, `Standard.Logic` or `Standard.Optional` row a procedure that may fail, the row has a twin named `try` and then its own name with the first letter upper-cased, `map` and `tryMap`, which takes one that may fail with anything and fails with what it fails with. The two are two procedures under two names: a call reads the one it names and nothing chooses between them.

*Standard.Logic*

| procedure | parameters | returns |
|---|---|---|
| `equal`, `notEqual` | `lhs`, `rhs` | whether the two are one value, and whether they are not |
| `not` | `value` | the other `Bool` |
| `and`, `or`, `tryAnd`, `tryOr` | `conditions`, the sides, each a procedure taking nothing, so one returning anything but a `Bool` **refuses at the build** where it is handed | whether every side returns `true`, and whether some side does. Over nothing, `and` and `tryAnd` return `true` and `or` and `tryOr` return `false`: no side decided the result, so the chain's own result stands |
| `select`, `trySelect` | `condition`, `then`, `else`, the two sides each a procedure taking nothing | what the side `condition` chooses returns |

`and` and `or` take procedures precisely so they need not run them all: the sides are read in order and the procedure stops at the first side that decides the result. The first false, the first true. What follows the stop is never evaluated. `select` takes them for the same reason and asks exactly one, so a side that would refuse is never a refusal of the side that was chosen. `equal` and `notEqual` decide by the value model's one sameness, and `not` turns a `Bool` around.

**`select` is how an operand chooses.** A `conditional` has no value, under [statements](STATEMENT.md), and an operand is read rather than run, so choosing among values inside one is a procedure here rather than grammar. The two sides return one type, worked out from the call the way any type parameter is.

*Standard*

The contracts. A call writes the contract's spelling, `Standard.Numeric.plus`, and the run picks the declaration satisfying it by the type that fills `Self`, under *calling a contract's procedure* in [types](TYPE.md): `Int.plus` for an `Int`, `Double.plus` for a `Double`.

| contract | procedure | parameters | returns |
|---|---|---|---|
| `Standard.Numeric` | `plus`, `minus`, `times`, `remainder` | `lhs`, `rhs` | the sum, the difference, the product and the remainder |
| `Standard.Numeric` | `dividedBy` | `lhs`, `rhs` | the quotient, a `Double` |
| `Standard.Comparable` | `lessThan` | `lhs`, `rhs` | whether `lhs` orders before `rhs` |
| `Standard.Collection` | `count` | `collection` | how many it holds |

| type | claims |
|---|---|
| `Int`, `Double` | `Standard.Comparable`, `Standard.Numeric` |
| `String` | `Standard.Collection`, `Standard.Comparable` |
| `Array`, `Dictionary` | `Standard.Collection` |

`count` reads a list's elements, bytes included, a dictionary's entries, and a string's characters as a person reads them. A declared struct is an instance of its own name, so `count` takes one only where a document claims `Standard.Collection` for it.

*Standard.Math*

| procedure | parameters | returns |
|---|---|---|
| `min`, `max` | `lhs`, `rhs` | the lesser and the greater of the two |
| `absolute` | `number` | the number without its sign |
| `floored`, `rounded` | `number` | the integer it floors to and the integer it rounds to |
| `greaterThan` | `lhs`, `rhs` | whether `lhs` orders after `rhs` |

`min` and `max` return one of the two as it arrived. On a tie, where the two order the same, `min` returns `lhs` and `max` returns `rhs`, so `min(0.0, -0.0)` is `0.0` and `max(0.0, -0.0)` is `-0.0`.

`floored` goes to the nearest integer toward the smaller side, below zero too: `-2.1` floors to `-3`. `rounded` goes to the nearest integer, and away from zero at the exact halfway: `2.5` rounds to `3`, `-2.5` to `-3`. `floored` and `rounded` return an `Int`, and only where an `Int` holds the result. `absolute` drops the sign and keeps the type it was given. The int's edge refuses at the run, as the edge rules below require.

*Standard.Text*

| procedure | parameters | returns |
|---|---|---|
| `text` | `value` | its spelling |
| `contains` | `text`, `other` | whether `other` stands inside `text` |
| `startsWith` | `text`, `prefix` | whether `text` begins with `prefix` |
| `uppercased`, `lowercased`, `trimmed` | `text` | the text upper-cased, lower-cased and trimmed |
| `characters` | `text` | its characters, each a string |
| `split` | `text`, `separator` | the pieces between the separators |
| `joined` | `strings`, `separator`, written between each two | the strings joined |
| `decoded` | `bytes`, `encoding` | the text the bytes are in the encoding. **refuses at the run** when an element is no byte (an integer from 0 to 255), the encoding is not one it has, or the bytes are not text in it |
| `encoded` | `text`, `encoding` | the bytes the text is in the encoding. **refuses at the run** when the encoding is not one it has |
| `replacing` | `text`, `target`, `replacement` | the text with every occurrence of the target replaced |

`characters` returns the string as an array of its characters, each one a string of its own, counted the way `count` counts. Computed for the whole string rather than read one at a time: a character is an extended grapheme cluster, so where the tenth one starts is only known by walking the nine in front of it, and a body reading them in order would pay that walk every round.

**Two bundles declare `contains`, and they ask different questions.** `Standard.Collection.contains` asks whether an array holds an element; `Standard.Text.contains` asks whether a string holds another string inside it. They are two procedures because a string is not an array here: it has a `count` but no elements to read by position, since where the tenth character starts is only known by walking the nine in front of it. A program that wants a string's characters as a collection asks `characters` for them.

`uppercased` and `lowercased` apply Unicode's full default case mapping and no locale's tailoring: `ß` uppercases to `SS`, a capital sigma ending a word lowercases to the final `ς`, and `i` uppercases to `I` on every machine, whatever its locale says about a dotted `i`.

`trimmed` removes the whitespace at either end and nothing from the middle. A character goes only if **every one of its code points** has Unicode's `White_Space` property, and nothing a platform adds to that set is whitespace here. Both halves of that rule are load-bearing: `\r\n` is one character and two code points, both of them `White_Space`, so it goes; a space carrying a combining mark is also one character and two code points, and the mark is not `White_Space`, so it stays where it was written. A zero-width space is not whitespace in Unicode and so is not trimmed, however a platform's own set decides.

`replacing` rewrites every occurrence, not only the first. `joined` over an array with nothing in it returns the empty string, whatever the separator: there is nothing to put between. `split` keeps the empty pieces a separator at either end leaves, since dropping them would be an opinion about the string rather than a reading of it. `split` fails on a separator holding no characters and `replacing` on a target holding none, since either would match everywhere and consume nothing. The failure is `aborted`, so a try around either catches it. The procedures that read strings, `contains` and `startsWith` included, read as a person reads, under the value model's canonical equivalence.

`text` spells a value in its own spelling, which is the type's and not a document's. A string is its own characters, unquoted; a number, a bool and `null` are the spelling a document writes; bytes are `x` and their hex digits. A container it spells on **one line**: an array's elements between `[` and `]`, a dictionary's entries between `{` and `}` as the key, spelled the way any value inside a container is, a colon and the value, a struct its fields the same, each field's name bare as its struct's name is, with its name and a space before the brace, a dictionary's entries in the **key order** `keys` returns them in and a struct's fields by name ascending, elements or entries joined by commas with no space, and an empty one `[]` or `{}`. Inside a container `null` is `null`, and a string, bytes or a procedure is quoted: between double quotes and escaped as the Warp text escapes a string, under [encodings](ENCODING.md), so `text` of `[x"6869"]` is `["x\"6869\""]` and of `[1, 2]` is `[1,2]`: a value's spelling does not change with how deep it sits. What no document carries is spelled in the language's own markers, never a host formatter's: a procedure is `<procedure>`, so `text` of a list holding one is `["<procedure>"]`. This is what `text` is for: a person reading a value. A carrier that has to give the value *back* is a different question, and one with no compact spelling writes bytes as what they are: an array of `Int`.

*Standard.Collection*

| procedure | parameters | returns |
|---|---|---|
| `append` | `array`, a variable handed in place, and `element` | nothing, having written the element onto the end of the array the variable holds, in place |
| `contains` | `array`, `element` | whether the array holds the element |
| `first`, `last` | `array` | the first and the last element, as its some. Over nothing there is no element, and each returns the none, `null`, so over `[null]` of `Array<Int?>` `first` returns the some of the inner none, which the caller tells apart from the none of an empty list |
| `reversed`, `dropFirst`, `dropLast` | `array` | the elements in the other order, without the first and without the last |
| `sorted` | `array` | every element once, in order where `lessThan` is a strict order |
| `appending`, `prepending` | `array`, `element` | the array with the element at the end and at the start |
| `gathering` | `array`, `positions`. Where to read, in the order to read it | the collection's own elements at those positions, in the collection's spelling. A position the collection does not hold refuses at the run |
| `map`, `tryMap` | `array`, `transform`, handed the item | what `transform` returns for each item |
| `filter`, `tryFilter` | `array`, `isIncluded`, handed the item | the items it returns `true` for |
| `reduce`, `tryReduce` | `array`, `initialResult`, `nextPartialResult`, handed the carried value, then the item | the carried value after the last item |
| `keys` | `dictionary` | the keys the dictionary holds, in its key order |
| `values` | `dictionary` | what the dictionary holds, in its key order |
| `setting` | `dictionary`, `key`, `value` | the dictionary with the entry under the key written. The dictionary's keys and the key read as one type, and its entries and the value as another, so two types there that neither takes **refuse at the build** |

`gathering` is how a procedure returns a collection's own elements. It says which by position, and the return value comes back in the spelling the collection arrived in: bytes rearranged are bytes. This is the whole of what `reversed`, `dropFirst`, `dropLast`, `filter` and `sorted` add to a walk, and it is the reason those are written in Warp rather than asked of an implementation. A body that read the elements out and put them back would return an array of numbers, because an array it started empty has no spelling to keep. The standard name for reading one collection at another's positions is a **gather**.

*Standard.Optional*

| procedure | parameters | returns |
|---|---|---|
| `unwrapped`, `tryUnwrapped` | `optional`, `else`, a procedure taking nothing | the payload of a some, and on a none what `else` returns |

`unwrapped` takes its fallback as a procedure for the reason `select` does: only a none asks it, so on a some `else` never runs, and a fallback that would refuse is no refusal of the call. It takes one level off, as `unwrap` does under [statements](STATEMENT.md): over `Int??`, the some of the inner none returns that none, `null`, and `else` is not asked. Both are written in Warp from `unwrap`, so neither is builtin.

*Standard.Control*

| procedure | parameters | returns |
|---|---|---|
| `abort` | `message`. What the failure says. Null says `aborted` | nothing: it fails |

*Standard.Concurrent*

| procedure | parameters | returns |
|---|---|---|
| `all` | `pieces`, a list of procedures taking nothing | each piece's return value, in the pieces' order |
| `allKeyed` | `pieces`, a dictionary of procedures taking nothing | each piece's return value, under its key |
| `first` | `pieces`, a list of procedures taking nothing | the return value of the first piece to succeed |
| `firstKeyed` | `pieces`, a dictionary of procedures taking nothing | the return value of the first piece to succeed |
| `map` | `array`, `transform`, handed the item, then its index | what `transform` returns for each item, in the collection's order |

**`Standard.Concurrent`**. Running closures at once. `all` takes a list of closures, runs every one, and returns every return value in the list's order; `allKeyed` takes a dictionary of closures under keys, and returns each return value under its key. A failure fails the whole procedure with `concurrent_failed`, whose `details` hold `failures`: every piece's failure under the piece's key, a dictionary's piece under the key it stood under and a list's under its position, an `Int`, and each is the envelope that piece raised, so a catch reads a piece's own `type`, `message` and `details` through it. `first` and `firstKeyed` take the same and return the first success, asking the rest to stop; which piece wins is the one timing fact this language admits. A piece that refuses at the run before one succeeds ends the race the way a success does, and refuses the whole run. What a piece does once the rest are asked to stop is not reported. `map` takes a collection and one closure, calls it once per element, handing it the element and then its index, and returns in the collection's order. These are procedures rather than grammar because a closure is already the safe unit of concurrent work, and being procedures makes concurrency a permission: what a host does not link, a program cannot do.

The names are plain ones with the module carrying the context. A call site spells the module, so `Standard.Collection.first` and `Standard.Concurrent.first` are two names, and a link carrying both bundles holds both: every `first` and every `map`, the sequential ones included, is written with its bundle, and concurrency shows at the call site.

What the checking sees comes from the declarations in the interface. `map` is checked the way the sequential one is: the collection's elements against what the closure takes, and what `map` returns is what the closure returns, at the build. Every closure these five run is run at once, so one that writes a captured variable refuses at the build before anything runs, and so does a piece the build reads as something other than a closure; a list or a dictionary literal is held to the slot part by part, so a piece that is not a closure refuses there too, and a list of pieces read as `Any` takes a cast first, the way any value read as `Any` does. Every piece returns the one type the call fills from them; pieces returning two types that neither takes fill it with `Any`, joined part by part the way a literal's parts are, and so does a piece written to return `Any`.

What the procedures hand their closures is one convention, shared with the sequential walks. `Standard.Collection.map`, `filter` and their `try` twins hand over the item, `reduce` and `tryReduce` hand over the carried value then the item, `Standard.Concurrent.map` hands over the item then its index, and a closure written for one of them **declares exactly as many parameters as it is handed, in that order**, under names of its own, whether or not its body goes on to read one. A closure of another count **refuses at the build**, the same as anywhere else a value is called: a walk is not a second calling convention. `Standard.Concurrent.first` run over nothing **refuses at the run**, and so does `firstKeyed` over a dictionary holding nothing: a race needs pieces to run, so a race over nothing is a refusal of the run's shape, not an element that is absent. And a `first` or a `firstKeyed` in which nothing succeeds fails the way `all` and `allKeyed` fail: every piece's failure reported under the piece's key, a dictionary's piece under the key it stood under and a list's under its position, an `Int`.

What the vocabulary says about **bytes**: they are an array of integers from 0 to 255, `Array<Int>`, and `x"6869"` is that array's compact spelling, under [values](VALUE.md). A slot taking bytes is written `Array<Int>`, or any other array the bytes fit. **The spelling is the value's own fact rather than the slot's**: a bytes value stands where `Array<Int>` is declared and crosses it *whole*, because the slot asked for an array and bytes are one. `Array<Double>` takes no byte at all, a byte being an integer. An element declared as a **bounded** type parameter stands for one type the call filled, so `sorted`, whose element carries `Standard.Comparable`, reads a compact spelling the way `reversed` does. An array of byte worths written out one by one stays as written: the compact spelling is the value's, and no slot puts it on.

An index reads an element out as an `Int`, and so does `some Element` filled by bytes: `first` of bytes returns an `Int?`. The collection vocabulary (`count`, `first`, `contains`, `reversed`, `map`, all of it) applies directly. A procedure that returns a collection's **own** elements (`reversed`, `filter`, `sorted`, `dropFirst`, `dropLast`) returns them in the spelling they arrived in, so bytes stay bytes; put something among them that is not a byte (`appending` a `300`) and the return value is the array it is. A procedure that builds **new** elements does not: `map` returns whatever its procedure returned, which its declaration says by naming a second type parameter for it. Two bytes values do **not** order: `Standard.Comparable` is claimed for numbers and strings, not for `Array`. Reading bytes *as* a string is a procedure that names its encoding: `decoded` and `encoded` are the two directions of one mapping (`encoding: "utf8"`, the only encoding they have). `decoded` completes no broken sequence, which would return a string nobody sent. `encoded` writes the string's code points as they stand and normalises nothing, and `decoded` keeps a byte order mark as the character it is: normalising the one or dropping the other would be an opinion about the string rather than a reading of it. The encodings are this specification's: each is one every implementation writes.

**`abort`**. Fail on purpose, with a message. Its declaration is everything the checking needs: nothing runs after it, and no name binds it. The message is what `message` spells as text. Sent null, the failure says `aborted`. It is a failure like any other, so a `try` around it catches it. Leaving is what a catch does not take, and this is failing, not leaving.

Behaviour at the edges, where implementations quietly differ, stated as requirements:

- Arithmetic takes two of one type under `Standard.Numeric`, as the interface declares it. An `Int` added to a `String` **refuses at the build**, and so do two `String`s, because no claim puts `String` under `Standard.Numeric`.
- Ordering (`lessThan`, `greaterThan`, `sorted`, `min`, `max`) compares two of one type under `Standard.Comparable`, `String` among them. A type no claim puts under it, or a reading whose type the build does not know, refuses at the build, under **Bounds** in [types](TYPE.md).
- `Int` arithmetic with no `Int` result **refuses at the run**. It does not wrap and does not silently widen. The rule covers every standard procedure that returns an `Int` and can miss it: `plus`, `minus`, `times` off the int's edge, `absolute` of the int's own minimum, and `floored`/`rounded` of a `Double` whose integer part is past what an `Int` holds. `remainder` is not on the list because its result always fits. A remainder is smaller in size than its divisor, and the one divisor that trips a machine's division instruction still has one: `-9223372036854775808 remainder -1` returns `0`. These run-stage refusals (overflow, and the zero divisor below) are the program's own defect, not a failure of the work: a `try` does **not** catch them, the way it does not catch an index past the end. What a catch takes is `abort` and a procedure's own failure.
- `Double` arithmetic with no finite result **refuses at the run**, at the door its result crosses under [running](RUNNING.md): infinity is a value the arithmetic can reach and no document can carry.
- `dividedBy` returns a `Double`, integral or not. Division by zero **refuses at the run**. The quotient is binary64's own: an `Int` operand reads as the `Double` nearest it first, and the division rounds once more, so two implementations spell the same quotient bit for bit.
- `remainder` truncates toward zero, for `Int` and `Double` alike: what is left takes the dividend's sign, so `-7 remainder 3` is `-1`, `7 remainder -3` is `1` and `-5.5 remainder 2.0` is `-1.5`. A zero divisor **refuses at the run**, the same as under `dividedBy`.
- An `Int` is no `Double`, and a `Double` is no `Int`, under [types](TYPE.md), which says too where an integer literal is read as the `Double` it names.

What a host brings beyond these (its own procedures, and which of them are const) is the host's, and is the boundary to the outside world: a program reaches nothing except by sending a procedure the host declared.

## Cases

What `conformance/` asks about this page, by the name each case's file carries.

- `a-closure-that-may-fail-handed-to-filter-refuses`
- `a-const-body-chooses-a-value-with-select`
- `a-const-map-rewrites-in-order`
- `a-document-gathers-a-collections-own-elements`
- `a-document-writes-a-short-circuiting-connective`
- `a-document-writes-map-over-a-const-slot`
- `a-document-writes-startsWith-over-characters`
- `a-double-divided-by-negative-zero-refuses`
- `a-double-divided-by-zero-refuses`
- `a-list-holding-no-byte-handed-to-decoded-refuses`
- `a-list-of-pieces-joining-to-any-at-a-fan-out-refuses`
- `a-mapped-procedure-chooses-what-it-returns`
- `a-piece-that-is-not-a-closure-refuses`
- `a-procedure-returning-a-collections-own-elements-keeps-the-spelling`
- `a-quotient-reads-an-int-operand-as-the-nearest-double`
- `a-side-not-saying-it-is-isolated-handed-to-and-refuses`
- `a-space-carrying-a-mark-is-not-trimmed`
- `a-string-counts-as-a-person-reads`
- `a-string-holding-another-is-a-string-question`
- `a-string-not-holding-another-returns-false`
- `a-string-procedure-returns-a-new-string`
- `a-zero-width-space-is-not-whitespace`
- `abort-says-its-message-spelled-as-text`
- `abort-sent-null-says-aborted`
- `absolute-drops-the-sign-of-negative-zero`
- `absolute-of-an-int-floored-and-rounded-return-an-int`
- `absolute-of-the-minimum-refuses`
- `all-keyed-returns-under-keys-of-any-type`
- `an-encoding-a-procedure-does-not-have-refuses`
- `an-isolated-body-filters-through-a-closure-that-fails-with-nothing`
- `an-operand-of-and-that-returns-no-bool-refuses`
- `and-over-nothing-returns-true`
- `append-writes-the-array-in-place`
- `arithmetic-divide-by-zero-refuses`
- `arithmetic-divides-to-a-double`
- `arithmetic-on-a-value-it-does-not-take-refuses`
- `arithmetic-on-two-strings-refuses`
- `arithmetic-overflow-refuses`
- `arithmetic-reads-an-integer-literal-beside-a-double-as-the-double`
- `arithmetic-returns-the-type-it-was-given`
- `bytes-at-a-list-of-doubles-refuse`
- `bytes-cross-an-array-slot-in-their-own-spelling`
- `case-mapping-takes-no-locale`
- `characters-returns-grapheme-clusters`
- `comparing-bytes-for-order-refuses`
- `concurrent-map-hands-the-item-then-its-index`
- `concurrent-map-over-nothing-returns-an-empty-list`
- `contains-asks-a-collection`
- `count-of-a-declared-struct-no-claim-names-refuses`
- `count-of-a-number-refuses`
- `count-of-bytes-is-their-length`
- `decoded-keeps-a-byte-order-mark`
- `decoded-reads-bytes-as-a-string-in-a-named-encoding`
- `decoded-reads-bytes-written-one-by-one`
- `decoding-what-is-not-utf8-text-refuses`
- `double-arithmetic-with-no-finite-result-refuses`
- `dropping-an-end-returns-the-rest`
- `encoded-writes-a-string-as-bytes-in-a-named-encoding`
- `encoded-writes-the-code-points-as-they-stand`
- `first-and-last-read-the-ends`
- `first-in-which-nothing-succeeds-fails-with-every-piece`
- `first-keyed-over-a-piece-that-refuses-before-one-succeeds-refuses`
- `first-keyed-over-nothing-refuses`
- `first-of-a-list-of-a-none-is-its-some`
- `first-of-nothing-is-none`
- `first-over-a-piece-that-refuses-before-one-succeeds-refuses`
- `first-over-nothing-refuses`
- `first-returns-the-first-success`
- `floored-past-the-int-refuses`
- `gathering-past-the-end-refuses`
- `gathering-reads-positions-written-as-bytes`
- `greater-than-mirrors-less-than`
- `indexing-bytes-reads-an-int`
- `joined-over-nothing-returns-an-empty-string`
- `keys-of-a-dictionary-keyed-by-hashable-refuses`
- `keys-return-a-dictionarys-own-keys-in-the-key-order`
- `keys-return-in-canonical-order`
- `last-of-a-list-ending-in-a-none-is-its-some`
- `lowercased-ends-a-word-with-final-sigma`
- `lowercased-folds-the-case`
- `map-over-a-closure-not-declaring-isolated-refuses`
- `map-returns-in-the-collections-order`
- `max-returns-rhs-on-a-tie`
- `min-and-max-pick-an-end`
- `min-returns-lhs-on-a-tie`
- `minus-and-times-compose-as-written`
- `minus-off-the-ints-edge-refuses`
- `not-and-notequal-say-the-opposite`
- `or-does-not-ask-past-the-first-yes`
- `or-over-nothing-returns-false`
- `ordering-compares-two-of-one-type`
- `overflow-inside-a-try-refuses`
- `prepending-writes-the-front`
- `reduce-folds-in-order`
- `remainder-at-the-ints-minimum`
- `remainder-by-zero-refuses`
- `remainder-is-what-truncating-division-leaves`
- `remainder-takes-the-sign-of-the-dividend`
- `replacing-nothing-fails`
- `replacing-swaps-every-occurrence`
- `reversed-turns-the-order-around`
- `rounded-past-the-int-refuses`
- `setting-a-key-of-another-type-than-the-dictionarys-refuses`
- `setting-returns-a-new-dictionary`
- `setting-writes-a-key-of-the-dictionarys-own-type`
- `sorted-orders-what-it-was-given`
- `sorted-returns-every-element-where-less-than-is-not-strict`
- `sorting-the-unorderable-refuses`
- `split-cuts-and-joined-writes`
- `split-keeps-the-empty-pieces`
- `split-on-nothing-fails`
- `starts-with-reads-the-head`
- `text-escapes-control-characters-inside-a-container`
- `text-of-a-list-holding-a-procedure-quotes-its-marker`
- `text-of-a-procedure-spells-a-marker`
- `text-of-null-spells-null`
- `text-spells-a-dictionarys-key-as-the-value-it-is`
- `text-spells-a-struct-on-one-line`
- `text-spells-bytes-the-way-a-document-writes-them`
- `the-side-select-does-not-choose-goes-unasked`
- `times-off-the-ints-edge-refuses`
- `trimming-takes-unicode-whitespace-from-both-ends`
- `tryAnd-fails-with-what-its-side-fails-with`
- `tryAnd-over-nothing-returns-true`
- `tryFilter-fails-with-what-its-closure-fails-with`
- `tryMap-fails-with-what-its-closure-fails-with`
- `tryOr-fails-with-what-its-side-fails-with`
- `tryOr-over-nothing-returns-false`
- `tryReduce-fails-with-what-its-closure-fails-with`
- `trySelect-fails-with-what-the-chosen-side-fails-with`
- `tryUnwrapped-fails-with-what-its-closure-fails-with`
- `unwrapped-runs-its-else-only-on-none`
- `unwrapped-takes-one-level-off`
- `uppercased-uses-unicode-full-case-mapping`
- `values-of-a-dictionary-keyed-by-ints-return-in-the-key-order`
- `values-return-in-canonical-order`
