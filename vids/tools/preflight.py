#!/usr/bin/env python3
"""Pocketfuzzy preflight: score hooks, lint captions, check VO timing.

Usage (VO length passes anywhere in the 20–30s range):
  python3 preflight.py pack.md [more_packs.md ...]      # check every episode in a pack
  python3 preflight.py --hook "Otters have pockets."    # score one hook (repeatable)
  python3 preflight.py --caption "Text #didyouknow #otters"
The scores are lexical heuristics: good at catching weak hooks, not at picking hits.
"""
import re, sys, statistics

WPM = 150                      # house VO pace
SHOT1_SECONDS = 4              # the hook has to land inside shot 1
HASHTAG_CAP = 5                # Instagram's current per-post cap
VISIBLE_CHARS = 125            # feed shows roughly this much before "more"
CAPTION_MAX = 2200
MIN_SECONDS = 20               # house length range from the packs' global settings:
MAX_SECONDS = 30               # anything from 20 to 30 seconds is fine

DEALBREAKERS = [r"^did you know", r"^hey\b", r"^hi\b", r"^welcome", r"^fun fact",
                r"stop scrolling", r"wait for it", r"you won'?t believe",
                r"in this video", r"^today we", r"^so,? let'?s", r"let'?s talk"]
SLOW_OPENERS = [r"^there'?s\b", r"^there (is|are)\b", r"^so\b", r"^okay\b", r"^ok\b",
                r"^here'?s\b", r"^this is\b", r"^let me\b"]
REVERSAL = [r"n'?t\b", r"\bnot\b", r"\bmyth\b", r"\bactually\b", r"\bused to\b",
            r"\bmade up\b", r"\bsecretly\b", r"\bfake\b", r"\bwrong\b", r"\bweirder\b",
            r"\bnamed (after|by)\b", r"\bwas a prank\b", r"\bturned into\b", r"\bmight have been\b"]
EXTREME = [r"\w+est\b", r"\bmost\b", r"\bfirst\b", r"\bonly\b", r"\bnever\b",
           r"\bevery\b", r"\boldest\b", r"\bbiggest\b"]
TREND_LEAN = [r"\bthis week\b", r"\bright now\b", r"\bis here\b", r"\bfrom the movies?\b",
              r"\beveryone'?s talking\b", r"\bthat (bird|guy|thing|meme|video)\b", r"\b20\d\d is\b"]
NUMBER_WORDS = r"\b(one|two|three|four|five|six|seven|eight|nine|ten|hundred|thousand|million|billion|half|dozen|forty|fifty)\b"
FUNCTION_WORDS = {"a", "an", "the", "this", "that", "these", "those", "there's", "there", "it", "it's",
                  "you", "your", "we", "i", "in", "on", "every", "one", "so", "here's", "what", "why", "how"}
GENERIC_TAGS = {"didyouknow", "animalfacts", "nature", "science", "history", "gross", "cute",
                "weirdscience", "wholesome", "mythbusting", "facts", "funfacts", "learn",
                "tech", "food", "travel", "november", "birds"}
CTA = [r"\bfollow\b", r"\bcomment\b", r"\bshare\b", r"\bsave this\b", r"\btag\b",
       r"\blink in bio\b", r"\bsend this\b", r"\bdm\b"]


def any_re(pats, text):
    return [p for p in pats if re.search(p, text, re.I)]


