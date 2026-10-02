# नाद · Naad

**From Paramtatva, a frontier computing lab.**

A lossless audio decoder you can read to the bottom: integer arithmetic only, <!--fig:lines-->1,547<!--/fig--> lines
of Sanskrit, compiled to 64-bit RISC-V, with no foreign code beneath it. One stream decodes
to one file on every machine, forever, and you can check.

The public page is [`index.html`](index.html), a static file with no build step, live at
<https://paramtatv.github.io/naad/>. The provenance of every number on the page is
[`figures.json`](figures.json), and `tools/check-figures.py` refuses the page, and this
file, when they disagree with it. The decoder's source is in [`kernel/`](kernel/); where it
came from is in [`kernel/PROVENANCE.md`](kernel/PROVENANCE.md).

## What is measured

Read [`figures.json`](figures.json); it is the source and this table is a mirror that the
check keeps in step.

| | |
|---|---|
| Decoder | **<!--fig:lines-->1,547<!--/fig--> lines, <!--fig:routines-->32<!--/fig--> public routines**, two files, <!--fig:foreign-->0<!--/fig--> foreign lines in the decode path |
| A whole recording | the Grieg file on the page, decoded end to end on the native image to **<!--fig:whole_pcm_octets-->44,378,214<!--/fig--> bytes** of PCM whose MD5 equals the one in the file's own header |
| Conformance | EBU SQAM: **<!--fig:sqam_match-->70<!--/fig--> of <!--fig:sqam_files-->70<!--/fig-->** files decode to the MD5 their own encoder stored. IETF subset: **<!--fig:ietf_pass-->57<!--/fig--> of <!--fig:ietf_files-->64<!--/fig-->**, the other <!--fig:ietf_declined-->7<!--/fig--> have more than two channels and are declined by design. IETF faulty set: **<!--fig:faulty_clean-->11<!--/fig--> of <!--fig:faulty_files-->11<!--/fig-->** end in a named status. No file produced wrong audio |
| Verification | all <!--fig:typecodes-->64<!--/fig--> subframe type codes and all four header code spaces enumerated; <!--fig:frames-->10<!--/fig--> whole frames graded; <!--fig:mutations-->17<!--/fig--> kernel mutations each caught |
| Decode cost | **<!--fig:walker_ipcs-->3,076<!--/fig--> instructions per channel-sample** on the path the product runs, the whole-record decoder reading a real 24-bit file; **<!--fig:realtime-->3.4×<!--/fig--> real time** for that recording is a projection at 1 GHz and one instruction per cycle, not a silicon timing |
| Determinism | one image on <!--fig:attest_hosts-->3<!--/fig--> machines and <!--fig:attest_isas-->2<!--/fig--> instruction sets: one audio digest and one instruction count |
| Encoder, a separate program in Python | **<!--fig:ratio-->+0.1%<!--/fig-->** vs `flac -8` on <!--fig:corpus-->64 of 64<!--/fig--> IETF test files, as an exact bit count; a simpler emitter writes real files at <!--fig:emit_ratio-->+1.44%<!--/fig--> on one file; the join between the two is open |

## What is not finished

There is no player: no seeking, no tags or cover art, no playback surface. More than two
channels is declined rather than guessed. The file walker still owes a bound on every
single read (a safety floor does that job today, at a cost in speed), and files whose
header block is not the first block are refused. The same digest on a third instruction
set is owed. The encoder is Python; none of it is written in Sassembly yet.

Naad is the codec. Śravaṇa is the programme it opens, whose aim is neural-quality audio
with an integer-only decoder. Nothing above the lossless stratum ships.

## Licence

GNU Affero General Public License, version 3 only; see [`LICENSE`](LICENSE). That covers
the decoder source in `kernel/`.

## Working on the page

    python3 tools/check-figures.py     # before every commit
    sh tools/verify-deploy.sh          # after a deploy to main

See [`HANDOFF.md`](HANDOFF.md) for the positioning, the claim ladder and the constraints.

## Enquiries

<naad@paramtatva.org>
