# Acceptance criteria

A WARP moves from `draft` to `accepted` when every criterion below holds, and a review says which hold and which do not. Each criterion is a yes or a no with evidence beside it: a WARP sentence, a case, or a line a runtime printed. A criterion nobody checked is a no. Where `spec-series lint` checks a criterion, its passing is the evidence.

The same criteria judge a change to accepted WARPs (`change` mode) and the live set (`series` mode). There a no is a finding against what is already accepted.

## A. It is Warp's to do

A no that shows the work is not this specification's rejects the WARP, whatever else holds: the work belongs to a front end, a vocabulary or a host. A no the text answers in place, a Motivation not yet written or a general rule not yet stated where the WARP already does the work, is revised like any other.

- **A1. A front end could not write it without this.** For each construct the WARP adds, its Motivation names what a front end could not express with the live set alone. Examples are a type a host's signature must name, a shape a value must cross the boundary in, or a construct no rewrite in place can stand for. A construct a front end can write out of what exists (a raw value, a nested pattern, a default argument) fails.
- **A2. What the runtime judges is a fact of the program.** Every check reads the document: its types, claims, names and structure. A check about what a value means (a range, a set of allowed strings, a unit) fails. That is a declared type and the procedures that make it, in a vocabulary.
- **A3. The base language decides what it decides.** No limit or promise about stack depth, memory, Unicode tables or when a process stops.
- **A4. It is general.** One rule covers the feature. A rule that adds a branch for one shape, where a general rule would cover it, fails until the general rule is found.

## B. What it says is right

- **B0. It has the template's shape.** Every section of `spec/TEMPLATE.md`, in its order, and every rule under Rules.
- **B1. Every answer is decided.** No document exists for which two conforming implementations could answer differently: an order, a spelling, a message, a rounding, a winner between two writes, a stage. A reviewer who finds one shows the document and the two answers.
- **B2. It agrees with the live set.** No sentence contradicts a live WARP, and no rule is stated in two places. Every link resolves, and the WARP it reaches says what the linking sentence claims.
- **B3. A document says each thing one way.** The WARP adds no second spelling for something that already has one.
- **B4. Each refusal has its stage, and the stage is the earliest that has what it needs.** The text alone gives the load, the link gives the build, a value gives the run.
- **B5. The words are standard and single.** The field's term, one sense per word across the specification. No history, and no rule hidden in a **Note.**
- **B6. Another runtime could follow it.** Someone writing a runtime in another language could implement it from the text alone, without knowing the Swift runtime.
- **B7. A form is given whole and stated as what it is.** Every name, spelling, node and byte layout the WARP adds or touches is a grammar or a table, not prose alone. No rule is phrased against the input that raised it ("holds no `:`") where the form it belongs to can be stated instead.

## C. The cases are enough

- **C1. Every rule sentence is held by a case.** Each refusal has a case at its stage. Each answer has a case that reads it. A sentence no case can hold says why, in a **Note.**
- **C2. Each case breaks one rule.** A refusing case refuses with the message and place of the rule it names, checked by running it rather than by reading its name.
- **C3. The edges are held.** Where a rule draws a line, there is a case just inside it and a case just outside it.
- **C4. It is held against what it meets.** For each accepted WARP the feature reaches, there is a case where the two meet (for an enum: with type parameters, a claim, the door, a cast, a dictionary key).
- **C5. The runtime passes them.** Every case is in the writer's layout and passes on the reference runtime pinned at this commit. Accepted means implemented: a WARP is accepted once the runtime is built against it and its cases pass.

## D. The series stays straight

- **D1. What it changes is made and classed.** Every accepted WARP whose text must change is changed in the diff under review: each place `spec-series impact` prints that restates or relies on what changes, and each link `spec-series lint --as` prints. A change made in place is a supplement, and a WARP whose decision moves is superseded. A supplement is shown by running the whole suite with the change and seeing no existing answer move.
- **D2. Supersession is whole.** A superseding WARP restates everything it keeps. `Supersedes` names exactly the WARPs it replaces, and no live WARP links to a superseded one.

## E. Nothing is left open

- **E1.** No critical or major finding is open.
- **E2.** Nothing in the WARP is marked **Open.**
- **E3.** Every question it raised for the owner has an answer, and the answer is in the text.

## Verdict

- **accept**: every criterion holds.
- **revise**: A holds, or each no in A is one the text answers in place, and something else does not. The review lists each no with what would turn it into a yes.
- **reject**: a no in A shows the work is not this specification's. The review says where the work belongs instead.
