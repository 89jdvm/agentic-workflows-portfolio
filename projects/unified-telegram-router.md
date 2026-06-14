---
project: Unified Telegram Router
slug: unified-telegram-router
date_built: 2026-04
last_updated: 2026-04-16
status: needs-polish
tags: [automation, ai-orchestration, second-brain, telegram, integration, productivity]
stack: [Claude Code, Supabase Edge Functions, Deno, TypeScript, PostgreSQL, Telegram Bot API, Groq Whisper, OpenRouter]
effort: ~3 days (4-phase rollout, completed 2026-04-16)
hero: ../assets/unified-telegram-router/hero.svg
repo: /Users/jdlovesyou/Agentic Workflows/OB1
demo_video: null
---

# Unified Telegram Router

> One Telegram chat, three personal AI workflows, zero dependence on a laptop being open. The backbone that makes my second brain, job-search assistant, and meeting notetaker all reliably reachable from my phone.

![hero](../assets/unified-telegram-router/hero.svg)

## The Problem

I had three different AI workflows running my life: a second brain (Open Brain) for capturing thoughts and tasks, a job-search assistant (JobMatch AI) that finds and applies to roles, and a meeting notetaker that records and summarizes calls.

All three spoke to me through one Telegram chat on my phone. Convenient in theory, but **nothing worked reliably**. For weeks, sending a voice note, approving a job, or pasting a meeting link would sometimes succeed and sometimes vanish. Fixing one workflow would break another. After a month of patching I had no idea what was running or where.

The root cause turned out to be simple: my Telegram "bot" was actually Claude Code on my laptop, polling for messages every few seconds. If my laptop was closed, asleep, or just not running Claude Code, messages disappeared. The whole thing was dressed up like infrastructure but was really a single interactive session masquerading as always-on service.

## The Solution

I replaced the brittle laptop-based router with a small cloud function that runs 24/7 on Supabase. Now when I send a message from my phone:

1. Telegram delivers the message directly to my cloud function (webhook mode, replaces the old "phone home every 3 seconds" polling).
2. The function authenticates the request (only my Telegram account, only with the right secret header), checks for duplicates, and fires an instant ⚡ reaction so I know it was received.
3. Simple commands like `task: buy milk` or `done: mow lawn` are handled right there in the cloud. They update my GTD database directly and reply back in under a second.
4. Voice notes are transcribed by Groq's free Whisper model, turned into captured thoughts with extracted action items, and confirmed back to me.
5. Every event is logged to a small audit table so I can ask `/status router` and see exactly what's been happening.

My laptop never has to be on. My Claude Code plugin for Telegram is retired. The system either works for everyone or fails clearly. No more ambiguous breakage.

## Screenshots

<!-- broken image dropped at build time (PNG never created): ![Phase 1a test flow on Telegram](../assets/unified-telegram-router/test-flow.png) -->*Quick test flow after deployment: `task:` adds to inbox, `done:` marks it complete, plain text captures with auto-extracted action items, voice notes transcribe and capture. All running with my laptop closed.*

<!-- broken image dropped at build time (PNG never created): ![Router status audit](../assets/unified-telegram-router/status-router.png) -->*`/status router` lets me check the last 24 hours of activity: what commands ran, any errors, all from my phone.*

## Result

- **Always-on routing.** Messages that would have been silently lost when my laptop was closed now land reliably. My Telegram interface finally behaves like the production tool it was pretending to be.
- **Instant feedback.** ⚡ reaction within a second of sending, typed reply within ~2 seconds for most commands. Felt responsive from the first test.
- **Zero marginal cost.** Built on Supabase's free tier + Groq's free Whisper tier + my existing Claude Max subscription. No new recurring spend.
- **Observable.** Every message is audited. I can ask the bot itself what it's been doing.
- **All workflows integrated.** JobMatch approvals, meeting bot dispatch, scheduled briefings. Everything runs through the same router. Four phases, all complete.
- **Proactive check-ins.** Morning prep, evening review, weekly GTD review, and stale waiting-for alerts arrive automatically via Telegram. No laptop needed. Server-side pg_cron.

Time saved: hard to quantify because the alternative wasn't "slower." It was "broken." What I recovered was **trust** in the system, which means I actually use it again.

## Key Decisions

- **Cloud function as dumb router, Claude routines for smart work.** The cloud function doesn't reason; it just validates and dispatches. Claude reasoning happens either (a) inline via direct database calls for trivial ops or (b) by firing a cloud-hosted Claude Code routine for anything complex. This keeps the router simple enough to debug and the intelligent work close to the data it needs.
- **Inline-first, routines second.** My subscription gives me 15 "routine runs" per day. Heavy tasks (voice capture, meeting summary, job approval) earn the routine spend; trivial mutations (`task:`, `done:`, status queries) handle themselves inline in the router. Worth the architectural split.
- **Phase-by-phase, old bot kept running.** Phase 1a replaces only the router, the fragile bit, without touching the specialized workflows. Each later phase adds one piece. If anything breaks, rollback is a single `deleteWebhook` call.
- **Plain-text output for any user-supplied content.** Learned the hard way: Telegram's Markdown parser silently drops messages with unbalanced `_`. Any reply containing user titles or internal category names goes through a non-Markdown send path.
- **Security at the edge.** Telegram webhook requires a matching secret token header and my chat ID is explicitly allow-listed. The cloud function rejects anything else before it even reads the payload.

## Under the Hood

**Stack:** Supabase Edge Functions (Deno/TypeScript), PostgreSQL, Telegram Bot API (webhook mode), Groq Whisper-large-v3, OpenRouter (embeddings + metadata extraction via GPT-4o-mini), Claude Code Routines (planned for later phases).

The edge function lives at `supabase/functions/telegram-capture/index.ts`. It owns three responsibilities: authenticate, classify, dispatch. Supporting tables: `telegram_update_dedup` (idempotency), `router_audit` (observability), plus the existing Open Brain `thoughts` and `gtd_tasks` tables. For reasoning-heavy flows in later phases, the router will fire Claude Code Routines via their `/fire` API endpoint, cloud-hosted Claude sessions with MCP access and repo clones, funded by my Claude Max subscription.

## How to Demo It

1. Show the before: describe how I used to send a voice note and cross my fingers hoping my laptop was awake.
2. **Close the laptop lid.**
3. From phone: send `task: demo task`. Show the instant ⚡ reaction, then the reply "Task added."
4. Send `done: demo task`. Reply: "✓ Done."
5. Send a voice note ("Remind me to call Juan Tuesday at 3"). Reply: transcription + captured as an observation + auto-created GTD task.
6. Send `/status router`. Reply: a table of the last 24 hours of events.
7. Open the Supabase dashboard briefly to show the `router_audit` rows being written in real time.

## Limitations & Setup

- Requires a deployed Supabase project with Edge Functions enabled, a Telegram bot token, and the Telegram webhook pointed at the function URL.
- Both pollers (JobMatch + Notetaker) require the Mac to be awake. Scheduled briefings run server-side and don't.
- Single-user system. The edge function allow-lists one Telegram chat ID.

## Demo Pitch

> "I use Telegram to talk to my AI systems from my phone. For weeks it was a mess. Messages would disappear if my laptop happened to be closed. I rebuilt the plumbing so the whole thing runs in the cloud, handles the quick stuff itself, and calls out to smarter agents only when needed. Now I can close my laptop on Friday and my assistants still work on Saturday."
