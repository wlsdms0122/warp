# The standard vocabulary

The procedures every implementation brings, what each answers, and which of
them an implementation has to write in native code rather than take from
`lib/std`. This is the layer a program does its work in: the language has no
arithmetic, no comparison and no collections of its own, and a program that is
granted none of these can compute nothing.

Seven bundles, each taken with what it depends on, so a receiver grants what
its programs have use for and no more. A bundle whose procedures are written in
Warp names the ones they call: `std.logic` and `std.collection` walk, so they
send `std.math.lessThan` and link only with `std.math` in the link. `std` is the
shared ground: it declares no procedures, only the constraints the other
bundles' signatures mention, and a bundle mentioning them (`std.math`,
`std.collection`) links only with `std` in the link:

| module | procedures |
|---|---|
| `std` |. Declares the memberships `Numeric`, `Comparable` and `Collection`, and the type `byte = int(0...255)` |
| `std.logic` | `equal` `notEqual` `not` `and` `or` `select` |
| `std.math` | `plus` `minus` `times` `dividedBy` `remainder` `min` `max` `absolute` `floored` `rounded` `lessThan` `greaterThan` |
| `std.text` | `text` `characters` `contains` `startsWith` `regex` `uppercased` `lowercased` `trimmed` `split` `joined` `replacing` `decoded` `encoded` |
| `std.collection` | `append` `count` `contains` `first` `last` `reversed` `appending` `prepending` `gathering` `dropFirst` `dropLast` `sorted` `map` `filter` `reduce` `keys` `values` `setting` |
| `std.control` | `abort`. Declared `returns: never` |
| `std.concurrent` | `all` `first` `map`. Run closures at once. Declares the membership `Pieces` |

## What an implementation must write

Not all of these. Most are written in Warp, from a small set that cannot be:
**builtin**. An implementation writes the builtin procedures in its own language
and takes the rest as a Warp module, the way any other module arrives.

| bundle | builtin |
|---|---|
| `std.logic` | `equal` |
| `std.math` | `plus` `minus` `times` `dividedBy` `remainder` `lessThan` `floored` `rounded` |
| `std.text` | `text` `joined` `characters` `uppercased` `lowercased` `encoded` `decoded` `trimmed` |
| `std.collection` | `count` `appending` `gathering` `keys` `setting` |
| `std.control` | `abort` |
| `std.concurrent` | `all` `first` |

Twenty-five, beside the memberships and the `byte` type `std` declares. What
makes one builtin is that the language cannot express it: arithmetic and
ordering are the machine's, case mapping and encoding carry Unicode's tables
with them, running at once is the host's scheduler, `appending` is the only way
an array grows, and `gathering` the only way an answer keeps the spelling its
receiver arrived in. Everything else is written from those.

A procedure being derivable is not a claim that it is unimportant, and a
document cannot tell the two apart: `greaterThan` is `lessThan` with its sides
swapped, and both are called the same way. An implementation that wants its own
`greaterThan` declares one under that name in a module it lays in the link **in
place of** the written one, and the link takes it: one name has one declarer,
and which body stands behind it is the receiver's, which is what every name
outside the builtin set is open to.

One of these is builtin for a reason that is not the set it removes. `trimmed`
names that set, and a body written from `characters` still could not answer it:
`characters` answers characters, and whether a character is whitespace is a
question about the code points inside it.

`regex` is the one procedure `std` declares that is in neither set. It cannot be
written in Warp and it is not required of an implementation: what a pattern
means differs between the engines a host would reach for, so a host brings this
one or leaves it out, the way it grants any bundle. A document reaching for it
is asking for something of its host rather than of the language.

**A bundle is not a module.** A module is compiled against the modules standing
before it, so the modules of a link have to have an order, and two that send to
each other have none. What a bundle declares for its host to answer has no body
and so waits for nothing; what it writes in Warp sends to whatever it needs. An
implementation that lands both halves of a bundle in one module holds the
builtin half to the written half's order, and two bundles whose written halves
lean on each other then have no order at all: `std.logic` walks, so it sends
`std.collection.count`, and a collection procedure comparing two elements sends
`std.logic.equal`. Landing them apart is how the same set of procedures links,
and it is what an implementation weighs when it writes a procedure in Warp
rather than in its own language.

