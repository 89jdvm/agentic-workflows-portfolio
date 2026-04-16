---
project: Meeting Notetaker
slug: meeting-notetaker
date_built: 2026-04
last_updated: 2026-04-16
status: needs-polish
tags: [automation, ai-orchestration, meetings, productivity, second-brain]
stack: [Claude Code, Recall.ai, Telegram Bot API, Open Brain, Supabase, Next.js, Python, OpenRouter]
effort: ~2 days
hero: ../assets/meeting-notetaker/hero.png
repo: ~/Agentic Workflows/Notetaker
demo_video: null
---

# Meeting Notetaker

> Automatically joins your video calls, turns every meeting into a clean summary with action items and highlights, and drops the tasks straight into your to-do list.

![hero](../assets/meeting-notetaker/hero.png)

## The Problem

I was using a popular free AI notetaker, but it capped me at five 1-hour meetings per month. Paid plans were expensive for what I actually needed. Worse:

- I couldn't join last-minute meetings that weren't on my calendar.
- Action items stayed trapped in the notes — I had to re-read them and copy each task into my to-do list by hand.
- Output was locked inside a closed tool. I couldn't feed it to other AI tools I was building.

So meetings kept generating friction: the notes existed, but the follow-through didn't.

## The Solution

Meeting Notetaker runs in the background and handles the whole lifecycle:

1. **Joining.** Either automatically from a calendar event, or on demand — paste a meeting link into Telegram and send `/join`.
2. **Recording.** A bot joins the call, records, and transcribes the whole thing.
3. **Processing.** When the meeting ends, the system generates a structured summary: what happened, who committed to what, key decisions, highlights.
4. **Routing.** Action items that belong to me land directly in my personal task inbox. The full summary lands in my personal knowledge base, searchable alongside everything else I've captured.
5. **Browsing.** A local dashboard gives me a fast way to flip through any past meeting — transcript, action items, highlights, metadata — without digging through files.

## Screenshots

![Dashboard overview](../assets/meeting-notetaker/dashboard.png)
*The dashboard index — every processed meeting, one click to the detail view.*

![Action items aggregate](../assets/meeting-notetaker/action-items.png)
*Cross-meeting action items, grouped by owner. This is the view I actually check every morning.*

![Detail view](../assets/meeting-notetaker/detail.png)
*Per-meeting tabs: transcript, action items, highlights, meta.*

## Result

- **No cap**: unlimited meetings, no freemium wall.
- **No manual task entry**: commitments made in calls show up in my inbox the same day.
- **Portable output**: summaries are plain markdown files, usable by any AI tool.
- **Ad-hoc joins**: can capture any meeting with a one-line message, not just scheduled ones.
- **Ballpark time saved**: 15–30 minutes per meeting (skipping manual notes + extracting action items). Over a typical week that's 2–4 hours back.

## Key Decisions

- **Separation of reasoning and execution.** AI handles the interpretation — reading transcripts, extracting commitments, writing summaries. Deterministic Python scripts handle the mechanics — downloading transcripts, file writes, API calls. If every step were AI, compounding small errors would tank reliability. This split keeps the system trustworthy.
- **Markdown as the universal output.** Every summary, action-item list, and highlight is a plain `.md` file. It renders well, versions cleanly in git, and any future AI tool can read it directly — no export step.
- **Polling over webhooks.** Recall's per-bot webhook parameter silently ignored delivery after 3 test cycles. Switched to a 60-second launchd poller — same pattern that works for JobMatch. Pragmatic over elegant.
- **Cross-meeting action-item view.** Individual per-meeting notes are useful, but what I actually need daily is "what do I owe people across every meeting this week?" The aggregate view is the driver.
- **Action items for me auto-route to my task inbox.** The loop closes on its own — meeting ends, commitments are queued for review, no manual step.

## Under the Hood

**Stack:** Claude Code (orchestration), Recall.ai (meeting bot), Telegram Bot API (command surface), Open Brain MCP (personal knowledge base + GTD), Next.js (dashboard), Python (deterministic tools), Google Calendar (auto-join), SQLite (state store).

Bot dispatch is handled by the Telegram router edge function (Supabase). Processing runs locally via `drain_notetaker_jobs.py` (launchd, every 60s): polls Recall API for finished bots, fetches transcripts, summarizes via OpenRouter gpt-4o-mini (~$0.01-0.05/meeting), writes output files, and pushes to Open Brain + GTD. All credentials live in `.env` — never checked in, never shown.

## How to Demo It

1. Open Telegram. Paste a Google Meet link and send `/join <url>`.
2. Show the bot dialing into the call.
3. End the call. Within a minute or two, the system processes the transcript.
4. Switch to the dashboard — the new meeting is at the top of the index.
5. Open it. Show the tabs: transcript, action items (grouped by owner), highlights, meta.
6. Switch to the cross-meeting action items page. Point out that tasks assigned to me are already queued in my to-do inbox.

## Limitations & Setup

- Recall.ai is a paid service (pay-per-meeting-minute). Not free, but an order of magnitude cheaper than alternatives at my volume.
- Summarization via OpenRouter gpt-4o-mini costs ~$0.01-0.05 per meeting.
- The drain poller runs locally via launchd — Mac must be awake for processing.
- Bot dispatch runs server-side (edge function) — works even with laptop closed.
- Single-user system today. Multi-user would need a proper auth layer.
- Spanish calls work fine; other non-English languages depend on the transcription model's coverage.

## Demo Pitch

> If you sit through a lot of calls and you're constantly losing track of what you committed to, this records every meeting, turns it into a clean summary, and drops your action items straight into your task list — without you doing anything. It pays for itself in about a week of meetings.
