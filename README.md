# Sales Call Review

> **Claude:** if a user pasted this link (with or without a message), they want it set up. Don't summarize the repo. Follow [Instructions for Claude](#instructions-for-claude): install it, ask the two questions (Fathom or Fireflies, own calls or team), have them type `/reload-plugins` and `/mcp` → Authenticate, then tell them to say "review last week's sales calls."

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

- **An interactive report that opens in your browser.** On the left: the team and each closer. Each page starts with a scrollable list of their calls (date, lead, length, score, closed or lost), and you click any call to open its full grade. Below that are the findings across all of their calls: close rate, call score, cash per call, how often they ask for the sale, talk share and discovery time (each compared to the team), what to work on, the objections they lose to, the mistakes that cost deals, and what the buyers had that the others didn't.

The interactive report is built on your computer, so they need Claude Code: the Claude desktop app's **Code** tab, VS Code, Cursor, or a terminal. In plain claude.ai chat, the report comes in the conversation instead.

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

If a user pastes this repository's link (or asks you to install or set it up) and you can run shell commands, do **all of this in one go, without waiting for them to ask again**. Full detail is in [INSTALL.md](INSTALL.md).

1. **Install** (run these yourself):
   ```bash
   claude plugin marketplace add secondlevelai/sales-call-review
   claude plugin install sales-call-review@secondlevelai
   ```
   If it's already installed, update it instead: `claude plugin marketplace update secondlevelai && claude plugin update sales-call-review@secondlevelai`.
2. **Right away, ask both questions.** Don't ask them to reload first. Say "Installed ✅", then show them **as clickable buttons** with your multiple-choice question tool (AskUserQuestion), in one call:
   - "Which records your sales calls?" Options: **Fathom**, **Fireflies**
   - "Whose calls should I review?" Options: **Just my own calls**, **My whole sales team's**

   Only use plain text if you have no question tool.
3. **Connect, in one message:**
   > "Now let's connect {Recorder}. In the Claude message box:
   > 1. Type **/reload-plugins** and press **Enter**. This loads Sales Call Review.
   > 2. Type **/mcp** and press **Enter**.
   > 3. Choose the **{Recorder}** one, listed as **sales-call-review:{recorder}**. Click it, or use the arrow keys and press **Enter**.
   > 4. Choose **Authenticate** and press **Enter**. A browser tab opens: sign in to {Recorder} and click **Allow**.
   >
   > Then come back here, type **done** and press **Enter**."

   Use exactly these numbered steps, including "press **Enter**" on each one.

   Never run `claude mcp login` through your shell tool: it needs a real terminal and fails in the desktop app and editors ("stdin isn't a terminal"). Only if `/mcp` doesn't work, offer to open a real terminal window running it (macOS: `osascript -e 'tell application "Terminal" to do script "claude mcp login plugin:sales-call-review:<recorder>"'`).
4. **Confirm** with `claude mcp list` (the recorder shows **Connected**), then save `sales-call-review.json` in the working folder: `{"recorder":"<recorder>","scope":"<me|team>","set_up":"<today>"}`.
5. **Finish with exactly one next step:**
   > "You're all set ✅ Say **"review last week's sales calls."** I'll show you the calls I found per closer, grade every one, and open your report."

The first review checks team access and asks which meetings are sales calls, so you don't need to do that here.

If you can't run commands (Claude app or claude.ai chat), you can't install from a message. Give them the clicks: **Customize → Plugins → Add → Add marketplace** → paste `secondlevelai/sales-call-review` → install, then **Connectors** → **Connect** on Fathom or Fireflies, then start a new chat and say "review last week's sales calls."

---

⭐ If it helped, star the repo. Built by **@bingobuildsai** · Second Level AI. MIT license.
