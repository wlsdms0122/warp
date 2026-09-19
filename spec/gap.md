# Known gaps

Written down because a specification that hides what it has not decided is
worse than one that admits it. Each is a place a second implementation would
have to guess, and would be entitled to guess differently.

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
  module declares. `bounds: { T: Comparable }` with no declaration of its
  own. States that dependency nowhere a caller can read before linking.
  Whether `imports` should widen to carry unresolved type and constraint
  mentions is undecided; until it is, that dependency surfaces only as a build
  refusal.
- **`regex` names no dialect.** The table says the pattern is a string and says
  nothing about what it means, so two hosts reaching for their own engines
  answer the same document differently. That is why it is required of no
  implementation, but naming a dialect would be a better answer than leaving it
  out.
- **The text decision is cheap in Swift and dear elsewhere.** Grapheme-cluster
  counting and canonical equivalence are the platform's gift in Swift and a
  library obligation in most other languages; the decision stands, and the
  cost lands on implementations unevenly.
- **The document grammar was written from the readers.** Field tables
  transcribed from one implementation carry its blind spots; the first reader
  who implements from these tables alone, and disagrees, is worth more than
  any amount of agreement.
- **The suite covers the constructs, the vocabulary and the encodings;
  cancellation is the exception.** Every construct, the naming and leaving
  rules, the envelope, the boundary settlements, the concurrency grant, every
  standard procedure and what a binary reader must refuse are held as cases,
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
- **Encodings beyond utf8.** `decoded`/`encoded` name their encoding and
  today name one. Which others join the `enum`, and whether a host may
  extend it. Is undecided; the type of the procedures is not.
- **Where a refusal points is not specified.** A case says the stage a
  document is refused at and nothing about the sentence, so two
  implementations agreeing on every case may still name the place
  differently, or name none. What an author is owed is the whole of the
  question: a refusal that does not say where sends them searching a
  document they did not write by hand. Whether the answer belongs here. A
  path spelled from the document's own keys, so that following it step by
  step lands on what was typed, or stays each implementation's to give, is
  undecided. What is decided is that a place is a fact about the **document**
  and never about the file it was authored in: a front end holds the file,
  and the document is what crossed the wire.
- **How a document is told from another document is decided; where the answer
  belongs is not.** Nothing a document says about itself can do it: what a
  document writes is declarations, and two documents may declare spellings
  under one prefix (a program split across files). A file path cannot do it
  either, since a
  document arrives as bytes and the wire carries no container. What is always
  there is the document itself, so a document is identified by the **digest of
  its canonical binary writing**, and by nothing it says about itself. It is
  derived and never declared: there is no field for it, which is what makes it
  impossible to write down wrongly, and two readers holding one document arrive
  at one answer without having agreed on anything but this paragraph. The
  digest is SHA-256 of the bytes the canonical binary writer produces. The
  same bytes a conforming reader already has to accept exactly, so an
  implementation that has the wire right has this right. What is undecided is
  whether identity belongs in this specification at all or stays a fact each
  implementation works out for itself, since nothing a program *runs* depends
  on it.
- **What a build writes down is the implementation's.** A document is what
  crosses the wire, and the pages here say everything about it. What a build
  makes of one, the judged rows, the lowered bodies, the numbering a link
  reads, is written and read by the implementation that made it, and nothing
  here says what it holds or in what order. Whether that writing becomes a
  format of its own, so that a build made by one implementation links and
  runs under another, is undecided; it waits on the lowering it would freeze.
