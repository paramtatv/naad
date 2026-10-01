# नाद · Naad

**From Paramtatva, a frontier computing lab.**

A lossless audio decoder you can read to the bottom: integer arithmetic only, 1,290 lines
of Sanskrit, compiled to 64-bit RISC-V, with no foreign code beneath it. One stream decodes
to one file on every machine, forever, and you can check.

The public page is [`index.html`](index.html), a static file with no build step. The
decoder it describes is under [`kernel/`](kernel/), vendored at the commit every figure was
taken from. The provenance of every number on the page is [`figures.json`](figures.json),
and `tools/check-figures.py` refuses the page when the two disagree.

## What is measured

Read [`figures.json`](figures.json); it is the source and this table is a mirror.

| | |
|---|---|
| Decoder | **1,290 lines, 25 public routines**, two files, 0 foreign lines in the decode path |
| Reconstruction | **bit-exact** on two engines, for every layer of a FLAC frame, one or two channels |
| Verification | all 64 subframe type codes and all four header code spaces enumerated; 10 whole frames graded; 17 kernel mutations each caught |
| Decode cost | **1,500 instructions per channel-sample** on native RV64; **7.6× real time** is a projection at 1 GHz and 1 IPC, not a silicon timing |
| Encoder, a separate program in Python | **+0.1%** vs `flac -8` on 64 of 64 IETF test files, as an exact bit count; the join is open |

## What is not finished

Nothing walks a file of frames, seeks, or reads metadata. More than two channels is
refused rather than guessed. The decoder has not yet been attested across instruction
sets; it is deterministic, which is the precondition. Naad is a verified codec core, not
a player, and the page says so.

Naad is the codec. Śravaṇa is the programme it opens, whose aim is neural-quality audio
with an integer-only decoder. Nothing above the lossless stratum ships.

## Working on the page

    python3 tools/check-figures.py     # before every commit
    sh tools/verify-deploy.sh          # after a deploy to main

See [`HANDOFF.md`](HANDOFF.md) for the positioning, the claim ladder and the constraints.

## Enquiries

<naad@paramtatv.org>
