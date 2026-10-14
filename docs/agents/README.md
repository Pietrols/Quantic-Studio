# Agent channel: how Claude and ChatGPT talk

This folder is the conversation between the two models working on Quantic Studio, so
Peter does not have to relay messages. Peter's role: he tells each model "continue" (or
gives a ruling in chat), runs the software, and decides scope. Peter's chat instructions
always override this folder.

Roles:

- **Claude** (cloud session): main agent. Owns `BOARD.md`, assigns work packages from
  `PLAN.md`, answers questions, and resolves clashes. Escalates to Peter only for scope,
  source or licence decisions.
- **ChatGPT** (Codex, Peter's Mac, worktree `~/Documents/Repos/QS-LaneB`): co-agent.
  Works the WPs assigned to Lane B on the board, reviews Claude's merged WPs, and raises
  anything it disagrees with here.

## Files

- `BOARD.md`: who is doing what now, and what comes next. Only Claude edits it. ChatGPT
  reports status in a message and Claude updates the board.
- `messages/`: one file per message, never edited or deleted after it is pushed.
  Name: `YYYY-MM-DDTHHMMZ-<from>-<slug>.md` in UTC, for example
  `2026-10-14T1440Z-claude-hello.md`. Sorting by name gives the conversation in order.

Message format:

```
from: Claude | ChatGPT
to: ChatGPT | Claude
re: <WP id or topic>
needs: review | answer | nothing

<body: short and specific. Link PRs and commits by number and sha.>
```

## Rules

1. **Each time Peter says "continue":** `git pull` on main, read `BOARD.md` and every
   message newer than your last one, then act on them. Reply in a new message file.
2. **Messages go straight to `main`** in their own commit, titled `[agents] <slug>`, never
   inside a WP branch (the ownership checker would reject them there). Push with `git` or
   `gh` if signed in, otherwise with the connected GitHub app; whichever works. If a push
   races, pull and push again: message files never collide because names differ.
3. **Finish a WP, then post.** After your WP merges with green CI, post a message with
   `needs: review` naming the PR, the merge sha and the acceptance command. Then start
   your next board item without waiting.
4. **Reviews are short.** Read the PR diff and rerun only that WP's acceptance command.
   Reply with findings, each tagged **blocking** or **note**. A blocking finding also gets
   a `dispute` log in `docs/log/` (AGENTS.md section 5) and is fixed by the implementer in
   a new PR. A review does not replace the milestone cross-audit (WP-2.7).
5. **Never touch the other lane's paths or Status lines.** If you need something changed
   in the other lane, ask here.
6. **Save credits:** no sub-agents, no repeated full-suite runs when a focused test
   answers the question (CI runs the full suite on every PR), and no long messages.
7. **Stop and ask Peter in chat** (not here) only for a scope, source or licence decision,
   or a missing book. Everything else is settled in this channel.
8. Same repository rules as always: AGENTS.md, no em dashes, never guess engineering
   numbers, books stay in `Pietrols/QE-References`.
