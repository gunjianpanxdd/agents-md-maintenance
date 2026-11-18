---
name: agents-md-maintenance
description: Maintain and evolve AI coding-agent instruction files (AGENTS.md, CLAUDE.md, GEMINI.md, .cursorrules, .github/copilot-instructions.md). This skill should be used when the user asks to "add a lesson to AGENTS.md", "沉淀规则", "update agent rules", "audit/clean up my agents file", "sync rules across tools", or after fixing a recurring mistake worth encoding as a rule. It supports proposal-first (safe) and gated-direct modes, auto-detects which rule-file system the repo uses, and enforces conflict/duplicate checks before any rule is added.
agent_created: true
---

# AGENTS.md Maintenance

## Purpose

Turn debugging lessons, collaboration decisions, and workflow corrections into durable, non-conflicting rules inside the repository's agent instruction file — without bloating it, duplicating existing rules, or breaking what already works.

**Hard safety rails (apply in every mode):**

1. **Never store rule text anywhere except the rule file itself.** Skills, scripts, memory folders, and proposals must not become shadow copies of rules — that guarantees drift. The rule file is the single source of truth; everything else points at it.
2. **Every substantive rule must come from a real, reproducible event** (a bug, a failed review, a repeated question). One-off accidents do not become rules.
3. **Never invent commands.** A command rule must be verified in this repository before being proposed; unverified commands are written as `TODO: verify` or left out.
4. **Report net change**: characters added/removed, rule count delta, and whether the file got heavier or lighter. Rules only accrete; they never get pruned — that is how instruction files rot.

## Step 0 — Detect the rule-file landscape

Before anything else, detect which instruction system(s) this repository uses. Check, in order:

1. `AGENTS.md` (repo root; also glob `**/AGENTS.md` for nested files in monorepos)
2. `CLAUDE.md`, `.claude/CLAUDE.md`
3. `GEMINI.md` or `.gemini/settings.json` (`context.fileName`)
4. `.github/copilot-instructions.md`, `.github/agents/*.md`
5. `.cursor/rules/*.mdc`, `.cursorrules`
6. `.windsurfrules`

If multiple exist, determine which is the source of truth (import/symlink chains reveal it — see `references/rules-file-landscape.md`). If none exists, ask the user whether to create one (default: `AGENTS.md`, the tool-agnostic standard) before writing anything. **Do not silently pick a file when several exist** — a rule written into the wrong file is worse than no rule.

## Mode selection

| Mode | Trigger | Writes rule file directly? |
|---|---|---|
| **audit** | "audit my agents file", "why isn't the agent following rules" | Never. Produces findings only. |
| **propose** (default) | "add this lesson as a rule", "沉淀规则" — any repo with collaborators, or any rule with wide blast radius | Never. Produces a proposal file; the user applies it in a normal session. |
| **gated-direct** | user explicitly opts in (solo repos, trusted loop) | Yes, but every step pauses for explicit user confirmation; no batch edits. |

Default to **propose** when unsure. Escalation to gated-direct is the user's explicit choice, never the skill's.

## Workflow (propose mode)

### 1. Collect input
- The session's own debugging trail, the user's stated lesson, recent fix-type commits (`git log --oneline -30`).
- Filter: would this mistake recur if the entry point, account, or task changed? No → not a rule, at most a note.

### 2. Classify and locate
Assign the rule to exactly one layer (see `references/best-practices.md` for layer definitions):
- **Commands** — verified build/test/lint commands, environment quirks
- **Boundaries** — never-touch / ask-first / always-do lists
- **Workflow** — how work must be done (verification steps, commit rules)
- **Domain** — project-specific conventions that diverge from defaults

Locate the landing spot in the existing file structure. **Do not create a new top-level section** unless nothing fits; if a new section seems needed, propose it separately with justification.

### 3. Conflict and duplicate check (mandatory, never skipped)
1. Read the rule file's current content from disk — never from memory or cache.
2. For each key phrase of the new rule, search the existing file for related rules.
3. Classify each hit:
   - **Conflict** (they say opposite things) → the proposal must *modify the old rule* to make them consistent; a silent contradiction means the model follows whichever rule is longer or later.
   - **Duplicate** (same rule in multiple places) → keep the most complete one; others become pointers or are removed.
   - **Complementary** (different angles) → keep both and cross-reference them.
4. Numeric rules: convert all same-kind constraints to one unit before comparing (e.g. chars-per-paragraph vs chars-per-section vs total length). The loosest constraint silently wins; make the loosest one the single source and tighten or delete the rest.

### 4. Draft the proposal
Write `docs/agents-proposals/YYYY-MM-DD-<topic>.md` using `assets/proposal-template.md`. The proposal must contain: target file + landing spot, disposition type (add / modify old rule N / merge / add pointer), final ready-to-paste text, the conflict-check record (including what was searched and found clean), net-change report, and rollback notes.

### 5. Hand off
Present the proposal path and net-change summary. State explicitly that this skill has not modified the rule file. The user applies it through the normal editing flow with their usual verification steps. Stop there — no half-applied state.

## Writing standards

Every proposed rule must pass the checklist in `references/best-practices.md`. The short version:

- Imperative and specific, never aspirational ("use async/await, not .then()" beats "write clean async code").
- Prohibitions carry a replacement path; write criteria + one or two real ✗/✓ pairs instead of banned-word lists (word lists get paraphrased around).
- Hard requirements carry a fallback ("what to do when material is insufficient"), or they force fabrication.
- Examples cost output fidelity: the model imitates the shape of your ✗/✓ pairs, so budget their length.
- One rule, one job. If three rules treat the same symptom, the root cause is upstream — fix that instead of adding a fourth rule.

## Audit mode

Run `scripts/audit_agents_md.py <path-to-rule-file>` for mechanical checks, then read the file and report:
- Sections missing vs. the consensus core (commands, boundaries, project layout, conventions)
- Line count (warning threshold: 200 lines standing context)
- Stale content: commands that no longer exist in `package.json`/`Makefile`/`pyproject.toml`, dates in "as of" statements older than 90 days, references to deleted paths
- Contradictions and near-duplicates (same topic appearing in multiple sections)
- Rules that a fresh agent cannot act on ("follow existing patterns" without saying where the patterns live)

## Field lessons

`references/field-lessons.md` records generalized lessons from real maintenance loops (large-prompt regression work, 60k+ character instruction files, multi-round optimization). Read it when drafting rules about rules — i.e., meta-rules for the instruction file itself — or when a user asks why a particular safety rail exists.
