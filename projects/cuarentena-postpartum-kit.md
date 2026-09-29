---
project: Cuarentena Kit. A Spanish Digital Product Business, Built as a Couple
slug: cuarentena-postpartum-kit
date_built: 2026-05
last_updated: 2026-05-27
status: in-progress
tags: [digital-products, business-design, spanish, market-research, content]
stack: [Claude Code, Python, Pillow, Markdown, Hotmart]
effort: ~1 week of planning sessions (launch pending)
hero: ../assets/cuarentena-postpartum-kit/hero.svg
repo: private
demo_video: null
---

# Cuarentena Kit

> A 40-day Spanish-language kit for first-time Latina mothers going through the cuarentena, the traditional postpartum rest period. My wife is the founder and the voice; I built the research, the offer and the tools behind it.

![hero](../assets/cuarentena-postpartum-kit/hero.svg)

## The Problem

My wife went through her own cuarentena about a year before this started. What she found in stores was English-language postpartum planners written in a clinical tone, and Spanish printables from Spain that do not reflect Latin American cuarentena customs. Nothing combined the tradition (rest, diet, family care) with modern postpartum mental-health tools.

We wanted to build a small business around that gap together. She has the story and the lived experience. I have the systems. We had a budget of zero dollars a month to start.

## The Solution

A planning repository in Spanish that works as the business's shared brain. It holds:

1. **A niche decision made on evidence.** Ten niches were scored on five criteria (pain, buying power, reachability, market growth, gap in supply). Cuarentena postpartum scored 42 of 50, tied for first. The other tied niche was dropped because neither of us has lived experience of it.
2. **An argued dashboard.** Twelve strategic decisions, each with its reasoning and a feedback box for each of us. It covers the price ladder ($7 / $27 / $97), the guarantee, the channels, the free first five kits and the $0 starting budget.
3. **A voice system.** A tone guide, voice samples, a calibration quiz she answers to set her own register, and a protocol for turning her voice notes into copy. The quiz was rewritten once to strip AI-sounding phrasing.
4. **Launch assets.** A competitive analysis, a community directory, the full 40-day journal draft, a welcome email sequence, a visual identity, and Pinterest SEO research in Spanish.
5. **Production tools.** Five Python scripts: Etsy keyword research, a Spanish listing writer, a mockup generator that places a printable on a lifestyle photo, a PDF-to-listing-images converter, and a bundle packager that builds the branded ZIP a buyer downloads.

## Result

- **One niche, chosen by a scored comparison of 10 options.**
- **A full launch kit written before the first sale**: 14 launch documents and the 40-day journal.
- **A channel decision that avoided a costly legal trap.** The research found that Etsy payments do not operate in Ecuador. Opening Etsy would have meant a US limited liability company (LLC) at about $500 a year, and reusing an old dormant LLC would have carried IRS filing duties with penalties of $25,000 per missed year. We moved to Hotmart, which pays Ecuadorian bank accounts in dollars and already has the Latin American audience.
- **A clear rule for returning to Etsy**: only after Hotmart passes $300 a month for two months in a row.

## Key Decisions

**She is the public founder.** In maternal mental health, an anonymous brand looks suspicious. Mothers buy from mothers they can see. The best-selling postpartum brands in English are all led by visible founders.

**"Cuarentena" over "postpartum".** Generic postpartum planners have thousands of competitors. Products built around the Latin American 40-day tradition had almost no supply on Etsy when we checked. Her Venezuelan and Ecuadorian background gives her two cuarentena traditions to write from.

**Three prices so the middle one is the obvious choice.** $27 sits above most single printables and below the $30 threshold. The $7 and $97 tiers exist mainly so the $27 kit reads as the sensible pick.

**The dashboard argues every decision.** It is a business we both own. Each decision has its reasoning written out and a place for her to push back, so she can disagree with the logic and keep the parts she agrees with.

**Voice before volume.** No content gets produced at scale until her tone is calibrated from her own voice notes. A correct sentence in the wrong voice would sound fake in this niche.

## Under the Hood

**Stack:** Markdown SOPs (market research, shop launch, product design, listing creation, offer, lead-magnet funnel, scale, continuity), Python tools (Pillow for mockups, PDF rendering for listing images, ZIP packaging), Hotmart as the sales channel.

The offer structure borrows from Alex Hormozi's $100M Offers, Leads and Money Models, which I condensed into reference files the agent reads before drafting.

## How to Demo It

1. Open the dashboard and read the one-sentence idea, then decision 1 (the niche) with its scored table.
2. Open the Hotmart pivot document and walk through the three questions that killed the Etsy plan.
3. Run the mockup generator on one journal page and show the listing image it produces.
4. Run the bundle packager and open the ZIP with its auto-generated welcome PDF.

## Limitations & Setup

- Not launched yet. The kit is drafted and the plan is ready; content is waiting on her voice notes.
- The Etsy tools were built before the Hotmart pivot. They still produce the images and bundles, but the listing writer targets Etsy's format.
- Market numbers in the dashboard are planning estimates, to be replaced with real sales data after launch.

## Demo Pitch

> "My wife and I designed a digital product business in a week, with every decision argued in writing so we could both push back. The research also caught a legal trap before we spent a dollar: the sales platform we'd planned on doesn't pay out in Ecuador, and the workaround carried $25,000-a-year penalty risk. If you're starting something small, this is how I'd set up the thinking before the spending."
