# Pulling sales calls from Fathom

Fathom's official connector is at `https://api.fathom.ai/mcp`. Tool names can change, so pick tools by what they do: one **lists meetings**, one **gets a transcript** for a recording, and others list teams and team members.

## Which calls this account can see

- Calls the signed-in user recorded, plus calls shared with them or their team.
- An Admin can be granted **view access to all shared calls**, which makes every shared call across teams visible.
- **Private calls** (not shared) are visible only to the person who recorded them. They will never show up here.

## Listing meetings (cheap: no transcripts)

Use the list-meetings tool with these filters when the tool exposes them:

| Filter | Use |
| --- | --- |
| `created_after` / `created_before` | The review's date range, as ISO timestamps, e.g. `2026-10-01T00:00:00Z`. |
| `calendar_invitees_domains_type` = `one_or_more_external` | Keeps calls with someone outside the company, which drops internal meetings. |
| `teams[]` | e.g. `Sales`, if the closers are on a Fathom team. |
| `recorded_by[]` | One closer's email, for a single-closer review. |
| `meeting_type` | If the org uses meeting types like "Sales call". |
| `cursor` | Pagination. **Keep requesting the next page until there is no cursor.** |

Do **not** ask for transcripts or summaries in the list call. Get each transcript separately, only for calls you're going to grade.

Each meeting includes a title, start and end times (for duration), who recorded it, invitees, and a `recording_id`. Use the `recording_id` with the get-transcript tool.

## Spotting sales calls from the list

Decide this yourself; never ask the user which meetings are sales calls. Treat a meeting as a sales call if all of these hold:
- At least one invitee outside the company.
- 15 minutes or longer.
- The title doesn't clearly mark it as something else: client coaching, onboarding, kickoff, check-in, support, interview, podcast, internal, standup or team meeting.

Lean toward including: an external 15+ minute call with a vague title ("Zoom meeting", a person's name) counts. Drop internal meetings, the non-sales calls above, calls under 15 minutes (usually no-shows), and duplicates (same start time and attendees). Say how many you skipped and why in one line.

## Rep and lead in the transcript

The rep is the person who recorded the call (or the team member on it). The lead is the external invitee. If speakers are labelled by name, match those names.

## When teammates' calls are missing

If every call comes from the signed-in user, tell them:

> "I can only see calls you recorded or that were shared with you. To review the whole team in Fathom, either (1) put your closers on a Sales team and have their calls shared to it, or (2) have a Fathom Admin turn on view access to all shared calls. Calls a closer keeps private can't be included."
