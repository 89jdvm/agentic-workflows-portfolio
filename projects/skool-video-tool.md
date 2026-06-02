---
project: Skool Video Tool. AI-Ready Transcripts
slug: skool-video-tool
date_built: 2026-03
last_updated: 2026-04-16
status: demo-ready
tags: [transcription, ai-ready, productivity, second-brain, local-first]
stack: [Node.js, Express, whisper-cpp, ffmpeg, MediaRecorder, Web Audio API]
effort: ~1 weekend
hero: ../assets/skool-video-tool/hero.svg
repo: /Users/jdlovesyou/Agentic Workflows/Skool Video Tool
demo_video: null
---

# Skool Video Tool — AI-Ready Transcripts

> A local-first browser tool that captures audio from any video playing in a tab (Skool, YouTube, Loom, internal training) and turns it into structured markdown that an AI can actually understand. No API keys. Nothing leaves your machine. Record, transcribe, and hand the output straight to Claude.

![hero](../assets/skool-video-tool/hero.svg)

## The Problem
I consume a lot of training videos — Skool courses, Loom walkthroughs, recorded webinars. The insight density is high, but videos are a terrible format for AI to work with. Pasting "here's a YouTube link, summarize it" is unreliable. Paid transcription services cost money and ship my audio to someone else's server. Raw transcript dumps are wall-of-text noise that tokenize badly.

I wanted: **record the video locally, get back a markdown file that Claude can ingest cleanly as structured context, and never send the audio anywhere.**

## The Solution
A one-page web app that runs on your laptop. Open it, click record, share the browser tab the video is playing in (with tab audio), hit play on the video, and when it's done you get a markdown file structured for AI consumption — all local, no API keys, no cloud.

What the output file looks like:

- **YAML frontmatter** with title, source, duration, date, and type — so downstream tools (Claude, NotebookLM, Obsidian) can parse metadata without reading the whole doc.
- **Sectioned transcript** automatically split on transition phrases ("alright, let's move on", "in summary", "first… second…") with auto-generated section titles. If transition detection fails, fallback splits every ~500 words so sections stay consistent.
- **Paragraph chunking** — sentences grouped into ~4-sentence paragraphs. Cleans up tokenization for the LLM.
- **Footer line** — "Auto-generated transcript. Optimized for AI processing." So any AI reading it immediately knows what kind of input it is.

All transcription happens locally via **whisper-cpp** running on CPU against the `base.en` quantized model. Nothing leaves the machine.

## Screenshots

<!-- broken image dropped at build time (PNG never created): ![Recording UI](../assets/skool-video-tool/recording.png) -->*Red record button, live waveform, timer, "Also share tab audio" reminder in red when silent. Browser-based, no install step beyond `npm start`.*

<!-- broken image dropped at build time (PNG never created): ![Structured markdown output](../assets/skool-video-tool/markdown.png) -->*YAML frontmatter + auto-sectioned transcript + paragraph chunking. Ready to hand to Claude as context.*

## Result
- **Local-first transcription** with zero API cost and zero data leakage.
- **AI-ready markdown output** (not a raw wall-of-text) that Claude, NotebookLM, and Obsidian can parse cleanly.
- **Past recordings browser** — every session is saved under `/output/<title>--<timestamp>/` with both the markdown and the raw transcript; old recordings are listable, viewable, downloadable, and deletable from the UI.
- **Works on any tabbed video source** — Skool, YouTube, Loom, recorded Zoom in the browser, internal training platforms.
- **About 15 minutes from "I just watched a video" to "Claude is answering questions about it."**

## Key Decisions
- **Local whisper-cpp, not the OpenAI API.** Zero marginal cost, no API key, audio never leaves the laptop. Acceptable CPU cost for personal use.
- **Tab audio capture via `getDisplayMedia`.** The browser requires you request video to get tab audio — so the app asks for `{ video: true, audio: true }`, then discards the video tracks. Clever workaround for a real browser API constraint.
- **Structure the markdown for AI, not for humans.** Transition-phrase regex detection produces semantic sections; paragraph chunking reduces tokenization noise; the footer explicitly labels the file as AI-optimized. Humans can read it — but the file is *for the model*.
- **Fallback splitting when transitions fail.** Not every video has clean "alright, let's move on" cues. Word-count fallback (~500 words/section) guarantees consistent structure.
- **Timestamp-based folder naming.** `title--2026-04-13T22-43-11-748Z` prevents collision when multiple videos are transcribed in parallel.
- **Self-describing output.** Each markdown file embeds its own metadata (duration, capture date, transcription method), so the file is portable between machines and contexts.
- **Vanilla JS on the frontend.** No React, no bundler, no framework. The whole UI is one HTML file + one JS file.

## Under the Hood
**Stack:** Node.js + Express (server), ffmpeg (audio conversion: webm → wav, 16kHz mono for Whisper), whisper-cpp (local CPU inference, `base.en` quantized model at `/usr/local/share/whisper-cpp/models/ggml-base.en.bin`), MediaRecorder API (browser capture), Web Audio API (live waveform visualization), vanilla JavaScript UI.

**Dependencies:** `express`, `uuid`. That's it. Zero ML libraries — whisper-cpp is a shell binary, and the Node server just orchestrates the pipeline (ffmpeg → whisper-cli → markdown post-processor).

## How to Demo It
1. `npm start` — Express server on localhost.
2. Open the web UI. Click the red record button.
3. In the Chrome tab picker, pick the tab playing the video and check "Also share tab audio."
4. Play the video. Show the live waveform and timer as audio streams in.
5. Stop recording. Watch ffmpeg → whisper-cli → markdown post-processor run in the Node console.
6. Open the output markdown file. Show the YAML frontmatter, sectioned transcript, and the AI-optimized footer line.
7. Drop the markdown into Claude and ask a question about the video. The answer is grounded and specific — because the input was structured, not a wall of text.

## Limitations & Setup
- Requires **whisper-cpp** installed locally at `/usr/local/bin/whisper-cli` with the `ggml-base.en.bin` model at `/usr/local/share/whisper-cpp/models/`.
- Requires **ffmpeg** on PATH.
- CPU-only transcription — a 30-minute video takes a few minutes on an M1/M2 Mac. Not real-time.
- Tab audio capture requires Chromium-based browsers (Chrome, Edge, Brave). Safari's `getDisplayMedia` does not support tab audio.
- `base.en` is English-only. For other languages, swap in the multilingual `base` model.
- "Also share tab audio" checkbox must be checked in the Chrome picker, or you'll record silence.

## Demo Pitch
> "It's a browser tool that records any video playing in a tab, transcribes it locally with Whisper — nothing leaves your machine — and gives you back a markdown file that's structured for AI to read, not just humans. So instead of asking ChatGPT to summarize a YouTube link and hoping, you drop a clean, sectioned markdown file into Claude and get grounded answers about what was actually in the video."
