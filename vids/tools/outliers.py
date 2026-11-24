#!/usr/bin/env python3
"""Pocketfuzzy outlier math: views divided by the account's own median.

  python3 outliers.py niche reels.tsv
      Rank other accounts' reels. TSV columns (header row, tab-separated):
      account  views  hook   [shares] [date] [url] [topic]
  python3 outliers.py audit posts.tsv [--packs pack1.md pack2.md]
      Rank your own posts and find which traits over-index. TSV columns:
      ep  views  [likes] [comments] [shares] [saves] [follows] [date] [any other trait columns]
      With --packs, hook, voice, trend and weird factor are filled in from the episode packs.
"""
import csv, re, sys, statistics as st

FORMULAS = [  # (name, pattern) — first match is the primary label
    ("MYTH FLIP",      r"n'?t\b.*\b(myth|actually|mostly|really)\b|\bmyth\b|\bisn'?t\b|\baren'?t\b|\bdon'?t\b|\bwrong\b|\bfake\b|\bmade up\b"),
    ("HIDDEN ORIGIN",  r"\bnamed (after|by)\b|\bstarted (as|with)\b|\bcomes? from\b|\boriginally\b|\bwas (chosen|invented)\b|\bturned into\b|\bthe first\b"),
    ("USED TO",        r"\bused to\b|\b(centuries|years) ago\b|\bancient\b|\bvictorian\b|\bmedieval\b|\bin the \d{3,4}s?\b"),
    ("GROSS-OUT",      r"\b(pee|poop|urine|lint|snot|vomit|butt|sweat|slime|rot|mold|mucus|fart|gross|blood)\w*"),
    ("NUMBER SHOCK",   r"\d|\b(hundred|thousand|million|billion|half)\b"),
    ("EXTREME",        r"\b(only|most|never|every|oldest|biggest|smallest|fastest|first)\b|\w{3,}est\b"),
    ("STORY",          r"^(a|an|one) \w+ \w+"),
    ("YOU",            r"\byou(r)?\b"),
    ("STRANGE TRAIT",  r"^(?!(the|this|that|there|it|so|here|what|why|how|in|on)\b)[a-z]+"),
]


def formula(hook):
    h = (hook or "").lower()
    for name, pat in FORMULAS:
        if re.search(pat, h):
            return name
    return "OTHER"
# STRANGE TRAIT = a concrete subject doing something unexpected ("Otters have pockets")


def num(x):
    try:
        return float(str(x).replace(",", "").replace("k", "e3").replace("K", "e3").replace("M", "e6").strip())
    except ValueError:
        return None


def read_tsv(path):
    with open(path, encoding="utf-8") as f:
        sample = f.read(2048); f.seek(0)
        dialect = "excel-tab" if "\t" in sample else "excel"
        return [{k.strip().lower(): (v or "").strip() for k, v in r.items() if k} for r in csv.DictReader(f, dialect=dialect)]


def per_k(a, views):
    a = num(a)
    return round(a / views * 1000, 1) if a is not None and views else None


