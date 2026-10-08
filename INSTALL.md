# Sales Call Review: Guided Installer

> A free Claude plugin from Second Level AI. Grades every sales call your team recorded in Fathom or Fireflies and shows where each closer is losing deals.

<!-- MODULE METADATA
module: sales-call-review
version: v1.1.0
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

You are helping someone install and set up Sales Call Review. They gave you this file (or pasted the repo link and asked you to set it up). Follow these rules:

**Behavior:**
- Assume they have never installed a Claude plugin or connected an app before.
- Explain each step in plain English **before** doing it. One step at a time; wait for "done" before the next.
- Use exact button names in **bold**.
- Celebrate small wins in one line ("Plugin's installed. Two steps left.").
- If something fails, don't dump error output. Explain the problem simply and give the fix.
- Never skip a **[VERIFY]**. If a check fails, stop and fix it.

**Pacing:**
- After install: "Plugin's installed. Now let's connect your call recorder."
- After connecting: "Connected. Let's check I can see your closers' calls."
- After the test grade: "You're set up. Here's your weekly routine."

**Error handling:**
- `claude plugin marketplace add` fails → check internet, then retry. It's a public GitHub repo, so no login is needed.
- Plugin installed but skills don't show → run `/reload-plugins` or restart Claude Code.
- Connector sign-in fails → sign out of Fathom/Fireflies in the browser and authenticate again.
- They're in the Claude app, not Claude Code → you can't install from chat. Give them the app steps (Step 1, Path A) and stop until they say it's installed.

---

## OVERVIEW

Read this to the user before starting:

We're setting up **Sales Call Review**. When we're done, you'll type "review last week's sales calls" and get:

- **Every sales call graded**: how well each one was run, scored 0–100, separate from whether it closed.
- **Where each closer is losing deals**: the objections they don't get past and the mistakes that show up on lost calls but not closed ones.
- **Exact quotes and what to say instead**, from your own calls.
- **Your team's best real answers** to each objection ("game film").
- **Three fixes for the week**, and a coaching sheet for any closer on request.

**Setup time:** 5–10 minutes
**Cost:** Free. It runs on your Claude plan. No API keys.
**How it works:** Fathom's or Fireflies' official connector lets Claude read your call transcripts with your own sign-in. The plugin tells Claude how to grade them and counts the patterns exactly. Nothing is stored on any server of ours.

---

## SCOPING

Ask both, then wait:

### Question 1: Where are you using Claude?