**The signatures, exactly.** A second implementation writes these; it must not
have to guess them. The *receiver* column is the parameter a call fills by
writing a receiver in front (the `of` key in a `call`); everything else is
written by name under `arguments`. A parameter with a `default` may be left out.
A slot typed `const procedure` takes only a procedure that answers without
running.

*std.logic*

| procedure | receiver | arguments | answers |
|---|---|---|---|
| `equal`, `notEqual` | `of: any = null` | `value: any = null` | `bool` |
| `not` | `of: bool` |. | `bool` |
| `and`, `or` | `of: array<const procedure>` |. | `bool`. Over nothing, `and` answers `true` and `or` answers `false`: no side settled the answer, so the chain's own answer stands |
| `select` | `of: bool` | `then`, `else`. `const` procedures taking nothing, each answering `some Answer` | `some Answer` |

`and` and `or` take procedures precisely so they need not run them all: the
sides are read in order and the procedure stops at the first side that settles
the answer. The first false, the first true. What follows the stop is never
evaluated. `select` takes them for the same reason and asks exactly one, so a
side that would refuse is never a refusal of the side that was chosen. `equal`
and `notEqual` answer by the value model's one sameness, and `not` turns a
`bool` around.

**`select` is how an operand chooses.** A `conditional` answers nothing and
takes no name, and an operand is read rather than run, so choosing among values
inside one is a procedure here rather than grammar. The two sides answer one
type, worked out from the call the way any type parameter is.

*std.math*

| procedure | receiver | arguments | answers |
|---|---|---|---|
| `plus`, `minus`, `times`, `remainder` | `of: some N` | `value: some N` | `some N`. Bounds `N: Numeric` |
| `min`, `max` | `of: some N` | `value: some N` | `some N`. Bounds `N: Comparable` |
| `dividedBy` | `of: some N` | `value: some N` | `double`. Bounds `N: Numeric` |
| `absolute` | `of: some N` |. | `some N`. Bounds `N: Numeric` |
| `floored`, `rounded` | `of: number` |. | `int` |
| `lessThan`, `greaterThan` | `of: some T` | `value: some T` | `bool`. Bounds `T: Comparable` |

`floored` goes to the nearest whole toward the smaller side, below zero too:
`-2.1` floors to `-3`. `rounded` goes to the nearest whole, and away from zero
at the exact halfway: `2.5` rounds to `3`, `-2.5` to `-3`. `absolute` drops
the sign and keeps the kind it was given. Each of these answers an `int` only
when an int holds the answer. The int's edge refuses at the run, as the
edge rules below require.

*std.text*

| procedure | receiver | arguments | answers |
|---|---|---|---|
| `text` | `of: any` |. | `string` |
| `contains`, `startsWith`, `regex` | `of: string` | `value: string` | `bool` |
| `uppercased`, `lowercased`, `trimmed` | `of: string` |. | `string` |
| `characters` | `of: string` |. | `array<string>` |
| `split` | `of: string` | `value: string` | `array<string>` |
| `joined` | `of: array<string>` | `value: string = ""` | `string` |
| `decoded` | `of: bytes` | `encoding: string = "utf8"`, enum `["utf8"]` | `string`. **refuses at the run** when the bytes are not text in that encoding |
| `encoded` | `of: string` | `encoding: string = "utf8"`, enum `["utf8"]` | `bytes` |
| `replacing` | `of: string` | `value: string`, `with: string` | `string` |

`characters` answers the text as an array of its characters, each one a string
of its own, counted the way `count` counts. Answered for the whole text rather
than read one at a time: a character is an extended grapheme cluster, so where
the tenth one starts is only known by walking the nine in front of it, and a
body reading them in order would pay that walk every round.