def score_hook(hook):
    h = hook.strip().strip('"“”')
    low = h.lower()
    words = re.findall(r"[\w'’$@.,-]+", h)
    n = len(words)
    secs = n / WPM * 60
    notes, props = [], {}

    # FRONTLOAD: the subject arrives first, no throat-clearing
    fl = 20
    if any_re(SLOW_OPENERS, low):
        fl -= 8; notes.append("slow opener: put the subject first")
    props["FRONTLOAD"] = fl

    # FITS SHOT 1: speakable inside the first shot
    props["FITS SHOT 1"] = 20 if secs <= SHOT1_SECONDS + 1 else 14 if secs <= 6 else 8 if secs <= 7.5 else 2
    if secs > SHOT1_SECONDS + 1:
        notes.append(f"{n} words ≈ {secs:.1f}s; shot 1 is ~{SHOT1_SECONDS}s, cut words")

    # SPECIFIC: a number or a proper noun
    sentences = re.split(r"(?<=[.!?…])\s+", h)
    proper = any(re.search(r"\s[A-Z][a-z]+", " " + " ".join(s.split()[1:])) for s in sentences)
    has_num = bool(re.search(r"\d", h) or re.search(NUMBER_WORDS, low))
    first = re.sub(r"[^a-z']", "", words[0].lower()) if words else ""
    concrete_subject = first not in FUNCTION_WORDS
    props["SPECIFIC"] = 20 if (has_num or proper) else 14 if concrete_subject else 10
    if not (has_num or proper):
        notes.append("no number or name: a count, date or place would sharpen it")

    # SURPRISE: reverses an assumption (strongest) or claims an extreme
    if any_re(REVERSAL, low):
        props["SURPRISE"] = 20
    elif any_re(EXTREME, low):
        props["SURPRISE"] = 14
    else:
        props["SURPRISE"] = 10; notes.append("no twist word: fine if the fact itself is surprising; otherwise say what belief it breaks")

    # OPEN LOOP: a second beat the payoff has to resolve
    two_beats = len([s for s in sentences if s.strip()]) >= 2 or "…" in h or "..." in h \
        or re.search(r",? (and|but|so|because) ", low)
    props["OPEN LOOP"] = 20 if two_beats else 10

    total = sum(props.values())
    flags = []
    db = any_re(DEALBREAKERS, low)
    if db:
        flags.append("DEALBREAKER: filler opener (" + db[0].strip("^\\b") + ")")
        total = min(total, 40)
    if any_re(TREND_LEAN, low):
        flags.append("LEANS ON TREND: makes no sense to someone who missed the news; name the actual subject")
    rating = "STRONG" if total >= 80 else "OK" if total >= 60 else "WEAK"
    weakest = min(props, key=props.get)
    return {"hook": h, "score": total, "rating": rating, "props": props,
            "weakest": weakest, "notes": notes, "flags": flags}


def stem(w):
    w = w.lower()
    return w[:-1] if w.endswith("s") and len(w) > 3 else w


def lint_caption(cap):
    cap = cap.strip()
    tags = re.findall(r"#(\w+)", cap)
    text = re.sub(r"#\w+", "", cap).strip()
    first_line = text.split("\n")[0]
    out = []
    out.append(("LENGTH", len(cap) <= CAPTION_MAX, f"{len(cap)}/{CAPTION_MAX} chars"))
    out.append(("VISIBLE LINE", len(first_line) <= VISIBLE_CHARS,
                f"{len(first_line)} chars before the cut" + ("" if len(first_line) <= VISIBLE_CHARS else " (gets truncated)")))
    out.append(("HASHTAGS", len(tags) <= HASHTAG_CAP and "didyouknow" in [t.lower() for t in tags],
                f"{len(tags)} tags" + ("" if "didyouknow" in [t.lower() for t in tags] else ", missing #didyouknow")))
    specific = [t for t in tags if t.lower() not in GENERIC_TAGS]
    text_stems = {stem(w) for w in re.findall(r"[A-Za-z]+", text)}
    text_join = re.sub(r"[^a-z]", "", text.lower())
    hit = [t for t in specific if stem(t) in text_stems or t.lower() in text_join]
    out.append(("SEARCH WORD", bool(hit) or not specific,
                ("topic word in text: " + ", ".join(hit)) if hit else
                ("none of " + ", ".join("#" + t for t in specific) + " appear as words; Instagram search reads caption text")))
    asks = any_re(CTA, text.lower())
    out.append(("ONE ASK", len(asks) <= 1, f"{len(asks)} call(s) to action"))
    return out


