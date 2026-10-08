# Sales Call Review: Guided Installer

> A free Claude plugin from Second Level AI. Grades every sales call your team recorded in Fathom or Fireflies and gives you an interactive report of where each closer is losing deals, plus a PDF for each closer.

<!-- MODULE METADATA
module: sales-call-review
version: v1.2.1
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

**Pacing (say these, in your own words):**
- After install: "**Sales Call Review is installed. Next: connect Fathom or Fireflies.** That's where your calls live."
- After connecting: "Connected. Let's check I can see your closers' calls."
- After setup: "You're set up. Want me to run last week's calls now? You'll get an interactive report and a PDF for each closer."

**Where they're running Claude:**
- **You can run shell commands** → Claude Code: the Claude **desktop app's Code tab**, **VS Code**, **Cursor**, or a **terminal**. Use **Path A** everywhere below.
- **You can't run commands** → the **Claude app or claude.ai chat**. Use **Path B**. You can't install plugins from a chat message, so give them the clicks.

**Error handling:**
- `claude plugin marketplace add` fails → check internet and retry. It's a public GitHub repo, so no login is needed.
- Plugin installed but skills don't show → `/reload-plugins`, or restart.
- `claude` not found in an editor's shell → use the `/mcp` route in Step 2 instead of the login command.
- Sign-in fails → `claude mcp logout plugin:sales-call-review:<recorder>`, then sign in again.

---

## OVERVIEW

Read this to the user before starting:

We're setting up **Sales Call Review**. When we're done, you'll say "review last week's sales calls" and get:

- **An interactive report in your browser.** Click between the team overview and each closer. You'll see close rate, call score, cash per call, how often they ask for the sale, talk share, discovery time, and paid-in-full rate, each compared to the team.
- **Where each closer is losing deals**: the objections they don't get past ("think about it", partner, price, "tried this before"…), the mistakes that show up on lost calls but not closed ones, and what the buyers had that the others didn't.
- **Exact quotes from the calls and what to say instead**, plus your team's best real answer to each objection.
- **A PDF for each closer** you can send them, and a team PDF.

**Setup time:** 5–10 minutes
**Cost:** Free. It runs on your Claude plan. No API keys.
**How it works:** Fathom's or Fireflies' official connector lets Claude read your call transcripts with your own sign-in. The plugin grades them, a script counts the patterns exactly, and the report is built on your computer. Nothing is stored on any server of ours.

---

## SCOPING

Ask, then wait:

1. **"Which records your sales calls: Fathom or Fireflies?"** → `RECORDER`. (Neither? They can paste a transcript and say "grade this call." Skip to the end.)
2. **"Review just your own calls, or your whole sales team's?"** → `SCOPE`.

Check whether it's already installed (Path A):

```bash
claude plugin list 2>/dev/null | grep -q "sales-call-review" && echo "INSTALLED=true" || echo "INSTALLED=false"
```

If installed, update it to the latest version and skip to Step 2:

```bash
claude plugin marketplace update secondlevelai && claude plugin update sales-call-review@secondlevelai
```

---

## PREREQUISITES

- **A paid Claude plan** (Pro, Max, Team or Enterprise). Connectors need one.
- **Fathom or Fireflies** recording the sales calls, with transcripts on.
- **Path A only:** `claude --version` works.
- **For PDFs:** Google Chrome, Microsoft Edge or Chromium installed. Most computers have one. Without it, the report's **Save PDF** button does the same.

[VERIFY] Ask: "Ready to start?"

---

## INSTALL

### Step 1: Install the plugin

**Path A: Claude Code (desktop app Code tab, VS Code, Cursor, terminal).** Run these yourself:

```bash
claude plugin marketplace add secondlevelai/sales-call-review
claude plugin install sales-call-review@secondlevelai
```

Then tell them to type `/reload-plugins` (or restart) so it loads.

**Path B: Claude app or claude.ai chat.** Give them the clicks:
1. **Customize** → **Plugins** → **Add** → **Add marketplace**.
2. Paste **`secondlevelai/sales-call-review`** → **Add**.
3. Install **Sales Call Review**.

[VERIFY] Path A: `claude plugin list` shows `sales-call-review@secondlevelai` enabled. Path B: they see it under **Customize → Plugins**.

Then say, clearly:

> "**Sales Call Review is installed. ✅ Next: connect Fathom or Fireflies.** That's where your sales calls live, and it's how I read them. It takes about 2 minutes."

---

### Step 2: Connect Fathom or Fireflies

Explain: "The plugin reads your calls through {Recorder}'s own official connector. You sign in once with your {Recorder} account."

