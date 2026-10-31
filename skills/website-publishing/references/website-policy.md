# Website editorial boundary

1. Preserve source-of-truth separation: research lives in `research/`,
   mathematical verification in `lean/`, canonical English paper TeX in
   `writing/`, source variants in `reference/`, and pages in `website/`.
2. A website is another research **output**, not a replacement for the
   institute or an authoritative proof source.
3. Verify the public status of each page, CV item, talk, document link, and
   reference before publishing it. Never treat repository visibility as
   blanket consent to publish every tracked file.
4. Preserve permanent URLs and publication dates where possible; updating
   a paper's summary should not silently rewrite its historical claim.
5. Keep site generator specifics in the site's configuration or a
   generator-specific private reference. Generic advice must work without
   `loam-ssg`.
6. Prefer reviewed, human-initiated publication for profile and research
   changes; an agent may draft pages and verify links beforehand.
