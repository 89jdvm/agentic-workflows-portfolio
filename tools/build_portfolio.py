"""Rebuild the README index, the site home page and any missing hero cards from projects/*.md.

Usage:
    python tools/build_portfolio.py            # write README index + missing heroes
    python tools/build_portfolio.py --check    # exit 1 if README or a hero is out of date
    python tools/build_portfolio.py --hero <slug> [--hero <slug> ...]   # regenerate these heroes

Each project page carries YAML frontmatter (see _template.md). The one-line
pitch is the first "> " line after the H1. Pages tagged `consulting` go in the
engagements table; everything else goes in the systems table. Both tables sort
newest first by last_updated (falling back to date_built).
"""

import argparse
import hashlib
import html
import re
import sys
import textwrap
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PROJECTS = ROOT / "projects"
ASSETS = ROOT / "assets"
README = ROOT / "README.md"
# GitHub Pages home. Jekyll rewrites .md links only in files with front matter,
# and README.md has none, so the site gets a copy that does.
SITE_INDEX = ROOT / "index.md"
SITE_FRONT_MATTER = "---\nlayout: default\ntitle: Agentic Workflows Portfolio\n---\n\n"
START = "<!-- PORTFOLIO:INDEX:START -->"
END = "<!-- PORTFOLIO:INDEX:END -->"

# (dark, light) gradient pairs, same family as the original hand-picked cards.
PALETTE = [
    ("#1d4ed8", "#60a5fa"), ("#0f766e", "#14b8a6"), ("#7c3aed", "#a78bfa"),
    ("#b45309", "#f59e0b"), ("#be185d", "#f472b6"), ("#15803d", "#4ade80"),
    ("#9f1239", "#fb7185"), ("#0e7490", "#22d3ee"), ("#4338ca", "#818cf8"),
    ("#a16207", "#facc15"),
]

GLYPH = (
    '<g transform="translate(850,200)" fill="#ffffff" fill-opacity="0.22">'
    '<rect x="20" y="20" width="110" height="110" rx="14"/>'
    '<rect x="150" y="20" width="110" height="110" rx="14" fill-opacity="0.35"/>'
    '<rect x="20" y="150" width="110" height="110" rx="14" fill-opacity="0.35"/>'
    '<rect x="150" y="150" width="110" height="110" rx="14"/></g>'
)


def load_pages():
    pages = []
    for path in sorted(PROJECTS.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
        if not m:
            sys.exit(f"{path.name}: no frontmatter")
        meta = yaml.safe_load(m.group(1)) or {}
        pitch = next((ln[2:].strip() for ln in m.group(2).splitlines() if ln.startswith("> ")), "")
        meta = {k: ("" if v is None else v) for k, v in meta.items()}
        meta.update(file=path.name, pitch=pitch, tags=meta.get("tags") or [])
        meta["slug"] = meta.get("slug") or path.stem
        meta["sort"] = str(meta.get("last_updated") or meta.get("date_built") or "")
        pages.append(meta)
    return pages


def hero_svg(page):
    slug = page["slug"]
    dark, light = PALETTE[int(hashlib.md5(slug.encode()).hexdigest(), 16) % len(PALETTE)]
    title = page["project"].split(". ")[0]
    size = 68 if len(title) <= 22 else 56 if len(title) <= 28 else 46
    lines = textwrap.wrap(page["pitch"], 48)[:4]
    if len(textwrap.wrap(page["pitch"], 48)) > 4:
        lines[-1] = lines[-1].rstrip(" ,.;:") + "…"
    esc = html.escape
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630" role="img" aria-label="{esc(title)}">',
        '  <defs>',
        '    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">',
        f'      <stop offset="0%" stop-color="{dark}"/>',
        f'      <stop offset="100%" stop-color="{light}"/>',
        '    </linearGradient>',
        '    <pattern id="grid" width="60" height="60" patternUnits="userSpaceOnUse">',
        '      <path d="M 60 0 L 0 0 0 60" fill="none" stroke="#ffffff" stroke-opacity="0.05" stroke-width="1"/>',
        '    </pattern>',
        '  </defs>',
        '  <rect width="1200" height="630" fill="url(#bg)"/>',
        '  <rect width="1200" height="630" fill="url(#grid)"/>',
        f'  {GLYPH}',
        f'  <text x="80" y="100" font-family="monospace" font-size="15" fill="#ffffff" fill-opacity="0.72" letter-spacing="2">{esc(str(page.get("status", "")).upper())}</text>',
        f'  <text x="80" y="220" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="{size}" font-weight="800" fill="#ffffff">{esc(title)}</text>',
    ]
    for i, line in enumerate(lines):
        out.append(f'  <text x="80" y="{334 + 38 * i}" font-family="-apple-system, sans-serif" font-size="26" fill="#ffffff" fill-opacity="0.88">{esc(line)}</text>')
    x = 80
    for tag in page["tags"][:4]:
        w = 32 + 14 * len(tag)
        out.append(f'  <g transform="translate({x}, 540)"><rect width="{w}" height="38" rx="19" fill="#ffffff" fill-opacity="0.18"/><text x="{w / 2}" y="25" font-family="monospace" font-size="15" fill="#ffffff" text-anchor="middle">{esc(tag)}</text></g>')
        x += w + 12
    out.append('  <text x="1120" y="600" font-family="monospace" font-size="14" fill="#ffffff" fill-opacity="0.55" text-anchor="end">built with Claude Code</text>')
    out.append('</svg>')
    return "\n".join(out) + "\n"


