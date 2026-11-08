# WARP-66: What the build decides

Status: accepted

## Summary

The build decides what the load cannot. The rules decide that a ref's steps are judged against the types they read, every procedure sent is declared, one spelling has one declarer in the link, documents stand in an order where each is declared before it is used, and that claims hold to what they ask.

## Motivation

Constants folding across two documents that each need the other have no order to fold in, so such a pair refuses. Recursion inside one document stands.

## Rules

- every step a `ref`'s path takes past its head is judged against the type the path reads there, under [a dot reads a name](../WARP-33/SPEC.md); what the head resolves to is decided at the load, under [what an implementation checks, and when](../WARP-65/SPEC.md);
- every procedure sent is declared by some module in the link;
- **one spelling has one declarer**: each spelling of either namespace under [names](../WARP-64/SPEC.md), sent, mentioned or neither, is declared by one module in the link, so two modules declaring one spelling **refuse**; two declarations under one spelling in one document refuse at the load;
- a build holds each document once, so one handed to it twice, the same identity a second time, **refuses**, even when everything it declares is `private`;
- the documents of a link stand in an order where what each one sends, and every type it names, is declared before it, since what a document says is read against those: the types its sends return, what its bodies reach, what its constants fold from. Two documents that each need the other have no such order and **refuse**, as the pair and not as a spot in either;
- a claim backed by a declaration that does less than the contract asked, running where it asked `const`, touching a shared name where it asked `isolated`, or failing with what the contract does not name, does not hold, under *a const procedure* in [procedures](../WARP-15/SPEC.md); a claim whose head names what is no type refuses, at the stage the table in [claims](../WARP-54/SPEC.md) gives;
- every procedure sent from another document is not `private`, and a claim backed by a `private` declaration does not hold, under *who may name a declaration* in [procedures](../WARP-13/SPEC.md); a `private` declaration takes no spelling, so *one spelling has one declarer* counts none;
- every call fits the declaration it reaches: how many arguments, each at its position, and what it returns, with type parameters filled as [types](../WARP-51/SPEC.md) says and every bound judged against the contracts it names;
- every declared type names a type that exists;
- every dictionary type is keyed by a type that conforms to `Hashable`, under *a dictionary's key* in [types](../WARP-62/SPEC.md);
- a condition (a `conditional`'s `when`, a `loop`'s `while`) is a `Bool`, held where it is written as any slot of a type is, under *what a slot takes, exactly* in [types](../WARP-48/SPEC.md);
- what an `unwrap` takes apart reads an Optional, and an `unwrap` with no `then` leaves on every way through its `else`, under [statements](../WARP-27/SPEC.md);
- what a `switch` takes apart reads an enum, every case it names and every field an arm binds is one the enum declares, every case has an arm or a `default` takes it, and a `default` takes at least one case, under [enums](../WARP-95/SPEC.md#switch);
- what stands between brackets reads `Int` on a list and the dictionary's key type on a dictionary, under [expressions](../WARP-36/SPEC.md);
- a call of a value reaches one whose type writes its parameters; one whose type writes none (`Procedure`, `Any`, a type parameter, a contract) is called only through a cast, under [procedures](../WARP-18/SPEC.md);
- inside a generic body every place reading its own type parameter takes only a value of it, under [types](../WARP-51/SPEC.md);
- a slot declared `const` takes only a const procedure, under *a const procedure* in [procedures](../WARP-15/SPEC.md); a slot declared `isolated` takes only a procedure declared isolated;
- a body declared `const` reaches nothing outside the run, one declared `isolated` touches nothing shared, and a body fails with no more than its declaration names, a closure literal's body included, under [procedures](../WARP-12/SPEC.md) and [statements](../WARP-26/SPEC.md);
- an operand (a call's arguments, a value call's callee and arguments, a `conditional`'s `when`, a `loop`'s `while`, what an `unwrap` or a `switch` takes apart) calls only a declaration declared `const` or a value whose written type is `const`, and a constant and a module variable fold only from what *what a constant folds from* admits, both under [procedures](../WARP-15/SPEC.md);
- a parameter bounded by a contract, and a slot naming one, takes only a value of a type a document within what the asking document stands on says conforms to it, and every claim is backed where it is written, under [a claim holds to members](../WARP-56/SPEC.md) and [associated types](../WARP-59/SPEC.md);
- an associated type is one a contract bounding what it stands on asks, a contract's bound names a declared contract, a value of a contract or `Any` fills no type parameter whose associated type the signature names, and the type a same type says conforms to the contracts that bound the associated type, under [types](../WARP-60/SPEC.md);
- a value of a contract fills a bounded type parameter only where that parameter stands alone at one position, under [types](../WARP-53/SPEC.md);
- every `set` writes through fields declared `var` where the type is a declared type, and what it writes fits what the path reaches; a write into a module variable or an `inout` parameter fits what the box holds;
- every `inout` parameter is handed a variable's path a write may take; two parameters handed paths under one head hold one box two ways, under [procedures](../WARP-18/SPEC.md), and nothing keeps them apart;
- what a closure writes into a variable it captured fits what the capturing body holds;
- a struct type fits only a value of exactly it: a value read under one declared struct name fits no slot declaring another, nor `Dictionary<String, T>`, and a dictionary fits no declared struct; a struct literal is read as the declared struct of the place it is written into, judged field by field and taking the name, and one written where no declared struct is read refuses; an [enum](../WARP-94/SPEC.md) fits only a value under one of its cases' spellings, and a case literal is read as the enum its place reads; a case's spelling written as a type in a document other than its enum's refuses;
- what `return` carries fits the declaration, and a body whose declaration writes `returns` reaches its end on no way through it, every way leaving by a `return`, a call returning `Never` or a loop written with no `while`, under *a procedure* in [procedures](../WARP-12/SPEC.md), a closure literal's body included;
- a statement whose call returns `Never`, as its callee's `returns` declares, never finishes: it takes no name, and nothing follows it, nor a `conditional` both of whose arms, a `try` whose body and catch, an `unwrap` whose `then` and `else`, or a `switch` every arm of which, and its `default` where one is written, end in such a call or a leave, one of them at least in such a call, under [statements](../WARP-29/SPEC.md);

## Interactions

- What the load refuses and what a refusal names are under [what an implementation checks, and when](../WARP-65/SPEC.md).
- The claims lines meet [what a document stands on](../WARP-57/SPEC.md) and [a claim holds to members](../WARP-56/SPEC.md).

## Alternatives considered

## Notes
