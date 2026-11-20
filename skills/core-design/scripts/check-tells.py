#!/usr/bin/env python3
"""Scan frontend source for common AI-default UI tells.

Usage:
    python3 scripts/check-tells.py [--only always|default] [--rtl] [PATH ...]

    --only always   print only [always] hits
    --rtl           also flag physical left/right spacing (ml-*, pr-*)

Prints one line per hit: file:line  [tag] name  ->  fix
Exit code is 1 when any [always] tell is found, else 0.

A hit is a prompt to look, not a verdict. `[default]` tells are fine when the
aesthetic direction calls for them. See references/anti-patterns.md.

To keep a hit on purpose, put `check-tells: ignore` in a comment on the same
line or the line above, followed by the reason.
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

IGNORE = "check-tells: ignore"

# Characters allowed between two utility classes in the same class string.
SAME_CLASS = r"[^\"'`\n]*"

# (tag, name, regex, fix, skip_if_line_matches)
TELLS: list[tuple[str, str, str, str, str | None]] = [
    # Color and mood
    ("default", "purple/indigo gradient", r"(from|via|to)-(purple|violet|indigo|fuchsia)-\d{2,3}|linear-gradient\([^)]*(#(7c3aed|8b5cf6|6366f1|a855f7|9333ea|4f46e5))", "flat brand accent", None),
    ("default", "gradient text", r"bg-clip-text|background-clip:\s*text", "solid text, emphasis via weight", None),
    ("default", "colored glow shadow", r"shadow-(purple|violet|indigo|blue|fuchsia|pink|cyan|emerald)-\d{3}(/\d+)?", "neutral low-opacity shadow", None),
    ("default", "light gray text (check background)", r"\btext-(gray|slate|zinc|neutral)-(300|400)\b", "on light surfaces use a darker neutral (>= 4.5:1)", None),
    # Borders and boxes: the left bar and its disguises
    ("default", "left-edge accent bar", r"\bborder-[ls]-(2|4|8)\b|border-(left|inline-start):\s*\d+px\s+solid", "tint, icon state, or weight shift", None),
    ("default", "left-edge bar via inset shadow", r"shadow-\[inset_\d+px_0_0|box-shadow:[^;]*inset\s+[2-9]px\s+0\s+0", "tint, icon state, or weight shift", None),
    ("default", "left-edge bar via ::before",
     rf"before:left-0\b{SAME_CLASS}before:w-(0\.5|1|1\.5|\[\d+px\])\b|before:w-(0\.5|1|1\.5|\[\d+px\]){SAME_CLASS}before:left-0\b",
     "tint, icon state, or weight shift", None),
    ("default", "top accent bar on card", r"\bborder-t-(4|8)\b|border-top:\s*[3-9]px\s+solid", "content or small label signals category", None),
    ("default", "glassmorphism", r"\bbackdrop-blur(-\w+)?\b|backdrop-filter:\s*blur", "one translucent layer max, solid fallback", None),
    # Typography
    ("default", "wide uppercase tracking",
     rf"\buppercase\b{SAME_CLASS}\btracking-(wider|widest|\[0\.[2-9])|\btracking-(wider|widest|\[0\.[2-9][^\]]*\]){SAME_CLASS}\buppercase\b",
     "sentence case, modest tracking", None),
    # Layout
    ("always", "h-screen", r"(?<![\w-])h-screen\b", "h-svh / h-dvh or content height", None),
    ("default", "100vh height", r"(?<![\w-])height:\s*100vh", "100svh / 100dvh on full-height sections", None),
    ("default", "100vh min-height", r"(?<![\w-])min-h-screen\b|min-height:\s*100vh", "min-h-dvh / 100dvh", None),
    ("rtl", "physical left/right spacing", r"\b[mp][lr]-(\d+|\[)", "logical ms-* / ps-* for RTL", None),
    # Motion
    ("always", "transition: all", r"transition:\s*all\b|\btransition-all\b", "list exact properties", None),
    ("always", "bounce/ping", r"\banimate-(bounce|ping)\b", "remove; motion that never stops is noise", None),
    ("default", "pulse", r"\banimate-pulse\b", "fine on skeleton loaders; remove on dots, badges, and CTAs", None),
    ("default", "infinite animation", r"animation:[^;]*\binfinite\b", "decorative loops: remove, or stop under reduced motion",
     r"spin|loader|loading|progress|indeterminate|skeleton"),
    ("default", "hover lift on cards", r"hover:-translate-y-(0\.5|1|2)\b", "subtle feedback only on clickable things", None),
    ("always", "scale(0) entrance", r"scale\(0\)|\bscale-0\b", "start from scale(0.95) + opacity 0", None),
    ("always", "layout property transition", r"transition(-property)?:[^;]*\b(width|height|top|left|right|bottom|margin|padding)\b", "transform for movement and size", None),
    # Accessibility and code
    ("always", "focus outline removed", rf"\bfocus:outline-none\b(?!{SAME_CLASS}\bfocus(-visible)?:(ring|outline))|outline:\s*(none|0)\b", "replace with a visible focus ring",
     r":not\(:focus-visible\)"),
    ("always", "z-index 9999", r"z-index:\s*9{3,}|\bz-\[9{3,}\]", "use a z-index scale", None),
    ("always", "!important", r"!important", "fix the cascade", r"^\s*(return|const|let|var)\b|/.*!important.*/[gimsuy]*"),
    # Content and copy
    ("always", "placeholder people/companies", r"\b(Acme( Inc| Corp)?|Jane Cooper|John Doe|Jane Doe|lorem ipsum)\b", "real or realistic microcopy",
     r"placeholder\s*[=:]|\be\.g\."),
    ("always", "buzzword copy", r"\b(seamless(ly)?|effortless(ly)?|supercharge|unleash|elevate your|next-gen|unlock the power)\b", "say what it actually does", None),
    ("default", "emoji in UI copy", "[\u2728\U0001F680\U0001F525\U0001F4A1\u26A1\U0001F389]", "real icon or none", None),
]

# Tells that can span lines. Matched on the whole file.
MULTILINE: list[tuple[str, str, str, str]] = [
    ("always", "div with onClick", r"<div\b[^>]*?\son[Cc]lick=", "<button> or <a>"),
]

REDUCED_MOTION = re.compile(r"prefers-reduced-motion|motion-reduce:|motion-safe:")
# Blocks where !important is expected: reduced-motion overrides and print styles.
OVERRIDE_BLOCK = re.compile(r"@media[^{]*(prefers-reduced-motion|\bprint\b)")
COMMENT_LINE = re.compile(r"^\s*(//|/\*|\*|<!--|\{/\*)")
# Input groups move the ring to the wrapper; look up to 20 lines up for it.
FOCUS_WITHIN = re.compile(r"focus-within:|:focus-within")
MOTION = re.compile(r"@keyframes|animation:|\banimate-\w|transition:\s*(transform|translate)", re.IGNORECASE)

COMPILED = [
    (tag, name, re.compile(rx, re.IGNORECASE), fix, re.compile(skip, re.IGNORECASE) if skip else None)
    for tag, name, rx, fix, skip in TELLS
]
COMPILED_MULTI = [(tag, name, re.compile(rx, re.IGNORECASE | re.DOTALL), fix) for tag, name, rx, fix in MULTILINE]


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


def ignored(lines: list[str], lineno: int) -> bool:
    """True when the hit line or the line above carries the ignore pragma."""
    here = lines[lineno - 1]
    above = lines[lineno - 2] if lineno >= 2 else ""
    return IGNORE in here or IGNORE in above


def override_lines(lines: list[str]) -> set[int]:
    """Line numbers inside reduced-motion or print @media blocks, tracked by braces."""
    inside: set[int] = set()
    active = opened = False
    depth = 0
    for lineno, line in enumerate(lines, 1):
        if OVERRIDE_BLOCK.search(line):
            active, opened, depth = True, False, 0
        if active:
            inside.add(lineno)
            opened = opened or "{" in line
            depth += line.count("{") - line.count("}")
            if opened and depth <= 0:
                active = False
    return inside


def scan(path: str, rtl: bool = False) -> list[tuple[int, str, str, str]]:
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError:
        return []
    lines = text.splitlines() or [""]
    blocks = override_lines(lines)
    hits = []
    for lineno, line in enumerate(lines, 1):
        if COMMENT_LINE.match(line) and IGNORE not in line:
            continue
        for tag, name, rx, fix, skip in COMPILED:
            if tag == "rtl" and not rtl:
                continue
            if name == "!important" and lineno in blocks:
                continue
            if name == "focus outline removed" and any(
                FOCUS_WITHIN.search(l) for l in lines[max(0, lineno - 20):lineno]
            ):
                continue
            if skip and skip.search(line):
                continue
            if rx.search(line) and not ignored(lines, lineno):
                hits.append((lineno, "default" if tag == "rtl" else tag, name, fix))
    for tag, name, rx, fix in COMPILED_MULTI:
        for m in rx.finditer(text):
            lineno = text.count("\n", 0, m.start()) + 1
            if not ignored(lines, lineno):
                hits.append((lineno, tag, name, fix))
    # File-level: motion with no reduced-motion handling anywhere in the file.
    if path.endswith((".css", ".scss", ".sass", ".less")) and MOTION.search(text) and not REDUCED_MOTION.search(text):
        m = MOTION.search(text)
        hits.append((text.count("\n", 0, m.start()) + 1, "always", "motion with no reduced-motion fallback",
                     "add @media (prefers-reduced-motion: reduce)"))
    hits.sort()
    return hits


def main(argv: list[str]) -> int:
    args = argv[1:]
    only = None
    rtl = "--rtl" in args
    if "--only" in args:
        i = args.index("--only")
        only = args[i + 1] if i + 1 < len(args) else None
        if only not in ("always", "default"):
            print("--only takes 'always' or 'default'", file=sys.stderr)
            return 2
        del args[i:i + 2]
    paths = [a for a in args if a != "--rtl"] or ["."]
    always = 0
    total = 0
    counts: dict[tuple[str, str], int] = {}
    for path in iter_files(paths):
        for lineno, tag, name, fix in scan(path, rtl=rtl):
            total += 1
            always += tag == "always"
            counts[(tag, name)] = counts.get((tag, name), 0) + 1
            if only is None or tag == only:
                print(f"{path}:{lineno}  [{tag}] {name}  ->  {fix}")
    print(f"\n{total} hit(s), {always} [always].", file=sys.stderr)
    for (tag, name), n in sorted(counts.items(), key=lambda kv: (kv[0][0] != "always", -kv[1])):
        print(f"  {n:>4}  [{tag}] {name}", file=sys.stderr)
    return 1 if always else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
