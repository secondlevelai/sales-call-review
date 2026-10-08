#!/usr/bin/env python3
"""Exact counts for the Sales Call Review report.

Claude grades each call into one compact JSON object (see references/rubric.md).
This script does all the counting, so the numbers in the report are exact.
Standard library only.

Usage:
  aggregate.py add LEDGER FILE [FILE...]   Merge graded calls into the ledger (deduped by src+id).
  aggregate.py seen LEDGER                 Print "src:id" for every call already graded.
  aggregate.py report SOURCE [--from YYYY-MM-DD] [--to YYYY-MM-DD] [--closer NAME] [--json]
                                           SOURCE is a ledger or a file holding one call or a list of calls.
"""
import argparse
import json
import sys
from collections import OrderedDict

OBJECTIONS = OrderedDict([
    ("price", "Too expensive"), ("cash", "Don't have the money right now"),
    ("spouse", "Need to talk to my partner"), ("think", "Need to think about it"),
    ("timing", "Not the right time"), ("trust", "Tried something like this before"),
    ("diy", "Can figure it out myself"), ("fit", "Not sure it'll work for me"), ("other", "Other"),
])
QUESTIONS = OrderedDict([
    ("price", "How much is it?"), ("payment_plan", "Is there a payment plan?"),
    ("guarantee", "Is there a guarantee?"), ("time", "How much time does it take?"),
    ("results", "How fast will I see results?"), ("support", "What support do I get?"),
    ("fit", "Is it right for someone like me?"), ("other", "Other"),
])
MISTAKES = OrderedDict([
    ("no_ask", "Didn't ask for the sale"), ("skipped_discovery", "Rushed or skipped discovery"),
    ("talked_too_much", "Talked more than the lead"), ("pitched_early", "Pitched before finding the pain"),
    ("no_urgency", "Never built urgency"), ("weak_price", "Dropped price or caved on it"),
    ("accepted_think", "Accepted “let me think about it”"),
    ("no_decision_maker", "Didn't get the decision-maker on the call"),
    ("no_follow_up", "Ended without a booked next step"),
])
STRENGTHS = OrderedDict([
    ("strong_discovery", "Deep discovery"), ("pain_tied", "Tied the offer to their pain"),
    ("handled_price", "Held firm on price"), ("urgency", "Built real urgency"),
    ("next_steps", "Clear next steps"), ("rapport", "Strong rapport"), ("proof", "Used a relevant case study"),
])
PAY_TYPES = ("pif", "plan", "deposit", "financing", "none", "unknown")
PAY_LABELS = {"pif": "Paid in full", "plan": "Payment plan", "deposit": "Deposit", "financing": "Financing", "unknown": "Not said"}

SAY_INSTEAD = {
    "no_ask": "“Based on everything you told me, this is exactly what you need. Do you want to get started today?” Then stop talking.",
    "skipped_discovery": "Before any pitch: “Walk me through where the business is today, where you want it in 12 months, and what's stopping you.” Spend 10+ minutes here.",
    "talked_too_much": "After every point, hand it back: “How does that land for you?” Aim to talk less than half the call.",
    "pitched_early": "Don't present until they've said the problem in their own words: “So if I'm hearing you right, the real issue is…?”",
    "no_urgency": "“What happens if nothing changes in the next 6 months?” Let them put a number on waiting.",
    "weak_price": "State the price once, then ask “How does that feel?” No discounts on the first call.",
    "accepted_think": "“Totally fair. What specifically do you need to think through? Let's do it now while I'm here.”",
    "no_decision_maker": "On the confirmation call: “Is there anyone else who'd weigh in on a decision like this? Let's get them on with us.”",
    "no_follow_up": "Never hang up without a time: “Let's lock in Thursday at 2 to finish this. Does that work?”",
}


# ---------- loading ----------

