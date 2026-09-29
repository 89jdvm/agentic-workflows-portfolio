---
project: Workspace Recovery Kit
slug: workspace-recovery-kit
date_built: 2026-07
last_updated: 2026-07-21
status: demo-ready
tags: [disaster-recovery, devops, documentation, claude-code]
stack: [PowerShell, Git, GitHub CLI, Markdown]
effort: 1 session
hero: ../assets/workspace-recovery-kit/hero.svg
repo: private
demo_video: null
---

# Workspace Recovery Kit

> When my laptop and its drive died, I rebuilt 17 projects from 21 GitHub repos on a borrowed Windows machine in one session, then wrote the checklist and script so the next rebuild takes minutes.

![hero](../assets/workspace-recovery-kit/hero.svg)

## The Problem

On 21 July 2026 my Mac and its hard drive failed. The project code was safe on GitHub. Everything outside git was gone: the Claude Code skills I had built, the record of which secret goes in which project, and the folder layout that ties related repos together.

Recovery took a full session of detective work on a borrowed Windows laptop. On top of that, a plain `git clone` failed on three repos and left their folders empty.

## The Solution

A small repository that holds everything a new machine needs and git does not carry:

1. **A migration checklist written for Claude to follow.** It installs Git and the GitHub CLI with winget, authenticates, sets the git identity, clones everything and restores the customizations. A fresh Claude Code session with no memory can run it step by step.
2. **A one-command restore script** (`clone-all.ps1`). It recreates the whole workspace folder from GitHub, including the three parent folders that group related repos (for example, one project that spans a monitoring system and two regional dashboards).
3. **A secrets checklist by name only.** Every environment variable each project needs, with no values. The values live in a password manager and in each provider's dashboard.
4. **A backup of the user-level Claude Code skills** that live outside any project repo.
5. **A project map.** The 21 repos sorted into 17 real projects, with a line on what each one is.

## Result

- **17 projects restored** on a new operating system.
- **The next rebuild is a checklist plus one script.**
- **The Windows clone failure is fixed for good.** Three repos carried a macOS Finder file named `Icon` followed by a carriage return, a character Windows does not allow in file names. The script detects the failed checkout and checks out everything except that one file.

## Key Decisions

**Write the checklist for the agent.** I work through Claude Code, so the reader of a recovery guide is likely to be a fresh Claude session. The steps are explicit enough for it to run without guessing, and they say where a human has to step in (the GitHub login in a browser).

**Names of secrets, never values.** A list of variable names is safe to keep in git and tells you exactly what to go and collect. Values in git would turn a backup into a leak.

**Fix the root cause in the script.** The `Icon` file problem would bite every future clone on Windows. Handling it once in the restore script means nobody has to remember it.

## Under the Hood

**Stack:** PowerShell, Git, GitHub CLI, Markdown. About 150 lines in all.

## How to Demo It

1. Show the project map: 21 repos, 17 projects, three grouped folders.
2. Open the migration checklist and read the first three steps.
3. Run `clone-all.ps1` against an empty folder and show the workspace appear, including a repo that would have failed a plain clone.

## Limitations & Setup

- Needs an interactive GitHub login in a browser before the script runs.
- Secrets still have to be re-entered by hand from the password manager.
- The skill backup is a copy. It has to be refreshed when a skill changes.

## Demo Pitch

> "My laptop died with 17 projects on it. The code was on GitHub, but nothing else was. After one session of rebuilding, I wrote the recovery kit I wish I'd had: one checklist an AI agent can follow, one restore script, and a list of every secret by name. If your small team's setup lives in one person's head, this takes an afternoon to write."
