#!/usr/bin/env python3
"""Scan frontend source for common AI-default UI tells.

Usage:
    python3 scripts/check-tells.py [PATH ...]

Prints one line per hit: file:line  [tag] name  ->  fix
Exit code is 1 when any [always] tell is found, else 0.

A hit is a prompt to look, not a verdict. `[default]` tells are fine when the
aesthetic direction calls for them. See references/anti-patterns.md.
"""

from __future__ import annotations

import os
import re
import sys

EXTENSIONS = {
    ".html", ".htm", ".css", ".scss", ".sass", ".less",
    ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".astro", ".mdx",
}
SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", ".nuxt", ".svelte-kit", ".astro", "coverage", "vendor"}

# (tag, name, regex, fix)
TELLS: list[tuple[str, str, str, str]] = [
    # Color and mood
    ("default", "purple/indigo gradient", r"(from|via|to)-(purple|violet|indigo|fuchsia)-\d{2,3}|linear-gradient\([^)]*(#(7c3aed|8b5cf6|6366f1|a855f7|9333ea|4f46e5))", "flat brand accent"),
    ("default", "gradient text", r"bg-clip-text|background-clip:\s*text", "solid text, emphasis via weight"),
    ("default", "colored glow shadow", r"shadow-(purple|violet|indigo|blue|fuchsia|pink|cyan|emerald)-\d{3}(/\d+)?", "neutral low-opacity shadow"),
    ("always", "light gray body text", r"\btext-(gray|slate|zinc|neutral)-(300|400)\b", "darker neutral (>= 4.5:1)"),
    # Borders and boxes
    ("default", "left-edge accent bar", r"\bborder-l-(2|4|8)\b|border-left:\s*\d+px\s+solid", "tint, icon state, or weight shift"),
    ("default", "top accent bar on card", r"\bborder-t-(4|8)\b|border-top:\s*[3-9]px\s+solid", "content or small label signals category"),
    ("default", "glassmorphism", r"\bbackdrop-blur(-\w+)?\b|backdrop-filter:\s*blur", "one translucent layer max, solid fallback"),
    # Typography
    ("default", "wide uppercase tracking", r"\buppercase\b[^\"'`]*\btracking-(wider|widest|\[0\.[2-9])", "sentence case, modest tracking"),
    # Layout
    ("always", "100vh hero", r"\bh-screen\b|\bmin-h-screen\b|height:\s*100vh|min-height:\s*100vh", "100svh / 100dvh or content height"),
    # Motion
    ("always", "transition: all", r"transition:\s*all\b|\btransition-all\b", "list exact properties"),
    ("always", "infinite pulse/bounce", r"\banimate-(pulse|bounce|ping)\b|animation:[^;]*infinite", "remove; motion that never stops is noise"),
    ("default", "hover lift on cards", r"hover:-translate-y-(0\.5|1|2)\b", "subtle feedback only on clickable things"),
    ("always", "scale(0) entrance", r"scale\(0\)|\bscale-0\b", "start from scale(0.95) + opacity 0"),
    # Accessibility and code
    ("always", "focus outline removed", r"\bfocus:outline-none\b(?![^\"'`]*\bfocus(-visible)?:ring)|outline:\s*(none|0)\b", "replace with a visible focus ring"),
    ("always", "div with onClick", r"<div[^>]*\son[Cc]lick=", "<button> or <a>"),
    ("always", "z-index 9999", r"z-index:\s*9{3,}|\bz-\[9{3,}\]", "use a z-index scale"),
    ("always", "!important", r"!important", "fix the cascade"),
    # Content and copy
    ("always", "placeholder people/companies", r"\b(Acme( Inc| Corp)?|Jane Cooper|John Doe|Jane Doe|lorem ipsum)\b", "real or realistic microcopy"),
    ("always", "buzzword copy", r"\b(seamless(ly)?|effortless(ly)?|supercharge|unleash|elevate your|next-gen|unlock the power)\b", "say what it actually does"),
    ("always", "emoji in UI copy", "[\u2728\U0001F680\U0001F525\U0001F4A1\u26A1\U0001F389]", "remove"),
]

# The reduced-motion block legitimately uses !important; ignore hits inside it.
REDUCED_MOTION = re.compile(r"prefers-reduced-motion")

COMPILED = [(tag, name, re.compile(rx, re.IGNORECASE), fix) for tag, name, rx, fix in TELLS]


def iter_files(paths: list[str]):
    for root in paths:
        if os.path.isfile(root):
            yield root
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fn in filenames:
                if os.path.splitext(fn)[1].lower() in EXTENSIONS:
                    yield os.path.join(dirpath, fn)


def scan(path: str) -> list[tuple[int, str, str, str]]:
    hits = []
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            lines = fh.readlines()
    except OSError:
        return hits
    in_reduced_motion = False
    opened = False
    depth = 0
    for lineno, line in enumerate(lines, 1):
        if REDUCED_MOTION.search(line):
            in_reduced_motion, opened, depth = True, False, 0
        for tag, name, rx, fix in COMPILED:
            if name == "!important" and in_reduced_motion:
                continue
            if rx.search(line):
                hits.append((lineno, tag, name, fix))
        if in_reduced_motion:
            # Track braces so the whole @media block is skipped, however long.
            opened = opened or "{" in line
            depth += line.count("{") - line.count("}")
            if opened and depth <= 0:
                in_reduced_motion = False
    return hits


def main(argv: list[str]) -> int:
    paths = argv[1:] or ["."]
    always = 0
    total = 0
    for path in iter_files(paths):
        for lineno, tag, name, fix in scan(path):
            total += 1
            always += tag == "always"
            print(f"{path}:{lineno}  [{tag}] {name}  ->  {fix}")
    print(f"\n{total} hit(s), {always} [always].", file=sys.stderr)
    return 1 if always else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
