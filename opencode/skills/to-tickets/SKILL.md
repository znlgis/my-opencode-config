---
name: to-tickets
description: Break a spec or plan into trackable GitHub issues. Use when a plan/spec needs splitting into work items, or the task mentions "tickets", "工单", "break into issues", "分解任务". Emits one issue per independently completable unit with acceptance criteria.
---

# To Tickets

Turn a written spec or plan into a set of trackable issues. One issue per unit
of work, each verifiable on its own.

## When to use

A spec/plan exists and needs to become actionable, reviewable issues — not when
the work is a single step you can just do inline.

## How to break down

- One issue = one unit that can be completed and verified independently.
- Every issue carries acceptance criteria (the observable "done" condition).
- Keep issues small enough to finish and review in one session; split anything
  that would outlive one.

## Creating issues with `gh`

For exact `gh` command syntax, flags, and pagination, load the `gh-cli` skill.

```bash
gh issue create --title "<summary>" --body "<body>" --assignee @me
```

- `--body` holds the scope, acceptance criteria, and dependency notes.
- Use `--type Task` (or `Bug`/`Feature`) when the repo uses issue types.
- Batch-create from a plan: one `gh issue create` per ticket.

## Notes

- Granularity: aim for units a single agent session can finish — not one giant
  issue, not twenty trivial ones.
- Dependencies: annotate blocking relationships (e.g. "blocked by #12") rather
  than assuming order.
- Don't create issues for work you're about to do inline — tickets are for
  tracking work across sessions or humans.