**Path A: Claude Code (desktop app Code tab, VS Code, Cursor, terminal)**

1. Start the sign-in yourself, **in the background** (it waits for them):

```bash
claude mcp login plugin:sales-call-review:{recorder}
```

2. Tell them: "A browser tab just opened. **Sign in to {Recorder} with the account that records your sales calls, and click Allow.** Then say done."
3. Confirm it worked:

```bash
claude mcp list 2>&1 | grep "sales-call-review:{recorder}"
```

It should say **Connected**.

4. Load it into this conversation: "Type **`/mcp`**, choose **`plugin:sales-call-review:{recorder}`**, and pick **Reconnect** if it doesn't already show connected." (Or `/reload-plugins`.)

**Doing it by hand instead** (or if the browser didn't open):
- **Claude desktop app (Code tab), VS Code, Cursor:** type **`/mcp`** in the Claude message box and press Enter.
- **Terminal:** type **`/mcp`** at the Claude prompt.
- Choose **`plugin:sales-call-review:{recorder}`** → **Authenticate** → sign in in the browser → **Allow**.

**Path B: Claude app or claude.ai chat**
1. **Customize** → **Plugins** → **Sales Call Review** → **Connectors** tab.
2. Next to **{Recorder}**, click **Connect** (or **Add**, then **Connect**). Sign in and click **Allow**.
3. On a Claude **Team or Enterprise** plan, if {Recorder} isn't listed, an Owner has to allow it first under **Customize → Connectors**.
4. **Start a new chat** and type **"set up Sales Call Review"**. The plugin's own setup takes over from here. Stop following this file.

[VERIFY] (Path A) Call the recorder's list-meetings tool for the last 14 days (metadata only). Meetings come back → "**{Recorder}'s connected.** That was the hard part."

---

### Step 3: Check team access

Group the last 14 days of meetings by who recorded them and show the counts per person.

If `SCOPE = team` and closers are missing:
- **Fathom:** put closers on one team (e.g. **Sales**) with sales calls shared to it, or have a Fathom **Admin** granted **view access to all shared calls** and connect with that account. Private calls can't be included.
- **Fireflies:** teammates in the same workspace are visible by default. A missing closer is either not in the workspace (invite them) or changed their privacy: **Settings → Personal → Recording & Privacy → Privacy & Access → Teammates & anyone with link**, applied to all meetings. "Only me" meetings can't be included.

[VERIFY] Re-run the list. Every closer they expect appears.

---

### Step 4: Define what a sales call is

Show 8–10 meeting titles and ask which are sales calls and what naming pattern they use (e.g. "Strategy Call"). Save the answer to `sales-call-review.json` in the working folder:

```json
{
  "recorder": "fathom",
  "scope": "team",
  "closers": ["Marcus Lee", "Dev Patel", "Ana Ruiz"],
  "sales_call_rule": "title contains 'Strategy Call' or 'Discovery'; external attendee; 15+ min",
  "set_up": "2026-10-08"
}
```

[VERIFY] The rule gives the count per closer they expect.

---

### Step 5: Run the first review

Say:

> "**You're set up. 🎉** Let's run your first review: every sales call from last week, graded. You'll get an interactive report that opens in your browser, where you click between the team and each closer, plus a PDF for each closer that you can send them. Want me to run it now?"

If yes → ask Claude (yourself) to **"review last week's sales calls"**. The plugin's **review-calls** skill does the rest: it lists the calls per closer for them to confirm, grades every one, asks once for dollar results, then builds and opens `sales-call-reports/<dates>/report.html` and the PDFs.

[VERIFY] The report opened in their browser, and `pdf/` holds `Team.pdf` plus one PDF per closer.

---

## WEEKLY WORKFLOW

- **Every Monday:** "Review last week's sales calls." New report, new PDFs, in `sales-call-reports/`.
- **Before a one-on-one:** "Coach Marcus on his last 30 days." You get his page and PDF.
- **One call:** paste a transcript and say "grade this call."
- **Dollar figures:** paste each deal's result (closed or lost, cash, paid in full or plan) when asked. Closers are then ranked by **cash per call**, and the top of that list should get the most calls.
- Calls already graded are tracked in `graded-calls.json` and never graded twice.
- **Big team (50+ calls a week):** each call is graded by a lightweight Haiku helper, which keeps usage down.

---

## WHAT'S NEXT

1. **Walk the team through the report** on Monday. Open it, click each closer, and play the game-film answers.
2. **Send each closer their PDF** with one fix to work on this week.
3. **Coach one closer a week:** "Coach [name]" before each one-on-one.

---

> Built by @bingobuildsai · Second Level AI · MIT license
