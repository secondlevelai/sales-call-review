# Sales Call Review: Guided Installer

> A free Claude plugin from Second Level AI. Grades every sales call your team recorded in Fathom or Fireflies and gives you an interactive report of where each closer is losing deals.

<!-- MODULE METADATA
module: sales-call-review
version: v1.4.1
status: RELEASED
released: 2026-10-08
requires: [claude-paid-plan, fathom-or-fireflies]
category: Sales
complexity: simple
api_keys: 0
setup_time: 5-10 minutes
-->

---

## FOR CLAUDE

You are helping someone install and set up Sales Call Review. They pasted this repo's link (or this file) and asked you to set it up. Follow these rules:

**Behavior:**
- Assume they have never installed a Claude plugin or connected an app before.
- Explain each step in plain English **before** doing it. One step at a time; wait for "done" before the next.
- Do the technical parts yourself (install commands, starting the sign-in, checking it worked). Their only jobs: sign in to Fathom/Fireflies in the browser, and answer questions.
- Use exact names in **bold**: **Customize**, **Plugins**, **Connectors**, `/mcp`.
- Celebrate small wins in one line.
- If something fails, don't dump error output. Explain it simply and give the fix.
- Never skip a **[VERIFY]**.

**Flow (Path A): one continuous run, with no "now say set it up" in between.**
Install → immediately ask the two questions → have them type `/reload-plugins` and then `/mcp` → **Authenticate** (one message) → confirm it's connected → save the setup → finish with ONE next step: "say 'review last week's sales calls'." Never run `claude mcp login` through your shell tool; it needs a real terminal.

**Where they're running Claude:**
- **You can run shell commands** → Claude Code: the Claude **desktop app's Code tab**, **VS Code**, **Cursor**, or a **terminal**. Use **Path A** everywhere below.
- **You can't run commands** → the **Claude app or claude.ai chat**. Use **Path B**. You can't install plugins from a chat message, so give them the clicks.

**Error handling:**
- `claude plugin marketplace add` fails → check internet and retry. It's a public GitHub repo, so no login is needed.
- Plugin installed but skills don't show → `/reload-plugins`, or restart.
- `claude mcp login` errors with "stdin isn't a terminal" → don't run it through your shell tool. Use `/mcp` → **Authenticate** (Step 3).
- Sign-in fails → `claude mcp logout plugin:sales-call-review:<recorder>`, then sign in again.

---

## OVERVIEW

Read this to the user before starting:

We're setting up **Sales Call Review**. When we're done, you'll say "review last week's sales calls" and get:

- **An interactive report in your browser.** Click between the team overview and each closer. You'll see close rate, call score, cash per call, how often they ask for the sale, talk share, discovery time, and paid-in-full rate, each compared to the team.
- **Where each closer is losing deals**: the objections they don't get past ("think about it", partner, price, "tried this before"…), the mistakes that show up on lost calls but not closed ones, and what the buyers had that the others didn't.
- **Exact quotes from the calls and what to say instead**, plus your team's best real answer to each objection.
- **Every call in a scrollable list** per closer (date, lead, length, score, outcome). Click one to open its full grade.

**Setup time:** 5–10 minutes
**Cost:** Free. It runs on your Claude plan. No API keys.
**How it works:** Fathom's or Fireflies' official connector lets Claude read your call transcripts with your own sign-in. The plugin grades them, a script counts the patterns exactly, and the report is built on your computer. Nothing is stored on any server of ours.

---

## PREREQUISITES

- **A paid Claude plan** (Pro, Max, Team or Enterprise). Connectors need one.
- **Fathom or Fireflies** recording the sales calls, with transcripts on.
- **Path A:** `claude --version` works.

Don't stop to ask about these. Mention them only if something fails.

---

## INSTALL (Path A: Claude Code: desktop app Code tab, VS Code, Cursor, terminal)

### Step 1: Install

Check, then install or update. Run these yourself:

```bash
if claude plugin list 2>/dev/null | grep -q "sales-call-review"; then
  claude plugin marketplace update secondlevelai && claude plugin update sales-call-review@secondlevelai
else
  claude plugin marketplace add secondlevelai/sales-call-review && claude plugin install sales-call-review@secondlevelai
fi
```

[VERIFY] `claude plugin list` shows `sales-call-review@secondlevelai` enabled.

### Step 2: Ask the two questions right away

In the same message that confirms the install:

> "**Sales Call Review is installed ✅** Two quick questions so I can connect it:
> 1. Do you record sales calls with **Fathom** or **Fireflies**?
> 2. Do you want to review **just your own calls**, or your **whole sales team's**?"

