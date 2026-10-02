# Where these files come from

Copied verbatim from `paramtatv/sravan` at commit `d27391f` (2026-10-02, "Merge stream:
Sravana's AGPL relicence, the IETF/SQAM conformance work, and the W-338 write-up"):

| file | lines | public routines |
|---|---|---|
| `nihshesha.t1` | 1,416 | 28 |
| `mapana.t1` | 131 | 4 |

That is the 1,547 lines and 32 routines the page quotes. `tools/check-figures.py`
re-takes both from these files on every run.

`sravan` is a private repository. These copies exist so that "read the decoder" is a link
that works for the public. They are not edited here; to update them, copy from a newer
commit and re-take every figure in `figures.json` that names a commit, together, in one
change.

**Licence: GNU Affero General Public License, version 3 only**, the same text as this
repository's `LICENSE` and the source repository's as of `d27391f`. History: an earlier copy
(from `85f90b2`, BSD 3-Clause at the time) was published here and withdrawn on 2026-10-01
while the licence was being settled; the owner ruled AGPL-3.0-only across all repositories on
2026-10-02 and approved restoring this copy the same day.

What is here is the decoder kernel: the frame decoder, the header reader and the resync,
with their bit-level helpers. The file walker that drives it over whole recordings
(`kernel/pariksha_i.t1` in the source repository) and its later safety fixes live on a
branch there and are cited by commit in `figures.json`; they are not vendored.
