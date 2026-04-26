---
project: JobMatch AI
slug: jobmatch-ai
date_built: 2026-02
last_updated: 2026-04-26
status: in-progress
tags: [job-search, ai-orchestration, document-generation, telegram-bot, automation]
stack: [Python, SQLite, Anthropic API, Telegram Bot API, Supabase, Google APIs, Playwright, python-docx, pikepdf]
effort: ~1 month (ongoing)
hero: ../assets/jobmatch-ai/hero.svg
repo: https://github.com/89jdvm/job-search-automation
demo_video: null
---

# JobMatch AI

> A fully automated job-hunting pipeline that scrapes 25+ boards every morning, scores each role with a bespoke rubric, sends the best matches to your phone, and generates a tailored CV and application package with one Telegram command.

![hero](../assets/jobmatch-ai/hero.svg)

## The Problem

Job hunting in international development and conservation means checking 25+ fragmented sources daily — UN Careers, ReliefWeb, ImpactPool, ClimateBASE, procurement feeds, conservation boards, direct org sites. Each has its own interface and alert system. A good role might appear on four boards, or only one obscure one.

What I was doing before: 2–3 hours every morning scanning boards, reading descriptions, deciding what was worth pursuing. Then another 1–2 hours per application tailoring a CV. The noise was crushing, the hit rate was low, and I still missed things.

## The Solution

JobMatch AI runs a two-phase automated pipeline — Phase 1 every morning at 5am without touching the laptop, Phase 2 on-demand the moment I approve a job from my phone.

### Phase 1 — Discovery (runs while I sleep)

1. **Scrape.** 25+ specialized scrapers pull new listings from UN Careers, ReliefWeb, UNDP, ImpactPool, ClimateBASE, Conservation Job Board, DevNetJobs, UNGM procurement, Idealist, GlobeSmart, target org sites (25 dream employers monitored directly), LinkedIn email alerts, and more.
2. **Deduplicate.** Cross-source dedup catches the same role posted on multiple boards, so I never see it twice.
3. **Pre-filter.** Hard rules drop obvious mismatches before the expensive scoring step — wrong seniority, wrong geography, salary floor violations.
4. **Score.** Two-stage AI: Haiku batches all surviving jobs (0–100 rubric with prompt caching for ~$0.65/month), then Sonnet re-scores the borderline range (45–72) where the rough model's confidence is lowest. Final score = HOT (85+), WARM (60–84), COLD, or SKIP.
5. **Route.** Deterministic logic assigns an action plan: `INSPIRA_PDF` (UN jobs), `EMAIL_FULL`, `EMAIL_CV_ONLY`, `PORTAL_UPLOAD`, or `MANUAL_REVIEW`. Zero AI in this step — rules based on org type and application requirements extracted during scoring.
6. **Notify.** Telegram HOT alert immediately for ≥85 scores. Daily digest at 8am with all WARM jobs, each with deadline countdown and the action plan already decided.

### Phase 2 — Application (on-demand, triggered by one Telegram command)

When I type `approve 75831` on my phone:

1. Scrapes the organization's context (website, about page) for CV personalization.
2. Generates a tailored CV in JSON using Sonnet — mirrors exact JD vocabulary, includes a gap acknowledgment if I'm missing a stated requirement (e.g., "I hold a BSc in Engineering, not an MSc in IR, but I've led governance tables across 3 Amazonian provinces…"), bold-highlights ATS keywords.
3. Assembles DOCX via template engine.
4. Runs Haiku hallucination check — cross-references every metric and credential in the CV against my profile. If it invented something, flags it for review instead of staging.
5. For UN Inspira jobs: generates an offline PDF template + a pre-filled cheatsheet (salary history, supervisor contacts, education dates, languages, publications, certifications) — turns a 3-hour Inspira form-filling session into 20 minutes.
6. Creates a Gmail draft ready to send (for email-apply jobs).
7. Creates a GTD next-action task + schedules a 60-minute calendar block automatically, computed from the job's deadline.
8. Sends me a Telegram confirmation with file paths and the next step.

## Screenshots

![Telegram alert](../assets/jobmatch-ai/telegram-alert.png)
*Daily digest on Telegram: score, org, deadline countdown, action plan — all decided before I see it.*

![Dashboard](../assets/jobmatch-ai/dashboard.png)
*Pipeline dashboard: score distribution, approval funnel, source ROI.*

## Result

- **Morning review: 5 minutes instead of 3 hours.** I wake up to a curated shortlist with deadlines and action plans already set.
- **Zero missed listings.** 25+ scrapers run daily. Nothing falls through the cracks.
- **Application prep: ~20 minutes instead of ~2 hours.** One Telegram command starts a pipeline that handles org research, CV writing, keyword optimization, and hallucination checking.
- **UN Inspira savings: ~2.5 hours per application.** The cheatsheet pre-answers the 30+ form fields that require digging through records.
- **Full audit trail.** Every job, score, decision, and outcome logged in SQLite. I can see which sources produce results and which waste tokens.
- **Cost: ~$0.65/month** for scoring ~140 jobs/week (Haiku with prompt caching + Sonnet re-scoring ~15% of jobs).

## Key Decisions

**Two-stage AI scoring instead of one model.** Haiku is fast and cheap but imprecise near the threshold. Running Sonnet only on the 45–72 range (borderline jobs) gets precision where it matters without burning money on clear SKIPs. Cost delta: ~$0.05/month more than Haiku-only, negligible accuracy improvement on obvious HOT/COLD, meaningful on the fence-sitters.

