# WARP-19: A statement

Status: accepted

## Summary

A statement binds a name to an expression, and a construct is the only thing that runs a body. The rules decide the statement dictionary, what the naming keys let, var and set each do, and that a construct sits only under value.

## Motivation

A body is where order lives, and every front end writes one. Were a statement's keys each front end's to read, one runtime would bind a name on a call that never finishes and another refuse it, and one would retype a declared `var` on a write and another hold it to its declaration: after `{ var: n, type: Double, value: 1 }` and `{ set: n, value: 2 }`, `n` would hold `2.0` in one and `2` in the other. So the IR fixes the statement's keys, what each naming key does to its name, and which kind of `value` takes which keys.

## Rules

What a body is made of. A statement binds a name to an expression, and a **construct** is the only thing that runs a body. Everything a program does in a particular order is decided here; what it does it *with* is [the standard vocabulary](../WARP-74/SPEC.md).

A statement is a dictionary of these keys, `{ let: x, value: { call: … } }`, `{ value: { loop: … } }`:

| key | takes | required |
|---|---|---|
| a naming key, `let`, `var` or `set` | under `let` and `var` the name, a value's name under [names](../WARP-67/SPEC.md); under `set` a `write-path` under [a path](../WARP-31/SPEC.md#the-grammar) | no, and at most one |
| `type` | type. What the name holds, below | no |
| `value` | an expression, under [expressions](../WARP-30/SPEC.md), a call among them, or a construct, a dictionary of its one key | yes, but beside `var`, where it is `null` when absent |

The construct keys, each detailed in a WARP of its own: [`conditional`](../WARP-23/SPEC.md), [`loop`](../WARP-24/SPEC.md), [`try`](../WARP-25/SPEC.md), [`unwrap`](../WARP-27/SPEC.md), [`return`, `break` and `continue`](../WARP-28/SPEC.md), and [`switch`](../WARP-95/SPEC.md#switch). `value` is the one place a construct key is read: a dictionary standing anywhere else, an argument or an element of an array among them, is an expression under [expressions](../WARP-30/SPEC.md), where a construct key names no form and **refuses at the load**, and a key under `struct` is a field name like any other.

What a statement writes beside each kind of `value`:

| `value` | naming key | `type` |
|---|---|---|
| an expression | any, or none | beside `let` or `var` |
| `loop`, `try`, `unwrap` | `let`, the name the construct binds its round, its failure or its payload through, or none | none |
| `conditional`, `switch` | none | none |
| `return`, `break`, `continue` | none | none |

Any other statement **refuses at the load**, and one naming a call that returns `Never` **refuses at the build**, below.

The naming key says what the statement does to its name:

| key | means |
|---|---|
| `let` | fixes the name. Written once, never again |
| `var` | introduces a name that may be written again |
| `set` | writes a path headed by a variable: one a `var` declared earlier, a module variable, or an `inout` parameter. `set "p.x"` and `set "people[0].name"` write into what the head holds |

**A name may say what it holds**, under **`type`**, written the way a parameter's type is: `{ let: x, type: Double, value: 1 }`. The declaration is what the name holds, and the build works out a reading only where the name declares none. What the statement was given has to fit the declaration, and a declaration naming a type nothing declares **refuses at the build**. One naming a type parameter of the procedure the body is written in reads it as the call filled it, under [types](../WARP-51/SPEC.md), and one naming any other type parameter **refuses at the load**.

A declaration is a slot like a parameter's, so **what the name takes is judged against it** the way an argument is: an integer literal written where it declares a `Double` is the `Double` it names, a struct literal written where it declares a struct is judged field by field and takes the name, a case literal written where it declares an enum is judged against its case and takes the case's spelling, a value whose type the build does not know stands where *what a slot takes, exactly* in [types](../WARP-48/SPEC.md) says, and any other value is held as it came.

`type` stands beside `let` and `var` alone because a `set` reaches a name something else declared and a statement with no naming key introduces none, and a construct that binds the name says what it holds itself: a loop's round, a try's failure and an unwrap's payload are the construct's to say.

A name that says what it holds is what it says, and a name that says nothing is the reading the build worked out; what a write into each does to its type is under *what a write reaches* in [statements](../WARP-20/SPEC.md). A declared name is what lets a name be handed to an `inout` slot, which asks for the same type the name is.

A statement with no naming key, `{ value: … }`, runs its expression and binds nothing. The result is dropped, which is how an effect is asked for on its own. Three families step out of this freedom, in different directions:

- The constructs that bind **through** the statement's name, `loop` (its round), `try` (its failure) and `unwrap` (its payload). The name they bind through is one the statement introduces, with `let`: nothing writes it, so one introduced with `var` **refuses at the load**, and so does a `set` of one. Written nameless they bind nothing: a loop with no name has no round to read, a try with no name has no failure to read and an unwrap with no name has no payload to read, and each runs and leaves the same otherwise.
- The leaving constructs (`return`, `break`, `continue`) take **no** naming key at all: such a statement never finishes, so its name could never bind, and a key that promises a binding that cannot happen **refuses**. The same rule reaches a **call**: a statement whose call returns `Never`, as its callee's `returns` declares, binds nothing and takes no name. Held at the **build**, whichever document declares the callee, because what a call returns is its callee's signature; a leave, which the document's own tree shows, is held at the load, under [nothing after a leave](../WARP-29/SPEC.md).
- A **`conditional`** and a **`switch`** take no naming key either, for the other reason: each finishes, but has no value, under [`conditional`](../WARP-23/SPEC.md) and [`switch`](../WARP-95/SPEC.md#switch). A `loop`, a `try` and an `unwrap` written with a `then` have no value either, an `unwrap` written with none has its payload, and the name of each is its round's, its failure's or its payload's alone, one that does not finish included.

**A `var` may leave out its `value`**, `{ var: name }` or `{ var: name, type: Int? }`, and introduces the name with nothing in it yet: a name holding nothing holds null, and what the name declares has to take that null, as it has to take any value the statement is given. Written with `value: null` it says what leaving `value` out says a second way, and **refuses at the load**. It is the declaration a conditional's arms write into; what the name reads as afterwards is under *what a variable reads as* in [checking](../WARP-68/SPEC.md). `let` and `set` say something about a value, so each writes one, and one written without it **refuses at the load**.

## Interactions

- What a write reaches: [WARP-20](../WARP-20/SPEC.md).
- Where a name may be introduced, and how far it is read: [WARP-21](../WARP-21/SPEC.md).
- The leaving constructs: [WARP-28](../WARP-28/SPEC.md).

## Alternatives considered

## Notes
