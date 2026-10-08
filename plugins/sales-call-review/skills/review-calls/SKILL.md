---
name: review-calls
description: Review, grade or analyze a sales team's recorded calls from Fathom or Fireflies, such as "review last week's sales calls", "where are my closers losing deals", "grade my team's calls", "what objections are we losing to", or a weekly closer performance report. Grades every call and reports each closer's leaks with exact quotes and what to say instead.
---

# Review sales calls

Grade **every** sales call in the range against `references/rubric.md`, count the patterns exactly with `scripts/aggregate.py`, and write the report in `references/report-template.md`. The reader is a sales manager or offer owner. Keep their attention cost low: no preamble, ask only the questions below, and keep progress updates to one line.

## 1. Find the recorder

Check which call-recorder tools are available: Fathom (meeting list + transcript tools) or Fireflies (`fireflies_*` tools). Choose by what the tools do, not their exact names.

- **Both connected:** ask once, as buttons (Fathom / Fireflies), which one holds the sales calls.
- **Neither connected:** say: "You haven't connected Fathom or Fireflies yet. Want me to walk you through it? It takes about 5 minutes. (Or paste a transcript and I'll grade that one call.)" If yes, follow the **setup** skill. If they paste a transcript, use the `grade-pasted-call` skill.

**Setup card:** if the user pasted a "Sales Call Review setup" card, or `sales-call-review.json` exists in the working folder (Claude Code / Cowork), use its recorder, scope and closers. Don't ask again for anything it already answers.

Read `references/fathom.md` or `references/fireflies.md` for that recorder before listing anything.

## 2. Set the range

Default: the last 7 days, or "since the last review" if the user pasted a results block from a previous report (skip every `src:id` listed in it). Use whatever range or closer the user names instead.

**Claude Code / Cowork only:** if `graded-calls.json` exists in the working folder, it is the ledger of calls already graded. Run `python3 ${CLAUDE_SKILL_DIR}/scripts/aggregate.py seen graded-calls.json` and skip those calls; the report can still cover them from the ledger.

## 3. List calls from metadata only

List meetings for the range **without transcripts or summaries**, paging until every result is in (Fathom: follow the cursor; Fireflies: `skip` by 50). Keep only sales calls, using the rules in the recorder reference (external attendee, 15+ minutes, not clearly coaching/onboarding/internal; drop no-shows and duplicates).

**Pick out the sales calls yourself; don't ask which meetings are sales calls.** Use the rules in the recorder reference, and say in one line how many meetings you skipped and why.

**Ask how many to grade.** There can be a lot of calls, so never start grading without this answer. Show one compact message and wait:

```
Found 38 sales calls (Oct 1–7) · skipped 21 internal/short/duplicate meetings
- Marcus Lee: 14   - Dev Patel: 13   - Ana Ruiz: 11

How many should I grade?
1. All 38
2. The most recent 10 per closer (30 calls)
3. Just certain closers or dates (tell me which)
```

Show the counts as text, then ask "How many should I grade?" **as clickable buttons** with your multiple-choice question tool (AskUserQuestion): options like **All 38**, **Most recent 10 per closer (30)** and **Certain closers or dates** (they type which via "Other"). Plain text only if you have no question tool. Adjust option 2 to the real numbers (if every closer has 10 or fewer, offer only "All" or "Certain closers or dates"). Grade exactly what they choose.

**Coverage check:** if every call belongs to the signed-in user but they asked about a team (or `sales-call-review.json` says `"scope": "team"`), give the "teammates' calls are missing" fix from the recorder reference, then offer to grade what is visible.

## 4. Grade every confirmed call

Never drop calls silently. Read each transcript once.

**If the `call-grader` agent is available (Cowork, Claude Code):** send each call to it, several at a time. Give each one: recorder (`fathom`/`fireflies`), the call ID, closer name and email, lead name, date, and duration. It fetches the transcript in its own context and returns one compact JSON object. You never load transcripts yourself.

