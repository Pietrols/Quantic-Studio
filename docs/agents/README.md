# Agent channel: how Claude and ChatGPT talk

This folder is the conversation between the two models working on Quantic Studio, so
Peter does not have to relay messages. Peter's role: he tells each model "continue" (or
gives a ruling in chat), runs the software, and decides scope. Peter's chat instructions
always override this folder.

Roles (plan v3, Peter 2026-11-04; full table in `AGENTS.md` section 0):

- **Claude** (cloud): product owner. Writes and revises `PLAN.md`, answers requirement
  questions, accepts each milestone. Acts rarely to save credits.
- **ChatGPT** (Codex, cloud): product manager. Owns `BOARD.md` and the queue, reviews and
  merges worker PRs, returns rework, audits milestones, escalates.
- **DeepSeek workers** (OpenCode, on Peter's PC, and the OpenCode GitHub action for
  rework): build every WP. They write one message here at the end of each session.

Each agent works on its own clone or worktree of `Pietrols/Quantic-Studio` and talks
through this folder on `main` and through PR reviews.

## Files

- `BOARD.md`: the work queue per track and who is doing what. Only the PM (ChatGPT) edits it,
  except Claude's v3 handover edit.
- `messages/`: one file per message, never edited or deleted after it is pushed.
  Name: `YYYY-MM-DDTHHMMZ-<from>-<slug>.md` in UTC, for example
  `2026-10-14T1440Z-claude-hello.md`. Sorting by name gives the conversation in order.

Message format:

```
from: Claude | ChatGPT | DeepSeek
to: ChatGPT | Claude | DeepSeek | all
re: <WP id or topic>
needs: review | answer | nothing

<body: short and specific. Link PRs and commits by number and sha.>
```

## Rules

For worker PRs, review and merge follow `AGENTS.md` sections 3 to 5, which replace rules 3 and 4 below. Rules 6 (no sub-agents) applies to Claude and ChatGPT only; workers use the OpenCode agents in `.opencode/agents/`.

1. **Each time Peter says "continue":** get the latest `main` in whatever way your
   environment allows (a fetch, a fresh clone, or reading the files through the GitHub
   connection; the method does not matter), read `BOARD.md` and every message newer
   than your last one, then **keep building** your current board item. Do not stop to
   ask how to sync: if one method fails, use another, and say which in your next
   message. Reply in a new message file only when you have something to report, a
   review, or a question.
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
   or a missing book. Everything else is settled in this channel. Owned-path or plan
   bookkeeping questions go to Claude here; Claude answers them on `main`. While waiting,
   continue on the paths you already own.
8. Same repository rules as always: AGENTS.md, no em dashes, never guess engineering
   numbers, books stay in `Pietrols/QE-References`.
