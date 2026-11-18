# Rule-File Landscape: which file, which tool, who wins

Different AI coding tools read different instruction files. This reference maps the ecosystem (as of 2026) so maintenance decisions land in the right file.

## File → tool matrix

| File | Read natively by | Notes |
|---|---|---|
| `AGENTS.md` | OpenAI Codex, Cursor, Gemini CLI, Copilot coding agent, Aider, Windsurf, Zed, Jules, Devin, opencode, goose, and most others | Open standard (agents.md), stewarded by the Agentic AI Foundation / Linux Foundation. **Default choice for new repos.** |
| `CLAUDE.md` | Claude Code | Supports `@path` imports and layered loading (user/project/local). |
| `GEMINI.md` / `.gemini/settings.json` | Gemini CLI | `context.fileName` can point at AGENTS.md. |
| `.github/copilot-instructions.md` | GitHub Copilot | IDE chat; per-repo. Copilot custom agents live in `.github/agents/*.md` with YAML frontmatter. |
| `.cursor/rules/*.mdc` (or legacy `.cursorrules`) | Cursor | Per-directory rule files with glob activation. |
| `.windsurfrules` | Windsurf (legacy) | Newer setups accept AGENTS.md. |

## Precedence rules (when an agent reads several files)

1. **Nested wins over root**: agents read the closest instruction file to the file being edited. Monorepos commonly put one `AGENTS.md` per package (the OpenAI repo itself ships ~88).
2. **Chat overrides files**: explicit user prompt in the session beats any instruction file.
3. **Symlink/import chains**: when `CLAUDE.md` contains `@AGENTS.md`, or `.cursorrules` is a symlink to `AGENTS.md`, the target file is the source of truth. **Edit the target, never the pointer.**

## Keeping one source of truth across tools

Anti-pattern: maintaining parallel copies in CLAUDE.md + .cursorrules + copilot-instructions.md — they drift within weeks.

Convergent patterns, from strongest to weakest:

1. **Everything is AGENTS.md.** Claude Code: `CLAUDE.md` contains a single line `@AGENTS.md`. Cursor: `.cursor/rules/main.mdc` → reference or symlink. Gemini CLI: `context.fileName: "AGENTS.md"`. Copilot: keep a thin `.github/copilot-instructions.md` containing only genuinely Copilot-specific notes and a pointer.
2. **Symlink where imports are unsupported**: `ln -s AGENTS.md CLAUDE.md` (note: Windows needs junctions or a checkout-time script; symlinks are a filesystem feature and don't travel through git on all platforms).
3. **Thin per-tool files**: only when a tool has genuinely tool-specific behavior worth separating.

## Layering for large projects

- Root file: repo-wide commands, boundaries, conventions. Keep standing context **≤ ~200 lines**.
- Per-directory files (`src/AGENTS.md`, `tests/AGENTS.md`, `apps/web/AGENTS.md`): rules that only apply when editing there.
- Long-form standards (API conventions, style manuals, prompt-design specs) go in `docs/` and are referenced with a trigger condition ("read docs/style.md before touching UI code") — not inlined into the standing file.
- Workflow-level procedures that only matter occasionally (release steps, migration generation) belong in skills (SKILL.md per agentskills.io), not in the standing instruction file.
