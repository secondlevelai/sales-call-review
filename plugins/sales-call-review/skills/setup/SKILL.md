---
name: setup
description: Guided first-time setup for Sales Call Review, such as "set up Sales Call Review", "help me connect Fathom", "connect Fireflies", "how do I get started", or right after the plugin is installed. Walks step by step through connecting Fathom or Fireflies (Claude app, desktop app, VS Code, Cursor or terminal), checking which closers' calls are visible, and running the first review with its interactive report.
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

Explain: "I'll open the {Recorder} sign-in page in your browser. Sign in with the account that records your sales calls and click **Allow**. That's all you need to do."

1. Run this yourself, **in the background** (it waits until they finish signing in):

```bash
claude mcp login plugin:sales-call-review:{recorder}
```

2. Tell them: "A browser tab just opened. Sign in to {Recorder} and click **Allow** / **Authorize**, then come back here and say **done**."
3. When they say done (or the command finishes), confirm:

```bash
claude mcp list 2>&1 | grep "sales-call-review:{recorder}"
```

It should say **Connected** (not "Needs authentication").

4. Load the connection into this conversation: tell them **type `/mcp`, choose `plugin:sales-call-review:{recorder}`, and pick Reconnect** if it isn't already shown as connected. (Or type `/reload-plugins`.)

**If the browser didn't open,** or they'd rather do it by hand:
- **Desktop app (Code tab), VS Code or Cursor:** in the Claude message box, type `/mcp` and press Enter.
- **Terminal:** type `/mcp` at the Claude prompt.
- Then choose **`plugin:sales-call-review:{recorder}`** → **Authenticate**, and sign in in the browser.

**If `claude` isn't found** (some editor setups don't put it on the PATH): use the `/mcp` route above.

### Path B: Claude app or claude.ai chat

Explain: "The plugin reads your calls through {Recorder}'s official connector. You sign in once."

1. Click **Customize** in the left sidebar.
2. Click **Plugins**, then **Sales Call Review**, then the **Connectors** tab.
3. Next to **{Recorder}**, click **Connect** (if it says **Add**, click that first).
4. Sign in to {Recorder} and click **Allow**. It should say **Connected**.
5. **Start a new chat** (so the connection loads) and type **"set up Sales Call Review"**. I'll pick up from the check.

**Not on the Connectors tab?** On Claude **Team or Enterprise** plans, an Owner must allow the connector first: they go to **Customize → Connectors**, add {Recorder}, and allow it. Then try again.

> Tip for Path B: the interactive report and PDFs need Claude to run code. In the Claude **desktop app**, open the **Code** tab and run reviews there. In plain chat you'll get the report in the conversation instead.

### [VERIFY]

Call the recorder's **list meetings** tool for the **last 14 days**: metadata only, no transcripts, first page.

- Meetings come back → "**{Recorder}'s connected.** That was the hard part." → Step 2.
- Tools not available yet → Path A: have them do the `/mcp` → **Reconnect** step. Path B: start a new chat.
- Auth error → "The sign-in didn't stick. Let's do it once more." Repeat Step 1 (Path A: `claude mcp logout plugin:sales-call-review:{recorder}` first, then login again).
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

**Fireflies:**
1. Set the sales team's **meeting privacy** so you can view their calls (workspace privacy settings).
2. Optional: put sales calls in a shared **Sales** channel.
3. Meetings private to their owner need a **Super Admin** account (Fireflies Enterprise).

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
> Let's run your first review: every sales call from **last week**, graded. You'll get an **interactive report** that opens in your browser. Click between the team overview and each closer to see their stats, the objections they lose to, the mistakes that cost deals, exact quotes, and what to say instead. You also get a **PDF for each closer** that you can send them.
>
> Want me to run it now?"

If yes → follow the **review-calls** skill for the last 7 days, using the saved setup.

If not now → "Any time, just type **'Review last week's sales calls'**."

---

## YOUR WEEKLY ROUTINE (say this after the first review)

- **Every Monday:** "Review last week's sales calls." New report, new PDFs.
- **Before a one-on-one:** "Coach Marcus on his last 30 days." You get his page and PDF.
- **One call:** paste a transcript and say "grade this call."
- **Dollar figures:** when I ask, paste each deal's result (closed or lost, cash, paid in full or plan). The report then ranks closers by **cash per call**, and the top of that list should get the most calls.

<sub>Built by @bingobuildsai</sub>
