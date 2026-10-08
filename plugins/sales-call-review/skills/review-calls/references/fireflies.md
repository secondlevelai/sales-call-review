# Pulling sales calls from Fireflies

Fireflies' official connector is at `https://api.fireflies.ai/mcp`. Pick tools by what they do. Current names include `fireflies_get_transcripts` (list meetings with filters), `fireflies_get_transcript` (one full transcript by ID), `fireflies_list_channels`, and `fireflies_get_summary`.

## Which calls this account can see

- Meetings the signed-in user organized, plus teammates' meetings the workspace's privacy settings let them view.
- `mine` is an option, not the default. Leave it off for team reviews.
- Meetings set private to their owner are visible only to a **Super Admin** (Fireflies Enterprise).

## Listing meetings (cheap: no transcripts)

Use the list tool (`fireflies_get_transcripts`). It returns IDs, titles, dates, participants and summaries, not the full transcript.

| Parameter | Use |
| --- | --- |
| `fromDate` / `toDate` | The review's date range, `YYYY-MM-DD`. |
| `limit` | Max 50 per request. |
| `skip` | Pagination. **Request again with `skip` + 50 until fewer than 50 come back.** |
| `organizers` | One or more closers' emails, for a single-closer or sales-team review. |
| `channelId` | A "Sales" channel/folder, if the team uses one (find it with the list-channels tool). |
| `mine` | Leave unset for team reviews. |
| `format` | Leave the default (`toon`, the most compact). |

Get each full transcript separately with `fireflies_get_transcript`, only for calls you're going to grade. Its lines look like `[00:05 - 00:08] Speaker: text`.

## Spotting sales calls from the list

Keep a meeting if all of these hold:
- At least one participant outside the company's email domain.
- 15 minutes or longer.
- The title looks like a sales or strategy call ("strategy call", "discovery", "consult", "application call", the offer name, or "[Lead name] <> [Closer]"), or the user said all external calls are sales calls.

Drop internal meetings, client coaching/onboarding calls, calls under 15 minutes, and duplicates.

## Rep and lead in the transcript

The rep is the organizer (the closer). The lead is the external participant. Match speaker names to the organizer and participants.

## When teammates' calls are missing

If every call is organized by the signed-in user, tell them:

> "I can only see meetings your Fireflies privacy settings let you view. To review the whole team, set the sales team's meeting privacy so teammates can view calls (or put sales calls in a shared Sales channel). Meetings set private to their owner need a Super Admin account, which is on Fireflies Enterprise."
