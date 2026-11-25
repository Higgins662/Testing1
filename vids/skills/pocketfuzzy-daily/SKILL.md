---
name: pocketfuzzy-daily
description: Run the Pocketfuzzy daily production pass: trend sweep with the 48-hour rule, queue update, scripts into the pack doc, preflight, render the next loop cuts, and a daily brief. Never posts.
---

# Pocketfuzzy daily run

One unattended pass that leaves the user with finished, checked videos and a short brief. The user posts by hand. Work through the steps in order and don't stop to ask questions: take the most reasonable reading, note it in the brief, and move on. Stop only at the stop rules below.

**Files**
- Queue sheet `1iurNV5lR9im3oFBPgyTrIpA94BxdnJtbhWeReQ-NWMc`
  - Tab `Queue`, columns A–M: Rank, Ep, Title, Hook, Kind (trend/holiday/evergreen), Post by, Status, Script in, Voice, Music, Video, Added, Notes.
  - Status values: idea → scripted → checked → rendered → posted, plus hold and dropped.
  - Tab `Runs`: one row per run, columns Date, New topics added, Scripted, Preflight, Rendered (ready to post), Needs you, Run notes.
- Pack docs in Drive > Vids:
  - Vol 1 `1HzbLPTaOeejR0k-ONxX-A7aXOp04THam7c__-Ut4SV8`: global settings, style block, voice and music tables, Retention playbook.
  - Vol 2 `19YzBiI2QKU7u8OH4YY1N59oFuxfshdqptdVvwB991q0`: trend rules and guardrails.
  - Vol 3 `1wCnpMhK70CSkXnAkmreZz-4uyQddc-XiOSG7eBUHadw`: where new episodes go.
- Repo `Higgins662/Testing1` (`vids/`):
  - `posting_log.tsv`
  - `tools/`: preflight.py, outliers.py, doc_append.py
  - `render/`: the pipeline
  - `skills/`: copies of these skills, in case the account skills aren't loaded

Load the google-workspace skill before the first Docs or Sheets write. Use pocketfuzzy-trends, pocketfuzzy-preflight and pocketfuzzy-render for their steps. If one isn't available, read its copy in `vids/skills/`.

## Stop rules (these override everything else)

- **Never publish:** no posting, messaging, emailing or sharing.
- **Never delete:** don't delete files, docs, rows or episodes. Mark rows `dropped` with a note instead.
- **Sourced facts only:** a new fact goes into a script only with a reputable source. Every new fact is listed under "Needs you: fact check" in the brief.
- **Sensitive topics:** a topic involving real harm, death, crime, tragedy or a real private person gets a kind tone and a PSA card, or is skipped.
- **Render cap:** at most 2 new renders per run. Don't render an episode whose hook scores under 60 after rewrites, or whose fact couldn't be confirmed. Leave those at `scripted` and say why.
- **Failures:** if a step fails twice, skip it, note it in the brief, and continue with what doesn't depend on it.

## Steps

### 1. Read the state

- Read `Queue!A1:M200` and `Runs!A1:G400`.
- Read `vids/posting_log.tsv`. Any episode logged there but not marked `posted` in the queue gets marked `posted`.
- Today's date and time are in Eastern Time.
- Mark `dropped` (note "window closed <date>") any `idea`, `scripted` or `checked` row whose Post by has passed.
- A `rendered` row whose Post by has passed goes under "Needs you": the user decides.

### 2. Trend sweep (48-hour rule)

Run pocketfuzzy-trends' news sweep, limited to what broke in the **last 48 hours**, plus dated events (holidays, launches, sky events) in the next 3 weeks that aren't already in the queue. Apply its filters: cartoon-able, IP-safe, true and sourced, tone, and not a repeat of anything in the queue or the packs. Keep the best 0–3.

For each one, add a Queue row:
- Ep blank, Status `idea`, Added today.
- Kind `trend` with Post by = trend date + 2 days, or `holiday` with Post by = the event date.
- Notes: the trend, the source and the guardrail wording.

A topic that broke within 48 hours and can make its window jumps to the top of the to-make list today. If nothing new qualifies, say so in the brief. That's a normal outcome.

### 3. Re-rank the queue

Rewrite column A so the order is:
1. `rendered` rows, by Post by.
2. Rows that have to be made today to make their window (48-hour trends, then Post by within 3 days).
3. Other dated rows, by Post by. Respect "not before" notes such as "Post Dec 1–20 only".
4. Evergreen rows:
   - ★ picks first, then the strongest hooks;
   - no two of the same theme in a row (pockets, goblins, birds, gross).
5. `hold`, then `dropped`, then `posted` last.

Sort the rows to match with `sortRange` on A2:M, by column A.

### 4. Pick today's episodes

- Take the top 1–2 rows from group 2, then 3, then 4 that aren't `rendered`.
- Make 2 only if a window forces it or the ready-to-post stock (rendered, not posted, window still open) is under 4.
- Otherwise make 1.

### 5. Script ideas into Vol 3

For each pick with status `idea`, write the full episode in the pack format and append it to Vol 3:
- **Number:** the next free number (the highest Ep anywhere in the queue + 1; Ep 13 is retired).
- **Voice:** from the Vol 1 pool, different from the last rendered episode's voice. That voice is in the newest Runs row with a render.
- **Music:** the next style in the rotation after the last rendered episode's style: folk → jazz → lo-fi → bossa nova → synthwave → ambient.
- **Loop-ready VO:** about 20–24s, and the last line leads into the hook.
- **4–5 shots:** one line each, `n · time · visual · ON-SCREEN · sfx`. The style block is implied by Vol 1.
- **The rest:** Never draw, Caption, Pinned comment (a question that invites replies), Source, and Accuracy guardrails.

To append it:
1. Write the markdown to a file.
2. Save `read_doc` of Vol 3 to a file.
3. Run `python3 vids/tools/doc_append.py <read_doc.json> <episode.md>`.
4. Send the `requests` with `update_doc` and `writeControl.requiredRevisionId` set to the printed `revisionId`.

Then set the queue row's Ep, Script in = Vol 3, Voice, Music, and Status `scripted`.

### 6. Preflight

Run pocketfuzzy-preflight on each pick's pack: export the doc as markdown, then run `preflight.py`. Fix hooks, captions and VO length in the doc itself, then set Status to `checked`. Picks from Vol 1 or 2 get the same check.

### 7. Render

Run pocketfuzzy-render for each `checked` pick, as a loop cut. That skill:
- commits the episode script,
- sends the MP4 into this run's conversation,
- sets the row to `rendered`.

If time is short, one finished episode beats two half-done ones.

### 8. Log and brief

Append a Runs row:
- **Date** today.
- **New topics added** titles, or "none".
- **Scripted** episode numbers and titles.
- **Preflight** a hook score for each checked episode.
- **Rendered (ready to post)** episode, voice, music and file name for each.
- **Needs you** fact checks, expired windows, failures. Write "nothing" when there's nothing.
- **Run notes** anything else in one line.

Then end with a brief for the user of 8 lines at most:
- what's ready to post today, in order, each with its caption and pinned comment;
- what's new in the queue;
- what needs them.

Put the brief in a SendUserMessage so it's the first thing they read.
