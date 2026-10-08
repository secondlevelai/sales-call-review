# Report template

Write the report in this order. Plain language, short sentences, numbers from `aggregate.py` only (never estimate a count). Quotes are exact, from the graded calls.

```markdown
# Sales call review: [date range]

**[Headline: the one pattern costing the team the most deals, with its number.]**
Example: "Leads who say 'let me think about it' close 9% of the time, and it came up on 14 of 41 calls. Marcus and Dev accept it and end the call."

Graded [X] of [X] sales calls from [first date] to [last date] across [N] closers.

## Team numbers
[Team table from aggregate.py]

## Closers
[Closers table from aggregate.py]

### [Closer name] · score [avg] · close rate [x%] · [n] calls
- **Biggest leak:** [mistake or objection], [the number, e.g. "on 6 of 8 lost calls"].
  > "[exact quote from one of their calls]" ([lead first name], [date])
  **Say this instead:** "[words to use]"
- **Second leak:** [same format]
- **Keep doing:** [strength], [the number].

[Repeat for every closer, best score first.]

## Objections
[Objections table from aggregate.py]

## Game film: the team's best answers
For each of the top 3 objections, the best real answer someone on the team gave on a call that closed:
- **[Objection]**: [closer] on [date]:
  > Lead: "[quote]"
  > [Closer]: "[response]"

## Mistakes that cost deals
[Mistakes table from aggregate.py]

## What the buyers had that the others didn't
[Buy-vs-not table from aggregate.py, then one sentence on the biggest gap.]

## This week's three fixes
1. [Fix for the team, with the words to say]
2. ...
3. ...

---
<details><summary>Results block: paste this into your next review so these calls aren't graded again</summary>

[One line per graded call: src:id|closer|date|out|score]

</details>

<sub>Built by @bingobuildsai</sub>
```

Rules:
- Every number comes from `aggregate.py`, or from a count you state you did by hand when scripts can't run.
- If fewer than 3 calls exist for a closer, say "too few calls to call it a pattern" instead of naming a leak.
- If outcomes were inferred from transcripts, say so once under the headline: "Outcomes are read from the calls; paste your results for exact close rates and dollar figures."
- No sales pitch, no links, no promotion. The only attribution is the small "Built by @bingobuildsai" line at the very end.
