---
project: Consultant Launch System — Personal Brand & LinkedIn Thought Leadership
slug: consultant-launch-system
date_built: 2026-04
last_updated: 2026-04-16
status: in-progress
tags: [personal-brand, linkedin, thought-leadership, content, writing, ai-orchestration, research]
stack: [Claude Code, Python, Claude Sonnet 4, GitHub Pages, HTML/JS]
effort: ~3 weeks (ongoing)
hero: ../assets/consultant-launch-system/hero.svg
repo: /Users/jdlovesyou/Agentic Workflows/Consultancy:PersonalBrand:LinkedinThoughtLeadership
demo_video: null
---

# Consultant Launch System — Personal Brand & LinkedIn Thought Leadership

> A complete launch system for a consultant's personal brand: market research, positioning, a style-guide-as-code, 12 pre-written LinkedIn posts, an AI drafting tool that writes in my voice, and a live hub of 10 free interactive tools grounded in my real field work. Built to go from zero to income in 60 days.

![hero](../assets/consultant-launch-system/hero.svg)

## The Problem
Most "personal branding" advice is noise — post 3x a week, use hooks, be consistent. None of that works if you haven't figured out **who you are, who you're for, and what you've actually done that nobody else has done.**

I'm a conservation governance consultant. I've spent years in the Ecuadorian Amazon building multi-stakeholder platforms that nobody posts about on LinkedIn. I didn't need a content calendar. I needed a *launch system* — market research, positioning, proof points, voice, distribution, and pipeline — all wired together, so when I started posting, I was posting *from* a position of credibility, not *for* attention.

## The Solution
A folder in Claude Code that functions as the control room for my consulting launch:

1. **Market research** — 5 deep research reports on NGO/DFI pain points, competitive whitespace, and the LinkedIn creator ecosystem. Output: a single defensible positioning — the "Practitioner-Scholar" — sitting at the intersection of Amazon governance, conservation finance, and AI workflows.
2. **Brand guide as executable rules** — `workflows/brand_guide.md` isn't a style doc gathering dust. It's the prompt scaffold that every AI drafting tool calls. Banned words ("leveraging synergies", "holistic", "capacity building"), required specificity (always anchor to real numbers / Amazon / Ecuador / orgs), voice parameters, and proof points.
3. **Content workflows** — How to study a creator I admire (e.g., Nate B. Jones), adapt their angle through my lens, draft a post, and publish it. All as markdown SOPs.
4. **AI drafting tools** — Two Python scripts: one ingests content inspiration and outputs 2-3 adapted post angles; the other takes a raw idea + content pillar + format and produces a full LinkedIn draft in my voice, character limits enforced. Model: Claude Sonnet 4.
5. **A content pipeline of 12 posts + calendar + visuals**, Tue-Thu 8-11am slots, all written before I post a single one.
6. **A free resource hub** — 10 interactive HTML tools ([89jdvm.github.io/resources](https://89jdvm.github.io/resources/)): Governance Canvas, Cooperation Table Blueprint, Power Mapping, DFI Decoder, Funding Readiness Score, Capital Stack Templates, and more. Each one is grounded in work I've actually done. No email gates. The implicit CTA is: *if you need someone who has done this, I'm that person.*
7. **4 investor playbooks** published separately (Territorial Trust Infrastructure, Local Cooperation Tables, Regeneration Opportunity, Bankable Climate Projects) that anchor every outreach email and post.

## Screenshots

![Brand guide rules](../assets/consultant-launch-system/brand-guide.png)
*Voice encoded as rules, not prose — so every AI tool drafting a post enforces specificity and bans AI slop automatically.*

![Resource hub](../assets/consultant-launch-system/resource-hub.png)
*10 free interactive tools on GitHub Pages. Fillable forms, live scoring, localStorage auto-save, mobile-first.*

## Result
- **One defensible positioning** ("Practitioner-Scholar") validated against market research instead of invented.
- **12 posts ready to ship** with calendar, visuals, and engagement SOP (15 min pre-post ritual, 2-hour post-publish engagement window, weekly review).
- **10 live interactive tools** on GitHub Pages as a credibility asset — and a lead magnet that doesn't feel like one.
- **2 AI drafting tools** that write in my voice because the voice is encoded as rules the model must follow.
- **4 published investor playbooks** as anchors for outreach.
- Critically: the system **enforces correct launch order.** The Mesas de Cooperación case study must exist before LinkedIn posting starts — so my content is grounded in a fresh, visible proof point, not generic commentary.

## Key Decisions
- **Voice as rules, not examples.** I didn't try to train a model on my old posts. I wrote down the rules (direct, specific, bridges field and finance, bans AI slop vocabulary) and made every tool call those rules. Easier to audit, easier to evolve.
- **Free tools over lead magnets.** No email gates. The hub is itself the CTA — someone who uses those tools already knows what I do.
- **Publishing order matters more than frequency.** Content pipeline only activates after the case study anchor exists.
- **Positioning from research, not intuition.** 5 deep research reports → one positioning. I ran the research on my own niche the same way I'd run it for a client.
- **Ban specific words in the system prompt.** "Synergies", "holistic", "let me know your thoughts" — explicitly forbidden at the model level. Removes the AI slop signature.

## Under the Hood
**Stack:** Claude Code, Python (Claude API via Anthropic SDK, dotenv), Claude Sonnet 4, GitHub Pages (static HTML/JS with localStorage for tool state), Jinja2 for any templated email work.

Follows the WAT framework (Workflows / Agents / Tools): markdown SOPs in `workflows/`, Claude as the decision-maker, Python scripts in `tools/` for deterministic execution (API calls, formatting, character counting). The brand guide is the shared dependency — every tool reads it, every workflow references it.

## How to Demo It
1. Open `workflows/brand_guide.md` — show voice rules and banned vocabulary.
2. Run `python tools/draft_post.py --pillar 2 --idea "why AI won't fix Amazon governance"`. Show the draft that comes out: specific, grounded, on-brand.
3. Open [89jdvm.github.io/resources](https://89jdvm.github.io/resources/) — walk through the Governance Canvas or Cooperation Table Blueprint. Point out: no email gate, works on a phone.
4. Open one of the 4 investor playbooks. Close the demo with: "This is the proof. The posts point back to this."

## Limitations & Setup
- `.env` requires `ANTHROPIC_API_KEY`.
- AI drafts still need human review — the system enforces structure and voice, not truth.
- The free resource hub lives in a separate repo (89jdvm/resources); this folder orchestrates content, the hub hosts the deliverables.
- Not yet actively publishing — activates once the Mesas case study is shippable.

## Demo Pitch
> "This is what it looks like when you treat your own launch like a consulting engagement. Market research, positioning, voice rules, 10 free tools that prove what I do, and an AI that drafts posts in my actual voice — because the voice is encoded as rules the model has to follow, not examples it tries to imitate."
