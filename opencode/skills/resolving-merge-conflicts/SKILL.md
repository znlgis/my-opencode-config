---
name: resolving-merge-conflicts
description: Use when resolving git merge/rebase conflicts. Resolve each hunk by finding primary sources (commit messages, PRs, issues) to understand original intent. Preserve both intents where possible; never invent new behavior and never --abort.
---

# Resolving Merge Conflicts

When facing an in-progress git merge or rebase with conflicts:

1. **See the current state.** Check `git status`, `git log --oneline --merge`, and the conflicting files with `git diff --diff-filter=U`.

2. **Find the primary sources for each conflict.** Understand why each change was made and its original intent. Read commit messages, check related PRs (use `gh-cli` skill), and trace back to issues/tickets.

3. **Resolve each hunk.** Preserve both intents where possible. Where incompatible, pick the one matching the merge's stated goal and note the trade-off. **Never invent new behavior** — you are resolving, not refactoring. Always resolve; never `git merge --abort` or `git rebase --abort`.

4. **Run automated checks.** Discover the project's verification commands from `package.json` scripts, `Makefile`, or `AGENTS.md`. Run typecheck, tests, then format. Fix anything the merge broke.

5. **Finish.** Stage the resolved files by explicit path (`git add <path1> <path2>`, or `git add -u` for tracked files only — never `git add .` or `git add <dir>`, per AGENTS.md Git Safety), commit (`git commit` without `-m` — review the auto-generated merge message), or if rebasing, `git rebase --continue` until all commits are rebased.

## Rules

- Conflict resolution is archaeology: understand the intent behind each side before touching code.
- Do not use `--abort` to escape — it discards both sides' work.
- If the same conflict pattern appears across multiple files, resolve them consistently.
- After resolution, the build must pass. If tests fail, the resolution broke something.
