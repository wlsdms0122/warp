# WARP-15: A const procedure

Status: accepted

## Summary

A construct runs a body, and a procedure is const when nothing it reaches stands outside the run it was handed. The rules decide what a const body may read, write and call, and what constness permits to be done with the procedure.

## Motivation

A front end cannot say constness for the IR, and a build that worked it out from a body would make a callee's insides part of its callers' contract.

## Rules

Some of what a program writes is **read** and some of it is **run**. A literal, a name, a struct, an index, a cast: reading those is what the language does to data. A **construct** runs a body, and it is the only thing that does. That line is what an operand stands on, under *what it permits* below; it is not what this section is about.

A procedure is **const** when nothing it reaches stands outside the run it was handed:

- it reads no module variable and writes no name it does not own: a module variable, a name a closure captured, or a parameter handed in place, whether written by `set` or handed in place to a call. What such a name holds is the run's rather than the text's, and a name the body introduces or a parameter it holds outright is its own;
- it calls a value only where **the type written for it** is a `const` procedure type. The type written for a value is the type a slot gave it (a parameter, a name that writes its type, a module variable's declared type), a closure literal's signature, the type a cast names, the return type a called declaration declares, the return type the type written for a called value says, or, for an unwrap's payload, what the type written for what it takes apart holds, and, for a name a switch's arm binds, the type the enum's declaration writes for the field, applied as the type written for what it takes apart applies it, under [enums](../WARP-95/SPEC.md#switch). A fixed name, a `let` or a module constant, that writes no type follows the type written where its value came from, and a path reaches inside one of those by the type written (an element of an array, an entry of a dictionary, a field of a struct type). A list or dictionary literal writes no type for its parts, so a part of one reached through a name that writes none carries no claim. The value is held to that type where it is handed over, made, cast or returned, so that is where something before the run says what kind of procedure the value is. A variable that writes no type holds whatever its writes leave, which nothing wrote, so calling what it holds carries no claim. The claim is the written type's, and so it stands wherever the name is read, a closure that **captured** the name included;
- and every procedure it sends is declared const.

A construct reaches nothing on its own. Which part of a `conditional`, `loop`, `try`, `unwrap` or `switch` runs is decided inside the body, so one of them is read exactly as far as the parts it holds are, and the same goes for `return`, `break` and `continue`. A name the body introduces is the body's own: a `let` and a `var` both make one, neither leaves the body, and so declaring either says nothing about what the body reaches.

A declaration says it is const by writing `const: true`, and the build holds its body to the rule above: a body declared `const` that reaches anything outside the run **refuses at the build**. Every procedure it sends is read by its own declaration, so a body is held alone, and two procedures that call each other are each held to what the other says. A **native procedure** says it the same way, and the sends it declared are held to what it said, under [a native procedure](../WARP-14/SPEC.md). A closure literal says it the same way and is held where it is written, and the claim travels with the closure as a value, so a slot reads it wherever the value arrives. What it captured it is judged with: a name the enclosing scope held under a type written a `const` procedure type is one the closure may call, which is what lets a body build a closure per element and hand the lot to `Standard.Concurrent.all`. A variable that declared it holds one is such a name too, since every write into it is held to the declaration; a variable that declared nothing is held from the capture on to the type it read as there, under *what a write reaches* in [statements](../WARP-20/SPEC.md), and that type is no slot's declaration, so it says nothing the closure can hold on to. **Isolation reads a captured name the same way**, through a type written an `isolated` procedure type.

**What it permits.** Three places, and they are what the claim is for:

- a **constant** and a **module variable** fold at the **build**, from these procedures alone, and from a narrower set of them still, under [what a constant folds from](../WARP-16/SPEC.md);
- a slot may **ask** for one, writing a `const` procedure type. That is how `Standard.Logic.and` takes sides it may decline to read and how `Standard.Collection.filter` takes a predicate that cannot reach the world;
- an **operand** may call one (a call's arguments, a value call's callee and arguments, a `conditional`'s `when`, a `loop`'s `while`, what an `unwrap` or a `switch` takes apart). Each of those is read rather than run, so an operand calling a declaration that does not say it, or a value **the type written for it** does not say it of, **refuses at the build**. A module variable it reads is read as any name is. A const body reads none because what one holds is the run's, and a constant folded from it would write one run's state into the compiled document, under [what a constant folds from](../WARP-16/SPEC.md); an operand is read while the program runs and writes nothing down.

A call through a contract reaches the declaration of the type that fills `Self`, so what it reads as is what the contract asked of every one of them. A contract's procedure is a declaration without a body and writes `const`, `isolated` and `failing` the way one does; a call through one writing `const` stands wherever a call to a declaration that does stands, an operand and a `const` body among them, and a claim backed by a declaration that says less than the contract asked, `const` or `isolated` left out or a failure the contract does not name, **does not hold**, and refuses at the build, at the claim. A contract's procedure writing neither may run, so a call through it is no operand and a body declared `const` may not send it.

Choosing among values in an operand is a procedure, `Standard.Logic.select`, under [the standard vocabulary](../WARP-76/SPEC.md).

## Interactions

- Isolation reads a captured name the same way: [WARP-73](../WARP-73/SPEC.md).

## Alternatives considered

- A body holding a construct is not const. That line would refuse a predicate for using a `conditional`, though a construct reaches nothing on its own, and an implementation without the evaluator that drew it would have no reason to reproduce it.
- Fewer slots asking for a const procedure, a collection's predicate asking nothing. Every collection procedure would then say it may reach outside the run, which is false.

## Notes