def load_calls(path):
    with open(path, encoding="utf-8") as f:
        text = f.read().strip()
    if not text:
        return []
    data = json.loads(text)
    if isinstance(data, dict) and "calls" in data:
        data = data["calls"]
    if isinstance(data, dict):
        data = [data]
    return [normalize(c) for c in data if isinstance(c, dict)]


def normalize(c):
    """Fill defaults so a slightly incomplete grade never crashes the counts."""
    sig = c.get("sig") or {}
    return {
        "id": str(c.get("id", "")),
        "src": c.get("src", "pasted"),
        "closer": (c.get("closer") or "Unknown closer").strip(),
        "lead": (c.get("lead") or "").strip(),
        "date": c.get("date") or "",
        "min": c.get("min"),
        "out": c.get("out", "unknown"),
        "out_by": c.get("out_by", "transcript"),
        "cash": c.get("cash"),
        "pay": c.get("pay") if c.get("pay") in PAY_TYPES else ("unknown" if c.get("out") == "closed" else "none"),
        "score": c.get("score"),
        "sum": c.get("sum", ""),
        "why": c.get("why", ""),
        "obj": [o for o in (c.get("obj") or []) if isinstance(o, dict)],
        "qs": [q for q in (c.get("qs") or []) if isinstance(q, dict)],
        "mis": [m for m in (c.get("mis") or []) if m in MISTAKES],
        "str": [s for s in (c.get("str") or []) if s in STRENGTHS],
        "sig": {
            "disc": sig.get("disc"), "pain": sig.get("pain"), "urg": sig.get("urg"),
            "dm": sig.get("dm"), "ask": sig.get("ask"), "bud": sig.get("bud"), "talk": sig.get("talk"),
        },
        "fix": c.get("fix") or [],
    }


def key(c):
    return f"{c['src']}:{c['id']}"


def read_ledger(path):
    try:
        return load_calls(path)
    except FileNotFoundError:
        return []


def write_ledger(path, calls):
    calls = sorted(calls, key=lambda c: (c["date"], c["closer"], c["id"]))
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"version": 1, "calls": calls}, f, ensure_ascii=False, indent=1)


# ---------- math ----------

def rate(n, d):
    return n / d if d else None


def avg(xs):
    xs = [x for x in xs if isinstance(x, (int, float))]
    return sum(xs) / len(xs) if xs else None


def closed(c):
    return c["out"] == "closed"


