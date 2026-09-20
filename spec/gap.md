# Known gaps

Written down because a specification that hides what it has not decided is
worse than one that admits it.

## Undecided

Each of these is a place a second implementation would have to guess, and
would be entitled to guess differently.

- **A caller has no way to hand a constant in.** A constant settles from
  bodies in the link and from the procedures this specification names, under
  *what a constant settles from* in [procedures](procedure.md), so a caller
  that wants the build to bake something of its own has nowhere to put it: a
  procedure it brings is exactly what that rule turns away. What is wanted is
  a **value**, which is data the link carries and a caller can hash, rather
  than a procedure that answers one. Where such a value is written, how a
  document names it, and whether it is a module of its own are undecided.
- **The bound is on documents, and a run builds values.** Nesting deeper than
  128 containers is refused at the wire, under [encodings](encoding.md), so no
  document a reader admits is deeper than that. A running program is under no
  such rule: a loop that wraps its last value in an array each time around
  builds a value of any depth, and whatever meets it afterwards, a comparison,
  a writer handed it to send, the host's own release of it, meets a depth no
  document ever had. Whether a value has a bound of its own, and where it would
  be refused, is undecided.
- **`imports` does not announce type or constraint dependencies.** The list
  gathers what a program *sends*; a document leaning on a constraint another
  module declares. `bounds: { T: std.Comparable }` with no declaration of its
  own. States that dependency nowhere a caller can read before linking.
  Whether `imports` should widen to carry unresolved type and constraint
  mentions is undecided; until it is, that dependency surfaces only as a build
  refusal.
- **`regex` names no dialect.** The table says the pattern is a string and says
  nothing about what it means, so two hosts reaching for their own engines
  answer the same document differently. That is why it is required of no
  implementation, but naming a dialect would be a better answer than leaving it
  out.
- **Encodings beyond utf8.** `decoded`/`encoded` name their encoding and
  today name one. Which others join the `enum`, and whether a host may
  extend it. Is undecided; the type of the procedures is not.
- **Whether a refusal names its place is not specified.** A case says the
  stage a document is refused at and nothing about the sentence, so two
  implementations agreeing on every case may still name the place
  differently, or name none. What a place *is* is decided: a fact about the
  **document** and never about the file it was authored in, the document's
  identity and the steps from its root, laid out under [objects](object.md)
  where an object carries one. Whether a refusal owes an author one, and in
  what sentence, stays each implementation's to give.

## Decided, and what it costs

Each of these is settled. What remains is a cost the decision lands on an
implementation, or a limit of the suite, and a second implementation is told
here rather than left to find it.

- **The text decision is cheap in Swift and dear elsewhere.** Grapheme-cluster
  counting and canonical equivalence are the platform's gift in Swift and a
  library obligation in most other languages; the decision stands, and the
  cost lands on implementations unevenly.
- **The document grammar was written from the readers.** Field tables
  transcribed from one implementation carry its blind spots; the first reader
  who implements from these tables alone, and disagrees, is worth more than
  any amount of agreement.
- **The suite covers the constructs, the vocabulary, the encodings and the
  objects; cancellation is the exception.** Every construct, the naming and
  leaving rules, the envelope, the boundary settlements, the concurrency
  grant, every standard procedure, what a binary reader must refuse and what
  a build writes down for each operation are held as cases,
  and each page names its own under *Cases*. Cancellation cannot be a data
  case at all: it needs a caller with a lever, so stopping is held only by
  tests inside the Swift implementation.
- **Two equivalences coexist, and the border is drawn.** Values compare as a
  person reads. `equal`, `contains`, ordering and `count` all read text
  under canonical equivalence, stated under the value model. Where names are
  matched as bytes, held to NFC at the check, so a document cannot declare
  `é` one way and reference it the other. What remains here is only the cost:
  an implementation whose platform compares by code unit owes a library the
  difference.
