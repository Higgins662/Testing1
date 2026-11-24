# Pocketfuzzy tools

These are helper scripts for the "Did You Know?" packs. They need Python 3 and no extra installs. The same code is built into the `pocketfuzzy-preflight`, `pocketfuzzy-trends` and `pocketfuzzy-audit` skills.

## preflight.py: check episodes before generating or posting

Run these from the repo root:

```bash
python3 vids/tools/preflight.py vids/*.md                  # every episode in the packs
python3 vids/tools/preflight.py --hook "Otters have pockets."
python3 vids/tools/preflight.py --caption "Sea otters keep a rock in a skin pocket 🦦 #didyouknow #seaotter"
```

What it checks:

- **Hook score (0–100).** Five checks: the subject comes first, the hook fits in shot 1, it's specific, it has a surprise, and it opens a question. A filler opener (such as "Did you know…") caps the score at 40.
- **Caption.**
  - The line before "more" is at most 125 characters.
  - There are at most 5 hashtags, and one of them is #didyouknow.
  - A topic word appears in the caption text itself.
  - There's at most one call to action.
- **VO timing.** The script is timed at 150 words per minute and must fit under the 28-second cap.

The scores are rough heuristics. They're good at catching weak hooks, but they can't pick the winner between two decent ones. `preflight_report_vol1-2.md` holds the first run over episodes 01–37.

## outliers.py: compare views to an account's own median

```bash
python3 vids/tools/outliers.py niche reels.tsv
python3 vids/tools/outliers.py audit posts.tsv --packs vids/*.md
```

- **niche:** ranks other accounts' reels against each account's own median and labels each hook's formula.
  - TSV columns: `account  views  hook  [shares] [date] [url]`
  - Collect these numbers by browsing normally. Don't use scrapers.
- **audit:** ranks your own posts and shows which formula, voice, topic, trend and music did better than your median.
  - TSV columns: `ep  views  [likes] [comments] [shares] [saves] [follows] [music] [...]`
  - `--packs` fills in each episode's hook, voice and topic details from the pack files.
