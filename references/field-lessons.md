# Field Lessons: meta-rules for maintaining rules

Generalized from a real maintenance loop: a production project with a ~13-rule instruction file, weeks of LLM-prompt regression work, instruction text over 60,000 characters, and several near-catastrophic edit accidents. These are recorded as experience, not consensus — the consensus lives in `best-practices.md`. Each lesson states the mechanism, because the mechanism is what transfers to other projects.

## 1. Check conflicts and duplicates before adding anything

Mechanism: an instruction file grows by accretion; nothing self-prunes. New prohibitions silently contradict old hard requirements ("don't fabricate cases" vs "every section must include a case example"), and the model resolves the contradiction arbitrarily.

Procedure that survived contact with reality:
1. Render the current state from disk — never reason from memory of what the file says.
2. Search the file for the new rule's key terms; list every related old rule.
3. Disposition order: **merge duplicates > modify the conflicting old rule > add new**. Complementary rules (different angles) stay separate but cross-reference each other.
4. Report the net change per rule category, not just one number.

## 2. Numeric constraints must be converted to one unit before comparing

Mechanism: when two numeric rules disagree, the model follows the looser one; the stricter rule becomes decorative.

Real case: "no paragraph over 40 characters" coexisted with a per-section limit of 320 characters. 40×5 = 200, so the section limit was 60% looser — and 47% of paragraphs exceeded 40 characters while hugging the section limit; total output grew from 1,500 to 2,350 characters.

Procedure: before touching any number, list all same-kind constraints in one unit; make the loosest one the single source of truth; tighten or delete the rest.

## 3. ✗/✓ examples have a length cost

Mechanism: the model imitates the shape of the examples, not just the rule. Adding 5 contrast pairs moved average paragraph length from 30 to 49 characters against a 30-character reference.

Procedure: every added example pair is checked against the output-length budget; verify rule adherence *and* output length, not just the former.

## 4. Multiple rules treating one symptom ⇒ the cause is upstream

Real case: four successive rules addressed "material citations crowding out narration", "verdicts turning preachy", "cross-section repetition", "moralizing endings" — all four were symptoms of one un-touched upstream variable (per-section length cap).

Procedure: if you are adding the second or third rule for the same symptom, go fix the upstream variable (length caps, hierarchy depth, supply volume). Afterward, **delete the now-redundant downstream rules** — do not let them keep occupying context.

## 5. Root cause or it isn't done

Mechanism: guardrails (try/except, defaults, fallbacks) mask the root cause and decay silently.

Definition of done for a fix-turned-rule:
- A phenomenon→mechanism→evidence chain exists (logs, data, reproducible command — not vibes);
- The same phenomenon via a different entry point no longer reproduces;
- The rule explains why it *used to look fine* before it broke.

Classify before acting: code defect → fix + test; config/data gap → fix the pipeline or state explicitly what's missing and the consequence of not fixing it; undefined requirement → stop and ask, do not invent plausible behavior. Never report a guardrail as a fix, and never let "you could manually…" be the deliverable.

## 6. Big-block replacement safety (the 18,599→50 incident)

Real case: a batch replacement crossing a constant's boundary deleted the constant definition line along with the target block. A 18,599-character prompt collapsed to 50.

Procedure:
- Batch replacements stay **within one constant/section**; never use line-range replacements across boundaries.
- The match string must **cover the original text's tail**, or the replacement concatenates with leftover text into a duplicated sentence.
- After replacement: re-read the file to confirm boundaries, `git diff --stat`, and re-render the affected artifact once.

## 7. Instruction files decay toward chat memory

Mechanism: the most valuable rules (verified commands, no-go zones, environment quirks) get learned in conversation and never written into the file — they die at the session boundary. The file keeps the generic rules; the file loses the expensive ones.

Procedure: after any session where a command was discovered by trial, a no-go zone was hit, or an environment quirk cost more than a minute — write it into the commands/boundaries section immediately. Command rules must be verified; unverified ones are marked `TODO: verify`.

## 8. The file is for both the agent and the maintainer

Mechanism: optimize only for the agent → dense text nobody maintains, stale in 3 months. Optimize only for humans → pleasant and useless. Target: an operations runbook — organized for humans to maintain, specific enough for machines to execute.

Practical test: every rule is either (a) a command an agent can run, (b) a boundary with a reason, or (c) a convention that diverges from framework defaults. Anything else is prose wearing a rule's clothes; cut it.
