---
name: coach-closer
description: Deep coaching for one closer from their recorded sales calls in Fathom or Fireflies, such as "coach Marcus", "why isn't Dev closing", "what should Ana work on", or a one-on-one prep for a sales rep. Finds their biggest leaks with exact quotes, compares them with the team, and gives words to say instead.
---

# Coach one closer

This is the `review-calls` workflow narrowed to one person, with deeper coaching. Use the `review-calls` skill's steps for finding the recorder, listing calls, grading (its rubric) and counting (its `aggregate.py`), with these changes:

1. **Scope to the closer.** Ask for their name if it wasn't given. Fathom: `recorded_by[]` = their email. Fireflies: `organizers` = their email. Default range: last 30 days (a closer needs enough calls for patterns).
2. **Reuse grades.** If `graded-calls.json` exists (Claude Code / Cowork) or the user pasted a results block, use those grades and only grade calls that are missing. Never re-fetch a transcript that's already graded.
3. **Team comparison.** If team grades are available in the ledger, run `aggregate.py report graded-calls.json` for the team and `aggregate.py report graded-calls.json --closer "Name"` for the closer, and compare them. Otherwise coach from the closer's calls alone and say so.
4. **Minimum evidence.** With fewer than 5 graded calls, say the read is early and keep it to what the calls clearly show.

## Report and PDF (when you can run code)

Write that closer's block to `coaching.json` (see the review-calls `references/coaching.md`), then build their page and PDF:

```bash
python3 ${CLAUDE_SKILL_DIR}/../review-calls/scripts/build_report.py graded-calls.json --from <date> --to <date> \
  --closer "Marcus Lee" --coaching coaching.json --open
```

This opens their page in the browser and writes `pdf/Marcus-Lee.pdf` to send them. Then give the coaching in chat as below.

## Coaching output

Lead with the pattern that costs this closer the most deals, and quote the numbers from `aggregate.py`. Never make up a number. Plain, direct language.

```markdown
# Coaching: [Name] · [date range] · [n] calls

**[Headline: the single biggest thing costing them deals, with a number.]**

## Fix 1: [title]
**Why:** [the pattern in their calls, with numbers, vs the team if known]
> "[exact quote from their call]" ([lead], [date])
**Say instead:** "[words for the next call]"

## Fix 2: ...
## Fix 3 (only if it's real): ...

## Keep doing
- [strength, with its number]

## Their numbers vs the team
[closer vs team: close rate, avg score, asked for the sale, talk share, objections overcome]

## Practice before the next call
Role-play the top objection: "[the lead's most common objection, in the lead's words]". Use [teammate]'s answer that closed: "[quote]".

<sub>Built by @bingobuildsai</sub>
```