Record `RECORDER` and `SCOPE`. Neither recorder? Tell them they can paste any transcript and say "grade this call" after `/reload-plugins`, and stop.

### Step 3: Load the plugin and connect the recorder

The plugin's connector only shows up in `/mcp` once the plugin is loaded, so this is where the one reload goes. Say:

> "Now let's connect {Recorder}. In the Claude message box:
>
> 1. Type **/reload-plugins** and press **Enter**. This loads Sales Call Review.
> 2. Type **/mcp** and press **Enter**.
> 3. Choose the **{Recorder}** one, listed as **sales-call-review:{recorder}**. Click it, or use the arrow keys and press **Enter**.
> 4. Choose **Authenticate** and press **Enter**. A browser tab opens: sign in to {Recorder} and click **Allow**.
>
> Then come back here, type **done** and press **Enter**."

This works the same in the desktop app's Code tab, VS Code, Cursor and the terminal.

**Never run `claude mcp login` through your own shell tool.** It needs a real terminal and fails with "stdin isn't a terminal" in the desktop app and editors.

**Fallback, only if the connector isn't in `/mcp` or Authenticate fails:** ask "Want me to open a terminal window for the sign-in?" and then:
- **macOS:** `osascript -e 'tell application "Terminal" to activate' -e 'tell application "Terminal" to do script "claude mcp login plugin:sales-call-review:{recorder}"'`
- **Windows:** `start cmd /k claude mcp login plugin:sales-call-review:{recorder}`
- **Linux:** ask them to open a terminal and paste `claude mcp login plugin:sales-call-review:{recorder}`.
After signing in there, they type `/mcp` → **Reconnect** on that connector.

[VERIFY]

```bash
claude mcp list 2>&1 | grep "sales-call-review:{recorder}"
```

Shows **Connected** → "**{Recorder}'s connected.** That was the hard part." Still "Needs authentication" → have them try `/mcp` → **Authenticate** again, or use the fallback.

### Step 4: Save the setup

Write `sales-call-review.json` in the working folder:

```json
{ "recorder": "fireflies", "scope": "team", "set_up": "2026-10-08" }
```

Fireflies teams: everyone in the same Fireflies workspace is visible by default. Fathom teams: closers' calls must be shared to the user's team, or the user must be an Admin with view access to shared calls. The first review checks this and gives the fix if anyone's missing.

### Step 5: One next step

End with exactly this, and nothing after it:

> "**You're all set ✅**
>
> **Last step:** say **"review last week's sales calls."**
>
> I'll show you how many sales calls I found per closer and ask how many to grade. Then I open your report: a team overview and a page per closer, each with their calls in a list and their patterns across all of them.

That's the end of install. The **review-calls** skill takes over when they ask for the review. On the first run it checks team access and asks which meetings count as sales calls.

---

## INSTALL (Path B: Claude app or claude.ai chat)

You can't install from a chat message. Give the clicks:

1. **Customize** → **Plugins** → **Add** → **Add marketplace** → paste **`secondlevelai/sales-call-review`** → install **Sales Call Review**.
2. Open its **Connectors** tab → **Connect** on **Fathom** or **Fireflies** → sign in → **Allow**. On Claude Team or Enterprise, an Owner may need to allow the connector first under **Customize → Connectors**.
3. Start a new chat and say **"review last week's sales calls."**

Tell them the interactive report needs Claude to run code: in the Claude **desktop app**, use the **Code** tab. In plain chat the report comes in the conversation.

---

## WEEKLY WORKFLOW

- **Every Monday:** "Review last week's sales calls." A new report each time, in `sales-call-reports/`.
- **Before a one-on-one:** "Coach Marcus on his last 30 days." You get his page.
- **One call:** paste a transcript and say "grade this call."
- **Dollar figures:** paste each deal's result (closed or lost, cash, paid in full or plan) when asked. Closers are then ranked by **cash per call**, and the top of that list should get the most calls.
- Calls already graded are tracked in `graded-calls.json` and never graded twice.
- **Big team (50+ calls a week):** each call is graded by a lightweight Haiku helper, which keeps usage down.

---

## WHAT'S NEXT

1. **Walk the team through the report** on Monday. Open it, click each closer, and play the game-film answers.
2. **Give each closer one fix** from their page to work on this week.
3. **Coach one closer a week:** "Coach [name]" before each one-on-one.

---

> Built by @bingobuildsai · Second Level AI · MIT license
