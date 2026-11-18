# agents-md-maintenance

A universal [Agent Skill](https://agentskills.io) for **maintaining and evolving AI coding-agent instruction files** — `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursorrules`, `.github/copilot-instructions.md` — across Claude Code, OpenAI Codex, Cursor, Gemini CLI, GitHub Copilot, Windsurf, Aider, WorkBuddy, and any tool that reads the AGENTS.md standard.

Instruction files fail in predictable ways: rules accrete and start contradicting each other; the most expensive lessons (verified commands, no-go zones) live only in chat history and die at the session boundary; a bad merge quietly degrades every future session. This skill encodes the maintenance loop that prevents all three.

## What it does

- **Detects the rule-file landscape** — which file is the source of truth when a repo has several (import chains, symlinks, precedence rules)
- **Three modes**: `audit` (findings only) / `propose` (default, zero write access — produces a conflict-checked proposal file) / `gated-direct` (opt-in, every step confirmed)
- **Enforces a conflict/duplicate check before any rule is added** — merge > modify old rule > add new, with a recorded search trail
- **Checks rule quality** against a community-consensus checklist (commands first, tiered boundaries, specific over aspirational, anti-patterns)
- **Ships hard-won field lessons** — numeric-constraint unit conversion, the length cost of ✗/✓ examples, symptom-chasing detection, big-block replacement safety (the "18,599→50 characters" incident), root-cause definitions of done
- **Includes `audit_agents_md.py`** — mechanical lint: line count, missing core sections, stale commands vs package.json/Makefile/pyproject, dead path references, 90-day-old "as of" dates

## Install

<details open>
<summary><b>WorkBuddy</b></summary>

Copy the folder to `~/.workbuddy/skills/agents-md-maintenance/` (user-level) or `<repo>/.workbuddy/skills/agents-md-maintenance/` (project-level).

</details>

<details>
<summary><b>Claude Code</b></summary>

Copy to `~/.claude/skills/agents-md-maintenance/` or `<repo>/.claude/skills/agents-md-maintenance/`. The `SKILL.md` frontmatter follows the [agentskills.io](https://agentskills.io) open standard.

</details>

<details>
<summary><b>Codex / Cursor / other AGENTS.md-native tools</b></summary>

Tools without a skills runtime can still use the content directly: point your rule file at `references/best-practices.md` and `references/field-lessons.md`, e.g. add to `AGENTS.md`:

```markdown
## Rule maintenance
Before adding any rule to this file, follow references/best-practices.md checklist
and run scripts/audit_agents_md.py.
```

</details>

## Usage examples

- "把这次踩的坑沉淀成规则" / "add this lesson to AGENTS.md" → propose mode, conflict-checked
- "审查一下我的 AGENTS.md" / "audit my agents file" → findings + mechanical lint
- "我的 CLAUDE.md 和 AGENTS.md 漂移了" / "sync rules across tools" → landscape detection + single-source wiring

## Repository layout

```
SKILL.md                        # workflow, modes, safety rails
references/
  rules-file-landscape.md       # per-tool file matrix, precedence, single-source wiring
  best-practices.md             # consensus checklist (commands first, boundaries, hygiene, anti-patterns)
  field-lessons.md              # generalized experience from real maintenance loops
scripts/
  audit_agents_md.py            # stdlib-only lint (python 3.9+, no dependencies)
assets/
  proposal-template.md          # proposal file template (conflict record, net change, rollback)
```

## Design principle

**The skill has proposal power, not write power (by default).** The rule file is injected into every session; one bad merge pollutes all future work. So the skill never edits the rule file directly unless you explicitly opt into gated-direct mode — proposals land in `docs/agents-proposals/`, the user applies them through their normal verified editing flow, and git history is the rollback.

**The skill stores no rule copies.** Rule text lives only in the rule file; skills, proposals, and memory hold pointers, never content — that is what prevents drift.

## Credits & prior art

- [agents.md](https://agents.md) — the open standard (Agentic AI Foundation / Linux Foundation)
- GitHub Blog: [How to write a great agents.md — lessons from 2,500 repositories](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)
- Field lessons contributed from a real production maintenance loop (2026)

## License

MIT

## Docs

- [中文说明 (Chinese README)](README.zh-CN.md)
