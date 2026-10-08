# Troubleshooting

| Problem | Fix |
| --- | --- |
| **I don't see Fathom or Fireflies on the Connectors tab** | On Claude Team or Enterprise, an Owner has to enable the connector for your organization first. Ask them to add it under Customize → Connectors. |
| **Sign-in keeps looping** | Sign out of Fathom or Fireflies in your browser, then click Connect again. If you use several Google accounts, sign in with the one tied to your recorder. |
| **"No meetings found"** | Check the date range ("review October 1–15") and that you connected the right recorder. |
| **"No sales calls found"** but you had calls | Tell Claude which ones are sales calls, or "all external calls are sales calls." Naming calls consistently ("Strategy Call: [Lead] <> [Closer]") fixes this for good. |
| **Only my own calls show up** | Your recorder isn't sharing teammates' calls with you. See [Fathom setup](setup-fathom.md) or [Fireflies setup](setup-fireflies.md). |
| **The review stopped partway** | Big weeks continue across messages. Reply "continue." For 50+ calls a week, run it in Claude Code or Cowork. |
| **Close rates look wrong** | Outcomes are read from the calls unless you give them. When Claude asks, paste each deal's result (closed or lost, cash). |
| **It graded a call twice** | In chat, paste the results block from the last report into your next review. In Claude Code, keep running it in the same folder so `graded-calls.json` is reused. |
| **Claude Code: plugin not found after install** | Run `/reload-plugins` or restart Claude Code. |

Still stuck? Open an issue on this repo.
