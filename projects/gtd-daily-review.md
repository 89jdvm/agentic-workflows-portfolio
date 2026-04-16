---
project: GTD Daily Review (Telegram)
slug: gtd-daily-review
date_built: 2026-04
last_updated: 2026-04-14
status: needs-polish
tags: [productivity, second-brain, gtd, telegram, automation, voice]
stack: [Supabase Edge Functions, Deno, TypeScript, Postgres, Telegram Bot API, Google Calendar, Groq Whisper, OpenRouter]
effort: ~1 day
hero: ../assets/gtd-daily-review/hero.png
repo: /Users/jdlovesyou/Agentic Workflows/OB1
demo_video: null
---

# GTD Daily Review (Telegram)

> A Telegram bot that turns inbox processing into a tap-driven conversation. Every thought you send gets captured to your second brain, and `/daily` walks you through your GTD inbox one item at a time with inline buttons.

![hero](../assets/gtd-daily-review/hero.png)

## The Problem

I had 50+ captured thoughts piling up in my GTD inbox — voice notes, messages, emails, random ideas from the day. Processing them meant sitting at a computer, context-switching away from whatever I was actually doing, and working through each one in a text conversation. A 30-item inbox turned into a 90-minute ordeal. I kept avoiding it, the inbox kept growing, and important next actions got lost in the noise.

The GTD method says the clarify-to-zero step should be fast and reflexive. It wasn't.

## The Solution

A Telegram bot that does two things:

1. **Captures everything passively.** Text messages become thoughts. Voice notes get transcribed and captured. Action items get auto-extracted into GTD tasks. This already existed.

2. **Processes the inbox with one command.** Send `/daily` from your phone. The bot walks you through every inbox item one at a time, with a keyboard of buttons below each one:

```
📥 Inbox  ▓▓▓▓░░░░░░░░  4/12

send in invoice for payment

 🎯 Next    ⏳ Wait    💭 Someday
 ✅ Done    🗑 Drop    📂 Project
 ℹ️ Context ⏭ Skip    🛑 End
```

Each tap is one decision:
- **Done / Drop / Someday** → one tap, committed, next item.
- **Next** → three more taps: context (@computer / @phone / @errands …), priority, due date.
- **Wait** → one tap, reply with the person's name.
- **Project** → one tap, reply with the project name. A new project is created and this task becomes its first next action.
- **Context (ℹ️)** → pulls the original captured thought so you remember why you wrote it.
- **Skip** → leaves it in the inbox, moves on.
- **End** → wraps the review early.

When the last item is done, the bot sends a summary: today's calendar, do-now tasks, due today, overdue, and stale waiting-for items.

## Screenshots

![Inbox card with decision buttons](../assets/gtd-daily-review/inbox-card.png)
*Each inbox item appears as a single message with decision buttons. Tap one and the card updates in place.*

![Next action sub-flow](../assets/gtd-daily-review/next-subflow.png)
*"Next" opens a sub-flow: context → priority → due date. Four taps total.*

![End-of-review summary](../assets/gtd-daily-review/summary.png)
*After the last item, the bot renders today's calendar, do-now tasks, overdue, and stale waiting-for.*

## Result

- **Processing time:** 50-item inbox went from ~90 minutes of typing to ~4 minutes of tapping.
- **Phone-first:** works from the lock screen. No laptop, no context switch.
- **Zero data loss:** 22 automated end-to-end tests cover every classification path, session timeout, duplicate session, malformed callback, voice-during-pending, and capture-flow regression.
- **Non-destructive:** skipping leaves tasks alone; `/cancel` only clears the session; no task mutation is ever reverted.

## Key Decisions

- **Stateless bot, stateful database.** Every button tap is a fresh HTTP request. All review state lives in a `gtd_review_sessions` table; the function reads it, acts, writes it back. Sessions carry a short-id prefix in every callback payload so stale buttons from a restarted session fail loud instead of silently corrupting state.
- **Edit cards in place.** When you tap a button, the card updates rather than sending a new message. The chat stays clean even after 50 taps. Edits that fail (message deleted, too old) fall back to a new message — no dead ends.
- **Voice notes during pending prompts.** If the bot asks "waiting on who?" and you reply with a voice note instead of typing, it transcribes the voice and uses the transcript as the delegate name. Mobile-first reality.
- **Webhook test harness over unit tests.** This is an integration on top of Supabase, Telegram, and Postgres — the interesting bugs are wire-protocol bugs. So the test suite POSTs real webhook payloads to the deployed function and queries the database to verify state transitions. Runs in <30 seconds.
- **Deliberate 30-min session timeout.** Long enough to get interrupted and come back. Short enough that a tap from yesterday's half-finished session fails safely.

## Under the Hood

**Stack:** Supabase Edge Functions (Deno/TypeScript), Postgres with `gtd_*` schema, Telegram Bot API (inline keyboards + callback queries), Google Calendar service account, Groq Whisper (voice transcription), OpenRouter (embedding + metadata extraction for captures).

The daily review flow is implemented as a single Edge Function that branches on Telegram update type:
- `callback_query` → `handleCallback` → resolves session by chat_id + short prefix, validates cursor, dispatches to per-action handler.
- `message.text` starting with `/` → command router (`/daily`, `/cancel`, `/status`, `/help`).
- `message.text` when a session has `pending_stage != null` → consumed as free-text follow-up (delegate name, project name).
- Everything else → falls through to the existing capture pipeline (embedding + thought insert + auto-task-creation).

Two helper Edge Functions support it: `gtd_task_context` (pulls the source thought for the ℹ️ Context button) and `gtd_calendar_today` (wraps the Google Calendar API for the `/status` command and the end-of-review summary).

## How to Demo It

1. "Open your phone. Here's my Telegram bot."
2. "Watch what happens when I send a voice note." *(dictate a thought with a few action items)* — bot replies in a few seconds: "Captured as task — 3 task(s) added to GTD inbox."
3. "Now watch this." *(send `/daily`)* — bot shows: "📥 Inbox 1/N" + title + buttons.
4. Tap through 3-4 items: one Done, one Next → @computer → high → tomorrow, one Wait → reply "Sarah".
5. When the review finishes, the summary message appears with today's calendar and overdue list.
6. "90 minutes → 4 minutes. Works from the lock screen. Never misses a capture."

## Limitations & Setup

Needs:
- A Telegram bot token
- Open Brain core schema (Postgres + pgvector) with the GTD extension applied
- Supabase project with secrets set: `TELEGRAM_BOT_TOKEN`, `OPENROUTER_API_KEY`, `GROQ_API_KEY`, and (optional but recommended) `GOOGLE_SERVICE_ACCOUNT_EMAIL` / `GOOGLE_PRIVATE_KEY` / `GOOGLE_CALENDAR_ID`
- Telegram webhook pointed at the deployed `telegram-capture` Edge Function

Single-user today — tasks are stored under a fixed UUID. Multi-user would take ~1 hour: add a `telegram_user_id → supabase_user_id` mapping table and parameterize the `USER_ID` constant.

Doesn't render Telegram's `MarkdownV2` everywhere — uses the classic Markdown parse mode and escapes only the characters that matter. One or two special chars in task titles could render weirdly; a future pass could switch to MarkdownV2 with a stricter escape.

## Demo Pitch

"I used to avoid my GTD inbox because processing it took an hour and required sitting at my computer. Now I tap through the whole thing from the bus in four minutes. Same method, different interface — and because the bot captures voice notes and auto-creates tasks, the inbox fills itself without me thinking about it."
