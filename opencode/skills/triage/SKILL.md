---
name: triage
description: Label-based issue triage workflow. Use when a batch of issues needs sorting by priority/type, or the task mentions "triage", "分流", "prioritize issues", "label". Pulls issues, classifies them, and applies labels/assignees via gh.
---

# Issue Triage

Sort a batch of issues by priority and type, and reflect that in labels and
assignees — without changing the issues' substance.

## When to use

A backlog needs routing: which are urgent, which are bugs vs features vs
chores, who owns what.

## Workflow

For exact `gh` command syntax, flags, and pagination, load the `gh-cli` skill.

1. Pull: `gh issue list --state open --search "<filters>" --json number,title,labels`
   (or `--label <name>` to scope to a label). Raise `-L` for large batches.
2. Classify: bucket each issue by type and severity from its title/body — not
   from assumptions.
3. Apply: `gh issue edit <n> --add-label <type> --add-label <severity>` and
   `--add-assignee @me` to claim ownership.

```bash
gh issue list --state open -L 50 --json number,title,labels,state
gh issue edit <n> --add-label bug --add-label P1 --add-assignee @me
```

## Notes

- Never close an issue during triage — routing only.
- Preserve original title/body; add context via comments, not edits.
- Don't re-label something already correctly labeled.
