# Finding tells mechanically

Read this file when reviewing a codebase or your own output for AI-default tells and you want a fast first pass before judging by eye.

## Run the checker

```bash
python3 scripts/check-tells.py src/
```

Run it from the skill directory, or pass the script's full path. It scans HTML, CSS, JS/TS, JSX/TSX, Vue, Svelte, Astro, and MDX, and skips `node_modules`, `dist`, `build`, and framework output folders.

Each hit prints as `file:line  [tag] name  ->  fix`. The exit code is `1` when any `[always]` tell is found, so it can gate CI.

## Read the hits

- `[always]` hits are bugs. Fix them.
- `[default]` hits need a reason. Keep one only if the aesthetic direction calls for it, and say so in the review.
- A clean run does not mean the design is good. Hierarchy, rhythm, and copy quality need eyes. Work through `references/anti-patterns.md` after the script.

## What it looks for

| Tell | Matches |
| --- | --- |
| Purple/indigo gradient | `from-purple-*`, `via-indigo-*`, purple hexes in `linear-gradient` |
| Gradient text | `bg-clip-text`, `background-clip: text` |
| Colored glow shadow | `shadow-indigo-500/50` and similar |
| Light gray body text | `text-gray-300`, `text-slate-400` |
| Left-edge accent bar | `border-l-4`, `border-left: 4px solid` |
| Top accent bar | `border-t-4`, `border-top: 4px solid` |
| Glassmorphism | `backdrop-blur`, `backdrop-filter: blur` |
| Wide uppercase tracking | `uppercase … tracking-widest` |
| 100vh hero | `h-screen`, `min-h-screen`, `100vh` |
| `transition: all` | `transition-all`, `transition: all` |
| Infinite motion | `animate-pulse`, `animate-bounce`, `animate-ping`, `infinite` |
| Hover lift | `hover:-translate-y-1` |
| `scale(0)` entrance | `scale(0)`, `scale-0` |
| Focus ring removed | `focus:outline-none` with no `focus:ring`, `outline: none` |
| Clickable div | `<div onClick=` |
| z-index 9999 | `z-index: 9999`, `z-[9999]` |
| `!important` | outside the reduced-motion block |
| Placeholder people | Acme, Jane Cooper, John Doe, lorem ipsum |
| Buzzword copy | seamless, effortless, supercharge, unleash, next-gen |
| Emoji in copy | ✨ 🚀 🔥 💡 ⚡ 🎉 |

## Extend it

Add a tuple to `TELLS` in `scripts/check-tells.py`: tag, name, regex, fix. Add the matching item to `references/anti-patterns.md` and a row to the table above in the same change.
