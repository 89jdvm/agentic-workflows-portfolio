---
project: Open Brain
slug: open-brain
date_built: 2026-03
last_updated: 2026-04-16
status: needs-polish
tags: [second-brain, ai-orchestration, productivity, automation, integration]
stack: [Supabase, pgvector, Deno, TypeScript, MCP Protocol, OpenRouter, Claude Code, Telegram]
effort: ~2 weeks (ongoing)
hero: ../assets/open-brain/hero.svg
repo: https://github.com/89jdvm/open-brain
demo_video: null
---

# Open Brain

> A personal AI memory that remembers everything you tell it, finds connections you'd miss, and keeps your to-do list in sync — accessible from any AI tool you use.

![hero](../assets/open-brain/hero.svg)

## The Problem

I was using multiple AI tools — Claude, ChatGPT, voice notes, meeting transcripts — but none of them remembered anything from last week. Every conversation started from scratch. Insights I'd shared with one tool were invisible to the others.

Meanwhile, my task management was scattered across sticky notes, chat threads, and mental lists. Things I committed to in meetings would slip through the cracks because they never made it into a system.

I needed one place where all my thinking lives, where any AI I use can access it, and where action items don't disappear.

## The Solution

Open Brain is a personal database with AI superpowers. Here's how it works:

1. **Capture anything.** Send a thought from Telegram (text or voice), and it's stored with semantic meaning — not just words, but what those words are about.
2. **Search by meaning.** Ask "what did I say about the Ecuador project?" and it finds relevant thoughts even if you never used those exact words. It understands concepts, not just keywords.
3. **Auto-extract action items.** When you capture a thought like "Need to follow up with Maria about the proposal by Friday," the system automatically creates a task in your to-do list.
4. **GTD task management.** A full Getting Things Done system: inbox, next actions, projects, waiting-for, someday/maybe. Process your inbox from Telegram with quick commands.
5. **Works with any AI.** Built on the MCP protocol — Claude Code, Claude Desktop, and any future AI tool can plug into the same memory. One brain, all your tools.
6. **Scheduled check-ins.** Morning briefings, evening reviews, and weekly GTD reviews arrive automatically via Telegram — no laptop needed.

## Screenshots

![Telegram capture](../assets/open-brain/telegram-capture.png)
*Send a voice note or text to Telegram. It gets transcribed, embedded, metadata-extracted, and stored — with action items auto-routed to your task inbox.*

![GTD dashboard](../assets/open-brain/gtd-dashboard.png)
*The GTD dashboard from Telegram: task counts by state, overdue items, stale waiting-fors.*

## Result

- **Zero-friction capture.** Thoughts go from my head to the database in seconds, from anywhere.
- **Nothing lost.** Every voice note, meeting summary, and random idea is searchable by meaning.
- **Tasks don't slip.** Action items from meetings and voice notes auto-create tasks. Weekly reviews catch stale items.
- **Always-on.** Briefings and reviews run server-side on a schedule — no laptop needed.
- **Portable.** Any AI tool that supports MCP can access the full memory. Not locked into one vendor.

## Key Decisions

- **Supabase + pgvector over dedicated vector DBs.** Keeps everything in one Postgres database — thoughts, tasks, metadata, embeddings. No extra services to manage or pay for.
- **MCP protocol for the AI interface.** Instead of building custom integrations for each AI tool, one MCP server exposes capture, search, list, and stats tools. Any MCP-compatible client connects instantly.
- **OpenRouter for embeddings and metadata extraction.** GPT-4o-mini via OpenRouter handles both semantic embeddings and structured metadata extraction (people, topics, action items, dates) at ~$0.01 per thought. Avoids vendor lock-in.
- **GTD built into the same database.** Tasks aren't a separate app — they share the same Supabase instance. A captured thought with action items creates tasks automatically. Meeting summaries push tasks. Everything is connected.
- **Scheduled briefings via pg_cron.** Morning prep, evening review, weekly GTD review, and stale waiting-for checks run as Supabase cron jobs calling an edge function. Zero infrastructure on the local machine.

## Under the Hood

**Stack:** Supabase (PostgreSQL + pgvector + Edge Functions + pg_cron), Deno/TypeScript, MCP Protocol (Model Context Protocol), OpenRouter (text-embedding-3-small + GPT-4o-mini), Claude Code, Telegram Bot API.

The MCP server runs as a Supabase Edge Function exposing five tools: `capture_thought`, `search_thoughts`, `list_thoughts`, `thought_stats`, and GTD management tools (`gtd_add_task`, `gtd_update_task`, `gtd_list_tasks`, `gtd_process_inbox`, `gtd_manage_project`, `gtd_dashboard`, `gtd_weekly_review`). Thoughts are stored with 1536-dimensional embeddings for semantic search via `match_thoughts` RPC. Metadata extraction runs inline at capture time.

## How to Demo It

1. Open Telegram. Send a voice note: "Remind me to follow up with Maria about the carbon credits proposal by next Friday."
2. Show the instant reply: thought captured, action item created.
3. Send `/status` — show the GTD dashboard with the new task in inbox.
4. Send "What do I know about carbon credits?" — semantic search finds the thought even without exact keyword match.
5. Open Claude Code and use `search_thoughts` MCP tool with the same query — same results, demonstrating cross-tool access.

## Limitations & Setup

- Requires a Supabase project with pgvector extension enabled.
- OpenRouter API key needed for embeddings and metadata extraction (~$0.01/thought).
- MCP server runs as a Supabase Edge Function — needs deployment with `--no-verify-jwt`.
- Single-user system. Multi-user would need Row Level Security policies.
- Semantic search quality depends on embedding model — works well for English and Spanish, other languages untested.

## Demo Pitch

> "Every thought, voice note, and meeting takeaway goes into one AI-powered memory. Any AI tool I use can search it by meaning — not just keywords. And action items I mention automatically become tasks. It's the glue that makes all my other AI tools actually useful."
