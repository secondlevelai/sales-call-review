# Sales Call Review

Grade every sales call your team recorded in Fathom or Fireflies, and see where each closer is losing deals: the objections they don't get past, the mistakes that show up on lost calls, exact quotes from the calls, and the words to say instead.

## Use it

1. Start a new chat and type **"Set up Sales Call Review."** Claude walks you step by step through connecting Fathom or Fireflies, checking it can see your closers' calls, and grading one call as a test.
2. Every week after that, ask: **"Review last week's sales calls."**
3. Claude lists the sales calls it found, grouped by closer, and asks you to confirm. It grades every one, counts the patterns, and writes a report: team numbers, a section per closer, the objection table, your team's best real answers, and three fixes for the week.

Other things to ask:
- "Coach Marcus on his last 30 days of calls."
- "Grade this call" (paste a transcript; no recorder needed).

## Data

Transcripts are read through Fathom's or Fireflies' official connector, signed in with your own account, and graded inside your Claude conversation. The plugin has no server of its own and stores nothing. In Claude Code, it keeps a `graded-calls.json` file in your working folder so calls aren't graded twice.

Built by @bingobuildsai. MIT license.
