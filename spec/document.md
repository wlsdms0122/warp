# The document format

What a document is: the record a program travels as, and the module it
declares. This page is the outline. What each of its slots holds is
[procedures](procedure.md), [statements](statement.md),
[expressions](expression.md) and [types](type.md), and the bytes it arrives as
are [encodings](encoding.md).

A document is one record. Every record this grammar names, on this page and on
the pages it points to, is **closed**: a key none of them names **refuses**. Every slot marked *expression*, *block*, *statements* or
*type* takes the grammar of that name.

## The module

| key | takes | required |
|---|---|---|
| `warp` | int. The language version this document is written for | yes |
| `imports` | array of strings. Every procedure the program calls and does not declare | yes, and empty where the program uses none |
| `description` | string | no |
| `types` | record: name → type | no |
| `constraints` | record: name → array of types the name admits | no |
| `contracts` | record: name → record: procedure → `{ parameters?, returns? }` | no |
| `satisfies` | record: type name → array of contract names that type answers | no |
| `const` | record: name → expression | no |
| `var` | record: name → expression; a variable every procedure beside it may read and write | no |
| `procedures` | record: name → procedure | yes, and not empty |

**A module variable.** Its start is written like a constant and settles the same
way: at the **build**, from what a constant settles from, beside the constants
and reading them, and them only: one start does not read another variable. Its type is the type of that settled value, and every write
into it is settled against that type. It is private to the document like a constant,
read by the same spelling (`ref`), and written by a `set` in a procedure the
document declares, or through a parameter such a procedure hands it to in place;
another document reaches it only through such a procedure. A name is a constant
or a variable, not both: one declared under both keys **refuses** at the load.
Every run starts each variable at its settled value, so two runs of one image
never see each other.

**The version.** Every document says it, and one that does not **refuses**. As
not a document rather than as a malformed one. A reader that filled in a default
would be answering, on the sender's behalf, the one question that has to be
answerable from the bytes alone; and a file of some other kind entirely would
get as far as having its keys judged. Nobody writes the number by hand anyway. A
front end computes it, so a document without one did not come from one.

The current version is **1**; the earliest that ever existed is **1**.
Pre-release, so the two ends of the reading range are one number. A reader must
refuse a document written for a later version than it implements, before judging
the document's keys. A later version may add keys, and checking the keys first
would turn "I am too old for this" into "this is malformed". A document claiming
a version below the earliest **refuses**. The number goes up when anything
portable changes what an existing program *means*: a type added, a type read
differently, a checking rule moved, a standard procedure answering differently.
It does not move when a procedure is *added*, since a program that does not call
it cannot tell, and one that does is refused by name.

What each version was:

| version | what moved |
|---|---|
| 1 | the language as specified here |

An implementation implements the **current** version only. An older document is
read, and held to the current rules. A program that leaned on what moved is
*refused with the reason named*, not quietly run to a different answer, and
that refusal being explicable is what the number buys. Forward compatibility is
not available to anyone: what a reader can do about a version it has never
heard of is refuse, and the point of the number is that it can.

**The imports list.** What the program *sends* and does not itself declare. From
procedure bodies, from constants and from a variable's start alike, each by the
spelling it is sent by,
which is its declared spelling: `std.math.plus`, never `plus`. A native
procedure's sends are in it too. What a body sends is read off its text; a
module the host assembled in its own language holds procedures with no text a
reader could read, so each declares the procedures it sends and those count the
same. A
module whose native procedures send things its list never mentioned would
understate what the module does, which is the one thing this list may not do.
The list is that set exactly, not a bound around it: **reading refuses** a
document whose list disagrees with what its program sends, in either direction.
A stage-1 refusal, and it can be, since what a program sends is a fact of its
text alone. The list is read before the program and a caller grants from it, so
a list saying less would be trusted and wrong, and a list saying more asks for a
grant the program has no use for.

**A module asks and does not carry.** What the list names is supplied by
whatever else stands in the link, and a module that shipped its own copy of a
bundle it uses would put that bundle's declarations in the link twice, which
the build refuses by the rule that one name has one declarer. Which modules
are in a link is decided where the link is assembled, the same way a program's
libraries are chosen where the program is built rather than by each library in
it. The same holds for the types and memberships a signature mentions, which
the list does not name: a module declares against a vocabulary and expects to
be linked beside whatever declares it.

A document says it, and one that does not **refuses**. The way one that does
not say its version does. Silence is not a claim a caller can act on: the list
is read before the program and a grant is decided from it, so a reader with no
list cannot tell a program that touches nothing from one that touches
everything, and the empty list is what says the first. Nobody writes it by
hand. It is computed from the program the way the version is filled in by
whatever produced the document, and the canonical writer always writes it.

It is refused after the types are read and not before them. A missing list is
the least specific thing that can be wrong with a document, and refusing for it
first would make it the only thing an author ever heard about. That ordering is
an implementation's to choose, though, which is why every case in the suite
writes the list, including the ones whose programs will not read at all. A case
with two things wrong with it is a case any reader passes for the wrong
reason.

## Spellings are not part of the document

A front end may offer shorthands. Operator keys like `is:` in a condition
slot, a `{ format:, with: }` template. That stand in for types the language
already has. They are the front end's own: it spends them before the document
leaves, and what leaves writes the types themselves.

A reader of documents **refuses** the spelled keys rather than reading them as
data. The reserved set is exactly `format` and `with`. An operator key like
`is:` lives inside a condition slot a front end owns and can never reach a
document, so it needs no reservation. The two stay reserved whether or not any
notation offers them. A document that writes one was written *for* a spelled
notation, and reading it as a record that happens to have those fields would
be running a program nobody wrote.

## Cases

What `conformance/` asks about this page, by the name each case's file carries.

- `a-constant-is-a-name-a-body-reads`
- `a-constant-sees-only-the-constants-beside-it`
- `a-later-document-refuses`
- `a-module-declares-a-constraint`
- `a-module-variable-handed-in-place-is-one-box`
- `a-module-variable-is-handed-in-place-to-a-native-procedure`
- `a-module-variable-is-shared-by-the-procedures-beside-it`
- `a-module-variable-keeps-the-type-it-started-as`
- `a-procedure-only-an-untaken-arm-sends-is-still-needed`
- `a-reserved-spelling-refuses-in-a-document`
- `a-send-is-a-declared-spelling-or-an-import`
- `a-version-that-never-existed-refuses`
- `an-overstated-manifest-refuses`
- `an-unknown-key-refuses`
- `an-untruthful-manifest-refuses`
- `constants-settle-in-the-order-they-read-each-other`
- `constants-that-name-each-other-refuse`
- `the-escape-quotes-a-form`
- `what-a-document-says-for-a-reader-is-carried`