def insights(rows, team_rows=None):
    team_rows = team_rows if team_rows is not None else rows
    won = [r for r in rows if closed(r)]
    lost = [r for r in rows if not closed(r)]
    all_obj = [o for r in rows for o in r["obj"]]
    cash_known = [r["cash"] for r in won if isinstance(r["cash"], (int, float))]
    avg_deal = avg(cash_known)

    objections = []
    for t, label in OBJECTIONS.items():
        calls = [r for r in rows if any(o.get("t") == t for o in r["obj"])]
        if not calls:
            continue
        raised = [o for o in all_obj if o.get("t") == t]
        lost_with = [r for r in calls if not closed(r)]
        objections.append({
            "type": t, "label": label, "calls": len(calls), "share": rate(len(calls), len(rows)),
            "overcome": rate(sum(1 for o in raised if o.get("ok")), len(raised)),
            "close_rate": rate(sum(1 for r in calls if closed(r)), len(calls)),
            "lost_deals": len(lost_with),
            "est_value_lost": (len(lost_with) * avg_deal) if avg_deal else None,
            "best": best_answer(team_rows, t),
        })
    objections.sort(key=lambda o: -o["calls"])

    def with_without(has):
        yes = [r for r in rows if has(r)]
        no = [r for r in rows if not has(r)]
        return {
            "count": len(yes), "share": rate(len(yes), len(rows)),
            "lost_share": rate(sum(1 for r in yes if not closed(r)), len(lost)),
            "won_share": rate(sum(1 for r in yes if closed(r)), len(won)),
            "close_with": rate(sum(1 for r in yes if closed(r)), len(yes)),
            "close_without": rate(sum(1 for r in no if closed(r)), len(no)),
        }

    def cost(m):
        return (m["lost_share"] or 0) - (m["won_share"] or 0)

    mistakes = []
    for t, label in MISTAKES.items():
        m = {"type": t, "label": label, **with_without(lambda r, t=t: t in r["mis"])}
        if m["count"]:
            m["cost"] = cost(m)
            mistakes.append(m)
    # Biggest cost first: how much more often it shows up on lost calls than won ones.
    mistakes.sort(key=lambda m: (-m["cost"], -m["count"]))

    strengths = []
    for t, label in STRENGTHS.items():
        s = {"type": t, "label": label, **with_without(lambda r, t=t: t in r["str"])}
        if s["count"]:
            strengths.append(s)
    strengths.sort(key=lambda s: -s["count"])

    questions = []
    for t, label in QUESTIONS.items():
        asked = [q for r in rows for q in r["qs"] if q.get("t") == t]
        if asked:
            questions.append({"topic": t, "label": label, "count": len(asked), "example": asked[0].get("q")})
    questions.sort(key=lambda q: -q["count"])

    def share(lst, f):
        vals = [f(r) for r in lst if f(r) is not None]
        return rate(sum(1 for v in vals if v), len(vals))

    def mean(lst, f):
        return avg([f(r) for r in lst])

    buy_vs_not = [
        ("Lead said their problem in their own words", "pct", share(won, lambda r: r["sig"]["pain"]), share(lost, lambda r: r["sig"]["pain"])),
        ("Lead had a reason to act now", "pct", share(won, lambda r: r["sig"]["urg"]), share(lost, lambda r: r["sig"]["urg"])),
        ("Decision-maker on the call", "pct", share(won, lambda r: r["sig"]["dm"]), share(lost, lambda r: r["sig"]["dm"])),
        ("Money discussed before the price", "pct", share(won, lambda r: r["sig"]["bud"]), share(lost, lambda r: r["sig"]["bud"])),
        ("Rep asked for the sale", "pct", share(won, lambda r: r["sig"]["ask"]), share(lost, lambda r: r["sig"]["ask"])),
        ("Minutes of discovery before the pitch", "min", mean(won, lambda r: r["sig"]["disc"]), mean(lost, lambda r: r["sig"]["disc"])),
        ("Rep's share of the talking", "pct", mean(won, lambda r: r["sig"]["talk"]), mean(lost, lambda r: r["sig"]["talk"])),
        ("Objections raised per call", "num", mean(won, lambda r: len(r["obj"])), mean(lost, lambda r: len(r["obj"]))),
    ]

    pay_known = [r for r in won if r["pay"] in ("pif", "plan", "deposit", "financing")]
    pay_mix = {k: sum(1 for r in won if r["pay"] == k) for k in ("pif", "plan", "deposit", "financing", "unknown")}
    cash_rows = [r for r in rows if r["out_by"] == "user"]
    return {
        "calls": len(rows),
        "closed": len(won),
        "lost": sum(1 for r in rows if r["out"] == "lost"),
        "not_pitched": sum(1 for r in rows if r["out"] == "not_pitched"),
        "pif_rate": rate(sum(1 for r in pay_known if r["pay"] == "pif"), len(pay_known)),
        "pay_mix": pay_mix,
        "cash_per_call": (sum(cash_known) / len(cash_rows)) if cash_known and cash_rows else None,
        "avg_deal": avg_deal,
        "avg_discovery": avg([r["sig"]["disc"] for r in rows]),
        "close_rate": rate(len(won), len(rows)),
        "outcome_from_user": sum(1 for r in rows if r["out_by"] == "user"),
        "cash": sum(cash_known) if cash_known else None,
        "avg_score": avg([r["score"] for r in rows]),
        "avg_minutes": avg([r["min"] for r in rows]),
        "talk_ratio": avg([r["sig"]["talk"] for r in rows]),
        "ask_rate": share(rows, lambda r: r["sig"]["ask"]),
        "overcome_rate": rate(sum(1 for o in all_obj if o.get("ok")), len(all_obj)),
        "objections": objections,
        "mistakes": mistakes,
        "strengths": strengths,
        "questions": questions,
        "buy_vs_not": [{"label": l, "kind": k, "bought": b, "didnt": d} for l, k, b, d in buy_vs_not],
    }


