# Finding tells mechanically

Read this file when reviewing a codebase or your own output for AI-default tells and you want a fast first pass before judging by eye.

## Run the checker

```bash
python3 <skill-dir>/scripts/check-tells.py src/
```

`<skill-dir>` is the folder holding `SKILL.md`. The script scans HTML, CSS, JS/TS, JSX/TSX, Vue, Svelte, Astro, and MDX, and skips `node_modules`, `dist`, `build`, and framework output folders.

Each hit prints as `file:line  [tag] name  ->  fix`, followed by a count per tell. The exit code is `1` when any `[always]` tell is found, so it can gate CI. It is `2` for a bad flag or a path that doesn't exist, so a typo in CI fails instead of passing.

| Flag | Effect |
| --- | --- |
| `--only always` | print only `[always]` hits; start here on a big codebase |
| `--only default` | print only `[default]` hits |
| `--rtl` | also flag physical left/right spacing (`ml-*`, `pr-*`) |
| `-h`, `--help` | print usage |

Comments are skipped, including the body of a multi-line block comment, so a comment that mentions `outline: none` is not a hit.

When scanning a folder, test, story, and fixture files are skipped (`*.test.*`, `*.spec.*`, `*.stories.*`, `__tests__/`, `__mocks__/`, `e2e/`, `fixtures/`). Their fake names and deliberate tells are not UI. Pass a file directly to scan it anyway.

## Read the hits

- `[always]` hits are bugs. Fix them.
- `[default]` hits need a reason. Keep one only if the aesthetic direction calls for it.
- A clean run does not mean the design is good. Hierarchy, rhythm, and copy need eyes. Work through `references/anti-patterns.md` after the script.

## Keep a hit on purpose

Put `check-tells: ignore` in a comment on the same line or the line above, with the reason:

```tsx
{/* check-tells: ignore — editorial pull quote, approved in design review */}
<blockquote className="border-l-4 border-accent ps-6">…</blockquote>
```

```css
/* check-tells: ignore — third-party widget overrides inline styles */
.vendor-chat { z-index: 10000 !important; }
```

## What it looks for

| Tell | Tag | Matches |
| --- | --- | --- |
| Purple/indigo gradient | default | `from-purple-*`, `via-indigo-*`, purple hexes in `linear-gradient` |
| Gradient text | default | `bg-clip-text`, `background-clip: text` |
| Colored glow shadow | default | `shadow-indigo-500/50` and similar |
| Light gray text | default | `text-gray-300/400`; fine on dark surfaces |
| Left-edge bar | default | `border-l-4`, `border-s-4`, `border-left` / `border-inline-start: 4px solid` |
| Left-edge bar, disguised | default | inset shadow `inset 3px 0 0`, `before:left-0 … before:w-1` |
| Top accent bar | default | `border-t-4`, `border-top: 4px solid` |
| Glassmorphism | default | `backdrop-blur`, `backdrop-filter: blur` |
| Wide uppercase tracking | default | `uppercase` + `tracking-widest`, either order |
| Italic or gradient word in headline | default | `<h1>` with an `<em>`, `<i>`, or an italic or gradient `<span>` inside |
| `h-screen` | always | `h-screen` (not `min-h-screen`) |
| 100vh height | default | `height: 100vh`; fine on hidden filler layers |
| 100vh min-height | default | `min-h-screen`, `min-height: 100vh` |
| Physical left/right spacing | default, `--rtl` only | `ml-*`, `pr-*` instead of `ms-*`, `pe-*` |
| `transition: all` | always | `transition-all`, `transition: all` |
| Bounce/ping | default | `animate-bounce`, `animate-ping`; fine on loaders and live-status dots |
| Pulse | default | `animate-pulse`; fine on skeleton loaders |
| Infinite animation | default | `animation: … infinite`; spinners and progress exempt |
| No reduced-motion fallback | always | a stylesheet with motion and no `prefers-reduced-motion`, `motion-safe:`, or `motion-reduce:`; spinners and progress don't count as motion |
| Hover lift | default | `hover:-translate-y-1` |
| `scale(0)` entrance | always | `scale(0)`, `scale-0` |
| Layout property transition | always | `transition: width …`, `max-height`, `top`, `left`, `margin`, `padding`; not `border-left-color` |
| Focus ring removed | always | `focus:outline-none`, `focus-visible:outline-none`, `outline-hidden`, `outline: none`, with no `focus:ring-*` or `focus:outline-*` within 3 lines (`ring-0` doesn't count). Exempt: `:focus:not(:focus-visible)` blocks, `main:focus` and `tabindex="-1"` targets, `focus-within:` wrappers |
| Bare outline-none | default | `outline-none` with no `focus:` prefix and no ring nearby; popups and menu items often show focus with a highlight instead |
| Clickable div | always | `<div … onClick=`, Vue `@click`, Svelte `on:click`, across lines; divs with `role` or `aria-hidden` exempt |
| z-index 9999 | always | `z-index: 9999`, `z-[9999]` |
| `!important` | always | outside reduced-motion and print blocks, and not in JS regexes |
| Placeholder people | always | Acme, Jane Cooper, John Doe, lorem ipsum, case-sensitive; `placeholder=` and "e.g." examples exempt |
| Buzzword copy | always | seamless, effortless, supercharge, unleash, next-gen; import lines exempt |
| Emoji in copy | default | ✨ 🚀 🔥 💡 ⚡ 🎉 |

## Extend it

Add a tuple to `TELLS` in `scripts/check-tells.py`: tag, name, regex, fix, and an optional regex that exempts a line. Put tells that span lines in `MULTILINE`. In the same change, add the item to `references/anti-patterns.md`, a row to the table above, and a line to `tests/fixtures/bad.tsx` (or a false alarm to `tests/fixtures/good.css`) with a test.
