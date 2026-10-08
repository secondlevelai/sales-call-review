# Writing coaching.json

The report's numbers all come from `aggregate.py`. Your only job is the coaching words: one block for the team and one per closer. Write them to `coaching.json` and pass it to `build_report.py --coaching coaching.json`.

First run `aggregate.py report <file> --json` (and `--closer "Name"` for each closer) and write **only from those numbers** plus quotes from the graded calls.

## Rules

- **Coach the pattern across all of a closer's graded calls, never a single call.** The headline and every fix must describe something that repeats ("on 6 of 9 lost calls", "overcome 2 of 7 times"). A one-off moment isn't a fix; leave it for that call's own grade.
- Lead with the pattern that costs the most deals, and quote its number ("on 6 of 8 lost calls", "overcome 20% of the time"). Never make up a number.
- Each fix needs words the closer can actually say on the next call.
- Use a real quote from that closer's graded calls (`obj[].q`, the lead's words) when one shows the problem. Copy it exactly.
- Prefer a teammate's real answer that closed (the objection's `best` answer) over a generic line.
- With fewer than 3 calls for a closer, say it's early and stick to what the calls clearly show.
- Plain, direct language. No filler, no hype.
- Two or three fixes per person, biggest impact first. One or two "keep doing" lines, each with a number.

## Shape

```json
{
  "team": {
    "headline": "Leads who say 'let me think about it' close 9% of the time. It came up on 14 of 41 calls, and Marcus and Dev accept it and end the call.",
    "fixes": [
      {
        "title": "Accepting “let me think about it”",
        "why": "On 11 of 20 lost calls vs 1 of 21 closed ones.",
        "quote": "I just need to think about it, it's a lot to take in.",
        "say_instead": "“Totally fair. What specifically do you need to think through? Let's do it now while I'm here.”"
      }
    ],
    "keep_doing": ["Holding firm on price: overcome 9 of 10 times."]
  },
  "reps": {
    "Dev Patel": {
      "headline": "Dev pitches in the first minute: 0 minutes of discovery on both calls, and 85% of the talking on the one he lost.",
      "fixes": [
        { "title": "Skipping discovery", "why": "...", "quote": "...", "say_instead": "..." }
      ],
      "keep_doing": ["..."]
    }
  }
}
```

Use the exact closer names as they appear in the graded calls. Any closer you leave out gets coaching written from the numbers automatically.
