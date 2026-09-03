---
name: diagnosing-bugs
description: Use when debugging a bug, test failure, or unexpected behavior, before proposing fixes. Build a tight red-capable feedback loop first, then reproduce, hypothesise, instrument, fix, and clean up.
---

# Diagnosing Bugs

Debugging is a discipline, not a guessing game. The single most important rule:
**build a tight, red-capable feedback loop BEFORE you theorize.** No hypothesis
is worth anything until you have a command that reproduces the failure and turns
red when it is present.

## Phase 1 — Build a red-capable feedback loop

Do not theorize yet. Construct the fastest command that reproduces the failure
and fails (turns red) when the bug is present. This is the skill.

Construction options, in priority order:

1. A failing test that exercises the bug
2. A `curl`/HTTP request against a running instance
3. A CLI fixture or script that drives the code path
4. A headless-browser interaction (UI bugs)
5. A replay of a recorded trace
6. A throwaway harness that calls the suspect function directly
7. A property/fuzz check that asserts the invariant
8. A bisection script over inputs or commits
9. A differential check against a known-good reference
10. A human-in-the-loop bash command (last resort)

Then **tighten** it: strip it to the smallest input that still turns red, and
make it run in seconds, not minutes.

**Completion criterion:** you have a command that reproduces the failure and
turns red. Do not proceed until this exists.

## Phase 2 — Reproduce and minimise

Run the loop to confirm it reproduces reliably. Minimise the failing input and
the code path until you cannot remove anything without the failure disappearing.

**Completion criterion:** the failure reproduces on the minimal input.

## Phase 3 — Hypothesise

Generate 3-5 falsifiable hypotheses about the root cause. Rank them by
likelihood and by how cheap each is to test. Each must be stated so that a
specific experiment could disprove it.

**Completion criterion:** a ranked list of falsifiable hypotheses.

## Phase 4 — Instrument

Test hypotheses one at a time. Change one variable per experiment. When you add
debug output, tag it so cleanup is a single grep:

```
[DEBUG-<hex>] <what you are observing>
```

Use a fresh hex tag per debugging session so you never sweep up someone else's
logs.

**Completion criterion:** one hypothesis survives; you can point at the exact
line or state transition that causes the failure.

## Phase 5 — Fix and add a regression test

Fix the bug at the correct seam — the narrowest place where the fix is correct,
not where the symptom appears. Add a regression test that would have caught this
bug, at that seam.

**Completion criterion:** the loop turns green, and the regression test fails
if you revert the fix.

## Phase 6 — Clean up

Re-run the loop to confirm the fix holds. Remove all `[DEBUG-<hex>]` tagged
logs. State the winning hypothesis and the fix in the commit message so the
"why" survives.

**Completion criterion:** loop green, no tagged logs remain, commit states the
root cause.
