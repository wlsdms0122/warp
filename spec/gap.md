# Known costs

Written down because a specification that hides what its decisions cost is
worse than one that admits it. Each of these is settled. What remains is a
cost the decision lands on an implementation, or a limit of the suite, and a
second implementation is told here rather than left to find it.

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
- **A run's values have no bound, and an implementation walks them on its own
  stack.** The nesting bound is the wire's, under [encodings](encoding.md), and
  a running program builds deeper values than any document. An implementation
  whose comparison, rendering or release of a value recurses meets a depth
  there that no document brought, and owes either a walk on a stack of its own
  or a caller that stops the run; the language refuses nothing there.
- **A refusal's sentence is not held.** A refusal names its place, under
  [checking](checking.md), and a case measures the stage; two implementations
  agreeing on every case may still say the reason in different words. The
  place is the part a front end reads to point at a line, so it is the part
  that is held.
