#!/usr/bin/env python3
"""Append a Pocketfuzzy episode (repo-style markdown) to the end of a Google Doc pack.

Usage:
  python3 doc_append.py read_doc.json episode.md > requests.json
    read_doc.json  the saved result of the Google Docs read_doc call on the pack (raw or wrapped in {"content": ...})
    episode.md     one episode in the pack format:
                     ## 38 — Title
                     **Length:** ~22s · **Voice:** Heart · **Music:** bossa nova · **Trend:** ...
                     **Hook:** ...
                     ### Voiceover script
                     > line one
                     > line two
                     ### Shot list
                     1 · 0:00–0:04 · visual description · ON-SCREEN TEXT · sfx
                     **Never draw:** ...
                     **Caption:** ...
                     **Pinned comment:** ...
                     **Source:** ...
                     **Accuracy guardrails:** ...
Prints {"revisionId": ..., "requests": [...]}: send the requests with update_doc and
writeControl.requiredRevisionId set to that revisionId. Headings get HEADING_2/3 styles,
"**Label:**" prefixes are bolded, voiceover lines become plain paragraphs (the export drops ">",
and preflight.normalize() puts it back), and any list/checkbox style inherited from the last
paragraph is removed.
"""
import json, re, sys


def u16(s):
    return len(s.encode('utf-16-le')) // 2


def body_of(doc):
    doc = doc.get('content', doc)
    tabs = doc.get('tabs')
    body = tabs[0]['documentTab']['body'] if tabs else doc['body']
    return doc.get('revisionId'), body['content']


def build(doc, md):
    rev, content = body_of(doc)
    end = content[-1]['endIndex']            # body end; the last "\n" sits at end-1
    paras = []                               # (text, style, bold_len)
    for raw in md.strip('\n').splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        if line.startswith('### '):
            paras.append((line[4:], 'HEADING_3', 0))
        elif line.startswith('## '):
            paras.append((line[3:], 'HEADING_2', 0))
        elif line.startswith('>'):
            paras.append((line.lstrip('> ').strip(), 'NORMAL_TEXT', 0))
        else:
            # "**A:** x · **B:** y" -> plain text with bold ranges
            spans, out, pos = [], '', 0
            for m in re.finditer(r'\*\*(.+?)\*\*', line):
                out += line[pos:m.start()]
                spans.append((u16(out), u16(m.group(1))))
                out += m.group(1)
                pos = m.end()
            out += line[pos:]
            paras.append((out, 'NORMAL_TEXT', spans))
    text = '\n' + '\n'.join(p[0] for p in paras)   # leading \n starts a fresh paragraph after the last one
    at = end - 1
    reqs = [{'insertText': {'location': {'index': at}, 'text': text}}]
    start = at + 1                                   # first inserted paragraph starts after the leading \n
    stop = at + u16(text) + 1
    reqs.append({'deleteParagraphBullets': {'range': {'startIndex': start, 'endIndex': stop}}})
    reqs.append({'updateTextStyle': {'range': {'startIndex': start, 'endIndex': stop - 1},
                                     'textStyle': {'bold': False, 'italic': False}, 'fields': 'bold,italic'}})
    i = start
    for t, style, spans in paras:
        n = u16(t)
        reqs.append({'updateParagraphStyle': {'range': {'startIndex': i, 'endIndex': i + n + 1},
                                              'paragraphStyle': {'namedStyleType': style}, 'fields': 'namedStyleType'}})
        for off, ln in (spans or []):
            reqs.append({'updateTextStyle': {'range': {'startIndex': i + off, 'endIndex': i + off + ln},
                                             'textStyle': {'bold': True}, 'fields': 'bold'}})
        i += n + 1
    return {'revisionId': rev, 'requests': reqs}


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(__doc__); sys.exit(1)
    doc = json.load(open(sys.argv[1], encoding='utf-8'))
    md = open(sys.argv[2], encoding='utf-8').read()
    json.dump(build(doc, md), sys.stdout, ensure_ascii=False)
