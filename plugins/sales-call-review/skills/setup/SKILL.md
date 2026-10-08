---
name: setup
description: Guided first-time setup for Sales Call Review, such as "set up Sales Call Review", "help me connect Fathom", "connect Fireflies", "how do I get started", right after the plugin is installed, or when the user pastes the github.com/secondlevelai/sales-call-review link. Walks step by step through connecting Fathom or Fireflies (Claude app, desktop app, VS Code, Cursor or terminal), checking which closers' calls are visible, and running the first review with its interactive report.
---

# Sales Call Review: guided setup

## FOR CLAUDE

You are walking a sales manager or offer owner through setting up Sales Call Review. Follow these rules:

**Behavior:**
- Assume they've never connected an app to Claude. Explain each step in one or two plain sentences **before** asking them to do it.
- **One step at a time.** Give the step, then wait for them to say it's done before moving on.
- Use exact names in **bold**: **Customize**, **Plugins**, **Connectors**, **Connect**, `/mcp`.
- Celebrate small wins in one line ("Fathom's connected. That was the hard part.").
- If something fails, explain it in plain English and give the one thing to try next. No raw errors.
- **Never skip a [VERIFY].**
- Keep messages short. The whole setup is about 5 minutes.

**Where they're running Claude decides how they connect.** Check once, silently:
- **You can run shell commands** (you have a Bash/terminal tool) → they're in **Claude Code**: the Claude desktop app's **Code** tab, VS Code, Cursor, or a terminal. Use **Path A**.
- **You can't run commands** → they're in the **Claude app or claude.ai chat**. Use **Path B**.

---

## If they pasted the repo link and it's already installed

Don't describe the plugin. Go straight to Step 0's questions. If `sales-call-review.json` already exists and the recorder shows **Connected** in `claude mcp list`, skip setup and say: "You're already set up ✅ Say **'review last week's sales calls'** to run a review."

## STEP 0: Right after install, say what's next

If they just installed the plugin, or this is their first message to it, say:

> "Sales Call Review is installed. ✅
>
> **Next: connect your call recorder.** That's where your sales calls live, and it's how I read them. It takes about 2 minutes: you sign in to Fathom or Fireflies once, and I do the rest.
>
> Which do you use: **Fathom** or **Fireflies**? And do you want to review **just your own calls** or your **whole sales team's**?"

Record `RECORDER = fathom | fireflies` and `SCOPE = me | team`. If they use neither: they can paste any call transcript and say "grade this call". Stop setup there.

If the recorder's tools already work (Fathom: list-meetings / get-transcript tools; Fireflies: `fireflies_*` tools), say "Looks like {Recorder} is already connected. Let me check it." and jump to **Step 2**.

---

## STEP 1: Connect {Recorder}

### Path A: Claude Code (desktop app Code tab, VS Code, Cursor, terminal)

Explain: "You'll sign in to {Recorder} once. It takes about 30 seconds."

1. Tell them exactly this:

> "In the Claude message box, type **`/mcp`** and press Enter. Choose **`plugin:sales-call-review:{recorder}`**, then **Authenticate**. A browser tab opens: sign in to {Recorder} with the account that records your sales calls, click **Allow**, then come back here and say **done**."

This works the same in the desktop app's Code tab, VS Code, Cursor and the terminal.

2. When they say done, confirm:

```bash
claude mcp list 2>&1 | grep "sales-call-review:{recorder}"
```

It should say **Connected**.

**Never run `claude mcp login` yourself through your shell tool.** It needs a real terminal and fails with "stdin isn't a terminal" in the desktop app and editors.

**Fallback, only if `/mcp` doesn't show the connector or Authenticate fails:** open a real terminal window running the sign-in. Ask first: "Want me to open a terminal window for the sign-in?"
- **macOS:** `osascript -e 'tell application "Terminal" to activate' -e 'tell application "Terminal" to do script "claude mcp login plugin:sales-call-review:{recorder}"'`
- **Windows:** `start cmd /k claude mcp login plugin:sales-call-review:{recorder}`
- **Linux:** ask them to open a terminal and paste `claude mcp login plugin:sales-call-review:{recorder}`.
Then have them type `/mcp` → **Reconnect** on that connector so this conversation picks it up.

### Path B: Claude app or claude.ai chat

Explain: "The plugin reads your calls through {Recorder}'s official connector. You sign in once."

1. Click **Customize** in the left sidebar.
2. Click **Plugins**, then **Sales Call Review**, then the **Connectors** tab.
3. Next to **{Recorder}**, click **Connect** (if it says **Add**, click that first).
4. Sign in to {Recorder} and click **Allow**. It should say **Connected**.
5. **Start a new chat** (so the connection loads) and type **"set up Sales Call Review"**. I'll pick up from the check.

