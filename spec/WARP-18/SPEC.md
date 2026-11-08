# WARP-18: A parameter handed in place

Status: accepted

## Summary

A parameter typed inout takes a variable rather than a value. The rules decide how the argument is written as a reference path, what the build holds that path to, and that the body reads and writes the caller's own box.

## Motivation

A value is never a reference, so a procedure that updates a caller's state needs a way to write the caller's own variable. Without one, a procedure updating an array a caller holds returns a new array that the caller writes back, and every update is a copy.

## Rules

**A parameter handed in place.** A parameter typed `inout T` takes no value: it takes a variable. The argument is `{ ref: <path> }`, and all of this is held at the **build**:

- the path's head is a variable where the call stands. A fixed name, a literal and a call's return value each **refuse**;
- the path is one a write may take, under *what a write reaches* in [statements](../WARP-20/SPEC.md);
- the variable's type is the same type as the parameter's, all the way in: what it declared, else what it reads as. A variable a closure or a call holds to a type, under *what a write reaches* in [statements](../WARP-20/SPEC.md), is handed only where that type is the parameter's too. Nothing is judged here, because nothing is handed over: the body reads and writes the caller's own box, so a variable of another type would be written values it does not hold.

Inside the body the parameter is a variable, and `set` writes it. The parameter holds the caller's box through the path it was handed, and the path is fixed where the call stands: the names between its brackets are read once, as the call is made, and a later write to one of those names moves nothing the parameter holds. A read finds what that place holds now, and each write lands in the box as it is made. One box reached two ways, by a parameter and by a name or by two parameters, is still one box, so a write through either is seen through the other at once. A call that fails after writing has written, the same as a variable written before a failure. A body declared `const` that writes through one **refuses at the build**, by the rule that such a body writes no name. What a native procedure writes through one is a value from outside, judged at the door it comes through, under [running](../WARP-71/SPEC.md).

A variable is handed in place only by a call a body writes: a `call` to a declaration, and a `call` of a value whose type the build reads as a procedure type writing its parameters, at each position that type writes `inout`, held at the **build** to the three rules above; a value whose type writes no parameters (`Procedure`, `Any`, a type parameter, a contract) is called only once a cast says what procedure it is, and a call of one **refuses at the build**. A value standing there whose own parameter takes a value reads what the variable holds. Every other way in hands values: a run hands its entry values, and a native procedure hands values to what it sends and to a procedure it was handed. So an entry taking a parameter in place **refuses at the run** before anything runs; a native procedure declaring a send to one, or a parameter asking for a procedure that takes one, **refuses at the build**; and a value taking one that is handed a value **refuses at the run** before its body runs.

**Note.** A `call` a body writes hands a variable at each position the callee's procedure type writes `inout`, and a value whose type writes no parameters is called only once a cast has judged its procedure type, so a value taking a parameter in place is handed a value only where host code calls a value it was handed, and that refusal at the run is held only by tests inside the implementation, as another count is under [a parameter](../WARP-17/SPEC.md).

## Interactions

## Alternatives considered

## Notes
