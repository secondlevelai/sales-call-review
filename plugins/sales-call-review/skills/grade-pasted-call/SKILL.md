---
name: grade-pasted-call
description: Grade a single sales call transcript the user pastes or uploads (Zoom, Google Meet, .vtt, .srt, .txt or plain "Name: text" lines), such as "grade this call", "what did my closer do wrong here", or "review this transcript". Use when no call recorder is connected or for one call.
---

# Grade one pasted call

1. **Identify the rep and the lead.** The rep (closer) runs the call and presents the offer; the lead is the prospect. If speaker names are ambiguous, ask once: "Which speaker is the closer?"
2. **Grade** with `references/rubric.md`: exact quotes, `ok` only if the lead moved past the objection on this call, and a score for how the call was run, not the outcome. If the result isn't clear from the call, ask once whether it closed.
3. **Reply** in this shape. Keep it scannable:

```markdown
# Call grade: [closer] with [lead] · score [0–100]

**[One-sentence verdict: why it closed or the real reason it didn't.]**

| Discovery before pitch | Lead stated their pain | Reason to act now | Decision-maker on call | Asked for the sale | Rep talk share |
| --- | --- | --- | --- | --- | --- |
| [x min] | yes/no | yes/no | yes/no | yes/no | [x%] |

## Objections
| Objection | Lead said | Rep said | Overcome? |
| --- | --- | --- | --- |

## What cost this deal
1. **[Mistake]**
   > "[exact quote]"
   **Say instead:** "[words]"

## What worked
- [strength, with the moment it happened]

<sub>Built by @bingobuildsai</sub>
```

4. **Optional:** end with the compact JSON for this call (per the rubric) inside a collapsed `<details>` block, so it can be pasted into a later team review.

If the transcript has no speaker labels at all, say grading needs speaker names and ask for the version with names (Zoom and Meet transcripts include them).
