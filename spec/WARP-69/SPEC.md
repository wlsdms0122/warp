# WARP-69: Where a run starts

Status: accepted

## Summary

A run starts from the declaration the host names. This WARP opens WARP-69 to WARP-73, what a run does once the build has decided everything it can: where it starts, its order, its doors, its refusals and what may run at once. The rules decide that the host gives a value for every parameter and nothing more, what refuses at the run before anything runs, and how the entry's result reaches the host.

## Motivation

A host builds an image once and calls into it many times, naming another declaration each time and handing it values from outside. Fixing what a start takes, a value for each parameter by name and nothing more, and refusing before anything runs otherwise, leaves no run starting on arguments two implementations would read apart.

## Rules

- A run starts from the declaration the host names when it starts the run, under *who may name a declaration* in [procedures](../WARP-13/SPEC.md). An image is every declaration the link judged, and which one runs is the host's choice each time. The host gives the entry its arguments by name, a dictionary from each parameter's name to the value it is handed, as a case's `arguments` holds them under *what a runner does* in [conformance](../WARP-1/SPEC.md#what-a-runner-does): a value for every parameter the entry declares, null included where the parameter's type takes it, and nothing more: a parameter given nothing, or a value under a name the entry does not declare, **refuses at the run** before anything runs, and so does an entry taking a parameter in place, under *a parameter handed in place* in [procedures](../WARP-18/SPEC.md). What an entry with a body returns the build held to the `returns` it declares, what a native entry hands back is judged at its door under [doors](../WARP-71/SPEC.md), and either reaches the host as it is.

## Interactions

- What is checked before a run starts is under [what an implementation checks, and when](../WARP-65/SPEC.md).

## Alternatives considered

- An entry fixed at the build, an image with one start. An image already holds every declaration the link judged, and the host calls into it more than once, so one start would name nothing the image needs.

## Notes
