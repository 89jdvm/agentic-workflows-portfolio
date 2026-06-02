---
project: Mesas de Cooperación. Conservación Internacional
slug: mesas-cooperacion-ci
date_built: 2026-03
last_updated: 2026-04-16
status: in-progress
tags: [client-work, consultancy, ai-orchestration, automation, writing, dashboard]
stack: [Claude Code, Python, python-docx, HTML dashboards]
effort: ~1 month of ongoing co-pilot work
hero: ../assets/mesas-cooperacion-ci/hero.svg
repo: /Users/jdlovesyou/Agentic Workflows/Entregable 5
demo_video: null
---

# Mesas de Cooperación — Conservación Internacional

> My consulting work for Conservation International Foundation Ecuador, reinvented: instead of chatting with AI, I now work *inside* the project files with Claude Code — producing better deliverables, dashboards for the Cooperation Tables in Sucumbíos and Orellana, and email automation for the two-year roadmap.

![hero](../assets/mesas-cooperacion-ci/hero.svg)

## The Problem
I'm the consultant behind the technical accompaniment to establish two **Mesas de Cooperantes** (Cooperation Tables) for conservation and sustainable development in the Amazonian provinces of Sucumbíos and Orellana. Contract runs October 2025 – April 2026. The work produces long, dense deliverables in Spanish (.docx reports, roadmaps, governance models, constitutional acts), plus the ongoing coordination of many stakeholders: provincial governments, NGOs, technical secretariats, and management groups.

Before Claude Code, I was using AI through chat interfaces — great for brainstorming, bad for real project work. Context was always lost. Every conversation started from zero. Feedback from the client had to be manually translated into edits. Deliverables lived in one place, my AI assistant lived in another, and I was the glue.

## The Solution
I moved the consultancy itself into Claude Code. The project folder holds every contract, every prior deliverable, every feedback document, every roadmap. Claude reads them directly — no re-explaining context, no copy-pasting.

What this unlocks:

1. **Deliverables get written with full context.** The main report (Entregable 5 — the Final Consolidated Report) is edited inside its own `.docx` file, preserving formatting, comments, and the table-of-contents structure that Word demands.
2. **Client feedback becomes a plan.** When the client sent back 14 review comments, Claude Code parsed them from `word/comments.xml`, grouped them into 5 phases, and worked through each one — with me approving every change.
3. **Roadmaps become dashboards.** The two-year roadmaps for each province (Hojas de Ruta 2026–2028) are being turned into interactive HTML interfaces where stakeholders can see their assigned actions, mark them done, and stay aligned.
4. **Follow-ups become automated.** Emails to the Grupo Gestor, reminders to the Secretaría Técnica, status requests to the Procurador Síndico — all templated and driven by the same structured data behind the dashboards.

The bigger shift is methodological: **my consultancy is now a repository**, not a series of chat threads.

## Screenshots

<!-- broken image dropped at build time (PNG never created): ![Dashboard for Hoja de Ruta](../assets/mesas-cooperacion-ci/dashboard.png) -->*Interactive dashboard for the 2026–2028 roadmap of one of the provinces — each action has an owner, a due date, and a status, and members of the Mesa can log in to track their part.*

<!-- broken image dropped at build time (PNG never created): ![Feedback plan](../assets/mesas-cooperacion-ci/feedback-plan.png) -->*Client feedback parsed out of `word/comments.xml` and turned into a 14-action, 5-phase implementation plan.*

## Result
- **Entregable 5** (Final Consolidated Report, 7 sections + annexes) produced inside Claude Code with full formatting preserved.
- **Client feedback loop** tightened: 14 review comments processed structurally instead of hunted for in a Word doc.
- **Dashboards** for the Cooperation Tables' two-year roadmaps — in progress, replacing the static spreadsheet view.
- **Email automation** scaffolded for stakeholder communications (in progress).
- **Methodological shift**: from chat-based AI assistance to project-based, context-rich work. This is reusable across every future consultancy engagement I take on.

## Key Decisions
- **Structured docx editing over export/reimport.** Instead of exporting to markdown, editing, and reimporting (which destroys formatting), edits happen directly on individual runs within paragraphs using `python-docx` + `lxml`. Tables of contents, comments, embedded images, and track changes all survive.
- **Comments parsed as first-class input.** Word comments live in `word/comments.xml` and are invisible to `python-docx`. I wrote a small parser that turns them into an actionable list — that became the bridge between client feedback and implementation.
- **Dashboards as the "living" deliverable.** A .docx is a snapshot; a dashboard keeps working after the contract ends. The dashboards are the handoff that gives the Mesas something to use, not just read.
- **Claude Code as a co-pilot, not an author.** Every major edit is reviewed before it touches the deliverable. The client gets consulting work, not AI output.

## Under the Hood
**Stack:** Claude Code, Python 3.13 (`python-docx`, `lxml`, `zipfile`), HTML/JS for dashboards, macOS `textutil` for quick text extraction.

The project folder functions like a small knowledge base: contract documents, previous deliverables (E2–E4), feedback files, and working drafts all sit side-by-side. Claude Code is instructed (via `CLAUDE.md`) on which files are targets for edits, which are reference-only, and the technical gotchas of editing .docx XML without breaking Word's rendering.

## How to Demo It
1. Open the project folder in Claude Code — show `CLAUDE.md`, the contract, the prior deliverables, and the main report side-by-side.
2. Show a real client comment in `Entregable 5.docx` and the feedback-implementation plan that came out of it.
3. Open the roadmap dashboard for one of the provinces — click through a stakeholder view.
4. Explain the shift: "This used to be five ChatGPT tabs and a lot of copy-paste. Now it's one project, one context, one co-pilot."

## Limitations & Setup
- Everything is in **Spanish** — deliberate, the client is Ecuadorian.
- `.docx` editing is fragile: always save-close-reopen between major edit phases, never modify paragraphs containing `<w:drawing>` or `<w:pict>`.
- After heading changes, the Table of Contents must be manually refreshed in Word (F9 on Windows, manual right-click on Mac).
- Dashboards and email automation are in progress — not yet end-to-end with the live Mesa members.
- **Client data is confidential.** The project folder itself stays private; only this portfolio doc is public.

## Demo Pitch
> "I'm a consultant working for Conservation International in the Ecuadorian Amazon. Claude Code replaced my chat-based AI workflow with something that lives inside the project itself — every contract, every deliverable, every comment from the client. It doesn't just help me write; it helps me run the whole engagement. The dashboards and email automation are how I'm turning a report into something the stakeholders can actually *use*."
