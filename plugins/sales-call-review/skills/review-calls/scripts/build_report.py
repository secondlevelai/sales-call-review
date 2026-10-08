#!/usr/bin/env python3
"""Build the Sales Call Review report: one interactive HTML file + PDFs.

Every number comes from aggregate.py. Claude only supplies the coaching words
(optional coaching.json); without it, coaching is written from the numbers.
Standard library only. PDFs are printed by a local Chrome/Edge/Chromium if one
is installed; otherwise the HTML's "Save PDF" button does the same job.

Usage:
  build_report.py SOURCE [--from YYYY-MM-DD] [--to YYYY-MM-DD]
                  [--coaching coaching.json] [--confirmed N] [--recorder fathom|fireflies]
                  [--out DIR] [--no-pdf] [--open]

SOURCE is a ledger (graded-calls.json) or a file holding a list of graded calls.
Writes DIR/report.html and DIR/pdf/Team.pdf + DIR/pdf/<Closer>.pdf.
Default DIR: ./sales-call-reports/<from>_to_<to>/
"""
import argparse
import datetime as dt
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import urllib.parse
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import aggregate as ag  # noqa: E402

TEMPLATE = HERE.parent / "assets" / "report-template.html"


# ---------- coaching written from the numbers (fallback) ----------

def pct(x):
    return "—" if x is None else f"{round(x * 100)}%"


def example_quote(rows, objection_type):
    for r in rows:
        for o in r["obj"]:
            if o.get("t") == objection_type and not o.get("ok") and o.get("q"):
                return {"quote": o["q"], "lead_reply": o.get("r"), "date": r["date"], "id": r["id"]}
    return None


def rule_coaching(i, rows, who):
    leaks = [m for m in i["mistakes"] if m.get("cost", 0) > 0][:2]
    weakest = sorted([o for o in i["objections"] if o["calls"] >= 2 and (o["overcome"] if o["overcome"] is not None else 1) < 0.6],
                     key=lambda o: o["overcome"] if o["overcome"] is not None else 1)
    fixes = []
    for m in leaks:
        fixes.append({
            "title": m["label"],
            "why": f"On {pct(m['lost_share'])} of lost calls vs {pct(m['won_share'])} of calls that closed.",
            "say_instead": ag.SAY_INSTEAD[m["type"]],
            "quote": None,
        })
    if weakest:
        w = weakest[0]
        best = w.get("best")
        ex = example_quote(rows, w["type"])
        fixes.append({
            "title": f"“{w['label']}”",
            "why": f"Comes up on {pct(w['share'])} of calls and is only overcome {pct(w['overcome'])} of the time.",
            "say_instead": (f"What worked for {best['closer']}: “{best['response']}”" if best and best.get("response")
                            else "Ask what's behind it before answering: “What part of it are you unsure about?”"),
            "quote": ex["quote"] if ex else None,
        })
    m0 = leaks[0] if leaks else None
    if i["calls"] < 3:
        headline = f"{i['calls']} graded call{'s' if i['calls'] != 1 else ''}: too few to call anything a pattern yet."
    elif m0:
        headline = (f"Biggest leak: {m0['label'][0].lower() + m0['label'][1:]}. "
                    f"It shows up on {pct(m0['lost_share'])} of lost calls and {pct(m0['won_share'])} of the ones that closed.")
    else:
        headline = f"Close rate {pct(i['close_rate'])} across {i['calls']} graded calls, with no repeated mistakes."
    keep = [f"{s['label']}: on {pct(s['share'])} of calls, closing {pct(s['close_with'])} when it happens."
            for s in i["strengths"] if (s["close_with"] or 0) > (s["close_without"] or 0)][:2]
    return {"headline": headline, "fixes": fixes, "keep_doing": keep, "writer": "rules"}


def merge_coaching(rule, given):
    if not given:
        return rule
    out = dict(rule)
    for k in ("headline", "fixes", "keep_doing"):
        if given.get(k):
            out[k] = given[k]
    out["writer"] = "claude"
    return out


# ---------- data ----------

def build_data(rows, team_rows, coaching, meta):
    team = ag.insights(rows, team_rows)
    closers = ag.closer_table(rows)
    reps = []
    for c in closers:
        mine = [r for r in rows if r["closer"] == c["closer"]]
        i = ag.insights(mine, team_rows)
        given = (coaching.get("reps") or {}).get(c["closer"]) if coaching else None
        reps.append({
            "name": c["closer"],
            "summary": {k: v for k, v in c.items() if k != "insights"},
            "insights": i,
            "coaching": merge_coaching(rule_coaching(i, mine, c["closer"]), given),
        })
    rank_key = (lambda r: -(r["summary"]["cash_per_call"] or 0)) if team["cash_per_call"] is not None else (lambda r: -(r["summary"]["avg_score"] or 0))
    reps.sort(key=rank_key)
    team_coach = merge_coaching(rule_coaching(team, rows, "Team"), (coaching or {}).get("team"))
    calls = sorted(rows, key=lambda r: (r["date"], r["closer"]), reverse=True)
    return {
        "meta": meta,
        "labels": {"objections": ag.OBJECTIONS, "questions": ag.QUESTIONS, "mistakes": ag.MISTAKES,
                   "strengths": ag.STRENGTHS, "pay": ag.PAY_LABELS, "say_instead": ag.SAY_INSTEAD},
        "team": team,
        "team_coaching": team_coach,
        "reps": reps,
        "calls": calls,
    }