- **A) The Claude app or claude.ai** (the chat app) → use Path A in Step 1.
- **B) Claude Code** (terminal, VS Code, or the desktop app's Code tab) → use Path B in Step 1. You can run the commands for them.

Record: `SURFACE = app | code`

### Question 2: Fathom or Fireflies?

"Which records your sales calls: **Fathom** or **Fireflies**?"

Record: `RECORDER = fathom | fireflies`. If neither: it still works by pasting transcripts; skip to Test 2.

Check whether it's already installed (Claude Code):

```bash
claude plugin list 2>/dev/null | grep -q "sales-call-review" && echo "INSTALLED=true" || echo "INSTALLED=false"
```

If installed → skip to Step 2.

---

## PREREQUISITES

### A paid Claude plan

Pro, Max, Team or Enterprise. Connectors need a paid plan. Ask: "Are you on a paid Claude plan?" If not, they can upgrade at claude.ai/upgrade, or use the paste-a-transcript route without connectors.

### Claude Code (Path B only)

```bash
claude --version
```

Any recent version works. If missing, install from https://claude.com/claude-code.

### Fathom or Fireflies

Recording the sales calls, with transcripts turned on.

[VERIFY] All checks pass. Ask: "Ready to start?"

---

## INSTALL

### Step 1: Install the plugin

"First we add the plugin. It's a one-paste install."

**Path A: Claude app or claude.ai**

1. Click **Customize** in the left sidebar.
2. Click **Plugins**.
3. Click **Add**, then **Add marketplace**.
4. Paste **`secondlevelai/sales-call-review`** and click **Add**.
5. Find **Sales Call Review** in the list and click **Install** (or **Add**).

Fallback if Add marketplace isn't available: download `sales-call-review.zip` from https://github.com/secondlevelai/sales-call-review/releases/latest, then **Customize → Plugins → Add → Upload plugin** and choose the zip.

**Path B: Claude Code** (run these for them):

```bash
claude plugin marketplace add secondlevelai/sales-call-review
claude plugin install sales-call-review@secondlevelai
```

Then: "Type `/reload-plugins` (or restart Claude Code) so the plugin loads."

[VERIFY]
- **Path A:** "Do you see **Sales Call Review** under **Customize → Plugins**, switched on?"
- **Path B:** `claude plugin list` shows `sales-call-review@secondlevelai` as enabled.

"Plugin's installed. Now let's connect your call recorder."

---

### Step 2: Connect Fathom or Fireflies

"The plugin reads your calls through {Recorder}'s own official connector. You sign in once."

**Path A: Claude app or claude.ai**
1. **Customize → Plugins → Sales Call Review → Connectors** tab.
2. Next to **{Recorder}**, click **Connect** (or **Add**, then **Connect**).
3. Sign in to {Recorder} in the window that opens and click **Allow** / **Authorize**.
4. It should say **Connected**.

If {Recorder} isn't on the tab and they're on a Claude **Team or Enterprise** plan: "Your Claude Owner needs to allow the {Recorder} connector first under **Customize → Connectors**. Once they have, come back here."

**Path B: Claude Code**
1. Type `/mcp`.
2. Select `plugin:sales-call-review:{recorder}`, then **Authenticate**.
3. Finish the sign-in in the browser.

[VERIFY] **Path B:** call the recorder's list-meetings tool for the last 14 days (metadata only). Meetings come back → connected. **Path A:** you can't test the connection from this conversation. Have them open a **new chat** and type **"set up Sales Call Review"**, which runs the same checks below from inside the plugin. Stop here for Path A.

"Connected. Let's check I can see your closers' calls."

---

### Step 3: Check team access

Group the last 14 days of meetings by who recorded them and show the counts per person.

If the user wants team reviews and closers are missing:

- **Fathom:** put closers on one team (e.g. **Sales**) with sales calls shared to it, or have a Fathom **Admin** granted **view access to all shared calls** and connect with that account. Private calls can't be included.
- **Fireflies:** set the sales team's meeting privacy so the user can view their calls (or use a shared **Sales** channel). Meetings private to their owner need a **Super Admin** account (Fireflies Enterprise).

Re-run the list after they make the change.

[VERIFY] Every closer they expect appears in the list.

---

### Step 4: Define what a sales call is

Show 8–10 meeting titles and ask which are sales calls and what naming pattern they use (e.g. "Strategy Call"). Write the rule to `sales-call-review.json` in the working folder:

```json
{
  "recorder": "fathom",
  "scope": "team",
  "closers": ["Marcus Lee", "Dev Patel", "Ana Ruiz"],
  "sales_call_rule": "title contains 'Strategy Call' or 'Discovery'; external attendee; 15+ min",
  "set_up": "2026-10-08"
}
```

[VERIFY] Applying the rule to the 14-day list gives the count per closer they expect.

"Setup's saved. The review uses it every time, so you won't be asked again."

---

## TEST

### Test 1: Grade one real call

Pick the most recent matching sales call, fetch its transcript, and grade it with the `grade-pasted-call` format.

"That's what every call gets: a score, the objections, what cost the deal or won it, exact quotes, and what to say instead."

[VERIFY] The grade includes real quotes from the call.

### Test 2: Paste route (works with no recorder)

Have them paste any sales call transcript and say **"grade this call."**

### Test 3: First full review (optional, recommended)

"Want me to run your first full review now?" If yes: **"Review last week's sales calls."**

If everything works: "Sales Call Review is live. Here's your weekly routine."

---

## WEEKLY WORKFLOW

- **Every Monday:** "Review last week's sales calls." Claude lists the calls per closer, you confirm, it grades every one and writes the report.
- **Before one-on-ones:** "Coach Marcus on his last 30 days."
- **Single call:** paste a transcript, then "grade this call."
- **Dollar figures:** when asked, paste each deal's result (closed or lost, cash).
- **Not grading twice:** Claude Code keeps `graded-calls.json` in the folder. In the app, paste last report's results block into the next review.
- **Big team (50+ calls a week):** run it in Claude Code or Cowork. Each call is graded by a lightweight Haiku helper, which keeps usage down.

---

## WHAT'S NEXT

1. **Make it a habit:** run it every Monday and share the "three fixes" with the team.
2. **Use the game film:** the report's "best answers" section is a ready-made script for your weakest objection.
3. **Coach one closer a week:** "Coach [name]" before each one-on-one.

---

> Built by @bingobuildsai · Second Level AI · MIT license
