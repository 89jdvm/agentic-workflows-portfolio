---
project: Forest Knight
slug: forest-knight
date_built: 2026-04
last_updated: 2026-04-16
status: demo-ready
tags: [creative, game-dev, father-son, vibe-coding]
stack: [Claude Code, HTML5 Canvas, JavaScript]
effort: ~20 min build + days of play-and-edit
hero: ../assets/forest-knight/hero.svg
repo: /Users/jdlovesyou/Agentic Workflows/video juego 1
demo_video: null
---

# Forest Knight

> A side-scrolling mobile game I built with my 4-year-old son — he designed the bosses, I wrote the prompts, and we edited the game together every time we played it.

![hero](../assets/forest-knight/hero.svg)

## The Problem
My son is four. He loves playing video games on tablets. I wanted him to understand something important: **the people who play games are cool, but the people who build them are cooler.** The only way to show that was to build one *with* him — not for him — and let his imagination drive it.

## The Solution
We opened Claude Code together and I typed what he asked for. A knight. A forest. Zombies. A dragon. Then he invented the bosses himself: a **poop knight**, a **bee queen**, an **alien named Bratt**. The first playable version was ready in about 20 minutes. After that, every time we played, something would spark an idea — *"the dragon should shoot fire"*, *"I want a lightning ball"* — and we'd jump back into Claude Code, change it, and keep playing.

The game runs in the browser, works on a phone with touch controls, and is entirely in Spanish so he can read the level names as he plays.

## Screenshots

![Level 1 — Pradera Encantada](../assets/forest-knight/level-1.png)
*Level 1: Pradera Encantada. First boss is the Poop Knight.*

![Mobile touch controls](../assets/forest-knight/mobile.png)
*Joystick on the left, attack button on the right — designed for a kid's thumbs on a phone.*

## Result
- A playable side-scrolling game with multiple levels (Pradera Encantada, Bosque Misterioso, Valle del Dragón…) and original bosses invented by a 4-year-old.
- More importantly: my son now knows that the games on his tablet didn't just *appear*. Someone built them. And he can build them too.

## Key Decisions
- **He drives, I type.** When he asked for a boss, I didn't sanitize it. If he said "poop knight", that's what went into the code. The game belongs to him.
- **Short build, long play-edit loop.** The magic wasn't the first 20 minutes — it was the days after, where a play session would end with "dad, let's add…" and we'd change the game together.
- **Spanish by default.** All level names and UI in Spanish so it matches the rest of his world.
- **Mobile-first.** Touch controls over keyboard because the tablet *is* the gaming device at his age.

## Under the Hood
**Stack:** HTML5 Canvas, vanilla JavaScript (no framework), Claude Code as the co-builder

Single-page game, no build step. Entities, levels, particles, sprites, HUD, and input each split into their own JS files so Claude Code can edit one piece without touching the rest. Runs from any static file server.

## How to Demo It
1. Open `index.html` in Chrome (or serve the folder).
2. On mobile: joystick to move, attack button to hit.
3. Walk into Pradera Encantada, beat the zombies, then the Poop Knight.
4. Tell the story: "The 4-year-old designed that boss. And the next one. And the next."

## Limitations & Setup
- No persistence (score/progress resets each run) — intentional, it's a kid's arcade game.
- Audio needs a user interaction before it plays (browser autoplay policy).
- Built for mobile screens first; desktop works but isn't the focus.

## Demo Pitch
> "This is a game I built with my four-year-old son in about 20 minutes. He designed the bosses. Now every time we play, we edit the game together. That's what AI tools like Claude Code unlock — not just code, but creative collaboration with a kid who can barely read."