def best_answer(rows, t):
    """The team's best real answer to an objection: overcome, deal closed, best-run call."""
    best = None
    for r in rows:
        if not closed(r):
            continue
        for o in r["obj"]:
            if o.get("t") == t and o.get("ok") and (best is None or (r["score"] or 0) > best["score"]):
                best = {"quote": o.get("q"), "response": o.get("r"), "closer": r["closer"], "score": r["score"] or 0}
    return best


def closer_table(rows):
    out = []
    for name in sorted({r["closer"] for r in rows}):
        mine = [r for r in rows if r["closer"] == name]
        i = insights(mine)
        weakest = sorted([o for o in i["objections"] if o["calls"] >= 2 and (o["overcome"] if o["overcome"] is not None else 1) < 0.6], key=lambda o: o["overcome"] if o["overcome"] is not None else 1)
        out.append({
            "closer": name, "calls": i["calls"], "close_rate": i["close_rate"], "avg_score": i["avg_score"],
            "ask_rate": i["ask_rate"], "talk_ratio": i["talk_ratio"], "overcome_rate": i["overcome_rate"],
            "pif_rate": i["pif_rate"], "cash": i["cash"], "cash_per_call": i["cash_per_call"], "avg_discovery": i["avg_discovery"],
            "top_mistake": i["mistakes"][0]["label"] if i["mistakes"] and i["mistakes"][0]["cost"] > 0 else None,
            "weakest_objection": weakest[0]["label"] if weakest else None,
            "insights": i,
        })
    return out


# ---------- formatting ----------

DASH = "\u2014"


def pct(x):
    return "—" if x is None else f"{round(x * 100)}%"


def num(x, d=0):
    return "—" if x is None else (f"{x:.{d}f}" if d else str(round(x)))


def money(x):
    return "—" if x is None else f"${round(x):,}"


def fmt(kind, x):
    return pct(x) if kind == "pct" else (f"{num(x, 1)} min" if kind == "min" and x is not None else num(x, 1))