**Otherwise (chat):** grade in batches of about 10. For each call, fetch its transcript, grade it against `references/rubric.md`, and write only the compact JSON object; don't restate or summarize the transcript. After each batch post one progress line ("Graded 20/38"). If you're running low on room in this conversation, post the JSON so far plus the list of calls still to grade, and say "Reply 'continue' and I'll grade the rest." Then continue from that list.

Grading rules that matter most (full rules in the rubric): tag only what is clearly said, exact quotes under about 25 words, `ok: true` only if the lead moved past the objection on this call, and score how the rep ran the call, not whether it closed.

## 5. Outcomes and cash (ask once, optional)

After grading, ask once:

> "Want dollar figures? Paste each deal's result (name or date, closed/lost, cash, and paid in full / plan / deposit / financing), or say skip and I'll use what was said on the calls. With cash, the report ranks closers by cash per call."

If they paste results, set `out`, `cash` and `pay` from them and `out_by: "user"`. If they skip, keep the transcript outcome (`out_by: "transcript"`).

## 6. Count exactly

Write all graded JSON objects to a file as one array (e.g. `graded-batch.json`), then:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/aggregate.py report graded-batch.json
```

**Claude Code / Cowork:** first merge into the ledger, then report from it so past weeks count too:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/aggregate.py add graded-calls.json graded-batch.json
python3 ${CLAUDE_SKILL_DIR}/scripts/aggregate.py report graded-calls.json --from 2026-10-01 --to 2026-10-07
```

Use `--closer "Name"` for one closer and `--json` if you need the raw numbers. If no code tool can run here, count by hand from the JSON and say "Counted by hand" under the headline.

## 7. Build the report

**When you can run code (Claude Code in the terminal, VS Code, Cursor or the desktop app; Cowork):** build the interactive HTML report.

1. Write the coaching words to `coaching.json`, following `references/coaching.md` (team + one block per closer, written only from patterns in the `aggregate.py` numbers across all of their calls, plus real quotes).
2. Run:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/build_report.py graded-calls.json --from 2026-10-01 --to 2026-10-07 \
  --coaching coaching.json --confirmed 38 --recorder fathom --open
```

(Use `graded-batch.json` instead of the ledger if there isn't one. `--confirmed` is the number of calls the user chose to grade. `--open` opens the report in their browser.)

It writes `sales-call-reports/<from>_to_<to>/report.html`: a team overview plus a page per closer. Each page starts with a scrollable list of that person's calls (date, lead, length, score, outcome, and click for the full grade), then the overall findings across all of their calls.

3. Reply in chat, short:

```
Your report is open in your browser: sales-call-reports/2026-10-01_to_2026-10-07/report.html
Graded 30 of 30 sales calls from Oct 1 to Oct 7 across 3 closers.

Biggest pattern: [team headline]

This week's three fixes:
1. ...
2. ...
3. ...

Click a closer on the left to see their calls and their patterns. Click any call to open its full grade.
```

**When you can't run code (claude.ai or Claude app chat):** write the report in the chat instead, following `references/report-template.md`: headline with a number, then this coverage line word for word with the real numbers: `Graded 38 of 38 sales calls from Oct 1 to Oct 7 across 3 closers.` (graded, then confirmed). Then the team table, a section per closer with exact quotes and "say this instead", objections, game film, mistakes, buyers-vs-not, three fixes, the collapsed results block, and the small "Built by @bingobuildsai" line. Mention once that the interactive report is available when this runs in Claude Code or the desktop app's Code tab.

No pitch, links or promotion either way.

The results block (chat only) lists one line per graded call (`src:id|closer|date|out|score`) so the next review can skip them. Claude Code tracks this in `graded-calls.json` instead.

## Failure cases

| Situation | Say |
| --- | --- |
| Zero meetings in range | "No meetings found from [dates]. Want a wider range?" |
| Meetings but none look like sales calls | Say so, list the 5 closest titles, and ask if any of them should be graded. |
| Only the user's own calls | The coverage fix from the recorder reference. |
| Transcript missing or empty | Skip it, count it as "not graded (no transcript)", and list it in the report. |
| A call isn't actually a sales call | Mark it skipped and say why in the coverage line. |