# ---------- output ----------

def find_browser():
    candidates = []
    system = platform.system()
    if system == "Darwin":
        candidates += [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
            "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        ]
    elif system == "Windows":
        for base in (os.environ.get("PROGRAMFILES", ""), os.environ.get("PROGRAMFILES(X86)", ""), os.environ.get("LOCALAPPDATA", "")):
            if base:
                candidates += [
                    os.path.join(base, "Google", "Chrome", "Application", "chrome.exe"),
                    os.path.join(base, "Microsoft", "Edge", "Application", "msedge.exe"),
                ]
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge", "msedge", "chrome"):
        p = shutil.which(name)
        if p:
            candidates.append(p)
    for c in candidates:
        if c and os.path.exists(c):
            return c
    return None


def safe_name(name):
    return re.sub(r"[^A-Za-z0-9._ -]+", "", name).strip().replace(" ", "-") or "rep"


def print_pdf(browser, html_path, view, out_pdf):
    url = html_path.resolve().as_uri() + "?" + urllib.parse.urlencode({"view": view, "print": "1"})
    cmd = [browser, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--hide-scrollbars",
           "--run-all-compositor-stages-before-draw", "--virtual-time-budget=4000",
           f"--print-to-pdf={out_pdf}", url]
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90, check=False)
    except (subprocess.TimeoutExpired, OSError):
        return False
    return out_pdf.exists() and out_pdf.stat().st_size > 1000


def open_file(path):
    system = platform.system()
    try:
        if system == "Darwin":
            subprocess.Popen(["open", str(path)])
        elif system == "Windows":
            os.startfile(str(path))  # type: ignore[attr-defined]
        else:
            subprocess.Popen(["xdg-open", str(path)])
    except OSError:
        pass


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("source")
    p.add_argument("--from", dest="date_from")
    p.add_argument("--to", dest="date_to")
    p.add_argument("--closer", help="Only this closer's calls (the team numbers still use everyone in range for comparison)")
    p.add_argument("--coaching", help="coaching.json written by Claude: {team:{headline,fixes,keep_doing}, reps:{Name:{...}}}")
    p.add_argument("--confirmed", type=int, help="How many sales calls were confirmed for grading (for 'Graded X of Y')")
    p.add_argument("--recorder", default="")
    p.add_argument("--out")
    p.add_argument("--no-pdf", action="store_true")
    p.add_argument("--open", action="store_true", help="Open the HTML report when done")
    a = p.parse_args()

    rows = ag.load_calls(a.source)
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

    coaching = None
    if a.coaching and Path(a.coaching).exists():
        with open(a.coaching, encoding="utf-8") as f:
            coaching = json.load(f)

    dates = sorted(r["date"] for r in rows if r["date"])
    first, last = (dates[0], dates[-1]) if dates else ("", "")
    meta = {
        "from": a.date_from or first, "to": a.date_to or last,
        "graded": len(rows), "confirmed": a.confirmed or len(rows),
        "recorder": a.recorder, "generated": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "outcomes_from_user": sum(1 for r in rows if r["out_by"] == "user"),
        "cash_known": any(isinstance(r["cash"], (int, float)) for r in rows),
        "single_closer": a.closer or None,
    }
    data = build_data(rows, team_rows, coaching, meta)

    out = Path(a.out) if a.out else Path("sales-call-reports") / f"{meta['from'] or 'start'}_to_{meta['to'] or 'end'}"
    out.mkdir(parents=True, exist_ok=True)
    html = TEMPLATE.read_text(encoding="utf-8")
    payload = json.dumps(data, ensure_ascii=False, default=str).replace("</", "<\\/")
    html = html.replace("/*__REPORT_DATA__*/null", payload)
    html_path = out / "report.html"
    html_path.write_text(html, encoding="utf-8")
    print(f"report: {html_path.resolve()}")

    pdfs = []
    if not a.no_pdf:
        browser = find_browser()
        if browser:
            (out / "pdf").mkdir(exist_ok=True)
            views = ([] if a.closer else [("team", "Team")]) + [(f"rep:{r['name']}", r["name"]) for r in data["reps"]]
            for view, label in views:
                pdf = out / "pdf" / f"{safe_name(label)}.pdf"
                if print_pdf(browser, html_path, view, pdf):
                    pdfs.append(pdf)
            for pdf in pdfs:
                print(f"pdf: {pdf.resolve()}")
            if not pdfs:
                print("pdf: browser found but printing failed; use the report's Save PDF button", file=sys.stderr)
        else:
            print("pdf: no Chrome/Edge/Chromium found; open the report and use its Save PDF button for each view")

    if a.open:
        open_file(html_path)


if __name__ == "__main__":
    main()
