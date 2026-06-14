---
project: Open Brain
slug: open-brain
date_built: 2026-03
last_updated: 2026-04-19
status: demo-ready
tags: [second-brain, ai-orchestration, productivity, automation, integration, executive-assistant, calendar-automation, gtd]
stack: [Supabase, pgvector, Deno, TypeScript, MCP Protocol, OpenRouter, Claude Code, Telegram, Google Calendar]
effort: ~3 weeks (ongoing)
hero: ../assets/open-brain/hero.svg
repo: https://github.com/89jdvm/open-brain
demo_video: null
---

# Open Brain

> A personal AI memory that listens, remembers, classifies your tasks, and books them on your calendar, all from a Telegram voice note.

![hero](../assets/open-brain/hero.svg)

## The Problem

I was using multiple AI tools (Claude, ChatGPT, voice notes, meeting transcripts) but none of them remembered anything from last week. Every conversation started from scratch. Insights I'd shared with one tool were invisible to the others.

Meanwhile, my task management was scattered across sticky notes, chat threads, and mental lists. Things I committed to in meetings would slip through the cracks because they never made it into a system.

Even when I did capture thoughts, the system was passive. It stored them and waited. I still had to remember to process my inbox, pick priorities, book time on my calendar. The friction wasn't gone. It had just moved.

I needed one place where all my thinking lives, where any AI I use can access it, and where action items don't just get stored: they get scheduled.

## The Solution

Open Brain is a personal database with AI superpowers that acts like a live-in executive assistant. Here's how it works:

1. **Capture anything from Telegram.** Send a voice note, text, or forwarded email. Transcribed, understood, stored, in seconds.
2. **Auto-classified at the moment of capture.** An LLM reads each capture and decides: is this a next action, something I'm waiting on someone else for, a project, or just a thought? What's the context (@computer, @phone, @errands)? What's the priority? When is it due? Did I say "on Friday" (do it Friday) or "by Friday" (deadline: do it before)?
3. **Auto-booked on your calendar.** When a task has a due date, Open Brain picks the earliest open 30-minute slot in your work blocks (mid-morning, afternoon, evening) and creates the event on a dedicated "Open Brain" Google Calendar. It respects your existing meetings but ignores multi-day busy blocks like travel or OOO. On reclassification or edits, the event reschedules itself.
4. **Block-aware briefings throughout the day.** Morning ping at 6 AM ("ready to work?"); when you reply, it piggybacks a full morning briefing with your calendar, priorities, and overdue items. Mid-morning at 10:30, afternoon at 3, nightly review at 9 PM. All timed to actual work blocks, not round-number office hours.
5. **One-tap edits in plain English.** Every confirmation comes with a 💬 "Edit in words" button. Reply "due Friday instead" or "change to @phone". The LLM patches the task, reconciles the calendar event, confirms.
6. **Search by meaning.** Ask "what did I say about the Ecuador project?" and it finds relevant thoughts even if you never used those exact words.
7. **Integrates with everything else.** Meeting Notetaker pushes action items as tasks. JobMatch AI funnel commands flow through the same router. Notetaker summaries land in the same memory. One brain for all of it.
8. **Works with any AI.** Built on the MCP protocol: Claude Code, Claude Desktop, and any future AI tool can plug into the same memory.

## Screenshots

<!-- broken image dropped at build time (PNG never created): ![Telegram capture](../assets/open-brain/telegram-capture.png) -->*Send a voice note or text to Telegram. It gets transcribed, classified, auto-scheduled on the calendar, and confirmed, with an edit button if you want to tweak it.*

<!-- broken image dropped at build time (PNG never created): ![GTD dashboard](../assets/open-brain/gtd-dashboard.png) -->*The GTD dashboard from Telegram: task counts by state, overdue items, stale waiting-fors.*

## Result

- **Zero-friction capture to calendar.** A voice note at the red light becomes a scheduled 30-minute block on my calendar before I reach the next light.
- **Nothing lost.** Every voice note, meeting summary, and random idea is searchable by meaning.
- **Tasks don't slip.** Action items auto-classify, auto-schedule, and surface again on nightly review if I missed them.
- **Briefings match my actual day.** No more 7 AM digest when I work from 10:30. Block-aware schedule mirrors when I'm actually at the keyboard.
- **On vs. by intent handled right.** "Call mom Friday" books Friday. "Submit report by Friday" books Thursday (buffer), Friday as last resort.
- **Always-on.** All scheduled automations run server-side on Supabase, no laptop required.

## Key Decisions

- **Autonomous classification, not confirm-then-act.** The LLM decides and acts immediately. Confirmation + edit button is the review surface, not a pre-commit gate. Friction stays at zero for the 95% case; edits handle the 5%.
- **Intent-aware scheduling ("on" vs "by").** A classifier field (`schedule_intent`) disambiguates action day vs deadline. "Friday" alone = on; "by Friday" = by. Scheduler builds different day preferences for each.
- **Ignore multi-day/all-day busy blocks when scheduling.** Travel days, OOO, focus-day blocks (≥12h) are dropped from conflict checks. Real meetings (<12h) are still respected. The scheduler assumes travel-day ≠ unavailable-for-all-work.
- **Morning piggyback pattern.** 6 AM ping fires via `pg_cron` regardless; the briefing only fires if/when the user replies during the morning window. Atomic claim RPC (`claim_morning_briefing`) prevents double-fires from race conditions between concurrent messages.
- **Non-blocking calendar writes.** Calendar API failures never fail the capture. The task still exists in GTD; a missing event is a warning, not an error.
- **Delete-and-recreate over patch for reschedules.** Simpler, correct in all cases, tolerated well by Google Calendar. No partial-state bugs.
- **Supabase + pgvector over dedicated vector DBs.** Everything in one Postgres database: thoughts, tasks, calendar links, embeddings. No extra services.
- **MCP protocol for the AI interface.** One MCP server, any AI client. Not locked into one vendor.
- **Scheduled briefings via pg_cron.** All automations run server-side. Zero infrastructure on the local machine.