**Not on the Connectors tab?** On Claude **Team or Enterprise** plans, an Owner must allow the connector first: they go to **Customize → Connectors**, add {Recorder}, and allow it. Then try again.

> Tip for Path B: the interactive report needs Claude to run code. In the Claude **desktop app**, open the **Code** tab and run reviews there. In plain chat you'll get the report in the conversation instead.

### [VERIFY]

Call the recorder's **list meetings** tool for the **last 14 days**: metadata only, no transcripts, first page.

- Meetings come back → "**{Recorder}'s connected.** That was the hard part." → Step 2.
- Tools not available yet → Path A: have them type `/mcp` and pick **Reconnect** on `plugin:sales-call-review:{recorder}` (or `/reload-plugins`). Path B: start a new chat.
- Auth error → "The sign-in didn't stick. Let's do it once more." Repeat Step 1 (Path A: `/mcp` → the connector → **Clear authentication** if offered, then **Authenticate** again; or use the terminal-window fallback).
- Zero meetings → try 30 days. Still none → "I'm connected but see no meetings. Is this the {Recorder} account that records your sales calls?"

---

## STEP 2: Check whose calls I can see

Group the meetings by who recorded them (Fathom: `recorded_by`; Fireflies: organizer) and show it:

```
Last 14 days, I can see 23 meetings recorded by:
- you (alex@company.com): 6
- marcus@company.com: 9
- dev@company.com: 8
```

If `SCOPE = me`, or everyone they expect is there → Step 3.

**If teammates are missing**, explain: "I can only see calls your {Recorder} account is allowed to see. Here's how to fix that."

**Fathom:**
1. Put your closers on one team in Fathom (for example **Sales**), with their sales calls shared to it.
2. Or have a Fathom **Admin** given **view access to all shared calls**, and connect with that Admin's account.
3. **Private** calls can't be included. Ask closers to share sales calls.
Can't find the setting? Fathom's help center → search "share calls with team".

**Fireflies:** by default everyone in the same Fireflies workspace can see each other's meetings (privacy "Teammates & anyone with link"). So a missing closer usually means one of two things:
1. **They're not in your Fireflies workspace.** Invite them to the same team in Fireflies.
2. **They changed their privacy.** Have them open **Settings → Personal → Recording & Privacy → Privacy & Access** in Fireflies and pick **Teammates & anyone with link** (or **Only participants & teammates**). When asked, choose to apply it to **all meetings**, not just future ones.
Meetings set to **Only me** stay private, even from admins.

[VERIFY] Re-run the 14-day list. Every closer they expect appears.

---

## STEP 3: Which meetings are sales calls

Explain: "So I never grade internal meetings or coaching calls, tell me what your sales calls look like."

Show 8–10 meeting titles from the list and ask which are sales calls and whether there's a naming pattern (e.g. "Strategy Call") or a meeting type.

Record the rule, e.g. `title contains "Strategy Call" or "Discovery"; external attendee; 15+ min`.

[VERIFY] Apply it to the 14-day list and show the count per closer: "Does that look right?"

Save it:
- **Path A:** write `sales-call-review.json` in the working folder: `{"recorder":"fathom","scope":"team","closers":["Marcus Lee","Dev Patel"],"sales_call_rule":"...","set_up":"YYYY-MM-DD"}`. Every review reads it.
- **Path B:** give them this card to keep (pin the chat, or paste it into a review if their call names change):

```
Sales Call Review setup
Recorder: Fathom · Scope: team (Marcus, Dev, Ana)
Sales calls: title contains "Strategy Call" or "Discovery"; external attendee; 15+ min
```

---

## STEP 4: Run your first review

Say:

> "**You're set up.** 🎉
>
> Let's run your first review: every sales call from **last week**, graded. You'll get an **interactive report** that opens in your browser: each closer's calls in a list you can scroll and click into, then their patterns across all of those calls (what to work on, the objections they lose to, the mistakes that cost deals, exact quotes and what to say instead).
>
> Want me to run it now?"

If yes → follow the **review-calls** skill for the last 7 days, using the saved setup.

If not now → "Any time, just type **'Review last week's sales calls'**."

---

## YOUR WEEKLY ROUTINE (say this after the first review)

- **Every Monday:** "Review last week's sales calls." A new report each time.
- **Before a one-on-one:** "Coach Marcus on his last 30 days." You get his page.
- **One call:** paste a transcript and say "grade this call."
- **Dollar figures:** when I ask, paste each deal's result (closed or lost, cash, paid in full or plan). The report then ranks closers by **cash per call**, and the top of that list should get the most calls.

<sub>Built by @bingobuildsai</sub>
