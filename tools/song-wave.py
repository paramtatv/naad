#!/usr/bin/env python3
"""Regenerate the Listen section's recording data from its public-domain source.

The recording is Grieg, Peer Gynt Suite No. 1, IV. In the Hall of the Mountain
King, performed by the Musopen Symphony, released to the public domain, hosted
on Wikimedia Commons as a 24-bit / 48 kHz FLAC. This script:

  1. downloads the original FLAC from Commons (25.8 MB; not kept in the repo);
  2. writes wave.json: 1,800 columns of [min, max, rms] over the whole piece,
     from a mono mix, which the page draws as the waveform;
  3. copies the original, unchanged, to grieg-mountain-king.flac (the master the
     page plays), and encodes it with the Vorbis encoder at 96 and 160 kbps to
     grieg-mountain-king-96k.ogg and -160k.ogg, the Normal and High stream
     settings the page lets the listener switch against;
  4. prints the loudness of the opening against the ending, which is where
     the "sixteen times louder" figure in figures.json comes from.

Needs ffmpeg and ffprobe on PATH. Run from the repository root:

    python3 tools/song-wave.py
"""
import array, json, math, os, subprocess, sys, urllib.request

SRC = ("https://upload.wikimedia.org/wikipedia/commons/8/84/"
       "Grieg_-_Peer_Gynt_Suite_No._1%2C_Op._46_-_IV._In_the_Hall_of_the_Mountain_King_%28Musopen_Symphony%29.flac")
UA = "naad-page/1 (naad@paramtatv.org)"
COLS = 1800

tmp = "/tmp/naad-song.flac"
if not os.path.exists(tmp):
    subprocess.run(["curl", "-sL", "-A", UA, "-o", tmp, SRC], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-ac", "1", "-f", "f32le", "-acodec", "pcm_f32le", "/tmp/naad-mono.f32"], check=True)
import shutil; shutil.copyfile(tmp, "grieg-mountain-king.flac")
for kbps in (96, 160):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-c:a", "libvorbis", "-b:a", f"{kbps}k", f"grieg-mountain-king-{kbps}k.ogg"], check=True)

a = array.array("f"); a.frombytes(open("/tmp/naad-mono.f32", "rb").read()); n = len(a); sr = 48000
step = n / COLS; env = []
for c in range(COLS):
    seg = a[int(c * step):int((c + 1) * step)]
    env.append([round(min(seg), 3), round(max(seg), 3), round(math.sqrt(sum(x * x for x in seg) / len(seg)), 3)])
json.dump({"cols": COLS, "duration": round(n / sr, 3), "excerpt": [0, round(n / sr, 3)], "env": env},
          open("wave.json", "w"), separators=(",", ":"))

def rms(s, e):
    seg = a[int(s * sr):int(e * sr)]; return math.sqrt(sum(x * x for x in seg) / len(seg))
o, e = rms(0, 10), rms(140, 150)
print(f"opening 0-10 s: {20*math.log10(o):.1f} dBFS   ending 140-150 s: {20*math.log10(e):.1f} dBFS   ratio {e/o:.1f}x", file=sys.stderr)
