---
name: "pocketfuzzy-trends"
description: "Find what's breaking out for Pocketfuzzy and turn it into a ranked shortlist of cartoon-able \"did you know\" topics for the next episode pack."
---

# Pocketfuzzy trends

Builds the topic shortlist for the next "Did You Know?" pack. Two evidence sources, used together:

1. **News sweep**: what went viral in the last ~4 weeks (web search).
2. **Niche outliers**: reels from similar accounts, ranked by how far each beat *its own account's median* views. Raw views are not evidence: a big account's average reel beats a small account's breakout.

Start right away. If the user gave no niche data, do the news sweep and ask for niche data alongside the results.

## Step 1: News sweep

Search for what went viral since the last pack (check the latest pack's date range: the packs are Google Docs in Drive > Vids titled "Pocketfuzzy Did You Know Pack (Vol N)"; read them with Drive `read_file_content`). Cover: animals and nature, science and space, history anniversaries, holidays in the next 3 weeks, internet memes, big entertainment and tech news, food and prices. For each trend, find a **true, sourced, cartoon-able fact** that it unlocks. The trend is the doorway, not the subject ("GTA 6 launch" → gators and crocs only coexist in Florida).

Speed matters (Vol 1's Retention playbook): a trend topic is only worth making if it can go up within 24–48 hours of the trend breaking, or if the trend has a known date ahead (a holiday, a launch, a sky event). Otherwise, treat the fact as evergreen or drop it.

## Step 2: Niche outliers (when the user provides data)

The user collects this by browsing, at human speed, in their own app: ~10 accounts in the niche (animated facts, weird nature, history toons), ~10–12 recent reels each. Never scrape, log in, or ask for passwords. Ask for a TSV or a pasted table with these columns: `account  views  hook  [shares] [date] [url]`. `hook` = the first line said or shown.

Write the script below to `outliers.py` and run `python3 outliers.py niche reels.tsv`. Then report:
- Breakouts (≥3× their own median) and the hook formula each used.
- Which formulas are over-represented in the top third vs the bottom third.
- Accounts with thin baselines (<6 reels), whose multiples are unreliable.

Then adapt each breakout's **underlying fact pattern** into new Pocketfuzzy topics. Never copy a topic, script or visual.

## Step 3: Filter every candidate

Drop or flag any candidate that fails one of these:
- **Cartoon-able:** it can be told entirely with original drawn creatures and objects, with the armless Fuzz as host. No real people, no news photos.
- **IP-safe:** no drawing of other studios' characters or worlds, logos, brand liveries, or recreations of viral images. Brand and franchise names may be *said* in VO when they're part of the fact, but they never go in generator prompts.
- **True and sourceable:** a primary or reputable source exists. Note the guardrail wording ("up to", "one study found").
- **Tone:** real harm or death means a gentle tone and a kindness card. Otherwise skip it.
- **Not a repeat** of any episode already in the packs, including Ep 13 (hippo), which was cut.

## Step 4: Output

A ranked shortlist of 12–25 topics:

| Rank | Working title | Hook draft | Hook overlay | Loop line | Formula | Trend / evergreen | Shelf life | Evidence | Source |

- **Evidence** = the niche multiple or the trend's reach.
- **Shelf life** = "post within 48h", "post before <date>", "~2 weeks" or "evergreen".
- **Loop line** = a draft last line that runs straight back into the hook, so the episode can loop (Ep 16's loop cut ends "…something's beeping outside at 3 AM, remember:" and restarts on "That car alarm at 3 AM might not be a car.").

Rank by evidence × shelf-life urgency × how likely people are to send it to someone (Instagram weighs shares most) × how strongly it fits the series (pockets, hoarding, goblins, gross-but-cozy, myth-busting). Then suggest a post order for the first week, putting the shortest shelf lives first.

Hook drafts must pass the preflight rules: subject first, about 12 words or fewer, a number or name when possible, a twist or open loop, and no "Did you know…" or "Let's talk…" openers. Pair each hook with a bold 3–5 word overlay for the first 3 seconds. When the user picks topics, write the new pack as a Google Doc in Drive > Vids (load the google-workspace skill first), titled "Pocketfuzzy Did You Know Pack (Vol N)". Upload it as HTML in which every line is its own paragraph and there are no horizontal rules, so it exports back to Markdown cleanly for the preflight and audit scripts. Offer to write the full episodes in the house pack format: VO script written loop-ready (the last line runs into the hook, and the last shot matches the first), 4–5 shot list with the style block, a hook overlay plus one short overlay per beat, SFX, caption, source, accuracy guardrails, **Never draw** line, plus the next voice (no back-to-back repeats) and music style in rotation. Aim for 20–24s of voiceover, within the 20–30s house range.

## Daily mode (when pocketfuzzy-daily runs this)

The output is queue rows instead of a shortlist. The queue is the Google Sheet "Pocketfuzzy Queue" (`1iurNV5lR9im3oFBPgyTrIpA94BxdnJtbhWeReQ-NWMc`, tab `Queue`).

- Sweep only what broke in the last 48 hours, plus dated events in the next 3 weeks.
- Check every candidate against the queue's titles and notes, as well as the packs, so nothing repeats.
- Keep 0–3 topics. Zero is a fine answer on a quiet day.
- Append each kept topic as a row:
  - Ep blank, Title, Hook (hook draft), Status `idea`, Added today.
  - Kind `trend` with Post by = the day it broke + 2 days, or `holiday` with Post by = the event date.
  - Notes: trend · source · guardrail wording · loop line.
- Don't write a new pack doc. Episodes get scripted into the Vol 3 doc by the daily run.

## outliers.py

```python
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
```