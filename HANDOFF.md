# Naad page — state, and the three constraints that shaped it

Live: https://paramtatv.github.io/naad/ · source `index.html` (single file, no
build step) · `logo.svg`, `concert.svg`, `devices.svg` are hand-authored vectors.

## Page order (deliberate, changed late)

hero → **live/concert** → **hardware** → what you get → enquire → *then* the
engineering (proof, Sassembly, frontier) → footer.

Euphoria first, technical proof below the fold. An earlier version led with the
spec sheet and it read as a lab report.

## Three constraints on the copy

1. **Never claim Naad sounds better than another LOSSLESS codec.** Bit-exact
   output is bit-identical output; two correct lossless decoders produce the
   same bytes. The audiophile audience is exactly the one that knows this, and
   the claim would cost every reader worth having. The legitimate and bolder
   claim is against **lossy** — what streaming actually serves.

2. **Every number on the page is one that was measured**, on a named corpus at
   a stated setting. The load-bearing ones:

   | figure | what it is |
   |---|---|
   | `+0.1%` vs `flac -8` | parity across 64/64 IETF test files — deliberately NOT a headline |
   | `6×` real time | 1,814 instructions/channel-sample at 1 GHz, 1 IPC |
   | `0.0000%` frame-to-frame drift | model predicted 12,097,471 instructions, measured 12,097,471 |
   | `1,182` lines / `0` foreign | `kernel/*.t1` in the sravan repo; no .rs/.c/.cpp in the decode path |
   | `12 MB` | the whole Sassembly toolchain |

   If a number changes in the sravan repo, it changes here.

3. **The frontier section stays.** It names six places Naad is behind the state
   of the art, each with what the gap measures. Deleting it would make the rest
   read as marketing. A codec that will not say where it is weak is one nobody
   can plan around.

## Known-open

- The display name is **Paramtatva** while the domain and org are `paramtatv`
  (`naad@paramtatv.org`, `github.com/paramtatv`). Not yet reconciled.
- `realtime_factor` will improve when the octet-wise CRC lands — CRC-16 is
  currently 37% of decode time. The frontier section says so and should be
  updated when it does.
- Pages deploys on push to `main`, ~40s. **Verify by comparing byte size to the
  local file**, not by grepping for a string — a content grep matched a
  substring that survived between versions and reported a deploy that had not
  happened.
