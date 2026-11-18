# WARP-N: Title

Status: draft
Supersedes: WARP-a, WARP-b
Superseded-By: WARP-c
Release: 0.1

<!--
The shape of a WARP's SPEC.md. A WARP starts as a copy of this file under the next number, with no field but its Status.

- The heading and the Status line are required. Supersedes is written only by a WARP that replaces others whole. Superseded-By is written into a replaced WARP when the WARP replacing it is accepted, and names every accepted WARP that supersedes it, once each. Release is written into an accepted WARP when the release it enters is cut. A draft writes neither.
- Every section below is written in every WARP, in this order. A section with nothing to say keeps its heading and is left empty.
- Rules is the only normative section. Everything else explains it and binds nothing.
-->

## Summary

One paragraph: what this WARP adds to the language or decides about it, for a front-end or runtime author reading it first.

## Motivation

Why this is Warp's to do, not a front end's, a vocabulary's or a host's. Name what a front end could not write without it, or what two implementations would answer differently without it, and show it with a concrete document.

## Rules

The normative text. Every sentence here is one a conforming implementation follows, and each is held by a case under `conformance/`. Subsections (`###`) by construct, as the rules need them. A `**Note.**` paragraph may stand beside the rule it is about, and binds nothing. A form (a name, a spelling, a node, a byte layout) is given whole as a grammar or a table, and each rule says what a thing is, never only the one input that raised it.

## Interactions

Where these rules meet what the live set already has: types, the door, casts, claims, concurrency, the object format. A rule another WARP states is linked to, not restated.

## Alternatives considered

The designs not taken, each with the rule or principle that set it aside.

## Notes

`**Note.**` paragraphs about the WARP as a whole: what it costs an implementation, and what no case can hold.
