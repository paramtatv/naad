# Naad page — the spec, and the mechanisms that keep it honest

Live: https://paramtatv.github.io/naad/ · source `index.html`, a single file with no
build step · `figures.json` is the provenance of every number on it · `kernel/` is the
decoder the page describes, vendored at the commit the figures were taken from.

**This branch (`redesign`) is not public.** Pages deploys on push to `main`. Nothing
here goes to `main` until the owner has seen it and said so.

## 1. Positioning, in one sentence

Naad is a lossless audio decoder you can read to the bottom: integer arithmetic only,
1,182 lines of Sanskrit, on a compiler that rebuilds itself byte for byte, so one stream
decodes to one file on every machine, forever, and you can check.

The page sells **verifiability**, not sound. Two correct lossless decoders return the
same bytes, so a lossless codec has no sound claim to make, and the earlier page's only
remaining material was "it is Sanskrit and we were careful". The claim that is true today,
unique, and citeable is reproducibility. The thesis in `sravan/THESIS.md` is the source of
the argument (§1, §3), and the page presents that thesis as **the programme**, with Naad
as its first stratum. Nothing above S1 is described as available.

## 2. Audiences, and the order they appear

1. Archives and broadcast: fix a digest at ingest, check it in 2056.
2. Reproducible research and forensic: the same integers in every lab.
3. Engineers who audit their stack: no runtime, no dependency tree, 12 MB.
4. Products and silicon: **later**, and the page says why (no stream or container layer).

The earlier page led with DJs and OEMs. A decoder that cannot open a file cannot serve
either, and the thesis's own §9 names the audiences above as the ones who would miss
bit-exact audio if it did not exist.

## 3. The claim ladder

Every figure on the page carries one of three tags, and the tag is part of the figure:

| tag | means | examples |
|---|---|---|
| **measured** | taken from a named repository at a named commit with a named command | 1,182 lines · 17 kernel mutations · +0.1% vs flac -8 |
| **projected** | computed from a measurement under a stated assumption | 6× real time, from 1,814 instructions/channel-sample at 1 GHz and 1 IPC; not timed on silicon |
| **planned** | a completion condition, written before the work | one digest on 3 instruction sets |

Two figures the earlier page conflated are now kept apart on purpose: the **encoder's**
+0.1% on 64 of 64 IETF files (Python, an exact bit count, join open) and the **decoder's**
10 frames, 78 headers and 64 type codes (`.t1`, both engines). "Naad clears all 64" was
the Rust decoder in `crates/nada`, which is a different program.

## 4. The mechanisms

**`figures.json` + `tools/check-figures.py`.** Every number on the page is a
`<span data-fig="id">` whose text must equal the value in `figures.json`, which carries
metric, status, source (repo, commit, file or section) and the command to take it again.
The check is three-way: page agrees with file, file is fully used by the page, and the two
figures the page can re-take itself (lines, routines) still agree with `kernel/`. It was
tested red on a changed figure and on a changed kernel before it was trusted. Run it before
every commit; a CI step on `main` should run it on push.

**`kernel/`.** `sravan` is **private**, so a link there 404s for the public and "reproducible
from the repository" was not true for anyone outside the lab. The two kernel files are
vendored here at `6b0001e`, which is where 1,182 lines and 21 routines were read. Updating
them means re-taking every figure in `figures.json` that cites a commit, not only the two
the check re-takes. `kernel/PROVENANCE.md` says which commit.

**`tools/hero-window.py`.** The hero scope draws **real audio**: 900 samples from
`sravan/vectors/real_audio.txt` at offset 4,650, and the residual under the fixed order-2
predictor, computed in the browser, on one shared vertical scale. The earlier page drew
synthetic sine waves plus random noise on a page whose ethos is that every figure was
measured. Constraint 4 below is that this never happens again.

**`tools/verify-deploy.sh`.** Compares the live page's `<meta name="naad-build">` stamp
and byte count to the checkout. Bump the stamp on every revision. Two instruments because
one was fooled before: a content grep matched a substring that survived between versions.

## 5. Constraints on the copy

1. **Never claim Naad sounds better than another lossless codec.** Bit-identical output is
   bit-identical. The audiophile audience is exactly the one that knows this.
2. **Every number is a `data-fig` span with provenance in `figures.json`.** A number in
   prose without a span is a defect; the check will not see it.
3. **The frontier section stays**, and now includes attestation as "not yet taken for
   Naad", because the page must not read as attested when it is only deterministic.
4. **Nothing synthetic on the page.** No generated waveforms, no illustrative numbers.
5. **Sassembly is a language and toolchain that compiles to RV64IMA.** It is not an
   instruction set architecture, and the earlier page said it was.
6. Say **projected** wherever a figure rests on an assumed clock or IPC.

## 6. Names

Naad is the codec. Śravaṇa is the programme it opens. The page says this once, in the
footer. The backronym "Natural Acoustic Audio Dynamics" is gone; the page's own best line
is that nāda is sound considered as vibration. Still open, owner's call: the display name
**Paramtatva** against the domain and org `paramtatv`; the Rust crate `nada` in the
monorepo and Darśana's planned D6 `नाद`, which are two more spellings of the same word.

## 7. What is next, in order

1. **Owner review of this branch.** Nothing is public until then.
2. **Attestation of S1** (`decode_hash_agreement` at k = 3 on Naad's decoder). The thesis
   lists it as step 2 of its own build order, Darśana has the machinery, and it turns the
   page's one **planned** rung into a **measured** one.
3. **The decoder on the page.** Build `nihshesha.t1` with the SQAM frame the thesis timed
   baked in, run it on `yantra-wasm` in the browser (`sansos/tools/build-sassembly-web.sh`
   emits a self-contained page; the machine takes an empty import object), stream samples
   out over the console call, draw the real decoded waveform, and show the digest beside the
   reference digest. User-supplied frames wait on the RAM-injection path (`wt-raminject`).
4. Self-host the two font families. Add an `og:image` card for Naad (the one in
   `brand-assets/` is Paramtatva's). Decide on analytics or decide against them in writing.
5. Generate `figures.json` from `sravan` metrics rather than by hand, once `sravan` keeps a
   metrics file.

## Known-open

- `realtime_factor` improves when the octet-wise CRC lands; CRC-16 is 37.1% of decode
  time. The proof sheet, the frontier and `figures.json` all carry the figure; change all
  three or the check goes red.
- The `sravan` working tree already reads 1,290 lines and more routines than `6b0001e`.
  The page is pinned to the commit, deliberately, until the figures are re-taken together.