**Two bundles declare `contains`, and they ask different questions.**
`std.collection.contains` asks whether an array holds an element;
`std.text.contains` asks whether a string holds another string inside it. They
are two procedures because a string is not an array here: it has a `count` but
no elements to read by position, since where the tenth character starts is only
known by walking the nine in front of it. A program that wants a string's
characters as a collection asks `characters` for them.

`trimmed` removes the whitespace at either end and nothing from the middle. A
character goes only if **every one of its code points** has Unicode's
`White_Space` property, and nothing a platform adds to that set is whitespace
here. Both halves of that rule are load-bearing: `\r\n` is one character and
two code points, both of them `White_Space`, so it goes; a space carrying a
combining mark is also one character and two code points, and the mark is not
`White_Space`, so it stays where it was written. A zero-width space is not
whitespace in Unicode and so is not trimmed, however a platform's own set
answers.

`regex` answers whether the pattern matches *anywhere* in the text. A program
asking about the whole anchors the pattern itself (`^…$`). A pattern that does
not compile, written as a constant, refuses before the run the way any constant
argument does. `replacing` rewrites every occurrence, not only the first.
`split` keeps the empty pieces a separator at either end leaves, since dropping
them would be an opinion about the text rather than a reading of it. Both refuse
a separator holding no characters, which would match everywhere and consume
nothing; the refusal is `aborted`, so an attempt around either catches it. The procedures that
read text, `contains` and `startsWith` included, read as a person reads, under
the value model's canonical equivalence.

`text` spells a value in its own spelling, which is the type's and not a
document's. A string is its own characters, unquoted; a number, `null` and a
bool are the spelling a document writes; bytes are `x` and their hex digits. A
container it spells on **one line**: an array's elements between `[` and `]`,
a dictionary's entries between `{` and `}` as the key quoted, a colon and the
value, a named record the same with its name and a space before the brace,
entries in **name order** ascending as `keys` answers them, elements or entries
joined by commas with no space, and an empty one `[]` or `{}`. Inside a
container a string or bytes is quoted the way a string in that position is
quoted, so `text` of `[x"6869"]` is `["x\"6869\""]` and of `[1, 2]` is
`[1,2]`: a value's spelling does not change with how deep it sits. What no
document carries answers in the language's own markers, never a host
formatter's: a procedure is `<procedure>`, a host's non-finite fraction is
`<infinity>`, `<-infinity>` or `<not a number>`, and a container holding one
shows whole as `<unencodable>`. This is what `text` is for. A person reading a
value. A carrier that has to give the value *back* is a different question,
and one with no compact spelling writes what `bytes = array<byte>` says
instead: the array.

*std.collection*

| procedure | receiver | arguments | answers |
|---|---|---|---|
| `append` | `to: inout array<some Element>` | `value: some Element` | `null`, having written the element onto the end of the array the variable holds, in place |
| `count` | `of: Collection`. The membership of `string`, `array` and `dictionary`; bytes stand as an array and a record as a dictionary |. | `int` |
| `contains` | `of: array<some Element>` | `value: some Element` | `bool` |
| `first`, `last` | `of: array<some Element>` |. | `some Element`. Over nothing there is no element to answer, and the read of one **refuses at the run**, the way any index past the end does |
| `reversed`, `dropFirst`, `dropLast` | `of: array<some Element>` |. | `array<some Element>` |
| `sorted` | `of: array<some Element>` |. | `array<some Element>`. Bounds `Element: Comparable` |
| `appending`, `prepending` | `of: array<some Element>` | `value: some Element` | `array<some Element>` |
| `gathering` | `of: array<some Element>` | `value: array<int>`. Where to read, in the order to read it | `array<some Element>`, the receiver's own, in the receiver's spelling. A position the receiver does not hold refuses at the run |
| `map` | `of: array<some Element>` | `value`. `const` procedure, handed `item`, answering `some Answer` | `array<some Answer>` |
| `filter` | `of: array<some Element>` | `value`. `const` procedure, handed `item`, answering `bool` | `array<some Element>` |
| `reduce` | `of: array<some Element>` | `from: some Carried`; `value`. `const` procedure, handed `carried` and `item`, answering `some Carried` | `some Carried` |
| `keys` | `of: dictionary<any>` |. | `array<string>` |
| `values` | `of: dictionary<some Entry>` |. | `array<some Entry>` |
| `setting` | `of: dictionary<any>` | `key: string`, `value: any` | `dictionary<any>` |

