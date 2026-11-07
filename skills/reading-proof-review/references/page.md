# The page

Built by `scripts/build_review_page.py` from a spec directory:

- `steps.json`: the [ledger](ledger.md).
- `bodies.json`: per step `l1` (one line, always visible), `l2` (key reasoning, folded), `l3`
  (line-by-line proof, folded again). HTML; math is `<span class="m">TeX</span>` inline or
  `<div class="d">TeX</div>` display.
- `review.json`: title, `summary_html`, optional `intro_html`, `key_ideas_html`, `groups` (headings
  over lists of step ids), `step_review` (risk and evidence per step), `panel` rows, `findings`
  (`id`, `sev` fatal/major/minor/form, `status` confirmed/suspected/unchecked, `short`, `steps`,
  `from`, `detail` HTML, `ruling`), `prior` rows, `prior_hole`, `uncited`, `admitted`, `indicator`.
- `demo.html` (optional): a small self-contained snippet, with its own script, that lets the reader
  move a parameter of a lemma on synthetic data.

Layout: summary and verdict, the result, the proof spine (dependency diagram, then step cards),
the key-versus-standard table, the optional demo, the review, prior work, the indicator.

Fold levels: key steps open to their key reasoning, standard steps stay folded, so the look of the
page is itself the comparison. The side panel opens or closes everything; following a link opens the
folds above its target; printing opens all.

Write the page in the user's language (`--lang`). Say plainly that it is a local file, not
published. Text fields are escaped; HTML fields are trusted, so do not paste untrusted markup.

## Math

KaTeX is inlined for a single offline file; pass `--katex-dir` (or set `KATEX_DIR`) to a directory
holding `katex.min.js`, `katex.min.css` and `fonts/`. If only some fonts are available the builder
warns; do not use the commands those fonts would need (`\mathbb`, `\mathbf`, `\mathcal`, symbols
such as a filled star). Without KaTeX the TeX source stays visible.

## Checks

`check_review_page.py` verifies placeholders, ids, links, a card for every step and finding, and,
with node and KaTeX, every math span and script. It does not see the screen: also open the page,
or take a screenshot with a headless browser, and read the key cards, the comparison table, the
findings list and the verdict.