def thirds(rows, key):
    rows = sorted(rows, key=lambda r: r["multiple"], reverse=True)
    k = max(1, len(rows) // 3)
    top, bot = rows[:k], rows[-k:]
    def share(group):
        c = {}
        for r in group:
            c[r[key]] = c.get(r[key], 0) + 1
        return {k_: round(v / len(group) * 100) for k_, v in c.items()}
    return share(top), share(bot)


def niche(path):
    rows = [r for r in read_tsv(path) if num(r.get("views")) is not None]
    by_acct = {}
    for r in rows:
        by_acct.setdefault(r["account"], []).append(num(r["views"]))
    med = {a: st.median(v) for a, v in by_acct.items()}
    for r in rows:
        v = num(r["views"])
        r["multiple"] = round(v / med[r["account"]], 2) if med[r["account"]] else 0
        r["formula"] = formula(r.get("hook"))
        r["sends_k"] = per_k(r.get("shares"), v)
    rows.sort(key=lambda r: r["multiple"], reverse=True)
    thin = [a for a, v in by_acct.items() if len(v) < 6]
    print("| # | Multiple | Account | Views | Formula | Sends/1k | Hook / topic |")
    print("|---|---|---|---|---|---|---|")
    for i, r in enumerate(rows, 1):
        print(f"| {i} | {r['multiple']}× | {r['account']} | {int(num(r['views'])):,} | {r['formula']} | "
              f"{r['sends_k'] if r['sends_k'] is not None else '-'} | {r.get('hook') or r.get('topic','')} |")
    top, bot = thirds(rows, "formula")
    print("\n**Formulas, top third vs bottom third (% of reels):**")
    for f_ in sorted(set(top) | set(bot), key=lambda x: -(top.get(x, 0) - bot.get(x, 0))):
        print(f"- {f_}: top {top.get(f_,0)}% · bottom {bot.get(f_,0)}%")
    print(f"\nBreakouts (≥3× own median): {sum(r['multiple'] >= 3 for r in rows)} of {len(rows)} reels "
          f"across {len(by_acct)} accounts.")
    if thin:
        print("Thin baselines (<6 reels, median is shaky): " + ", ".join(thin))


def pack_meta(paths):
    meta = {}
    for p in paths:
        txt = open(p, encoding="utf-8").read()
        for m in re.finditer(r"^\| (\d{2}) \| ([^|]+?) \| \*{0,2}(\w+)\*{0,2}[^|]*\|", txt, re.M):
            if m.group(3) in {"Michael", "Puck", "George", "Lewis", "Heart", "Emma"}:
                meta.setdefault(m.group(1), {})["voice"] = m.group(3)
        for m in re.finditer(r"^\| (\d{2}) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|", txt, re.M):
            ep, title, c3, c4 = (x.strip() for x in m.groups())
            d = meta.setdefault(ep, {})
            d.setdefault("title", title.replace("★", "").strip())
            if "Gross" in c4 or "Myth" in c4 or c4.replace(" ★", "") in {"Wholesome", "Weird", "History", "On-brand", "Myth-ish"}:
                d["factor"] = c4.replace("★", "").strip()
        for m in re.finditer(r"\n## (\d{2}) — [^\n]*\n(.*?)(?=\n## \d{2} — |\n## Production|\Z)", txt, re.S):
            ep, body = m.groups()
            d = meta.setdefault(ep, {})
            h = re.search(r"\*\*Hook[^*]*:\*\*\s*(.+)", body)
            if h:
                d["hook"] = h.group(1).strip()
            t = re.search(r"\*\*Trend:\*\*\s*([^\n·]+)", body)
            d["kind"] = "trend" if t else "evergreen"
            v = re.search(r"\*\*Voice:\*\*\s*(\w+)", body)
            if v:
                d["voice"] = v.group(1)
    return meta


METRICS = {"views", "likes", "comments", "shares", "saves", "follows", "date", "url", "ep", "hook", "title", "reach"}


def audit(path, packs):
    rows = [r for r in read_tsv(path) if num(r.get("views")) is not None]
    meta = pack_meta(packs) if packs else {}
    for r in rows:
        ep = r.get("ep", "").zfill(2)
        r["ep"] = ep
        for k, v in meta.get(ep, {}).items():
            r.setdefault(k, v) if r.get(k) else r.__setitem__(k, v)
    med = st.median(num(r["views"]) for r in rows)
    for r in rows:
        v = num(r["views"])
        r["multiple"] = round(v / med, 2) if med else 0
        r["formula"] = formula(r.get("hook"))
        for m in ("shares", "saves", "follows"):
            r[m + "_k"] = per_k(r.get(m), v)
    rows.sort(key=lambda r: r["multiple"], reverse=True)
    print(f"Account median: {int(med):,} views across {len(rows)} posts\n")
    print("| # | Ep | Title | Views | Multiple | Sends/1k | Saves/1k | Follows/1k | Formula |")
    print("|---|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(rows, 1):
        f = lambda x: "-" if x is None else x
        print(f"| {i} | {r['ep']} | {r.get('title','')} | {int(num(r['views'])):,} | {r['multiple']}× | "
              f"{f(r['shares_k'])} | {f(r['saves_k'])} | {f(r['follows_k'])} | {r['formula']} |")
    traits = [k for k in rows[0] if k not in METRICS and not k.endswith("_k") and k != "multiple"]
    print("\n**What over-indexes (median multiple by trait; n<3 is a hint, not a finding):**")
    for t in traits:
        groups = {}
        for r in rows:
            if r.get(t):
                groups.setdefault(r[t], []).append(r["multiple"])
        if len(groups) < 2:
            continue
        parts = sorted(((st.median(v), k, len(v)) for k, v in groups.items()), reverse=True)
        print(f"- {t}: " + " · ".join(f"{k} {m:.2f}× (n={n}{'' if n >= 3 else ', thin'})" for m, k, n in parts))
    winners = [r for r in rows if r["multiple"] >= 2]
    flops = [r for r in rows if r["multiple"] <= 0.5]
    print(f"\nBreakouts (≥2×): {', '.join(r['ep'] for r in winners) or 'none yet'} · "
          f"Flops (≤0.5×): {', '.join(r['ep'] for r in flops) or 'none'}")
    if len(rows) < 8:
        print("Fewer than 8 posts: treat every pattern above as a guess until more data is in.")


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 2:
        print(__doc__); sys.exit()
    if a[0] == "niche":
        niche(a[1])
    elif a[0] == "audit":
        packs = a[a.index("--packs") + 1:] if "--packs" in a else []
        audit(a[1], packs)
