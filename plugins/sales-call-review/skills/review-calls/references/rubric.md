# Call grading rubric (v1)

Use this to grade one recorded sales call for a high-ticket coaching or info-product offer (programs roughly $3,000–$25,000, usually sold on one 30–60 minute call by a closer).

The output for each call is counted across hundreds of calls to find each closer's patterns, so be consistent.

## Grading rules

- Tag only what is clearly in the transcript. If you're unsure whether something happened, leave it out.
- Copy quotes exactly from the transcript. Never invent or tidy up lines. Keep each quote under about 25 words; cut to the key phrase.
- An objection is **overcome** only if the lead clearly moved past it on this call, not if the rep merely answered it.
- **Score how well the rep ran the call** (discovery, control, objection handling, closing), not whether the lead bought. A great call can end with no sale; a sloppy call can still close.
- Coaching fixes are for the rep: specific, with the exact words to use next time. Up to three.
- **Rep** = the closer: the person who recorded the call, a member of the sales team, or the speaker who runs the call and presents the offer. **Lead** = the prospect (external person).

## Output: one compact JSON object per call

Write exactly these keys. No extra prose.

```json
{
  "id": "recorder's meeting/transcript id",
  "src": "fathom | fireflies | pasted",
  "closer": "Closer's name",
  "date": "YYYY-MM-DD",
  "min": 42,
  "out": "closed | lost | not_pitched | dq | unknown",
  "out_by": "transcript | user",
  "cash": null,
  "pay": "none",
  "score": 72,
  "sum": "One sentence: who the lead is and what happened.",
  "why": "One sentence: why they bought, or the real reason they didn't.",
  "obj": [{ "t": "price", "q": "lead's exact words", "r": "what the rep said back", "ok": false }],
  "qs": [{ "t": "payment_plan", "q": "lead's exact question" }],
  "mis": ["accepted_think"],
  "str": ["strong_discovery"],
  "sig": { "disc": 12, "pain": true, "urg": false, "dm": true, "ask": true, "bud": false, "talk": 0.58 },
  "fix": ["Specific fix with the words to say instead."]
}
```

Field meanings:

| Key | Meaning |
| --- | --- |
| `out` | `closed` = paid or committed on the call (PIF, plan, deposit). `lost` = pitched, didn't buy. `not_pitched` = showed but the offer was never presented. `dq` = disqualified. `unknown` = can't tell. |
| `out_by` | `transcript` if you inferred the outcome from the call; `user` if the user gave it. |
| `cash` | Cash collected in dollars, only if the user gave it. Otherwise `null`. |
| `pay` | How a closed deal was paid: `pif` (paid in full), `plan` (payment plan / split pay), `deposit`, `financing` (Affirm, Klarna, Splitit and similar), or `unknown` if it closed but the call doesn't say. `none` if it didn't close. |
| `score` | 0–100, how well the rep ran the call regardless of outcome. |
| `obj` | Every objection the lead raised, in order. `t` = type key below, `q` = lead's exact words, `r` = rep's reply (copied or closely paraphrased), `ok` = overcome on this call. |
| `qs` | Questions the lead asked about the offer. `t` = topic key below. |
| `mis` | Mistakes clearly visible in the transcript (keys below). |
| `str` | Strengths clearly visible in the transcript (keys below). |
| `sig.disc` | Minutes from the start of the call until the rep began pitching. |
| `sig.pain` | The lead said, in their own words, what problem they need solved. |
| `sig.urg` | The lead gave a reason to act now. |
| `sig.dm` | Everyone needed to say yes was on the call. |
| `sig.ask` | The rep directly asked the lead to buy. |
| `sig.bud` | Money or ability to invest came up before the price was given. |
| `sig.talk` | Share of the words spoken by the rep, 0 to 1. |
| `fix` | Up to three fixes for this rep, each with what to say instead. |

## Tag keys

**Objections (`obj.t`)**

| Key | Means |
| --- | --- |
| `price` | Too expensive |
| `cash` | Don't have the money right now |
| `spouse` | Need to talk to my partner |
| `think` | Need to think about it |
| `timing` | Not the right time |
| `trust` | Tried something like this before |
| `diy` | Can figure it out myself |
| `fit` | Not sure it'll work for me |
| `other` | Other |

**Questions (`qs.t`)**

| Key | Means |
| --- | --- |
| `price` | How much is it? |
| `payment_plan` | Is there a payment plan? |
| `guarantee` | Is there a guarantee? |
| `time` | How much time does it take? |
| `results` | How fast will I see results? |
| `support` | What support do I get? |
| `fit` | Is it right for someone like me? |
| `other` | Other |

**Mistakes (`mis`)**

| Key | Means |
| --- | --- |
| `no_ask` | Didn't ask for the sale |
| `skipped_discovery` | Rushed or skipped discovery |
| `talked_too_much` | Talked more than the lead |
| `pitched_early` | Pitched before finding the pain |
| `no_urgency` | Never built urgency |
| `weak_price` | Dropped price or caved on it |
| `accepted_think` | Accepted "let me think about it" |
| `no_decision_maker` | Didn't get the decision-maker on the call |
| `no_follow_up` | Ended without a booked next step |

**Strengths (`str`)**

| Key | Means |
| --- | --- |
| `strong_discovery` | Deep discovery |
| `pain_tied` | Tied the offer to their pain |
| `handled_price` | Held firm on price |
| `urgency` | Built real urgency |
| `next_steps` | Clear next steps |
| `rapport` | Strong rapport |
| `proof` | Used a relevant case study |

## Default "say this instead" lines

Use these when a mistake shows up and the call itself gives no better example. Prefer a teammate's real answer from the same review when one exists.

| Mistake | Say this instead |
| --- | --- |
| `no_ask` | "Based on everything you told me, this is exactly what you need. Do you want to get started today?" Then stop talking. |
| `skipped_discovery` | Before any pitch: "Walk me through where the business is today, where you want it in 12 months, and what's stopping you." Spend 10+ minutes here. |
| `talked_too_much` | After every point, hand it back: "How does that land for you?" Aim to talk less than half the call. |
| `pitched_early` | Don't present until they've said the problem in their own words: "So if I'm hearing you right, the real issue is…?" |
| `no_urgency` | "What happens if nothing changes in the next 6 months?" Let them put a number on waiting. |
| `weak_price` | State the price once, then ask "How does that feel?" No discounts on the first call. |
| `accepted_think` | "Totally fair. What specifically do you need to think through? Let's do it now while I'm here." |
| `no_decision_maker` | On the confirmation call: "Is there anyone else who'd weigh in on a decision like this? Let's get them on with us." |
| `no_follow_up` | Never hang up without a time: "Let's lock in Thursday at 2 to finish this. Does that work?" |
