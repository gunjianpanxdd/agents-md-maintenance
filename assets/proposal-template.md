# Rule Proposal: <topic>

- **Date:** YYYY-MM-DD
- **Mode:** dev | pm
- **Source:** <this session's incident / commit <sha> / user-stated lesson>
- **Target file:** <AGENTS.md | CLAUDE.md | ...>
- **Landing spot:** <section name / rule number, or "new section N (justification attached)">
- **Disposition:** add | modify rule N | merge into rule N | add pointer to rule N

## Proposal text

```markdown
<final, ready-to-paste rule text>
```

## Conflict-check record

| Searched term | Hits in current file | Disposition |
|---|---|---|
| <keyword> | rule N (…) | conflict → modify / duplicate → merge / complementary → cross-ref |
| <keyword> | none | — |

## Net-change report

- Characters: +X / −Y (heavier | lighter)
- Rule count: ±N
- Sections touched: <list>

## Risk & rollback

- What could this rule mis-trigger on: <scenarios>
- Rollback: `git revert <commit>` / restore section <name> from git history
