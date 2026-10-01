#!/usr/bin/env python3
"""Refuse index.html when any figure on it disagrees with figures.json.

Three checks, each of which can go red on its own:
  1. every <span data-fig="ID">TEXT</span> in index.html has an entry in
     figures.json and TEXT equals that entry's value, character for character;
  2. every figure in figures.json appears on the page at least once, so a
     figure cannot be quietly dropped while its provenance stays green;
  3. the two figures the page can take for itself, lines and routines, are
     re-taken from kernel/ and must still agree.

Exit status is the number of failures. Prints nothing on green except OK.
"""
import json, re, subprocess, sys, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
html = (root / "index.html").read_text(encoding="utf-8")
figs = json.loads((root / "figures.json").read_text(encoding="utf-8"))["figures"]

fails = []
seen = set()
for m in re.finditer(r'data-fig="([^"]+)"[^>]*>([^<]*)<', html):
    fid, text = m.group(1), m.group(2).strip()
    seen.add(fid)
    if fid not in figs:
        fails.append(f"page uses data-fig={fid!r} which figures.json does not define")
    elif text != figs[fid]["value"]:
        fails.append(f"{fid}: page says {text!r}, figures.json says {figs[fid]['value']!r}")

for fid in figs:
    if fid not in seen:
        fails.append(f"{fid}: defined in figures.json but not on the page")

def retake(cmd):
    return subprocess.run(cmd, shell=True, cwd=root, capture_output=True, text=True).stdout

lines = routines = None
if (root / "kernel" / "nihshesha.t1").exists():
    lines = sum(int(l.split()[0]) for l in retake("wc -l kernel/nihshesha.t1 kernel/mapana.t1").splitlines() if "total" not in l)
    if f"{lines:,}" != figs["lines"]["value"]:
        fails.append(f"lines: kernel/ has {lines:,} lines, figures.json says {figs['lines']['value']}")
    routines = sum(int(l.split(":")[-1]) for l in retake("grep -c 'सार्वजनिक वृत्तिः' kernel/nihshesha.t1 kernel/mapana.t1").splitlines())
    if str(routines) != figs["routines"]["value"]:
        fails.append(f"routines: kernel/ has {routines}, figures.json says {figs['routines']['value']}")

for f in fails:
    print("RED", f, file=sys.stderr)
if not fails:
    print(f"OK {len(seen)} figures on the page agree with figures.json; " + (f"kernel/ re-taken: {lines:,} lines, {routines} routines" if lines is not None else "kernel/ not vendored (withheld pending licence), lines and routines carried from figures.json"))
sys.exit(len(fails))
