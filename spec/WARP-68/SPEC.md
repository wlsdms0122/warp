# WARP-68: What a variable reads as

Status: accepted

## Summary

A variable reads as what the ways through the text could have left in it. The rules decide what a declared name reads as, how writes are held to a declaration, and how the reading follows the flow the run takes.

## Motivation

A document may leave a variable's type unwritten, `var x`, and the build still has to know what `x` reads as at every later use to judge it.

## Rules

**What a variable reads as.** A name a statement fixed reads as what that statement bound, and a variable reads as what the ways through the text could have left in it. The checking follows the flow the running takes:

- a name that **declared** what it holds reads as that declaration, and no write changes it. What is written is held to the declaration instead, a list, dictionary or struct literal part by part along what the declaration asks of each part (every element of a list, every key and value of a dictionary, each field a struct names), an empty list holding no element, so `[[], [1]]` written where `Array<Array<String>>` is declared refuses at the build, and so does `[1, "s"]` where `Array<Int>` is. Every slot a value is written into holds it that way: a name's start value or a later write, a parameter of a call or of a called value, and a declared return type, from a `return`;
- a variable a closure captured or a call handed in place is held to the type it read as there, under *what a write reaches* in [statements](../WARP-20/SPEC.md), and a write into it is judged against that type and leaves it reading it, since the taker may write any value of it later;
- an **unconditional** write retypes any other variable: after `set x` at the top of the flow, `x` reads as what was written, whatever it held before;
- a write only **some** ways make (one arm of a conditional, a loop's round, one way of a try or of an unwrap, one arm or the `default` of a switch) joins with what the name held. Null beside a reading other than `Null` reads its Optional, or the reading itself where that is an Optional: after `var x` and a conditional whose one arm sets an int, `x` reads `Int?`, because the run either took the arm or did not. Two readings join part by part under [types](../WARP-47/SPEC.md), so where one way writes an integer literal and another a `Double`, the ways meet at `Any`. This join is not the variable's own rule: it reads wherever two readings of one slot meet, an array literal's elements among them, so `[1, null]` reads `Array<Int?>`, and there an integer literal beside a `Double` is the `Double` it names, under [types](../WARP-47/SPEC.md), so `[1, 2.5]` reads `Array<Double>`. A literal's elements are no ways: each is written into the reading the elements join to, as into a place, so `[null, x]` of an `x` of `some T` reads `Array<some T?>` and holds `x` as its some. Ways that meet are no place, so a value stands at the meet as its way left it, and where a value of the reading one way leaves would change to stand at the reading the ways meet at, promoted to its some or its held type dropped at `Any`, under [types](../WARP-48/SPEC.md), the build **refuses**: past the arms of a conditional, the ways of an unwrap and the ways of a [switch](../WARP-95/SPEC.md#switch), which are its arms and its `default` and no other, at the start of a round and past a loop, and at the start of a catch and past a try. Declaring the name's type makes every write into it a place. After `var y` and a conditional whose one arm sets `y` to a value of `some T`, the arms meet at `some T?`, where a value of `some T` may be a none, so the build refuses, and `y` declaring `some T?` takes the arm's value as its some. A meet that changes no value stands: an `Int` beside `Null` meets at `Int?`, where the some of an int is the int;
- a write **both** arms make is unconditional again, whichever arm ran, the write happened, and an arm that **leaves** contributes nothing: no run comes back from it, so the ways that finish are the only ways a reading after the conditional can stand on. `var x` with one arm setting an int and the other returning reads `Int` afterwards, plain;
- a try's **body and catch** are its two ways in the same sense. The catch runs where the body failed and reads what the body wrote on the way there, and after the try the way that finished the body meets the way that finished the catch. A write both make is unconditional, so `var x` with a body and a catch that each set an int reads `Int` afterwards;
- what an arm **declares** (`let`, `var`) stays its own. Declarations die with the arm, and only the box a `set` writes outlives it.

## Interactions

## Alternatives considered

## Notes
