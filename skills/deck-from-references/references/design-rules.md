# Design rules

These rules fix failures of crowded, small, uneven pages. Check them on the render.

## Size and density

- Suggested defaults, to calibrate against the audience and format: on a 16 x 9 cm
  page use body text of about 11 pt. Measure with `deck_audit.py`: aim for a median
  body word height of at least 1.75 percent of page width and at most about 150 words
  per page (formulas count extra). These are proposed defaults, not measurements
  of reference decks.
- One idea per page. If a page needs more, split it or move the detail to the
  speaker's notes or a backup page; never shrink the text to fit.
- Captions, source tags and footers may be smaller, but nothing the audience must
  read.

## Hierarchy and position

- Fixed order from top: navigation and progress, subsection tag, title, grey
  subtitle, body, source tag, closing bar, footer. The same positions on every page.
- Titles take one line (about 24 Japanese or 45 Latin characters at the title
  size). A two-line title costs the subtitle or a body line.
- Two accent colours with fixed roles: one for structure and links, one for contrast
  (roles, cases, supplementary experiments). No meaning carried by colour alone.
- At most three levels of emphasis on a page.

## Layout

- At most two columns; panels side by side have equal height; margins equal.
- Leave open space; a full page is a handout.
- Tables up to about five rows and three columns; otherwise use a list. Avoid
  mixed-script table cells with paragraph columns (baselines drift); use list items.
- Formulas: at most two displayed formulas per page; break a long formula; check
  the right edge for clipping.

## Figures and code

- A figure takes at least 40 percent of the page width; text inside figures is
  generated at the final size so labels are legible at the body size.
- A figure is cut out of the source, not edited: cut a box, trim blank margins, render at a
  higher resolution to enlarge. Never retouch, recolor, remove labels or change the aspect
  ratio; the source file stays untouched. `scripts/crop_source.py` makes the cut as a new
  image and records source, page, box and hashes in a manifest; the credit says the figure is
  cut out (and enlarged). Do not carry the page's margins or the source's own caption along.
- Figures come from the source or its cited originals first (credited as person, publication,
  title, figure and page); a figure made for the talk is a labelled schematic.
  Prefer a figure that already exists in the source or in a paper it cites; make one only
  when none can be found, and then label it on the page as an AI-created auxiliary figure
  (補助図) and list it in the plan with the searches that failed to find an original.
- Every figure has the explanation block: what is drawn, axes and colours, how to
  read it, source page. A schematic or a supplementary experiment (state who or what produced it; AI-written code is
  never called the speaker's own) carries a visible chip saying so.
- Code: follow [code pages](code-pages.md). One function or step per page, left
  column about 60 percent of the width at 7 pt or more, a numbered "look at" list on the
  right, no line counts in titles, provenance of the code stated. `deck_audit.py` may flag
  a code page as small text; that is expected for the code only.
- A root's shared example is the same cut-out at the same place on every subsection of that
  root, so the audience recognizes it; a method's specific example appears only on that
  method's pages ([roots and lenses](../../reading-reference/references/roots-and-lenses.md)).
- Boxes take the height of their content. The stage style's `\flowbox` is at least
  `\flowh` high, grows with its text, and shares the tallest height across the page; do
  not set a fixed box height and do not shrink text to make it fit. Before release,
  `deck_audit.py` must report no words drawn over each other and none outside the page
  (it exits 1 otherwise): an overflowing box, a label printed on text and a closing line
  running into the footer all show up there, without a LaTeX warning.

## Bilingual decks

Both languages share the layout and page count. Shorten each language separately to
fit; check both renders.
