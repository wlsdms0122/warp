# WARP-10: The imports list

Status: accepted

## Summary

The imports list holds every name a program uses and does not declare, each by its declared spelling, and a document lists beside it the claims of other documents it stands on. The rules decide which sends, types and contracts the list holds, that a list disagreeing with what the program uses, in either direction, refuses at the load, and how a claim is imported.

## Motivation

The host lays the link before it builds anything, and it can bring only what it is told the program needs. A document sending `App.Wallet.fee` that did not say so would leave the host to find the send by reading every body, a constant and a variable's start among them, before it could decide whether to run the program at all. The list is what the host reads first and trusts, so the reader holds it to the text, and a front end cannot write it in the host's place. A claim another document makes declares no name for the list to hold, so a document that stands on one says so beside it.

## Rules

**The imports list.** Every name the program *uses* and does not itself declare, each by its declared spelling: `Standard.Numeric.plus`, never `plus`. Two kinds of name are in it, and they are the two kinds a link resolves. The procedures the program sends, from procedure bodies, from constants and from a variable's start alike; and the types and contracts it names, in a declaration, a bound, a local binding, a cast, a closure's signature, an extension or a claim it makes. The document declaring an [enum](../WARP-93/SPEC.md) declares each of its cases' spellings and lists none of them; a document writing another document's case's spelling where a type is written lists it as it lists a type it names, and the link resolves it to the case, which the build refuses as no type. A type member's spelling written where a type is written is listed as a type's name is, and a type applied to what its brackets hold followed by a type member's name lists both names it uses, the type's and the type member's spelling: `App.Wrapper<String>.Item` lists `App.Wrapper` and `App.Wrapper.Item`, and the link resolves each. A case literal and a switch's arm name a case by its bare name, which no link resolves, so neither is listed. The sends a native procedure declares are in it too. What a body sends is read off its text; a module the host assembled in its own language holds procedures with no text a reader could read, so each declares the procedures it sends and those count the same.

The list holds spellings and not kinds: a spelling in it asks for whatever the link declares under it, so a program using the procedure and the type of one spelling lists it once. The list is that set exactly, not a bound around it: **reading refuses** a document whose list disagrees with what its program uses, in either direction. It refuses at the load, since what a program uses is a fact of its text alone. The list is read before the program: the host lays the link from it, whatever kind each spelling turns out to declare, so a list saying less would be trusted and wrong, and a list saying more asks for what the program has no use for.

**A claim imported.** A claim declares no name, so a document stands on a claim another document makes by listing the pair the claim is about under `importedClaims`, a `claim` under [the grammar](#the-grammar): `[T.Card, App.Describable]`, and `[Optional, App.Describable]` for a claim about an Optional. What it stands on is what its build asks a contract of, under [what a document stands on](../WARP-57/SPEC.md): a claim made in a document it stands on is within its reach already, and one made in a document it does not stand on is reached this way alone. Which claims a document asks of is its build's, not its text's, so a claim imported is not held to the program's use as a name is, and it puts neither of its names in `imports`. A claim imported that the document makes itself or that the language makes, and an entry the grammar below does not give, **refuse at the load**, and a claim imported that no document in the link makes **refuses at the build**. What a claim imported brings is under [what a document stands on](../WARP-57/SPEC.md).

**A module asks and does not carry.** What the list names is supplied by whatever else stands in the link, and a module that shipped its own copy of a bundle it uses would put that bundle's declarations in the link twice, which the build refuses by the rule that one name has one declarer. Which modules are in a link is decided where the link is assembled. The same holds for the types and contracts a signature mentions: the list names them, and what declares them is still the link's to bring.

A document says its list, and one that does not **refuses at the load**, the way one that does not say its version does: the list is read before the program and the link is laid from it, so a reader with no list cannot tell a program that uses nothing from one that uses everything, and the empty list is what says the first.

### The grammar

Each string `imports` holds is an `import`, read as a `qualified-name` from [names and their grammar](../WARP-67/SPEC.md):

```
import          = qualified-name
```

Each entry `importedClaims` holds is a `claim`: an array of exactly two strings, the type's name and then the contract's, each read as a `qualified-name`.

| part | what it may be |
|---|---|
| an `import` | a name a module declares: a procedure's or a type's name, or a spelling, under [names and their grammar](../WARP-67/SPEC.md#the-grammar) |
| a `claim` | an array of two strings, no more and no fewer |
| a `claim`'s first string | the name of the type a head is about, under [heads](../WARP-55/SPEC.md#the-grammar): `Int`, `Array`, `Optional` |
| a `claim`'s second string | a contract, under *what a name names* in [names and their grammar](../WARP-67/SPEC.md) |

## Interactions

- A module carrying a copy of what it imports is refused by the rule that one name has one declarer: [WARP-66](../WARP-66/SPEC.md).
- A native procedure declares its sends under [WARP-14](../WARP-14/SPEC.md), and a case's vocabulary writes them under `sends`, [WARP-1](../WARP-1/SPEC.md).
- The order the list is written in: [WARP-11](../WARP-11/SPEC.md).

## Alternatives considered

- Bare names in the list, `fee` for `App.Wallet.fee`. A bare name does not say what to bring: which declaration it is depends on what the link holds, so the list could not be judged before the link, which is what it is for. A shorter spelling is a front end's.
- A list of the procedures sent, and nothing else. The types and contracts a program names are declared by the link too, and the host lays the link from the list. A spelling in the list asks for whatever the link declares under it, as a linker's undefined symbol does not say what kind of symbol it is.
- A claim written among the names as one string, `"T.Card: App.Describable"`. The string holds a grammar of its own that a reader reads a second time, it holds only while no name can hold `": "`, and its order among the names falls out of the bytes of `.` and `:`. An object already writes the claims it imports apart, as pairs, under [what an object holds](../WARP-85/SPEC.md).

## Notes
