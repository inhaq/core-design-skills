# AGENTS.md

Instructions for AI coding agents working in or with this repository.

## Project purpose

This repo provides a portable Agent Skill that teaches AI coding tools how to generate frontend UI that feels considered rather than generic. The skill follows the open [Agent Skills](https://agentskills.io/specification) standard so it works across Claude Code, Kiro, Codex, OpenCode, Copilot, Cursor, Windsurf, and any other Skill-aware tool.

The skill lives at `skills/core-design/`. It is the canonical source. Everything else supports it.

## Skill anatomy

```
skills/core-design/
├── SKILL.md                       # entry point: frontmatter + main instructions
├── references/
│   ├── anti-patterns.md           # loaded when reviewing UI for genericness
│   ├── grep-tells.md              # how to run and extend the tell checker
│   ├── examples.md                # before/after code for common tells
│   └── advanced-motion.md         # loaded when working on springs, gestures, perf, framework motion
└── scripts/
    └── check-tells.py             # regex scan for AI-default tells; exit 1 on [always] hits
```

`evals/` at the repo root holds test prompts for the skill. It is not part of the installed skill.

This is hub-and-spoke. `SKILL.md` is the always-loaded body. `references/` files load only when the agent decides to read them. Keep it that way.

## When this skill applies

Apply `skills/core-design/SKILL.md` whenever the task touches what a user will see:

- Generating components, pages, dashboards, marketing sites, or full applications
- Translating designs into HTML, CSS, React, Vue, Svelte, or any framework
- Reviewing existing UI for polish or hierarchy issues
- Making decisions about styling, spacing, motion, color, or typography

If the output renders in a browser, the skill applies.

## How to apply the skill when generating UI

1. Read `skills/core-design/SKILL.md` first.
2. Pick a clear aesthetic direction before styling.
3. Apply the Non-negotiables. Then work in priority order: hierarchy → spacing → typography → color → components → motion → polish.
4. Run `scripts/check-tells.py` on the output, then read `references/anti-patterns.md` before finishing or when reviewing.
5. Read `references/advanced-motion.md` only when the core motion rules in `SKILL.md` are not enough (springs, gestures, performance under load, Framer Motion specifics).
6. Run the Review Checklist near the bottom of `SKILL.md`.

When reviewing existing UI, present findings as a markdown table with `Before | After | Why` columns, grouped by principle. Lead with the highest-leverage fixes first; label lower-priority polish items clearly when an exhaustive pass is requested.

## Output expectations

Generated UI must:

- Match the request — framework, scope, and intent.
- Commit to one aesthetic direction.
- Use design tokens or CSS variables for color, spacing, radius, and type. No magic values.
- Establish clear hierarchy with one primary action per screen.
- Implement every interactive state: hover, focus-visible, active, disabled, loading, empty, error, success.
- Be accessible: semantic HTML, keyboard navigation, sufficient contrast, `prefers-reduced-motion` support.
- Be responsive — mobile redesigned, not just resized.
- Animate sparingly: `transform`/`opacity`/`filter` only, specific transition properties, `ease-out` for UI motion by default.
- Avoid every pattern listed in `references/anti-patterns.md`.

## Rules for extending or editing the skill

The skill is most useful when it stays short, opinionated, and practical. Apply these rules when changing it.

### Spec compliance

- `name` in frontmatter must be lowercase letters, numbers, and hyphens only, must match the directory name, and must not contain reserved words like `claude` or `anthropic`.
- `description` must describe both **what** the skill does and **when** to use it. Write in third person. Include concrete triggers (frameworks, surface types, the words a user would actually say).
- Keep `SKILL.md` body under 500 lines. Anthropic's recommendation; ours sits around 435.
- Reference files stay one level deep. No nested reference chains. Agents may only partially read deeply nested files.

### Authoring discipline

- **Stay tool-agnostic in `SKILL.md`.** Tool-specific notes go in `AGENTS.md` or `README.md`. Framework-specific motion guidance lives in `references/advanced-motion.md`.
- **Prefer removal over addition.** Every token in a loaded skill costs attention every session. If a sentence wouldn't change agent behavior, delete it.
- **Don't restate things the model already knows.** No CSS-101, no font-licensing tutorials, no "what is a card." If it's easy to explain, the model already knows it.
- **Cite specific values.** "Use a custom easing curve" is weaker than `cubic-bezier(0.23, 1, 0.32, 1)`.
- **Frame defaults as defaults.** Where a brand or context could justifiably deviate (font choice, durations, easing), say so. Avoid absolute wording.
- **Move heavy material to references.** If a section is more than ~30 lines and only relevant in specific situations, it belongs in `references/`. Add a one-line pointer in `SKILL.md` describing when to read it.
- **Update the Review Checklist** when adding new rules.
- **Update `references/anti-patterns.md`** when forbidding something so the rule is enforced both ways. Write each item as **Pattern.** why → fix, tagged `[always]` or `[default]`.
- **Add a regex to `scripts/check-tells.py`** when the new tell can be found in source, and a row to `references/grep-tells.md`.
- **Add an eval case** to `evals/cases.json` when a tell slipped through in real use.

### Structure

- Section order in `SKILL.md` is intentional: Contents → How to use → Non-negotiables → principles in priority order → Polish → Output expectations → Review checklist. Don't reshuffle.
- Tables for comparisons (timings, principles, before/after).
- Fenced code blocks must be valid and copy-pastable. CSS is fine inline; React or library-specific syntax belongs in `references/advanced-motion.md`.
- Include a short Contents list at the top of any reference file longer than ~100 lines so agents can preview the scope when partially reading.

### Iteration

- Test changes to `description` carefully. Description changes affect when the skill activates and can have outsized impact on routing. Avoid casual edits.
- Append to anti-patterns and gotchas as agents trip over things in real use.
- Don't expand instructions to compensate for one failure case — add a specific gotcha or anti-pattern instead.

## Preferences

- **Concise over comprehensive.** A short rule that gets followed beats a long rule that gets skipped.
- **Frontend-friendly decisions.** Default to web-platform primitives. Reach for libraries only when the platform genuinely lacks the capability.
- **Production-grade output.** No placeholder lorem ipsum where real microcopy would do. No `console.log` debugging. No commented-out code.
- **Restraint is a feature.** Removing decoration, narrowing color use, and trimming animation almost always improves AI-generated UI.

## Quick checklist for any UI change

- [ ] Read `skills/core-design/SKILL.md` first
- [ ] Aesthetic direction chosen and consistent
- [ ] One primary action per screen
- [ ] Spacing, color, radius, and type follow a system
- [ ] All interactive states implemented
- [ ] Accessibility verified (contrast, focus, keyboard, reduced motion)
- [ ] `scripts/check-tells.py` shows no `[always]` hits
- [ ] Cross-checked against `references/anti-patterns.md`
- [ ] Review Checklist in the skill has been run
