"""Check the skill against the Agent Skills spec and this repo's own limits. Run: python3 tests/validate_skill.py"""

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "core-design"
MAX_LINES = 500

errors = []

skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
match = re.match(r"^---\n(.*?)\n---\n", skill, re.DOTALL)
if not match:
    errors.append("SKILL.md: missing YAML frontmatter")
else:
    front = dict(line.split(":", 1) for line in match.group(1).splitlines() if ":" in line)
    front = {k.strip(): v.strip() for k, v in front.items()}
    name = front.get("name", "")
    if name != SKILL_DIR.name:
        errors.append(f"SKILL.md: name '{name}' must match directory '{SKILL_DIR.name}'")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 64:
        errors.append("SKILL.md: name must be lowercase letters, numbers, and single hyphens, max 64 chars")
    if re.search(r"claude|anthropic", name):
        errors.append("SKILL.md: name must not contain reserved words")
    description = front.get("description", "")
    if not description or len(description) > 1024:
        errors.append("SKILL.md: description must be 1-1024 chars")

body_lines = skill.count("\n") + 1
if body_lines > MAX_LINES:
    errors.append(f"SKILL.md: {body_lines} lines, limit {MAX_LINES}")

# Every references/ or scripts/ path named in SKILL.md must exist.
for rel in sorted(set(re.findall(r"`((?:references|scripts)/[\w.-]+)`", skill))):
    if not (SKILL_DIR / rel).exists():
        errors.append(f"SKILL.md: points to missing file {rel}")

try:
    cases = json.loads((ROOT / "evals" / "cases.json").read_text(encoding="utf-8"))
    for case in cases:
        missing = {"id", "prompt", "must", "must_not"} - case.keys()
        if missing:
            errors.append(f"evals/cases.json: case {case.get('id', '?')} missing {sorted(missing)}")
except (OSError, ValueError) as exc:
    errors.append(f"evals/cases.json: {exc}")

if not (ROOT / "LICENSE").exists():
    errors.append("LICENSE file missing")

for e in errors:
    print(e)
print(f"{len(errors)} problem(s).")
sys.exit(1 if errors else 0)