def cell(text):
    return str(text).replace("|", "\\|").replace("\n", " ")


def build_index(pages):
    # load_pages() returns pages in file-name order; the stable sort keeps that order for ties.
    systems = sorted((p for p in pages if "consulting" not in p["tags"]), key=lambda p: p["sort"], reverse=True)
    engagements = sorted((p for p in pages if "consulting" in p["tags"]), key=lambda p: p["sort"], reverse=True)
    rows = [START, "<!-- Auto-generated by tools/build_portfolio.py. Do not edit between these markers. -->", "",
            f"### Systems and builds ({len(systems)})", "", "| | Project | Status |", "|---|---|---|"]
    for p in systems:
        link = f"projects/{p['file']}"
        tags = " · ".join(f"`{t}`" for t in p["tags"])
        effort = f" <br> Built in {cell(p['effort'])}" if p.get("effort") else ""
        rows.append(
            f"| [![{cell(p['project'])}](assets/{p['slug']}/hero.svg)]({link}) "
            f"| **[{cell(p['project'])}]({link})** <br> {cell(p['pitch'])} <br><br> {tags}{effort} "
            f"| `{p.get('status', '')}` |"
        )
    rows += ["", f"### Consulting engagements ({len(engagements)})", "",
             "The field work the systems above grew out of.", "",
             "| Engagement | What I did | Since |", "|---|---|---|"]
    for p in engagements:
        rows.append(f"| **[{cell(p['project'])}](projects/{p['file']})** | {cell(p['pitch'])} | {str(p.get('date_built', ''))[:4]} |")
    rows += ["", END]
    return "\n".join(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--hero", action="append", default=[])
    args = ap.parse_args()

    pages = load_pages()
    stale = []

    for p in pages:
        if "consulting" in p["tags"]:
            continue
        hero = ASSETS / p["slug"] / "hero.svg"
        if hero.exists() and p["slug"] not in args.hero:
            continue
        stale.append(str(hero.relative_to(ROOT)))
        if not args.check:
            hero.parent.mkdir(parents=True, exist_ok=True)
            hero.write_text(hero_svg(p), encoding="utf-8")

    readme = README.read_text(encoding="utf-8")
    if START not in readme or END not in readme:
        sys.exit("README.md: index markers missing")
    head, rest = readme.split(START, 1)
    new = head + build_index(pages) + rest.split(END, 1)[1]
    if new != readme:
        stale.append("README.md")
        if not args.check:
            README.write_text(new, encoding="utf-8")

    site = SITE_FRONT_MATTER + new
    if not SITE_INDEX.exists() or SITE_INDEX.read_text(encoding="utf-8") != site:
        stale.append("index.md")
        if not args.check:
            SITE_INDEX.write_text(site, encoding="utf-8")

    if args.check:
        if stale:
            print("out of date: " + ", ".join(stale))
            sys.exit(1)
        print("up to date")
    else:
        print("wrote: " + (", ".join(stale) if stale else "nothing, already current"))


if __name__ == "__main__":
    main()
