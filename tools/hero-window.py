#!/usr/bin/env python3
"""Emit the hero scope's data from the real vector, so the page draws real audio.

Reads sravan/vectors/real_audio.txt (one line, comma-separated integers), finds
the 900-sample window of highest energy, and prints a JS literal of the
samples. The residual is computed on the page, in the browser, with the fixed
order-2 predictor the decoder implements: r[i] = s[i] - 2 s[i-1] + s[i-2].

    python3 tools/hero-window.py ../sravan/vectors/real_audio.txt

Paste the output over the SAMPLES line in index.html, then update win_offset,
win_peak and res_peak in figures.json from what this prints on stderr.
"""
import sys
path = sys.argv[1] if len(sys.argv) > 1 else "../sravan/vectors/real_audio.txt"
v = [int(x) for x in open(path).read().strip().split(",") if x.strip()]
N = 900
best = max(range(0, len(v) - N, 50), key=lambda s: sum(abs(x) for x in v[s:s + N]))
w = v[best:best + N]
res = [0, 0] + [w[i] - 2 * w[i - 1] + w[i - 2] for i in range(2, N)]
print(f"offset {best:,} peak {max(map(abs, w)):,} residual peak {max(map(abs, res)):,}", file=sys.stderr)
print("var SAMPLES=[" + ",".join(map(str, w)) + "];")