## Under the Hood

**Stack:** Supabase (PostgreSQL + pgvector + Edge Functions + pg_cron), Deno/TypeScript, MCP Protocol (Model Context Protocol), OpenRouter (text-embedding-3-small + Claude Sonnet for classification), Google Calendar API v3 (service-account JWT), Claude Code, Telegram Bot API.

The `telegram-capture` edge function is the router: receives Telegram webhooks, transcribes voice via Groq Whisper, classifies via OpenRouter, persists the thought with embedding, auto-creates GTD tasks, and auto-books calendar events. The classifier returns a `gtd_decisions[]` array: one capture can produce multiple tasks (e.g. "text Carlos and schedule with Ana for Friday" = two decisions).

The scheduler module (`schedule_event.ts`) is a pure block-selection algorithm on top of an async Google Calendar writer. It generates candidate 30-minute slots across four fixed work blocks, queries freeBusy across the user's main + Open Brain calendars, filters out meetings but keeps all-day blocks out of scope, and picks the earliest conflict-free slot in the intent-aware day preference order.

The free-text edit flow uses a `pending_edits` table with a 10-minute TTL window. Tap "Edit in words", type a reply, an LLM patches the row, the calendar event reconciles, a new confirmation replaces the old one. All callbacks are prefixed (`ed:` for edit, `rv:` for review) to keep the two flows separate.

The MCP server runs as a Supabase Edge Function exposing `capture_thought`, `search_thoughts`, `list_thoughts`, `thought_stats`, and the GTD management tools (`gtd_add_task`, `gtd_update_task`, `gtd_list_tasks`, `gtd_process_inbox`, `gtd_manage_project`, `gtd_dashboard`, `gtd_weekly_review`).

## How to Demo It

1. Open Telegram. Send a voice note: *"Remind me to follow up with Maria about the carbon credits proposal by next Friday."*
2. Show the instant reply: task classified as a next-action, `@computer`, due Friday, **scheduled for Thursday 3:00 PM on the Open Brain calendar** (note: "by Friday" = buffer day).
3. Send a second voice note: *"Call Ana on Friday at the cooperative."* Show it scheduled for Friday itself (note: "on Friday" = action day).
4. Show Google Calendar: both events on the Open Brain calendar, correctly placed.
5. Tap 💬 Edit in words on one of them: *"change to Monday."* Watch the calendar event update in place.
6. Send `/status`: GTD dashboard shows both tasks.
7. Open Claude Code and use `search_thoughts` MCP tool with the same query: same memory accessible from any AI tool.

## Limitations & Setup

- Requires a Supabase project with pgvector extension enabled, pg_cron configured, and Edge Functions deployed with `--no-verify-jwt`.
- OpenRouter API key needed for embeddings + classification (~$0.02/capture with classification).
- Google Calendar integration needs a service account with `calendar` scope and a user-created "Open Brain" calendar shared with the service-account email.
- MCP server runs as a Supabase Edge Function; connect Claude Desktop via Settings → Connectors → Add custom connector.
- Single-user system. Multi-user would need Row Level Security policies.
- Semantic search quality depends on embedding model: works well for English and Spanish, other languages untested.
- Fixed 30-min slot duration and fixed work-block boundaries (6–8:30, 10:30–12:30, 15–17, 21–23). Dynamic block detection is future work.

## Demo Pitch

> "I send a voice note to Telegram. By the time I finish talking, the task is classified, booked on my calendar in my next free work block, and confirmed with a tap-to-edit button. Meanwhile every thought is semantically searchable from any AI tool I use. It's the glue between my voice, my tasks, my calendar, and every AI I use."

## Changelog

- **2026-04-19: Executive Assistant upgrade (Phases 1–3 shipped).** Added block-aware briefing schedule with 6 AM morning ping + piggyback pattern, auto-classification via LLM (`gtd_decisions[]` array) at capture time, free-text "Edit in words" flow with 10-minute TTL, Google Calendar auto-scheduling with `on` vs `by` intent semantics, ignore-multi-day-busy-blocks policy, 30-min slot picker across four fixed work blocks, atomic claim RPC for briefing race-safety. ~25 commits across three feature branches fast-forwarded to main; 4 edge functions redeployed. 105/105 Deno tests passing.
- **2026-04-16: Phase 1 SHIPPED.** New pg_cron schedule (morning ping 06:00, mid-morning 10:30, afternoon 15:00, nightly review 21:00, weekly GTD Fri 16:00), `daily_state` table, English-only prompts, atomic claim for morning-briefing piggyback (Codex-reviewed race fix).
- **2026-03: Initial build.** Core capture + semantic search + GTD + MCP + scheduled briefings via pg_cron.