`gathering` is how a procedure answers its receiver's own elements. It says which
by position, and the answer comes back in the spelling the receiver arrived in:
bytes rearranged are bytes. This is the whole of what `reversed`, `dropFirst`,
`dropLast`, `filter` and `sorted` add to a walk, and it is the reason those are
written in Warp rather than asked of an implementation. A body that read the
elements out and put them back would answer an array of numbers, because an
array it started empty has no spelling to keep. The standard name for reading
one collection at another's positions is a **gather**.

*std.control*

| procedure | receiver | arguments | answers |
|---|---|---|---|
| `abort` | `of: any`. What the refusal says. Null says `aborted` |. | `never` |

*std.concurrent*

| procedure | receiver | arguments | answers |
|---|---|---|---|
| `all`, `first` | `of: Pieces`. The membership of `array<isolated procedure>` and `dictionary<isolated procedure>` |. | `any` |
| `map` | `over: array<some Element>` | `by`. `isolated procedure`, handed `item` and `index`, answering `some Answer` | `array<some Answer>` |

**`std.concurrent`**. Running closures at once. `all` takes a record or an array
of closures, runs every one, and answers every answer. A record's under its
keys, an array's in its order; a failure fails the whole procedure with every
piece's failure reported, keyed by the piece it came from. `first` takes the
same and answers the first success, asking the rest to stop, which piece wins is
the one timing fact this language admits. `map` takes a collection and one
closure, calls it once per element. Each call handed `item` and `index`, and
the closure's own signature says which it reads, and answers in the collection's
order. These are procedures rather than grammar because a closure is already the
safe unit of concurrent work, and being procedures makes concurrency a
permission: what a receiver does not link, a program cannot do.

The names are plain ones with the module carrying the context, the way
`Array.map` and `TaskGroup.next` lean on their types. A call site spells the
module, so `std.collection.first` and `std.concurrent.first` are two names, and
a link carrying both bundles holds both: every `first` and every `map`, the
sequential ones included, is written with its bundle, and concurrency shows at
the call site.

What the checking sees: `map` declares its types the way the sequential one
does. The collection's `Element` meets the closure's parameter, and the
answer's type is the closure's answer, checked at the build. Its `by` is an
`isolated procedure<(item: some Element, index: int) -> some Answer>`, so a
closure that writes a captured variable refuses there before anything runs.
`all` and `first` take `std.concurrent.Pieces`, the membership of
`array<isolated procedure>` and `dictionary<isolated procedure>`, so a piece
that is not a closure and a piece that writes what it captured both refuse at
the build. They answer `any`: the answer is shaped like what went in, and a
membership names a set of types rather than tying one of them to another. What
a fan-out's answer feeds is checked from `map`, not from these two.

What the procedures hand their closures is one convention, shared with the
sequential walks. `std.collection.map` hands over `item`, `reduce` hands over
`carried` and `item`, `std.concurrent.map` hands over `item` and `index`, and a
closure written for one of them **declares every name it is handed**, whether or
not its body goes on to read one. A name the closure does not declare refuses,
the same as anywhere else a call is settled: a walk is not a second calling
convention. `std.concurrent.first` run over nothing is refused, the way
`std.collection.first` of nothing is: a procedure that answers exactly one
thing has no empty answer. And a `first` in which nothing succeeds fails the
way `all` fails: every piece's failure reported, keyed by the piece it came
from.

