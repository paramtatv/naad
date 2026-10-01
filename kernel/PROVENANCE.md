# Where these files come from

Copied verbatim from `paramtatv/sravan` at commit `6b0001e` (2026-09-30, "S1: a whole
FLAC frame decodes natively, from its bits alone"):

| file | lines | public routines |
|---|---|---|
| `nihshesha.t1` | 1,051 | 17 |
| `mapana.t1` | 131 | 4 |

That is the 1,182 lines and 21 routines the page quotes. `tools/check-figures.py`
re-takes both from these files on every run.

`sravan` is private. These copies exist so that "read the decoder" is a link that works
for the public. They are not edited here; to update them, copy from a newer commit and
re-take every figure in `figures.json` that names a commit.

BSD 3-Clause, as in the source repository.
