---
project: JobMatch AI
slug: jobmatch-ai
date_built: 2026-02
last_updated: 2026-04-16
status: needs-polish
tags: [automation, ai-orchestration, scraping, productivity, workflow]
stack: [Claude Code, Python, SQLite, Telegram Bot API, OpenRouter, Google Docs API, Supabase]
effort: ~3 weeks
hero: ../assets/jobmatch-ai/hero.png
repo: https://github.com/89jdvm/job-search-automation
demo_video: null
---

# JobMatch AI

> An automated job-hunting pipeline that scrapes 15+ job boards every morning, scores each role against your profile, and sends the best matches to your phone — with one-tap approve to generate a tailored CV and application.

![hero](../assets/jobmatch-ai/hero.png)

## The Problem

Job hunting in international development and conservation is a nightmare of fragmented sources. Roles are posted across UN Careers, ReliefWeb, Idealist, ImpactPool, DevAid, LinkedIn, ClimateBase, and a dozen niche boards. Each has its own interface, its own search quirks, its own alert system.

I was spending 1-2 hours every morning just checking boards, reading descriptions, and deciding which were worth applying to. Then another hour per application tailoring a CV. The volume was crushing and the hit rate was low — most listings didn't match my actual profile.

## The Solution

JobMatch AI runs a fully automated pipeline every morning at 5am:

1. **Scrape.** 15+ specialized scrapers pull new listings from UN Careers, ReliefWeb, Idealist, ImpactPool, DevAid, LinkedIn alerts, ClimateBase, ClimateTechList, Acre, SCB, Conservation Job Board, OnThinkTanks, IFPRI, UNDP, and UNGM procurement.
2. **Deduplicate.** Cross-source dedup catches the same role posted on multiple boards.
3. **Pre-filter.** Quick keyword/location/seniority filters drop obvious mismatches before the expensive scoring step.
4. **Score.** Each surviving listing is scored against my detailed professional profile — skills match, sector relevance, seniority alignment, location fit. Scored 0-100.
5. **Route.** High scores (85+) trigger a "hot alert" to Telegram immediately. Everything else goes into a daily digest.
6. **Notify.** Telegram message with job title, org, score, and action buttons: `approve`, `skip`, or `url` to add the application link.
7. **Apply (on approval).** When I tap `approve` on my phone, Phase 2 kicks in: scrape the org's context, generate a tailored CV highlighting the most relevant experience, assemble a DOCX, verify it, and draft the application materials.

The whole thing runs while I sleep. I wake up to a curated shortlist on my phone.

## Screenshots

![Telegram alert](../assets/jobmatch-ai/telegram-alert.png)
*Hot alert on Telegram: score, key details, one-tap approve/skip.*

![Dashboard](../assets/jobmatch-ai/dashboard.png)
*Pipeline dashboard showing recent runs, score distribution, and approval funnel.*

## Result

- **Morning check: 2 minutes instead of 2 hours.** Review a curated list on Telegram instead of manually browsing 15 sites.
- **Higher hit rate.** Scoring surfaces roles I would have missed in the noise, and filters out the ones that look good but don't match.
- **One-tap applications.** Approving a job from my phone triggers CV generation automatically. Application prep time dropped from ~1 hour to ~15 minutes (review and submit).
- **Zero missed listings.** Scrapers run daily. Nothing falls through the cracks between board checks.
- **Full audit trail.** Every job, score, decision, and outcome is logged in SQLite. I can see patterns over time.

## Key Decisions

- **Profile-based scoring, not keyword matching.** A detailed markdown profile describes my skills, experience, preferences, and deal-breakers. The scorer reads the full job description against this profile. Much more accurate than keyword alerts.
- **Two-phase pipeline.** Phase 1 (scrape/score/notify) runs automatically and is cheap. Phase 2 (org research/CV generation) only runs on approval — saves time and API cost on roles I'll skip anyway.
- **Telegram as the control surface.** All decisions happen from my phone. `approve 42`, `skip 42`, `url 42 <link>`, `jobmatch status`. The edge function queues commands; a local poller drains them. Works even when my laptop is closed.
- **SQLite for the job database.** Simple, local, no server. The pipeline runs on my Mac and writes directly. Good enough for personal-scale data (~100-200 jobs/day).
- **WAT framework (Workflows, Agents, Tools).** Deterministic Python scripts handle all execution (scraping, scoring, CV generation). AI handles reasoning (scoring logic, CV tailoring). Keeps reliability high even across 50+ tool scripts.

## Under the Hood

**Stack:** Python (50+ tool scripts), SQLite (job database), Claude Code (orchestration + CV generation), Telegram Bot API (notifications + commands), OpenRouter (scoring), Google Docs API (CV assembly), Supabase (command queue via `jobmatch_commands` table), launchd (60s drain poller).

Architecture follows the WAT pattern: markdown workflows in `workflows/` define each process, Claude Code acts as the reasoning agent, and Python scripts in `tools/` handle deterministic execution. The master pipeline (`run_pipeline.py`) wires all Phase 1 tools in sequence. Phase 2 runs on-demand per approved job.

## How to Demo It

1. Show the Telegram daily digest: a list of scored jobs from this morning's run.
2. Tap into a high-scoring job. Show the score breakdown.
3. Type `approve 42` — show the confirmation and the Phase 2 pipeline kicking off.
4. Open the generated CV — point out how it's tailored to the specific role.
5. Show the dashboard: pipeline health, score distribution, approval funnel.
6. Show `jobmatch status` on Telegram for a quick summary.

## Limitations & Setup

- Scrapers break when job boards change their HTML. Maintenance is ongoing — expect 1-2 scrapers to need fixes per month.
- CV generation uses Claude via OpenRouter (~$0.05-0.10 per CV). Not free, but much cheaper than the time saved.
- Pipeline runs locally on the Mac via launchd. Mac needs to be awake at 5am for the daily run.
- Single-user system. The profile and scoring are specific to one person's career.
- Some job boards (LinkedIn) require authenticated sessions that expire periodically.

## Demo Pitch

> "I built an AI that checks 15 job boards every morning before I wake up, scores each role against my actual profile, and sends me the best matches on Telegram. When I see one I like, I tap 'approve' and it generates a tailored CV automatically. What used to take 3 hours a day now takes 2 minutes."
