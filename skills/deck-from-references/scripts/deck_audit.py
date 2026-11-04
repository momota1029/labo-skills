#!/usr/bin/env python3
"""Measure how heavy and how small each page of a slide PDF is.

Words per page (Latin tokens + CJK characters / 2), the median height of body
words relative to the page width, words drawn over each other (a label printed on
text, an overflowing box) and words outside the page, so decks with different paper sizes compare.
Suggested defaults are a 150-word page limit and a minimum median body word
height of 1.75 percent of page width. Calibrate these for the audience and format;
they are starting points, not measurements of reference decks.
Needs `pdftotext` (poppler) only.

  deck_audit.py deck.pdf [--max-words 150] [--min-median 0.0175] [--json]
"""
import argparse, json, re, statistics, subprocess, sys
from xml.etree import ElementTree

CJK = re.compile(r'[぀-ヿ一-鿿]')
LATIN = re.compile(r'[A-Za-z0-9]+')


PAGE = re.compile(r'<page width="([\d.]+)" height="([\d.]+)">(.*?)</page>', re.S)
WORD = re.compile(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>', re.S)


def bbox_pages(pdf):
    out = subprocess.run(['pdftotext', '-bbox', pdf, '-'], capture_output=True, text=True, check=True).stdout
    for m in PAGE.finditer(out):
        words = [(t, float(x0), float(y0), float(x1), float(y1)) for x0, y0, x1, y1, t in WORD.findall(m.group(3))]
        yield float(m.group(1)), float(m.group(2)), words


def collisions(words, w, h, min_share=0.4):
    """Words drawn over each other, and words reaching outside the page.

    Two word boxes collide when their intersection covers at least `min_share` of the
    smaller box; words of one or two characters are ignored (math limits and
    sub/superscripts touch legitimately).
    """
    outside = [t for t, x0, y0, x1, y1 in words if x0 < 0 or y0 < 0 or x1 > w or y1 > h]
    boxes = [(t, x0, y0, x1, y1) for t, x0, y0, x1, y1 in words if len(t) > 2]
    hits = []
    for i in range(len(boxes)):
        t, a0, b0, a1, b1 = boxes[i]
        for u, c0, d0, c1, d1 in boxes[i + 1:]:
            iw, ih = min(a1, c1) - max(a0, c0), min(b1, d1) - max(b0, d0)
            if iw <= 0 or ih <= 0:
                continue
            small = min((a1 - a0) * (b1 - b0), (c1 - c0) * (d1 - d0))
            if small > 0 and iw * ih / small >= min_share:
                hits.append((t, u))
    return hits, outside


def audit(pdf, max_words=150, min_median=0.0175, min_height=0.014, header=0.09, footer=0.07):
    pages = []
    for i, (w, h, words) in enumerate(bbox_pages(pdf), 1):
        text = ' '.join(t for t, *_ in words)
        count = len(LATIN.findall(text)) + len(CJK.findall(text)) / 2
        body = [(t, y1 - y0) for t, x0, y0, x1, y1 in words if header * h < y0 and y1 < (1 - footer) * h]
        small = [t for t, ht in body if ht / w < min_height]
        overlaps, outside = collisions(words, w, h)
        pages.append({'page': i, 'words': round(count, 1), 'body_words': len(body), 'small_body_words': len(small),
                      'small_share': round(len(small) / len(body), 2) if body else 0.0,
                      'median_height_over_width': round(statistics.median(ht for _, ht in body) / w, 4) if body else None,
                      'overlaps': [' / '.join(p) for p in overlaps[:5]], 'outside': outside[:5]})
    counts = [p['words'] for p in pages]
    summary = {'pages': len(pages), 'median_words': statistics.median(counts) if counts else 0,
               'max_words': max(counts) if counts else 0,
               'heavy_pages': [p['page'] for p in pages if p['words'] > max_words],
               'small_text_pages': [p['page'] for p in pages
                                    if p['median_height_over_width'] is not None and p['median_height_over_width'] < min_median],
               'overlap_pages': [p['page'] for p in pages if p['overlaps']],
               'outside_pages': [p['page'] for p in pages if p['outside']]}
    return {'summary': summary, 'pages': pages}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('pdf'); ap.add_argument('--max-words', type=float, default=150)
    ap.add_argument('--min-median', type=float, default=0.0175, help='floor of the page median of word-box height / page width')
    ap.add_argument('--min-height', type=float, default=0.014, help='words below this are counted in small_share (captions, tags)')
    ap.add_argument('--json', action='store_true')
    a = ap.parse_args()
    r = audit(a.pdf, a.max_words, a.min_median, a.min_height)
    if a.json:
        print(json.dumps(r, indent=2, ensure_ascii=False))
        return 1 if r['summary']['overlap_pages'] or r['summary']['outside_pages'] else 0
    s = r['summary']
    print(f"{a.pdf}: {s['pages']} pages, median {s['median_words']} words, max {s['max_words']}")
    print('heavy pages (> %g words):' % a.max_words, s['heavy_pages'] or 'none')
    print('pages whose median body text is below %g of the page width:' % a.min_median, s['small_text_pages'] or 'none')
    print('pages with words drawn over each other:', s['overlap_pages'] or 'none')
    print('pages with words outside the page:', s['outside_pages'] or 'none')
    for p in r['pages']:
        if p['overlaps'] or p['outside']:
            print(f"  p{p['page']}: overlaps {p['overlaps']} outside {p['outside']}")
    return 1 if s['overlap_pages'] or s['outside_pages'] else 0
    for p in r['pages']:
        print(f"  p{p['page']:>3}  words {p['words']:>6}  small {p['small_share']:.2f}  median-h/w {p['median_height_over_width']}")


if __name__ == '__main__':
    sys.exit(main())
