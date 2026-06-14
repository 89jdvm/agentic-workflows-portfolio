---
project: Instrument Kickstarter. Project Ops System
slug: instrument-kickstarter-ops
date_built: 2026-04
last_updated: 2026-04-16
status: in-progress
tags: [project-management, kickstarter, client-work, dashboard, automation, email, ai-orchestration]
stack: [Claude Code, Python, Gmail API, Google Sheets, Google Drive, Jinja2, HTML dashboards]
effort: ~2 weeks (ongoing through launch)
hero: ../assets/instrument-kickstarter-ops/hero.svg
repo: /Users/jdlovesyou/Agentic Workflows/Instrument Project
demo_video: null
---

# Instrument Kickstarter. Project Ops System

> A complete operational system for launching a handmade-instrument Kickstarter in 31 weeks. Milestones, gates, budget, email list, competitor research, and a live HTML dashboard, all driven by one living context file that gets updated after every weekly meeting.

![hero](../assets/instrument-kickstarter-ops/hero.svg)

## The Problem
Launching a Kickstarter product is not a marketing problem. It's an operations problem. 31 weeks to go-live. Six parallel sub-projects (spec sheets, luthier contract, pricing, video production, audience building, campaign). Four stakeholders with different approval authorities. A single luthier as the only production partner. Pre-campaign budget of $4,500 in milestone payments plus operational costs. Most founders run this on a Notion board and hope. I wanted a system that would tell me on any given Monday: **where are we, what's blocked, what gate are we approaching, and who needs to decide what this week.**

## The Solution
One folder, one living context file (`instrument_project_context_from_meeting.md`, 1,000+ lines, updated after every weekly meeting), and a toolchain that reads it and produces everything else.

What the system does:

1. **Interactive HTML dashboard** (`render_dashboard.py`): Health score, critical path (6 nodes), per-project progress bars, milestone statuses, **gate readiness** (G0–G6 countdowns with condition checklists), risk register ranked 1–5, budget tracking, week-by-week task lists. Opens in your browser. One command.
2. **Milestone tracker** (`milestone_tracker.py`): Computes current week from `PROJECT_START_DATE=2026-04-01`. Auto-classifies milestones as completed / on-track / due-this-week / at-risk / overdue / blocked. Plain-text terminal report for fast standups.
3. **Task tracker** (`task_tracker.py`): Pushes all 48+ milestones into a shared Google Sheet with two views: full milestone list (dropdown status column) and a grouped weekly view. Replaces paid project-management tools, editable by the whole team in real time.
4. **Email campaign system** (`email_manager.py` + templates): Zero-cost email marketing built on Gmail API + Google Sheets + Jinja2. Subscriber database (10 columns: email, name, source, subscription state, unsubscribe token, campaigns received, etc.), Spanish-language branded campaigns, mandatory unsubscribe links, web-form signup via a cPanel PHP endpoint. Replaces Mailchimp/Klaviyo ($54–180/mo).
5. **Kickstarter competitor research** (`ks_research.py`): Scrapes Kickstarter campaigns via their JSON endpoint (HTML fallback). Extracts goal, pledged, backers, tier structure, Early Bird discount, video presence, duration, outcome. Analyzed 10 handmade-instrument campaigns to validate the $249 cajón and $499 guitar price points against market comps.
6. **Google Drive management** (`gdrive_manager.py`): 8-folder hierarchy (Spec Sheets, Meetings, Contracts, Financial Model, Marketing, Kickstarter, Brand Assets, Operations) with auto-refreshing OAuth. Spec sheets, research reports, and subscriber lists auto-upload to the correct folder.
7. **Gate logic**: 6 go/no-go gates (G0 Foundation → G6 Launch). Each gate has locked conditions. You can't proceed to video production (G3) without strategy approval (G2). Failures at gates trigger team decisions, not auto-escalation.
8. **Workflows** as markdown SOPs for the non-obvious operations (KS account setup: Ecuador isn't eligible, so the campaign launches under the Ecuadorian luthier's partner as an individual; prototype measurement checklists; competitor research protocol; email campaign QA).

## Screenshots

