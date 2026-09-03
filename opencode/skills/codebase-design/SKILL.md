---
name: codebase-design
description: Use when designing architecture, choosing module boundaries, or reviewing whether a codebase's structure is sound. A shared vocabulary glossary for module/interface/depth/seam/adapter/leverage/locality.
---

# Codebase Design

A shared vocabulary for reasoning about code structure. This is a glossary, not
a process — use the terms precisely so design discussions stay concrete. Adopt
these words over looser ones: say **module**, not component or service; say
**interface**, not API.

## Terms

- **Module** — a unit of code with a boundary and a purpose. Not "component" or
  "service"; those imply a specific framework or deployment shape.
- **Interface** — everything a caller must know to use a module correctly: its
  functions, its invariants, its error modes, and its performance characteristics.
  Wider than "API" — it includes the contract a caller relies on.
- **Depth** — the leverage a module gives per unit of interface. A **deep**
  module hides a lot of implementation behind a small interface. A **shallow**
  module has a large interface relative to the work it does.
- **Seam** — a place where you can alter behavior without editing that place
  (Feathers). A seam is where you insert a test double or swap an implementation.
- **Adapter** — code that translates one interface to another. One adapter is a
  hypothetical seam; two adapters make it a real seam worth keeping.
- **Leverage** — how much downstream code a module's design decision affects.
  High-leverage decisions (a widely-imported module's interface) deserve the
  most design care.
- **Locality** — whether related code lives close together. Poor locality forces
  readers to jump across the codebase to understand one behavior.

## Tests

- **Deletion test** — delete a module. Does its complexity vanish, or does it
  reappear scattered across N callers? If the latter, the module was not
  encapsulating anything real.
- **Depth test** — is the interface smaller than the implementation it hides?
  A module whose interface is as big as its body is shallow and probably not
  earning its place.

## Testability

- Accept dependencies; do not create them inside the module.
- Return results; do not produce side effects from a function that claims to
  compute.
- Keep the surface small — every public entry point is a promise you maintain.
