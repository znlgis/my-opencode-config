---
name: grill-with-docs
description: Use when requirements are ambiguous AND the domain language is fuzzy — compose the grilling and domain-modeling skills to converge intent while sharpening terminology.
---

# Grill With Docs

Compose the `grilling` and `domain-modeling` skills when a request is ambiguous
and the project's domain terms are themselves fuzzy. Converge on intent one
question at a time while pinning down the vocabulary.

## When to use

- Requirements are ambiguous (multiple interpretations with different effort).
- The domain language is inconsistent — the same concept is called different
  things, or a term's meaning shifts between uses.

## How

1. Load the `grilling` skill for the question discipline: ask ONE question at a
   time, prefer multiple choice, until intent is clear.
2. Load the `domain-modeling` skill for the glossary discipline: as each answer
   sharpens a term, record it in `CONTEXT.md` inline.
3. Alternate: a grilling question that exposes a fuzzy term becomes a
   domain-modeling clarification before you continue grilling.

## Rules

- Never batch questions — one at a time, per grilling.
- Never let a fuzzy term pass unexamined — if a word could mean two things, the
  answer is ambiguous until you pin it down.
- Stop as soon as intent is clear enough to proceed; do not over-grill.
