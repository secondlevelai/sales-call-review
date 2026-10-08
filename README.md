# Sales Call Review

**A free Claude plugin that grades every sales call your team recorded in Fathom or Fireflies, and shows where each closer is losing deals.**

You get the objections each closer doesn't get past, the mistakes that show up on lost calls but not on closed ones, exact quotes from the calls, your team's best real answers, and the words to say instead.

> "Leads who say 'let me think about it' close 9% of the time. It came up on 14 of 41 calls, and two closers accept it and end the call."
> That's the kind of headline you get, from your own calls.

---

## Set it up in 2 steps

You need a paid Claude plan (Pro, Max, Team or Enterprise) and Fathom or Fireflies recording your sales calls.

### 1. Add the plugin (one paste)

**In the Claude app or claude.ai:**

1. Open **Customize → Plugins**.
2. Click **Add → Add marketplace**.
3. Paste **`secondlevelai/sales-call-review`** and click **Add**.
4. Install **Sales Call Review**.

**In Claude Code:** paste this repo's link into a session (desktop app **Code** tab, VS Code, Cursor or terminal) and say **"set this up."** Claude installs it, opens the Fathom or Fireflies sign-in for you, and walks you through the rest.

### 2. Start a new chat and type

> **Set up Sales Call Review**

Claude walks you through the rest one step at a time (about 5 minutes):

1. **Connect Fathom or Fireflies.** It shows you exactly where to click and you sign in once.
2. **Check whose calls it can see.** It lists your closers and, if any are missing, tells you the setting to change in Fathom or Fireflies.
3. **Define what a sales call is,** so internal meetings and coaching calls are never graded.
4. **Grade one real call as a test,** so you see exactly what you'll get.

Then it offers to **run your first review**. Every week after that, just type **"Review last week's sales calls."**

### What you get

- **An interactive report that opens in your browser.** Switch between the team overview and each closer: close rate, call score, cash per call, asked-for-the-sale rate, talk share, discovery time and paid-in-full rate, each compared to the team. Then the objections they lose to, the mistakes that cost deals, what the buyers had that the others didn't, and every call with its quotes and fixes.
- **A PDF for each closer** (and one for the team) that you can send them.

The interactive report and PDFs are built on your computer, so they need Claude Code: the Claude desktop app's **Code** tab, VS Code, Cursor, or a terminal. In plain claude.ai chat, the report comes in the conversation instead.

<details>
<summary>Prefer to do it by hand?</summary>

1. **Claude app chat:** **Customize → Plugins → Sales Call Review → Connectors**, then click **Connect** on **Fathom** or **Fireflies** and sign in. **Claude Code** (desktop app Code tab, VS Code, Cursor, terminal): type `/mcp`, choose `plugin:sales-call-review:fathom` (or `fireflies`), then **Authenticate**.
2. To review your whole team, see [Fathom setup](docs/setup-fathom.md) or [Fireflies setup](docs/setup-fireflies.md).
3. On a Claude Team or Enterprise plan, an Owner may need to allow the Fathom or Fireflies connector first.
4. Type **"Review last week's sales calls."**

</details>

---

## What you can ask

| Ask | You get |
| --- | --- |
| "Review last week's sales calls" | Team report: numbers per closer, objections, mistakes that cost deals, your team's best answers, three fixes for the week |
| "Coach Marcus on his last 30 days" | A one-on-one coaching sheet for one closer, compared with the team |
| "Grade this call" + a pasted transcript | One call graded, no recorder needed |
| "Review October 1–15, just Dev and Ana" | Any date range or set of closers |

Want dollar figures? When Claude asks, paste each deal's result (closed or lost, and cash). Otherwise it reads outcomes from the calls.

## Big teams (50+ calls a week)

It grades every call, and it's built to keep usage down:
- It picks sales calls from meeting details first, so internal meetings and no-shows are never read.
- In **Claude Code** or **Cowork**, each call is graded by a lightweight Haiku helper in its own context, and a `graded-calls.json` file keeps track so no call is graded twice.
- In regular chat, it grades in batches and continues in the next message if a week is very large. Each report ends with a results block you paste into next week's review so those calls are skipped.

For big teams, Claude Code or Cowork is the cheapest way to run it.

## Your data

Calls are read through **Fathom's and Fireflies' own official connectors**, signed in with your account, and graded inside your Claude conversation. This plugin has no server and stores nothing. Calls must be recorded with your leads' consent; that's on you and your recorder's settings.

## Troubleshooting

See [docs/troubleshooting.md](docs/troubleshooting.md).

---

## Instructions for Claude

If a user pastes this repository's link and asks you to install or set it up, follow **[INSTALL.md](INSTALL.md)** step by step. It covers both the Claude app and Claude Code.

Short version for Claude Code:

```bash
claude plugin marketplace add secondlevelai/sales-call-review
claude plugin install sales-call-review@secondlevelai
```

Then have the user run `/reload-plugins`, and continue with INSTALL.md from Step 2 (connect the recorder).

If you're in the Claude app or claude.ai chat, you can't install plugins from a message. Give the user the app steps from INSTALL.md (Step 1, Path A). Once it's installed, they type "Set up Sales Call Review" in a new chat.

---

⭐ If it helped, star the repo. Built by **@bingobuildsai** · Second Level AI. MIT license.
