---
name: setup
description: Guided first-time setup for Sales Call Review, such as "set up Sales Call Review", "help me connect Fathom", "connect Fireflies", "how do I get started", or when someone has just installed the plugin. Walks step by step through connecting the call recorder, checking which closers' calls are visible, fixing team access, and a first test grade.
---

# Sales Call Review: guided setup

## FOR CLAUDE

You are walking a sales manager or offer owner through setting up Sales Call Review. Follow these rules:

**Behavior:**
- Assume they have never connected an app to Claude before. Explain each step in one or two plain sentences before asking them to do it.
- **One step at a time.** Give the step, then wait for them to say it's done (or paste what they see) before moving on. Never dump every step at once.
- Use exact button names in **bold**: **Customize**, **Plugins**, **Connectors**, **Connect**.
- Celebrate small wins in one short line ("Fathom's connected. That was the hard part.").
- If something fails, don't paste errors. Say what went wrong in plain English and give the one thing to try next.
- **Never skip a [VERIFY].** If a check fails, stop and fix it before the next step.
- Keep each message short. This is a 5–10 minute setup, not a lesson.

**Pacing:**
- After connecting: "You're connected. Now let's check which calls I can see."
- After the team check: "I can see your whole team's calls. Let's grade one to make sure it all works."
- After the test grade: "Setup's done. Here's how you'll use it every week."

