# Sales Call Review

**A free Claude plugin that grades every sales call your team recorded in Fathom or Fireflies, and shows where each closer is losing deals.**

You get the objections each closer doesn't get past, the mistakes that show up on lost calls but not on closed ones, exact quotes from the calls, your team's best real answers, and the words to say instead.

> "Leads who say 'let me think about it' close 9% of the time. It came up on 14 of 41 calls, and two closers accept it and end the call."
> That's the kind of headline you get, from your own calls.

<!-- 90-second setup video: replace with your Loom link -->
**[Watch the 90-second setup](LOOM_LINK_HERE)**

---

## Set it up in 3 steps

You need a paid Claude plan (Pro, Max, Team or Enterprise) and Fathom or Fireflies recording your sales calls.

### 1. Add the plugin (one paste)

**In the Claude app or claude.ai:**

1. Open **Customize → Plugins**.
2. Click **Add → Add marketplace**.
3. Paste: **`bingobuildsai/sales-call-review`** and click **Add**.
4. Install **Sales Call Review**.

![Add marketplace](docs/images/add-marketplace.png)

**In Claude Code:** paste this repo's link into a session and say **"install this plugin."** (Or run the two commands in [Instructions for Claude](#instructions-for-claude).)

### 2. Connect your call recorder

Open the plugin's **Connectors** tab, click **Connect** on **Fathom** or **Fireflies**, and sign in with your account.

To review your whole team (not just your own calls), see [Fathom setup](docs/setup-fathom.md) or [Fireflies setup](docs/setup-fireflies.md). It takes a minute.

> On a Claude Team or Enterprise plan, an Owner may need to enable the Fathom or Fireflies connector for your organization first.

### 3. Run it

Type:

> **Review last week's sales calls.**

Claude lists the sales calls it found, grouped by closer, and asks you to confirm. Then it grades every one and writes the report.

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

If a user pastes this repository's link and asks you to install it, and you're running in Claude Code with a shell, run:

```bash
claude plugin marketplace add bingobuildsai/sales-call-review
claude plugin install sales-call-review@bingobuildsai
```

Then tell the user to run `/reload-plugins` (or restart Claude Code), connect Fathom or Fireflies with `/mcp`, and ask "Review last week's sales calls."

If you're in the Claude app or claude.ai chat, you can't install plugins from a message. Tell the user to open **Customize → Plugins → Add → Add marketplace** and paste `bingobuildsai/sales-call-review`.

---

⭐ If it helped, star the repo. Built by **@bingobuildsai**. MIT license.
