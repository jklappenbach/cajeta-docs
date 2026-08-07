# cajeta-docs

`dev.cajeta.docs` — **the** text/document library for the cajeta
ecosystem. One parse produces a structured model and every consumer
selects a granularity from it, rather than re-parsing:

- **The dual-view model** — a logical tree (document · section ·
  paragraph · sentence · list · table · code block · element) plus an
  orthogonal physical page/line view over the same canonical text. A
  paragraph spanning a page break is *one* paragraph on *both* pages.
- **Provenance everywhere** — every node at every granularity resolves
  document (content hash + version + source), character range, pages,
  and section path. A chunk without provenance is not valid output.
- **Elements are first-class** — images (bytes retrievable), tables
  (structured, round-tripping to `nucleo.frame.DynFrame`), charts,
  equations (source form retained), footnotes (linked to their
  reference site).
- **Readers** — text, Markdown, HTML, CSV/JSON (via `cajeta.codec`).
  Source code, OOXML, and PDF land when their prerequisites exist
  (cajeta-codec XML, cajeta-font). Document input is untrusted by
  definition: every reader is bounded and fuzzed.
- **Text pipeline** — Unicode normalization via `cajeta.lang.String`,
  configurable tokenization with offsets, rule-based sentence
  segmentation, a documented English stopword list.
- **Vectorization** — count and TF-IDF over `CsrMatrix`, sklearn-1.9.0
  variant-exact; chunking that never splits a table or code block;
  BPE/WordPiece against published vocabularies, token-for-token.

**Deliberately depends on no other cajeta library** (spec §12.7): the
`Transformer` adapter for `dev.cajeta.ml` ships with ml, not here.

## Build, test, tour

```
./run-tests.sh    # unit suite (cajeta-unit reflective @Test discovery)
./run-tour.sh     # self-checking tour
cajeta build      # emit build/archive/dev.cajeta.docs-<version>.cja
```