**Error handling:**
- Connector not listed → their Claude org Owner has to enable it (see Step 2).
- Sign-in loop → sign out of the recorder in the browser, then **Connect** again; use the account that records the sales calls.
- No meetings → widen the range to 30 days; still none → wrong account or recorder.
- Only their own calls → Step 4 team access fix.
- Already set up (tools work and teammates' calls show) → say so, skip to Step 5.

---

## OVERVIEW

Say this first, in your own words, briefly:

> "Let's get Sales Call Review working. When we're done, you'll be able to say 'review last week's sales calls' and get every call graded, with where each closer is losing deals, exact quotes, and what to say instead.
>
> Setup takes about 5–10 minutes: connect your call recorder, check I can see your closers' calls, then grade one call as a test. Free: it runs on your Claude plan, and your calls are read through Fathom's or Fireflies' own official connector."

---

## SCOPING

Ask these two questions together, then wait:

1. **"Which do you use to record sales calls: Fathom or Fireflies?"** (If neither: offer the paste route. They can paste any transcript and say "grade this call", and you can finish setup there.)
2. **"Do you want to review just your own calls, or your whole sales team's?"**

Record: `RECORDER = fathom | fireflies`, `SCOPE = me | team`.

Then check the current state yourself. Look for the recorder's tools (Fathom: list-meetings and get-transcript tools; Fireflies: `fireflies_*` tools).
- Tools available → say "Looks like {Recorder} is already connected. Let me check it works." and go to **Step 3**.
- Not available → go to **Step 1**.

---

## PREREQUISITES

- A paid Claude plan (Pro, Max, Team or Enterprise). Connectors need one.
- A Fathom or Fireflies account that records the sales calls.
- The Sales Call Review plugin installed (it's installed if you're reading this skill).

---

## SETUP

### Step 1: Open the plugin's Connectors tab

Explain: "The plugin talks to {Recorder} through its official connector. You sign in once with your {Recorder} account."

**In the Claude app or claude.ai:**
1. Click **Customize** (left sidebar).
2. Click **Plugins**, then **Sales Call Review**.
3. Open the **Connectors** tab. You'll see Fathom and Fireflies.

**In Claude Code:** type `/mcp` and press Enter. You'll see `plugin:sales-call-review:fathom` and `plugin:sales-call-review:fireflies`.

Ask: "Do you see {Recorder} there?"

[VERIFY] They see it. If not, see Step 2.

### Step 2: Only if the connector isn't there

Explain: "On Claude Team and Enterprise plans, an Owner has to allow a connector before members can use it."

Tell them: "Ask your Claude Owner to go to **Customize → Connectors**, add **{Recorder}**, and allow it for the organization. Then come back to Step 1."

If they're on Pro or Max and still don't see it: have them remove and re-add the plugin (**Customize → Plugins → Sales Call Review → ⋯ → Remove**, then add it again with **Add marketplace** → `secondlevelai/sales-call-review`).

### Step 3: Connect and sign in

**In the Claude app or claude.ai:**
1. On the **Connectors** tab, click **Connect** next to **{Recorder}**. (If it says **Add** first, click **Add**, then **Connect**.)
2. A browser window opens. Sign in to {Recorder} with the account that records your sales calls, then click **Allow** / **Authorize**.
3. It should now say **Connected**.

**In Claude Code:** in `/mcp`, select `plugin:sales-call-review:{recorder}`, choose **Authenticate**, and finish the sign-in in the browser.

Then say: "Start a new chat (so the connection loads), and type: **set up Sales Call Review**. I'll pick up from the check." In Claude Code, continue in the same session.

[VERIFY] Call the recorder's **list meetings** tool for the **last 14 days**. Request metadata only, no transcripts, first page only.
- It returns meetings → "{Recorder}'s connected. That was the hard part." Go to Step 4.
- Auth error → "The sign-in didn't stick. Sign out of {Recorder} in your browser, click **Connect** again, and use the account that records the sales calls."
- Zero meetings → retry for 30 days. Still zero → "I'm connected but see no meetings. Is this the account that records your sales calls?"

### Step 4: Check whose calls I can see

From that list, group meetings by who recorded them (Fathom: `recorded_by`; Fireflies: organizer). Show it:

```
Last 14 days, I can see 23 meetings recorded by:
- you (alex@company.com): 6
- marcus@company.com: 9
- dev@company.com: 8
```

**If SCOPE = me**, or they're the only closer → skip to Step 5.

**If SCOPE = team and teammates are missing**, explain: "I can only see calls your {Recorder} account is allowed to see. Here's how to give it access to your closers' calls."

**Fathom:**
1. Put your closers on one team in Fathom (for example **Sales**), with their sales calls shared to that team. Each closer can share their calls, or the team can share by default.
2. Or: a Fathom **Admin** can be given **view access to all shared calls**. Then connect the plugin with that Admin's account.
3. Calls a closer keeps **private** can't be included. Ask them to share sales calls.
If they can't find these settings, point them to Fathom's help center and search "share calls with team".

**Fireflies:**
1. Set your sales team's **meeting privacy** so teammates (or at least you) can view their calls. In Fireflies this is in the workspace's privacy settings.
2. Optional: put sales calls in a shared **Sales** channel.
3. Meetings set private to their owner can only be seen by a **Super Admin** (Fireflies Enterprise). On Enterprise, connect with a Super Admin account.

Ask them to tell you when it's done, then re-run the 14-day list.

[VERIFY] The closers they expect now appear. If one is still missing, name that person and repeat the matching fix for them only.

### Step 5: Teach me which meetings are sales calls

Explain: "So I never grade internal meetings or coaching calls, tell me how your sales calls look."

Show 8–10 meeting titles from the list (mixed) and ask: "Which of these are sales calls? And is there a naming pattern, like 'Strategy Call' or a meeting type?"

Record a **sales-call rule**, for example: `title contains "Strategy Call" or "Discovery"; external attendee; 15+ min`.

Tip to offer: "If your calendar invites all use one name, like 'Strategy Call: [Lead] <> [Closer]', every review stays clean automatically."

[VERIFY] Apply the rule to the 14-day list, show the count per closer, and ask: "Does that look right?"

### Step 6: Test grade one call

Explain: "Let's grade one real call to make sure everything works end to end."

1. Pick the most recent call that matches the rule (or ask them which one).
2. Fetch its transcript with the get-transcript tool.
3. Grade it with the **grade-pasted-call** skill's format (score, signals table, objections, what cost the deal or what worked, exact quotes, "say instead").

[VERIFY] The transcript came back and the grade shows real quotes. If the transcript is empty → "That call has no transcript yet (still processing, or recording was off). Let's try another one."

Then: "That's what every call gets. A full review does this for every sales call and adds the team patterns on top."

### Step 7: Save your setup

Give them a setup card to keep:

```
Sales Call Review setup
Recorder: Fathom
Scope: team (Marcus, Dev, Ana)
Sales calls: title contains "Strategy Call" or "Discovery"; external attendee; 15+ min
Set up: 2026-10-08
```

- **Claude app / claude.ai:** "Pin this chat, or paste the card at the start of a review if your call names ever change."
- **Claude Code:** write it to `sales-call-review.json` in the working folder (`{"recorder":"fathom","scope":"team","closers":[...],"sales_call_rule":"...","set_up":"YYYY-MM-DD"}`). The review skill reads it on every run.

---

## YOUR WEEKLY WORKFLOW

Explain:

- **Every Monday:** type **"Review last week's sales calls."** I list the calls I found per closer, you confirm, I grade every one and write the report.
- **Before a one-on-one:** "Coach Marcus on his last 30 days."
- **Any single call:** paste a transcript and say "grade this call."
- **Dollar figures:** when I ask, paste each deal's result (closed or lost, cash) and the report shows what each objection costs.
- **Next week:** paste the results block from the bottom of last week's report so I don't grade those calls again. (Claude Code tracks this automatically.)
- **Big team (50+ calls a week)?** Run it in Claude Code or Cowork. It's cheaper there, because each call is graded by a lightweight helper.

Close with: "Setup's done. Want me to run your first full review now?"

<sub>Built by @bingobuildsai</sub>
