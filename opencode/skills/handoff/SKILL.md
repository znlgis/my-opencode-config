---
name: handoff
description: Compact the current conversation into a handoff document for the next agent session. Use when handing off work, ending a long session, or the task mentions "handoff", "交接", "hand over", "continue in next session". References artifacts by path — never copies.
---

# Handoff

Compact the current conversation so a fresh agent can continue without replaying
the session. Reference existing artifacts — never paste their content.

## When to use

- Ending a session with unfinished work
- Task mentions "handoff", "交接", "continue later", "next session"
- Context is too large and you need to preserve current state

## Structured format

Every handoff uses these exact headings, in this order:

```
## Goal
## Constraints & Preferences
## Progress (Done / In Progress / Blocked)
## Key Decisions
## Next Steps
## Critical Context
## Suggested Skills (optional)
```

Fill each with short bullets, not prose. Leave a section empty (with a single
`—`) rather than padding it. Omit the optional Suggested Skills heading entirely
when no skills apply.

## What to include

- **Goal**: the end state this session was driving toward
- **Progress**: what's done / in progress / blocked — paths to artifacts, not content
- **Key Decisions**: trade-offs made, alternatives rejected, and why
- **Next Steps**: the concrete first actions for the next session
- **Critical Context**: gotchas, constraints, or facts the next agent must know
- **Artifact references**: paths/URLs to specs, plans, diffs, issues — never inline

## What NOT to include

- Full files or large code blocks — reference paths
- Secrets (API keys, passwords, tokens, PII) — redact with `<REDACTED>`
- Content already captured in artifacts — the path is enough
- Session chatter irrelevant to the next agent's work

## Output

Save to the OS temp directory:

| Platform | Path |
|----------|------|
| Windows  | `$env:TEMP\opencode-handoff-YYYY-MM-DD-HHmm.md` |
| Unix     | `$TMPDIR/opencode-handoff-YYYY-MM-DD-HHmm.md` |

## Agent workflow

1. Collect paths of existing artifacts (specs, plans, PRs, diffs)
2. Fill the structured headings with short bullets: goal, progress, decisions, next steps, critical context
3. Add an optional **Suggested Skills** section listing skills the next session should load (omit if none)
4. Write to the OS temp directory, report the path to the user

The handoff is a signpost, not a replay. Keep it under 100 lines.