**Bridge multiplier for cross-domain candidates.** My profile spans governance architecture, bioeconomy, trade policy, and sustainability consulting — rare combinations. The rubric adds +5–12 points when a job touches 2+ of my expertise clusters. Without this, many of the most relevant roles (e.g., "Trade & Climate Policy Advisor") score mid-range because no single dimension fully fires.

**Gap acknowledgment in CV generation.** Most tailored CV systems pretend the candidate has everything required. This one acknowledges gaps upfront, then pivots to compensating evidence. Counterintuitively, this increases credibility — especially for UN/INGO hiring managers who read hundreds of CVs that claim perfect fits.

**Deterministic action plan routing (zero AI).** After scoring, routing to INSPIRA_PDF vs. EMAIL_FULL vs. PORTAL_UPLOAD uses hard rules, not AI inference. The AI scores relevance; the rules handle logistics. Keeps the routing fast, auditable, and free of hallucinated instructions.

**Telegram as the only control surface.** All approvals, skips, URL additions, and status checks happen from my phone via chat. No app to open, no dashboard to load. The edge function on Supabase queues commands; a local drain poller processes them. Works even when the laptop is closed and asleep.

**Fallback for Markdown in Telegram.** Job titles from real postings often contain underscores in their URLs (e.g., Oracle Cloud's `/sites/CX_1/`). Telegram's Markdown parser breaks on these, silently dropping entire messages. Fixed with a retry: if a message fails with a 400 entity error, resend as plain text. Messages always arrive.

**Hallucination verification before staging.** Sonnet can occasionally invent a metric or credential when tailoring. Added a Haiku verification pass that cross-references every claim in the CV against the source profile. False positives from truncation are handled with a suffix-repair JSON parser. CVs that fail verification go to `NEEDS_REVIEW` rather than staging automatically.

## Under the Hood

**Stack:** Python (50+ tool scripts), SQLite (WAL mode, jobs/scores/cvs/outcomes/pipeline_runs tables), Anthropic API (Haiku 4.5 for scoring/verification, Sonnet 4.6 for CV generation), Telegram Bot API, Supabase (Edge Functions for command queueing, GTD/calendar integration), Google APIs (Gmail OAuth, Sheets), Playwright (JS-rendered job boards), python-docx (DOCX assembly), pikepdf (Inspira offline PDFs), launchd (macOS cron).

Architecture follows the WAT pattern (Workflows, Agents, Tools): markdown SOPs in `workflows/` define each process; Python scripts in `tools/` handle all deterministic execution; Claude Code acts as reasoning agent for CV generation and scoring. The pipeline is orchestrated by `run_pipeline.py`; Phase 2 runs per-job on-demand via `notify_telegram.py::handle_command()`.

Source ROI is tracked per scraper: hit rate, skip rate, tokens burned. Dead scrapers (0 relevant results for 7+ days) surface in the health check alert.

## How to Demo It

1. Open Telegram — show the morning digest with scored jobs, deadline countdowns, and action plans pre-decided.
2. Pick a HOT job, type `approve <id>`. Show the immediate "Generating..." confirmation.
3. 2 minutes later: show the generated CV DOCX — point out the gap acknowledgment, the keyword bolding, the tailored bullets.
4. For a UN job: show the Inspira cheatsheet — 30+ fields pre-answered, saving ~2.5 hours of form hunting.
5. Show the SQLite dashboard: source ROI table (which boards produce HOT jobs, which waste tokens), score distribution histogram.
6. Show `jobmatch status` on Telegram for a real-time funnel summary.

## Limitations & Setup

- Scrapers break when job boards change their HTML. Expect 1–2 needing fixes per month — the source ROI tracker surfaces dead ones quickly.
- CV generation costs ~$0.10–0.20 per CV (Sonnet). Not free, but far cheaper than the time saved.
- Pipeline runs locally on the Mac via launchd. Laptop needs to be awake at 5am (or triggered manually later).
- Single-user system. The scoring rubric and gap acknowledgment are tuned to one person's career profile.
- LinkedIn scraper depends on email alert forwarding rather than the API — requires periodic Gmail OAuth refresh.
- Gmail draft staging and apply_inspira.py Playwright automation require the laptop display to be accessible (not headless-only).

## Demo Pitch

> "I built an AI that checks 25 job boards every morning before I wake up, scores each role against my actual background using a custom rubric, and sends me the best matches on Telegram with deadlines and action plans already decided. When I see one I like, I type 'approve' and it writes a tailored CV, runs a hallucination check, and for UN jobs generates a pre-filled cheatsheet that turns a 3-hour Inspira form into 20 minutes. What used to take 3 hours a day now takes 5 minutes."

## Changelog

### 2026-04-26
- Full rewrite of portfolio doc to reflect ~1 month of additions
- Added: two-stage Haiku/Sonnet scoring, bridge multiplier, gap acknowledgment in CV generation
- Added: Inspira PDF automation + cheatsheet generation (UN-specific)
- Added: calendar scheduling on approve (GTD task + 60-min block)
- Added: hallucination verification with JSON suffix-repair
- Added: Telegram Markdown fallback (plain text retry on 400 entity errors)
- Updated: 25+ sources (was 15+), effort (~1 month, was ~3 weeks), status (in-progress, was needs-polish)
- Updated: tags and stack to reflect Anthropic API direct + pikepdf + Playwright

### 2026-04-16
- Initial portfolio doc
