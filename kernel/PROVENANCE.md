# Where these files come from

Copied verbatim from `paramtatv/sravan` at commit `eff3245` (2026-10-04: the compiler pin moved to sansos 3309cb42, W-356; it carries 1dbc6ed, the STREAMINFO search, the metadata-chain refusals and the array guards). The copy before was `667f10d` (2026-10-03, "mid/side: halve
through signed names, so the shift is arithmetic under a compiler with W-333"). The previous copy
was `249e608` (2026-10-02, the per-read bound); the one change between them declares the two
mid/side temporaries signed and rewrites five margins about the right shift. Built by the
toolchain the page is pinned to, the two copies give the SAME decoder image, byte for byte
(see `machine/PROVENANCE.md`):

| file | lines | public routines |
|---|---|---|
| `nihshesha.t1` | 1,766 | 28 |
| `mapana.t1` | 141 | 4 |

That is the 1,907 lines and 32 routines the page quotes. `tools/check-figures.py`
re-takes both from these files on every run.

`sravan` is a private repository. These copies exist so that "read the decoder" is a link
that works for the public. They are not edited here; to update them, copy from a newer
commit and re-take every figure in `figures.json` that names a commit, together, in one
change.

**Licence: GNU Affero General Public License, version 3 only**, the same text as this
repository's `LICENSE` and the source repository's as of `eff3245`. History: an earlier copy
(from `85f90b2`, BSD 3-Clause at the time) was published here and withdrawn on 2026-10-01
while the licence was being settled; the owner ruled AGPL-3.0-only across all repositories on
2026-10-02 and approved restoring this copy the same day.

What is here is the decoder kernel: the frame decoder, the header reader and the resync,
with their bit-level helpers. The file walker that drives it over whole recordings
(`kernel/pariksha_i.t1` in the source repository) and its later safety fixes live on a
branch there and are cited by commit in `figures.json`; they are not vendored.
