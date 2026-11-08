# WARP-72: A run refuses, and a refusal is not a failure

Status: accepted

## Summary

A run refuses, and a refusal is not a failure. The rules decide that arithmetic past an Int, a zero divisor, a missing index or key, and a value a door does not take each stop the run, that no catch holds a refusal, and that a refusal names the places of the frames it stopped in.

## Motivation

A catch is written for what a procedure declares it may fail with, and a defect such as an overflow is in no declaration, so a catch that took one would hand the program a case its author never wrote a branch for.

## Rules

**A run refuses, and a refusal is not a failure.** Arithmetic past what an `Int` holds, a zero divisor under `dividedBy` or `remainder`, an index or a key that is not there read without `?`, a key holding a procedure, under [the value model](../WARP-3/SPEC.md), a value arriving at a door that its slot does not take: each stops the run where it stands. No catch holds one, the way none holds a build's refusal, and it reaches the host as the run's refusal. A failure is what a procedure raised and a catch holds, under [statements](../WARP-25/SPEC.md), and the two never trade places.

**A run's refusal names where it stopped**, as a list of [places](../WARP-65/SPEC.md), one for each frame the run stood in that was running a statement, the outermost first. A frame is one call of a body, a procedure's or a closure's, and its place is that of the innermost statement it was running, one under `then` rather than the conditional holding it, under *where an instruction stands* in [operations](../WARP-88/SPEC.md#where-an-instruction-stands). So the list leads from the statement the entry was running, through each call, to the statement that stopped:

| frame | in the list |
|---|---|
| a call of a body, running a statement | the statement's place |
| a call of a body, before its first statement, at the door its arguments arrive at | nothing |
| a native procedure | nothing, since it runs no statement |
| a body whose document has no identity, an object writing `document` as `[]` | nothing |

A refusal no frame was running a statement at, a value refused at the entry's door or at the door of a closure a host calls, names an empty list. Which round of a loop and which piece of a concurrent procedure a frame stood in are the implementation's to say, as the sentence beside the places is.

## Interactions

- What a procedure may fail with is declared under [what a body may fail with](../WARP-26/SPEC.md).
- The arithmetic edges that refuse are [Standard's](../WARP-77/SPEC.md), and a value a door does not take is under [doors](../WARP-71/SPEC.md).
- A piece of `Standard.Concurrent` that refuses refuses the whole run, under [Standard.Concurrent](../WARP-83/SPEC.md).

## Alternatives considered

- Where left to the implementation, beside the sentence. A host would read a build's refusal and a run's in two forms, and could not take a run's back to the document's source the way it takes a build's.
- The innermost place alone. A run stopping inside a body the host never wrote, one of Standard's among them, would name only that body, and the statement in the host's document that reached it would be lost.

## Notes

**Note.** A case writes the stage a program is refused at, under [what an implementation checks](../WARP-65/SPEC.md), so the places a run's refusal names are held only by tests inside the implementation, as a build's are.

**Note.** A refusal reaches the host as the run's refusal, so what follows it is the host's to decide: the run stands inside the host's process, and an implementation that ended the process on a refusal would take that decision from the host.