def markdown(rows, closers, team, dates, scope="Team"):
    L = []
    first, last = dates
    L.append(f"_Counts: {team['calls']} graded calls, {first or '?'} to {last or '?'}. "
             f"Outcomes from you on {team['outcome_from_user']}, from the transcript on {team['calls'] - team['outcome_from_user']}._\n")

    L.append(f"### {scope}")
    L.append("| Calls | Closed | Close rate | Avg call score | Rep talk share | Asked for the sale | Objections overcome |")
    L.append("| --- | --- | --- | --- | --- | --- | --- |")
    L.append(f"| {team['calls']} | {team['closed']} | {pct(team['close_rate'])} | {num(team['avg_score'])} | {pct(team['talk_ratio'])} | {pct(team['ask_rate'])} | {pct(team['overcome_rate'])} |")
    if team["cash"] is not None:
        L.append(f"\nCash collected (from your results): {money(team['cash'])}")

    L.append("\n### Closers")
    L.append("| Closer | Calls | Close rate | Avg score | Asked for sale | Talk share | Biggest leak | Weakest objection |")
    L.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for c in sorted(closers, key=lambda c: -(c["avg_score"] or 0)):
        L.append(f"| {c['closer']} | {c['calls']} | {pct(c['close_rate'])} | {num(c['avg_score'])} | {pct(c['ask_rate'])} | {pct(c['talk_ratio'])} | {c['top_mistake'] or '—'} | {c['weakest_objection'] or '—'} |")

    if team["objections"]:
        L.append("\n### Objections")
        L.append("| Objection | Calls | Overcome | Close rate when it comes up | Lost deals | Est. value lost | Best answer on the team |")
        L.append("| --- | --- | --- | --- | --- | --- | --- |")
        for o in team["objections"]:
            b = o["best"]
            best = f"{b['closer']}: “{b['response']}”" if b and b.get("response") else "—"
            L.append(f"| {o['label']} | {o['calls']} ({pct(o['share'])}) | {pct(o['overcome'])} | {pct(o['close_rate'])} | {o['lost_deals']} | {money(o['est_value_lost'])} | {best} |")
        if all(o["est_value_lost"] is None for o in team["objections"]):
            L.append("\n_Est. value lost needs cash amounts for closed deals. Paste results to fill it in._")

    leaks = [m for m in team["mistakes"] if m["cost"] > 0]
    if leaks:
        L.append("\n### Mistakes that cost deals")
        L.append("| Mistake | On lost calls | On closed calls | Close rate with / without | Say this instead |")
        L.append("| --- | --- | --- | --- | --- |")
        for m in leaks[:6]:
            L.append(f"| {m['label']} | {pct(m['lost_share'])} | {pct(m['won_share'])} | {pct(m['close_with'])} / {pct(m['close_without'])} | {SAY_INSTEAD[m['type']]} |")

    L.append("\n### What the buyers had that the others didn't")
    L.append("| Signal | Bought | Didn't buy |")
    L.append("| --- | --- | --- |")
    for s in team["buy_vs_not"]:
        L.append(f"| {s['label']} | {fmt(s['kind'], s['bought'])} | {fmt(s['kind'], s['didnt'])} |")

    if team["questions"]:
        L.append("\n### Questions leads ask most")
        for q in team["questions"][:5]:
            L.append(f"- {q['label']}: {q['count']}× (e.g. “{q['example']}”)")
    return "\n".join(L)


# ---------- commands ----------

def cmd_add(a):
    ledger = {key(c): c for c in read_ledger(a.ledger)}
    before = len(ledger)
    added = updated = 0
    for f in a.files:
        for c in load_calls(f):
            if not c["id"]:
                print(f"skipped a call with no id in {f}", file=sys.stderr)
                continue
            if key(c) in ledger:
                updated += 1
            else:
                added += 1
            ledger[key(c)] = c
    write_ledger(a.ledger, list(ledger.values()))
    print(f"ledger: {before} before, {added} added, {updated} updated, {len(ledger)} total")


def cmd_seen(a):
    for c in read_ledger(a.ledger):
        print(key(c))


def cmd_report(a):
    rows = load_calls(a.source)
    if a.date_from:
        rows = [r for r in rows if r["date"] >= a.date_from]
    if a.date_to:
        rows = [r for r in rows if r["date"] <= a.date_to]
    team_rows = rows
    if a.closer:
        rows = [r for r in rows if r["closer"].lower() == a.closer.lower()]
    if not rows:
        print("No graded calls match.", file=sys.stderr)
        sys.exit(1)
    team = insights(rows, team_rows)
    closers = closer_table(rows)
    dates = sorted(r["date"] for r in rows if r["date"])
    span = (dates[0] if dates else None, dates[-1] if dates else None)
    if a.json:
        for c in closers:
            c.pop("insights", None)
        json.dump({"team": team, "closers": closers, "dates": span}, sys.stdout, ensure_ascii=False, indent=1, default=str)
        print()
    else:
        print(markdown(rows, closers, team, span, scope=rows[0]["closer"] if a.closer else "Team"))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("add")
    s.add_argument("ledger")
    s.add_argument("files", nargs="+")
    s.set_defaults(fn=cmd_add)
    s = sub.add_parser("seen")
    s.add_argument("ledger")
    s.set_defaults(fn=cmd_seen)
    s = sub.add_parser("report")
    s.add_argument("source")
    s.add_argument("--from", dest="date_from")
    s.add_argument("--to", dest="date_to")
    s.add_argument("--closer")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_report)
    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