<!-- broken image dropped at build time (PNG never created): ![Interactive dashboard](../assets/instrument-kickstarter-ops/dashboard.png) -->*The dashboard: health score, critical path, gate readiness, risk register, budget. Opens in the browser from a single `render_dashboard.py` call.*

<!-- broken image dropped at build time (PNG never created): ![Competitor research report](../assets/instrument-kickstarter-ops/ks-research.png) -->*10 handmade-instrument Kickstarter campaigns analyzed: pledged amounts, tier structures, Early Bird patterns, success/failure mix. Used to lock pricing and tier design.*

## Result
- **One context file → every artifact.** Update the meeting notes, rerun the tools, the dashboard, Google Sheet, and email list all reflect the new state.
- **6 gates + 48 milestones + 10 top risks** tracked and visualized, with ownership explicitly assigned.
- **Pricing validated against 10 real Kickstarter campaigns** before committing ($249 cajón, $499 guitar, Early Bird 10–20% discount).
- **Budget tracked in two tracks**: milestone payments ($4,500 pre-campaign across 7 payouts) and operational line items ($668–1,868 for video tools, email platform, legal, ads, samples).
- **Zero-cost email stack** instead of a $54–180/mo SaaS bill, fully owned.
- **Post-campaign decision sequence documented** (KS fees → production payment → fulfillment reserves → founder ROI → Collection 2 seed capital), so the win isn't accidental.

## Key Decisions
- **Living context file, not a ticket tracker.** The 1,000-line markdown doc is the source of truth, updated after every meeting. Every tool reads it. This is the opposite of Jira. Meeting notes *are* the plan.
- **Gates over deadlines.** A milestone can slip; a gate cannot be crossed without its conditions. G0 requires Ivan-contract-signed AND pricing-approved. No amount of optimism moves that date forward.
- **Profit-first pricing.** Prices derived backwards from a 60% margin target, not forward from cost plus markup. $62 cajón cost → $249 retail, validated against 10 comparable campaigns.
- **Single-point-of-failure risk has its own mitigation.** The luthier (Ivan) is the only production partner. Before signing his contract, the plan *requires* two alternative luthier quotes on file. R6 in the risk register.
- **Ecuador can't host a Kickstarter, so the system planned for it.** The campaign launches under an individual partner, not the Ecuadorian entity. Documented in `ks_account_setup.md`, not discovered in week 15.

## Under the Hood
**Stack:** Claude Code, Python 3.13, Gmail API + Google Sheets API + Google Drive API (OAuth with auto-refresh), Jinja2 for email templates, raw HTML/CSS/JS for the dashboard, Kickstarter JSON endpoint + BeautifulSoup HTML fallback for research.

WAT framework (Workflows / Agents / Tools). Folder IDs cached in `.env` so every script references the same Drive structure. The context parser (`tools/common.py`) is the shared dependency, all downstream tools call it.

## How to Demo It
1. Open `instrument_project_context_from_meeting.md`, one file, the whole project state.
2. Run `python tools/render_dashboard.py` → browser opens. Walk through the gate countdowns, risk register, budget.
3. Run `python tools/milestone_tracker.py` → terminal shows "Week 3 of 31, X overdue, Y due this week."
4. Open the Google Sheet task tracker: show the milestone list and weekly view; explain that the whole team edits it live.
5. Show the KS competitor JSON in `.tmp/ks_research/campaigns.json` and how it informed the pricing decision.

## Limitations & Setup
- Requires Google OAuth credentials for Gmail, Sheets, and Drive APIs.
- Kickstarter doesn't expose a real API. The scraper falls back from JSON to HTML when they change the DOM. Rate limiting is manual.
- The dashboard is client-facing-ready but currently rendered locally; a public-facing version would strip budget and risk details.
- Email system doesn't yet handle replies, designed for one-way campaigns + web signup.

## Demo Pitch
> "This is what it looks like when you treat a Kickstarter launch like running a small company. One context file holds the truth: meetings, decisions, risks, budget. One command renders a dashboard with gate readiness and critical path. One Google Sheet keeps the whole team aligned. The founder doesn't have to remember; the system does."
