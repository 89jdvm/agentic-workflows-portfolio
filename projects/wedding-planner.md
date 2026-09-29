---
project: Wedding Planner. Public Site, Planning Backend and Ceremony Script
slug: wedding-planner
date_built: 2026-04
last_updated: 2026-06-19
status: demo-ready
tags: [wedding, full-stack, astro, supabase, ai-orchestration]
stack: [Claude Code, Astro, Supabase (Postgres, Edge Functions, pg_cron), GitHub Pages, GitHub Actions]
effort: ~4 sessions across 2 days, plus a ceremony script in June
hero: ../assets/wedding-planner/hero.svg
repo: https://github.com/89jdvm/wedding-site
demo_video: null
---

# Wedding Planner

> Our wedding, run from one database: guests RSVP and sign the guestbook on a free static site, we track budget and vendors in planning tables, and the ceremony script lives on a web page.

![hero](../assets/wedding-planner/hero.svg)

## The Problem

Wedding planning spreads across a spreadsheet for the budget, WhatsApp threads with vendors, a paper guest list, a gift registry on another site, and a Word file for the ceremony. RSVPs come in through five channels and someone has to type them up. Nobody has one view of what is paid, what is booked and who is coming.

## The Solution

Three pieces sharing one Supabase database:

1. **The guest site.** An Astro site in Spanish with our story, the day's schedule, the locations, a gallery, the gift list, an RSVP form and a guestbook. It builds and deploys to GitHub Pages on every push.
2. **The planning backend.** A `wedding` schema in Postgres with tables for budget, vendors, the timeline, guests, RSVPs, the guestbook and gift orders. Row-level security keeps it private; guests can only read approved guestbook entries.
3. **The ceremony script.** A single web page with the full ceremony in order, from the prelude and meditation through the vows, the handfasting and the ring exchange to a closing ritual where guests share reflections. Every change is a commit, so each revision can be read and undone.

## Result

- **RSVPs and guestbook messages land straight in the database.** No retyping.
- **One place for the planning numbers**: budget lines, vendor status and the task timeline, each with its own status field.
- **Guestbook moderation.** Every message has an approval flag, so we can hide one without deleting it.
- **A ceremony script with a full edit history.** Seven revisions in about an hour and a quarter, each one a readable change.

## Key Decisions

**One form endpoint that guests can hit safely.** The RSVP and guestbook forms post to a single Supabase Edge Function. It validates every field, checks the origin, and rate-limits by a hash of the sender's IP. A nightly `pg_cron` job clears old rate-limit rows. Guests never see a database key.

**Reuse the backend I already run.** The wedding schema lives in the same Supabase project as my second brain ([Open Brain](open-brain.md)). No new account, no new bill, and the same security rules.

**The guest site is static.** Astro builds plain HTML, and GitHub Pages hosts it for free. Only the two forms need a server, and that is the Edge Function.

**The ceremony is a page.** A web page scrolls on any screen, has large type and cannot be lost in an inbox. Each section is numbered, so moving a moment (the candle, an entrance) is one edit plus a renumber.

**Audit every submission.** A `submit_audit` table logs the status of every form post, so a lost RSVP can be traced.

## Under the Hood

**Stack:** Astro (ten components: hero, our story, the day, locations, gallery, gifts, RSVP form, guestbook, footer and a decorative sprig), Supabase Postgres with row-level security, a Deno Edge Function with validation, CORS and rate-limit modules, `pg_cron`, GitHub Actions deploying to GitHub Pages.

## How to Demo It

1. Open the guest site on a phone and scroll the sections.
2. Submit an RSVP. Show the row appear in the `rsvps` table.
3. Post a guestbook message, flip its `approved` flag to false, and refresh the site to show it gone.
4. Open the ceremony page and scroll from the prelude to the closing ritual.

## Limitations & Setup

- Built for one wedding, in Spanish. Names, places and dates are hard-coded in the components.
- The planning side is database tables. Reading them needs the Supabase dashboard or a query.
- Rate limiting fails open: if its lookup errors, the submission goes through and the error is logged.

## Demo Pitch

> "We ran our wedding from one database: guests RSVP on a free static site, and every answer lands next to our budget and vendor list. It's the same pattern I'd use for any small event or client portal. Keep the public site static and free, and put a single, locked-down endpoint in front of the data."
