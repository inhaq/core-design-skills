# Core Design Skills

Skill that teaches AI coding tools how to build better frontend UI. Drops into any Skill-aware tool — Claude Code, Kiro, Codex, OpenCode, Copilot, Cursor etc.

## Installation


```bash
npx skills add inhaq/core-design-skills
```

Other forms:

```bash
# Install only the core-design skill (this repo only ships one)
npx skills add inhaq/core-design-skills --skill core-design

# Install globally (available across all projects)
npx skills add inhaq/core-design-skills -g

# Install to specific agents only
npx skills add inhaq/core-design-skills -a claude-code -a kiro-cli

# Non-interactive (CI/CD friendly)
npx skills add inhaq/core-design-skills -y

# List skills available in the repo before installing
npx skills add inhaq/core-design-skills --list
```

The CLI auto-detects which coding agents you have installed and copies (or symlinks) the skill into each agent's skills directory — for example `.claude/skills/core-design/` for Claude Code and `.kiro/skills/core-design/` for Kiro CLI. After installation the skill, use it as a `/core-design` slash command on agents that support it.

## Why this exists

AI coding tools default to the same look: purple gradients, card soup, Inter everywhere, icons in colored circles, centered everything. Polished at first glance, forgettable five seconds later.

This repo gives those tools a single, opinionated reference to lean on instead. Cognitive principles condensed into rules, hierarchy, typography, spacing, color, components, motion, polish — written for AI agents that generate UI.


## Supported tools

The skill works with any tool that reads the Agent Skills format, plus any tool that can read repository files as context:

- [Claude Code](https://www.anthropic.com/claude-code) — drop into `~/.claude/skills/` or `.claude/skills/`
- [Kiro](https://kiro.dev) — drop into `~/.kiro/skills/` or `.kiro/skills/`
- [OpenCode](https://opencode.ai), [Codex CLI](https://openai.com/codex), [Copilot](https://github.com/features/copilot), Cursor, Windsurf, Continue, Aider — reference from `AGENTS.md` or the tool's instructions file

Nothing inside `SKILL.md` is tool-specific.

## Structure

```
.
├── README.md                              # this file
├── AGENTS.md                              # repo-level instructions for agents working on the skill
└── skills/
    └── core-design/
        ├── SKILL.md                       # entry point — frontmatter + main instructions (~370 lines)
        └── references/
            ├── anti-patterns.md           # AI-default tells to avoid; loaded when reviewing or shipping
            └── advanced-motion.md         # springs, clip-path, gestures, framework notes; loaded when needed
```

The split keeps the always-loaded body small and pushes heavy reference material into files the agent only reads on demand. This is the [progressive disclosure pattern](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices#progressive-disclosure-patterns) recommended for Skills.

## How to use it

### As an Agent Skill (recommended)

Run `npx skills add inhaq/core-design-skills` (see [Installation](#installation) above). The CLI handles directory placement, agent detection, and updates.

### Manual install

If you'd rather not use the CLI, copy the `skills/core-design/` directory into your tool's skills location:

- **Claude Code** — `~/.claude/skills/core-design/` (global) or `.claude/skills/core-design/` (workspace)
- **Kiro CLI** — `~/.kiro/skills/core-design/` (global) or `.kiro/skills/core-design/` (workspace)
- **Cursor** — `.agents/skills/core-design/`
- **Codex / OpenCode** — `.agents/skills/core-design/`
- See the full [list of supported agents and paths](https://github.com/vercel-labs/skills#supported-agents) in the Vercel Skills CLI docs.

The Skill-aware agent will discover it automatically based on the `description` and load the `SKILL.md` body when relevant. Reference files load only when the agent reads them.

### As steering or rules in non-Skill tools

For tools without native Skill support, reference `SKILL.md` from your project's instructions file (`AGENTS.md`, `.cursor/rules/*.mdc`, `.github/copilot-instructions.md`, `opencode.md`, etc.):

```markdown
When generating or reviewing frontend UI, follow the principles in
`skills/core-design/SKILL.md`. For genericness checks, see
`skills/core-design/references/anti-patterns.md`. For advanced motion
(springs, gestures, performance under load), see
`skills/core-design/references/advanced-motion.md`.
```

### As a prompt addendum

When you do not control the tool's configuration, paste the relevant section into the prompt. The Non-negotiables, Concentric border radius, and Review Checklist sections work well as standalone snippets.

## What is in the skill

`SKILL.md` covers:

- Non-negotiables — the 10 rules that prevent the most common AI-generated UI mistakes
- Aesthetic direction
- Visual hierarchy
- Spacing, typography, color
- Layout, components, states
- Motion — when to animate, easing, duration, accessibility
- Polish details — concentric radii, optical alignment, tabular nums, image outlines, scale on press
- Output expectations and Review checklist


## Contributing

The skill is meant to stay short, opinionated, and practical. When extending it:

- Keep `SKILL.md` under 500 lines. Move heavy material into `references/`.
- Stay tool-agnostic. Tool-specific notes go in `AGENTS.md` or this README.
- Prefer removing rules over adding them. Every token costs context every time the skill loads.
- Frame defaults as defaults. Where a brand or context could justifiably deviate, say so.
- Update the Review Checklist and `references/anti-patterns.md` together when adding or forbidding patterns.
- Keep references one level deep from `SKILL.md`. No nested reference chains.

## License

MIT.