What the vocabulary answers about **bytes**: `bytes = array<byte>`. Bytes are
not a special material. They are the compact spelling of an array of small whole
numbers, `byte` being the range `int(0...255)` that `std` declares. The equation
is read everywhere the types are, and **the spelling is the value's own fact
rather than the slot's**: a bytes value stands where `array<int>` is declared
and crosses it *whole*, because the slot asked for an array and bytes are one.
There is nothing to settle, and unpacking would spend an element per byte to
answer questions like `first` that read one. An `array<…>` slot reads the bytes
out one by one only where its element declaration would not leave a byte as it
is: `array<double>` changes every one of them, a range narrower than `byte` has
something to ask of each, and a fraction range (`double(0.0...255.0)`) is both.
It widens every byte it takes. An element declared as a **bounded** type
parameter asks each value for its membership, and a member of the constraint
that takes every byte answers that for all of them at once, so `sorted`, whose
element carries `Comparable`, reads a compact spelling the way `reversed` does
rather than by whether its declaration happened to carry a bound. An array of
byte worths standing where `bytes` is declared does settle to the compact
spelling. The asymmetry is the declaration's: naming `bytes` names a spelling,
naming `array<…>` names a type bytes already have.

An index reads an element out as a `byte`, the range `std` names, and so does
`some Element` filled by bytes: `first` of bytes answers a `byte`. The
collection vocabulary. `count`, `first`, `contains`, `reversed`, `map`, all of it. Applies
directly. A procedure that answers its receiver's **own** elements. `reversed`,
`filter`, `sorted`, `dropFirst`, `dropLast`. Answers them in the spelling they
arrived in, so bytes stay bytes; put something among them that is not a byte
(`appending` a `300`) and the answer is the array it now is. A procedure that
builds **new** elements does not: `map` answers whatever its procedure answered,
which its declaration says by naming a second type parameter for it. Two bytes
*values* still do **not** order, for the array reason rather than an opacity
one: `Comparable` admits numbers and strings among themselves, not collections.
Reading bytes *as* text is a procedure that names its encoding: `decoded` and
`encoded` are the two directions of one mapping (`encoding: "utf8"`, the default
and today the only member), and bytes that are not text in that encoding
**refuse at the run**. Completing a broken sequence would answer a text nobody
sent.

**`abort`**. Fail on purpose, with a message. Declared `returns: never`, which
is everything the checking needs: nothing runs after it, and no name binds it.
The message is what `of` spells as text. Sent null, the refusal says `aborted`.
The refusal it raises is a failure like any other, so an `attempt` around it
catches it. Leaving is what a rescue does not catch, and this is failing, not
leaving.

Behaviour at the edges. Where implementations quietly differ, so stated as
requirements:

- Arithmetic takes two of a kind and answers that kind: both sides and the
  answer are one type parameter, bounded by `Numeric`. A whole number added to
  text **refuses at the build**, and so do two pieces of text, because
  agreement is not admission.
- Ordering (`lessThan`, `greaterThan`, `sorted`, `min`, `max`) compares two of a
  kind under `Comparable`, and text is a kind. A kind the constraint does not
  admit refuses at the build where the text says so, and at the boundary where
  the value arrives through `any`.
- Whole-number arithmetic with no whole answer **refuses at the run**. It does
  not wrap and does not silently widen. The rule covers every standard
  procedure that answers an `int` and can miss it: `plus`, `minus`, `times` off
  the int's edge, `absolute` of the int's own minimum, and `floored`/`rounded`
  of a fraction whose whole part is past the int. `remainder` is not on the
  list because its answer always fits. A remainder is smaller than its
  divisor, and the one divisor that trips a machine's division instruction
  still has one: `-9223372036854775808 remainder -1` answers `0`. These
  run-stage refusals. Overflow, and the zero divisor below. Are the
  program's own defect, not a failure of the work: an `attempt` does **not**
  catch them, the way it does not catch an index past the end. What a rescue
  catches is `abort` and a procedure's own failure.
