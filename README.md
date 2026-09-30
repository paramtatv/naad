# नाद · Naad

**From Paramtatva — a frontier computing lab.**

**Natural Acoustic Audio Dynamics** — a lossless audio codec whose entire decoder
is 1,182 lines of Sanskrit, compiled to 64-bit RISC-V, with no foreign code
beneath it.

The public page is [`index.html`](index.html). It is a static file with no build
step and no dependencies: open it, or serve the directory.

## What is measured

| | |
|---|---|
| Compression vs `flac -8` | **+0.1%** — parity, on 64 of 64 files of the official IETF FLAC test corpus |
| Decode speed | **6× real time** — 1,814 instructions per channel-sample at 44.1 kHz, at 1 GHz and 1 IPC |
| Reconstruction | **bit-exact** — the same integers in and out |
| Decoder size | **1,182 lines**, 21 public routines |
| Foreign code in the decode path | **0** |

Every figure is reproducible from the Śravaṇa repository on the named corpus at
the stated setting.

## What is not finished

The frame decoder is complete and verified on two independent engines. The
container layer — walking a file of frames, seeking, metadata — is in progress,
as is support for more than two channels and a command-line encoder and player.
Naad is a verified codec core, not yet a drop-in player. The page says so too.

## Enquiries

<naad@paramtatv.org>

Naad is one of several things Paramtatva builds on Sassembly. The lab works on
the layer most of the industry treats as settled — the language, the instruction
set, the compiler — on the view that a stack you cannot read to the bottom is a
stack you do not own.

## On the claims

The page deliberately does **not** claim that Naad sounds better than other
lossless codecs. Lossless decoding returns an identical bitstream; two correct
lossless decoders produce byte-identical output. A codec that promises a
different *sound* is either not lossless or not honest, and an audiophile
audience is precisely the one that knows this. What Naad claims instead is
verifiability: enumerated code spaces rather than sampled ones, CRCs anchored to
published check values, and a decoder short enough to read in full.