def vo_timing(vo_lines, target):
    words = sum(len(re.findall(r"[\w'’$@-]+", l)) for l in vo_lines)
    secs = words / WPM * 60
    ok = MIN_SECONDS <= secs <= MAX_SECONDS
    return words, secs, ok


def parse_pack(path):
    txt = open(path, encoding="utf-8").read()
    eps = re.split(r"\n## (\d{2}) — ", txt)
    for i in range(1, len(eps), 2):
        num, body = eps[i], eps[i + 1]
        title = body.split("\n", 1)[0].replace("★", "").strip()
        hook = re.search(r"\*\*Hook[^*]*:\*\*\s*(.+)", body)
        cap = re.search(r"\*\*Caption:\*\*\s*(.+)", body)
        length = re.search(r"\*\*Length:\*\*\s*~?(\d+)s", body)
        vo = re.search(r"### Voiceover script\n((?:>.*\n?)+)", body)
        vo_lines = [l.lstrip("> ").strip() for l in vo.group(1).splitlines()] if vo else []
        yield {"ep": num, "title": title, "hook": hook.group(1) if hook else None,
               "caption": cap.group(1) if cap else None,
               "target": int(length.group(1)) if length else None, "vo": vo_lines}


def report_pack(paths):
    rows, fixes, timing = [], [], []
    for p in paths:
        for e in parse_pack(p):
            hs = score_hook(e["hook"]) if e["hook"] else None
            lint = lint_caption(e["caption"]) if e["caption"] else []
            fails = [f"{k}: {m}" for k, ok, m in lint if not ok]
            w, s, ok = vo_timing(e["vo"], e["target"]) if e["vo"] else (0, 0, True)
            if e["vo"]:
                timing.append((s, e["target"]))
            rows.append((e["ep"], e["title"], hs["score"] if hs else "-", hs["rating"] if hs else "-",
                         hs["weakest"] if hs else "-", f"{s:.0f}s/{e['target']}s", len(fails)))
            items = []
            if hs and (hs["rating"] != "STRONG" or hs["flags"]):
                items.append(f"hook {hs['score']} {hs['rating']}: " + "; ".join(hs["flags"] + hs["notes"]))
            items += ["caption " + f for f in fails]
            if not ok:
                items.append(f"VO is {w} words ≈ {s:.0f}s, outside the {MIN_SECONDS}–{MAX_SECONDS}s range")
            if items:
                fixes.append((e["ep"], e["title"], items))
    print("| Ep | Title | Hook | Rating | Weakest | VO time | Caption fails |")
    print("|---|---|---|---|---|---|---|")
    for r in rows:
        print("| " + " | ".join(str(x) for x in r) + " |")
    scores = [r[2] for r in rows if isinstance(r[2], int)]
    over = [(s_ - t) for s_, t in timing if t]
    if over:
        print(f"VO runs {statistics.median(over):+.0f}s vs the labeled length on median (at {WPM} wpm)")
    if scores:
        print(f"\nMedian hook score {statistics.median(scores)} · "
              f"STRONG {sum(r[3]=='STRONG' for r in rows)} · OK {sum(r[3]=='OK' for r in rows)} · "
              f"WEAK {sum(r[3]=='WEAK' for r in rows)}")
    print("\n## Fix list")
    for ep, title, items in fixes:
        print(f"- **{ep} {title}**: " + " | ".join(items))


def main(argv):
    if not argv:
        print(__doc__); return
    if argv[0] in ("--hook", "--caption"):
        it = iter(argv)
        for flag in it:
            val = next(it)
            if flag == "--hook":
                r = score_hook(val)
                print(f"{r['score']}/100 {r['rating']} · weakest {r['weakest']} · {r['props']}")
                for x in r["flags"] + r["notes"]:
                    print("  -", x)
            else:
                for k, ok, m in lint_caption(val):
                    print(f"  {'PASS' if ok else 'FAIL'} {k}: {m}")
        return
    report_pack(argv)


if __name__ == "__main__":
    main(sys.argv[1:])