- Fraction arithmetic with no finite answer **refuses at the run** for the
  same reason: infinity is a value the arithmetic can reach and no document
  can carry, and a value that exists only until someone writes it down is not
  an answer.
- `dividedBy` answers a fraction, whole or not. Division by zero **refuses at
  the run**. The quotient is binary64's own: a whole operand reads as the
  fraction nearest it first. The same widening every mixed operation
  performs, and the division rounds once more, so two implementations spell
  the same quotient bit for bit.
- A whole number where a fraction is expected widens; the reverse refuses.

What a host brings beyond these. Its own procedures, and which of them answer
without running. Is the host's, and is the boundary to the outside world:
a program reaches nothing except by sending a procedure the receiver declared.

## Cases

What `conformance/` asks about this page, by the name each case's file carries.

- `a-const-body-chooses-a-value-with-select`
- `a-const-map-rewrites-in-order`
- `a-document-gathers-its-receivers-own-elements`
- `a-document-writes-a-short-circuiting-connective`
- `a-document-writes-map-over-a-const-slot`
- `a-document-writes-startsWith-over-characters`
- `a-mapped-procedure-chooses-what-it-answers`
- `a-quotient-widens-its-operands`
- `a-string-holding-another-is-a-text-question`
- `a-string-not-holding-another-answers-false`
- `a-text-procedure-answers-new-text`
- `a-zero-width-space-is-not-whitespace`
- `abort-sent-null-says-aborted`
- `absolute-floored-and-rounded-answer-a-whole`
- `absolute-of-the-minimum-refuses`
- `append-writes-the-array-in-place`
- `arithmetic-admits-only-numbers`
- `arithmetic-answers-the-kind-it-was-given`
- `arithmetic-divide-by-zero-refuses`
- `arithmetic-divides-to-a-fraction`
- `arithmetic-is-checked-before-it-runs`
- `arithmetic-overflow-refuses`
- `arithmetic-whole-widens-to-fraction`
- `bytes-do-not-order`
- `concurrent-map-offers-item-and-index`
- `contains-asks-a-collection`
- `count-asks-a-collection`
- `count-of-a-record-is-its-fields`
- `count-of-bytes-is-their-length`
- `cutting-on-nothing-refuses`
- `decoded-reads-bytes-as-text-in-a-named-encoding`
- `dropping-an-end-answers-the-rest`
- `encoded-writes-text-as-bytes-in-a-named-encoding`
- `first-and-last-read-the-ends`
- `first-over-nothing-refuses`
- `floored-past-the-int-refuses`
- `gathering-past-the-end-refuses-at-the-run`
- `greater-than-mirrors-less-than`
- `keys-answer-in-canonical-order`
- `lowercased-folds-the-case`
- `map-answers-in-the-collections-order`
- `map-takes-only-an-isolated-closure`
- `min-and-max-pick-an-end`
- `minus-and-times-compose-as-written`
- `not-and-notequal-say-the-opposite`
- `or-does-not-ask-past-the-first-yes`
- `ordering-compares-two-of-a-kind`
- `prepending-writes-the-front`
- `reduce-folds-in-order`
- `regex-finds-a-match-anywhere`
- `remainder-at-the-ints-minimum-answers`
- `remainder-is-what-whole-division-leaves`
- `replacing-swaps-every-occurrence`
- `reversed-turns-the-order-around`
- `setting-answers-a-new-record`
- `sorted-orders-what-it-was-given`
- `sorting-the-unorderable-refuses-at-the-build`
- `split-cuts-and-joined-writes`
- `split-keeps-the-empty-pieces`
- `starts-with-reads-the-head`
- `text-counts-as-a-person-reads`
- `text-spells-bytes-the-way-a-document-writes-them`
- `the-side-select-does-not-choose-goes-unasked`
- `trimming-takes-unicode-whitespace-from-both-ends`
- `values-answer-in-canonical-order`
- `what-is-not-utf8-text-refuses-to-decode`
