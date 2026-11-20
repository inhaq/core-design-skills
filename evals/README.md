# Evals

Prompts for checking that the skill changes what an agent produces. Not loaded by the skill.

## Run

1. Pick a case from `cases.json`.
2. Run the prompt in a Skill-aware agent with the skill installed. Run it once without the skill as a baseline.
3. Save the output and run the checker on it:

   ```bash
   python3 skills/core-design/scripts/check-tells.py path/to/output
   ```

4. Check each item in the case's `must_not` list by eye. Check each `must` item too.
5. A case passes when the checker reports no `[always]` hits and every `must` / `must_not` item holds.

## Add a case

When an agent ships a tell in real use, add a case that would have caught it. Keep prompts short and realistic; the tell should appear without the skill and disappear with it.
