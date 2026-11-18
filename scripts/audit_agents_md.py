#!/usr/bin/env python3
"""audit_agents_md.py - mechanical checks for agent instruction files.

Usage:
    python audit_agents_md.py [path/to/AGENTS.md]

Default path: AGENTS.md in the current directory.
Exit code 0 = no warnings; 1 = warnings found; 2 = file missing / unreadable.

Checks (mechanical only - semantic review is the agent's job):
  1. Line count (warn > 200 for standing context)
  2. Consensus core sections present (commands / boundaries / layout / conventions)
  3. Code-block commands cross-checked against package.json / Makefile / pyproject.toml (stale command detection)
  4. Referenced paths that no longer exist on disk
  5. "as of <date>" statements older than 90 days
  6. TODO/FIXME placeholders left in the file
"""
from __future__ import annotations

import datetime
import json
import re
import sys
from pathlib import Path

WARN_LINE_LIMIT = 200
STALE_DAYS = 90
CORE_SECTIONS = {
    "commands": re.compile(r"^#{1,3}\s.*command|^#{1,3}\s.*(setup|dev|build|test|lint|命令速查|命令)", re.I | re.M),
    "boundaries": re.compile(r"^#{1,3}\s.*(boundar|never|guardrail|禁区|边界)", re.I | re.M),
    "layout": re.compile(r"^#{1,3}\s.*(layout|structure|director|目录|结构)", re.I | re.M),
    "conventions": re.compile(r"^#{1,3}\s.*(convention|style|规范|准则|约定|流程|准则)", re.I | re.M),
}
CMD_IN_BLOCK = re.compile(r"^(?:npm|pnpm|yarn|python|pip|make|cargo|go|docker|pytest|ruff|eslint|tsc)\s+\S+", re.I)
DATE_RE = re.compile(r"(?:as of|截至|更新于)[:\s]*([0-9]{4}-[0-9]{2}-[0-9]{2})", re.I)
PATH_RE = re.compile(r"`((?:[\w./-]+\.)+(?:py|ts|tsx|js|jsx|json|md|ya?ml|toml|sh|scss|css|vue))`")
BACKTICK_RULE = re.compile(r"^#{1,3}.*```|```", re.M)


def warn(msg: str) -> None:
    print(f"  [WARN] {msg}")


def info(msg: str) -> None:
    print(f"  [ok]   {msg}")


def load_known_commands(root: Path) -> set[str]:
    cmds: set[str] = set()
    pkg = root / "package.json"
    if pkg.exists():
        try:
            scripts = json.loads(pkg.read_text(encoding="utf-8")).get("scripts", {})
            cmds |= {f"npm run {k}" for k in scripts} | {f"npm {k}" for k in scripts}
        except Exception:
            warn("package.json exists but is not valid JSON")
    makefile = root / "Makefile"
    if makefile.exists():
        cmds |= {f"make {m}" for m in re.findall(r"^([a-zA-Z][\w-]*):", makefile.read_text(errors="ignore"), re.M)}
    pyproj = root / "pyproject.toml"
    if pyproj.exists():
        text = pyproj.read_text(errors="ignore")
        m = re.search(r"\[project\.scripts\](.*?)(?:\n\[|\Z)", text, re.S)
        if m:
            cmds |= {line.split("=")[0].strip() for line in m.group(1).splitlines() if "=" in line}
    return cmds


def main() -> int:
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("AGENTS.md")
    if not target.exists():
        print(f"error: {target} not found")
        return 2
    text = target.read_text(encoding="utf-8", errors="ignore")
    root = target.parent
    warnings = 0
    print(f"auditing {target} ({len(text)} chars, {text.count(chr(10)) + 1} lines)")

    n_lines = text.count("\n") + 1
    if n_lines > WARN_LINE_LIMIT:
        warn(f"{n_lines} lines > {WARN_LINE_LIMIT} - consider splitting into nested files / docs/")
        warnings += 1
    else:
        info(f"line count {n_lines} within limit")

    for name, rx in CORE_SECTIONS.items():
        if rx.search(text):
            info(f"core section present: {name}")
        else:
            warn(f"core section missing: {name}")
            warnings += 1

    known = load_known_commands(root)
    blocks = re.findall(r"```[a-z]*\n(.*?)```", text, re.S)
    for block in blocks:
        for line in block.splitlines():
            line = line.strip().lstrip("#$ ").strip()
            if not CMD_IN_BLOCK.match(line):
                continue
            base = " ".join(line.split()[:2]) if line.startswith(("npm", "pnpm", "yarn")) else line.split()[0]
            if known and base not in known and not any(k in line for k in known):
                if any(tok in line for tok in ("run", "test", "build", "lint")):
                    warn(f"command not found in package.json/Makefile/pyproject: {line}")
                    warnings += 1

    SKIP_DIRS = {"node_modules", ".git", "dist", "build", "__pycache__", ".venv", "venv"}

    def path_exists_deep(p: Path) -> bool:
        if p.exists():
            return True
        # shallow recursive search, pruning heavy dirs (instruction files often
        # reference paths relative to a subpackage, not the audit root)
        try:
            for hit in root.rglob(p.name):
                if any(part in SKIP_DIRS for part in hit.parts):
                    continue
                return True
        except OSError:
            pass
        return False

    for m in PATH_RE.finditer(text):
        ref = m.group(1)
        if "xxx" in ref.lower() or "<" in ref or ref.startswith("docs/"):
            continue  # example names / non-literal references
        if not path_exists_deep(root / Path(ref).name if "/" not in ref else root / ref):
            warn(f"referenced path does not exist: {ref}")
            warnings += 1

    for m in DATE_RE.finditer(text):
        try:
            d = datetime.date.fromisoformat(m.group(1))
            age = (datetime.date.today() - d).days
            if age > STALE_DAYS:
                warn(f'stale date "{m.group(1)}" ({age} days old) - verify statement still true')
                warnings += 1
        except ValueError:
            pass

    if re.search(r"\b(TODO|FIXME|XXX)\b", text):
        warn("TODO/FIXME placeholders left in the file")
        warnings += 1

    print(f"\n{warnings} warning(s)")
    return 1 if warnings else 0


if __name__ == "__main__":
    sys.exit(main())
