#!/usr/bin/env python3
"""Refuse index.html when any figure on it disagrees with figures.json.

Four checks, each of which can go red on its own:
  1. every <span data-fig="ID">TEXT</span> in index.html has an entry in
     figures.json and TEXT equals that entry's value, character for character;
  2. every figure in figures.json appears on the page at least once, so a
     figure cannot be quietly dropped while its provenance stays green;
  3. the two figures the page can take for itself, lines and routines, are
     re-taken from kernel/ and must still agree;
  4. every figure that follows by arithmetic from files shipped beside the page
     or from other figures is re-derived and must still agree: the recording's
     format, length and sizes from its own STREAMINFO, the stream settings from
     the stream files' own headers, and the speed chain from
     the two measured step counts. A figure in this set is never typed by hand;
     change its inputs and copy what this script prints.

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

# 4. Derived figures. Inputs: the FLAC shipped beside the page (its STREAMINFO is the
# studio's own description of the recording), the 160 kbps stream beside it, and the two
# measured step counts walker_steps1 and walker_steps10. Real time is taken at THIS
# recording's sample rate and channel count, because the per-sample cost was measured on
# this recording and the page says "to play the master".
MACHINES = {  # clock in Hz times instructions per cycle; assumptions, named on the page
    "realtime": 1.0e9 * 1,    # the most pessimistic core anyone ships
    "rt_phone": 2.4e9 * 2,    # a phone's big core
    "rt_laptop": 3.5e9 * 3,   # a laptop core
}
def integer(fid):
    return int(figs[fid]["value"].replace(",", ""))

derived = {}
flac_path = root / "grieg-mountain-king.flac"
if flac_path.exists():
    flac = flac_path.read_bytes()
    if flac[:4] != b"fLaC" or (flac[4] & 0x7F) != 0:
        fails.append("grieg-mountain-king.flac does not begin with a STREAMINFO block")
    else:
        packed = int.from_bytes(flac[18:26], "big")   # 20 bits rate, 3 channels-1, 5 depth-1, 36 samples
        rate, channels = packed >> 44, ((packed >> 41) & 7) + 1
        depth, total = ((packed >> 36) & 31) + 1, packed & ((1 << 36) - 1)
        pcm = total * channels * depth // 8
        derived["whole_flac_octets"] = f"{len(flac):,}"
        derived["whole_pcm_octets"] = derived["whole_pcm_octets_proof"] = f"{pcm:,}"
        derived["song_fmt"] = f"{depth}-bit / {rate // 1000} kHz"
        derived["whole_secs"] = str(round(total / rate))
        derived["song_len"] = f"{total // rate // 60}:{total // rate % 60:02d}"
        ogg = root / "grieg-mountain-king-160k.ogg"
        if ogg.exists():
            derived["master_x"] = f"{round(len(flac) / ogg.stat().st_size)}×"
        # The stream tiles show the encoder SETTING, as services name their tiers; it is the
        # nominal bitrate in each file's own Vorbis identification header, not its average.
        for fid, name in (("s_norm", "grieg-mountain-king-96k.ogg"), ("s_high", "grieg-mountain-king-160k.ogg")):
            if (root / name).exists():
                head = (root / name).read_bytes()[:4096]
                at = head.find(b"\x01vorbis")
                if at < 0:
                    fails.append(f"{name}: no Vorbis identification header")
                else:
                    derived[fid] = str(int.from_bytes(head[at + 20:at + 24], "little") // 1000)
        share = integer("whole_ram_octets") / len(flac)   # memory high water against the file's own size
        derived["ram_share"] = "a quarter" if abs(share - 0.25) < 0.02 else f"{round(100 * share)}%"
        samples = integer("real_samples")
        derived["real_secs"] = f"{samples / rate:.3f}"
        derived["pcm_octets"] = f"{samples * channels * depth // 8:,}"
        derived["whole_ram_mb"] = f"{integer('whole_ram_octets') / 1e6:.1f}"
        block = 4096                                   # this file's frames, flac -a
        per_frame = (integer("walker_steps10") - integer("walker_steps1")) / 9
        derived["walker_frame_steps"] = f"{round(per_frame):,}"
        derived["walker_ipcs"] = f"{round(per_frame / (block * channels)):,}"
        per_second = per_frame * rate / block          # instructions per second of this recording
        derived["realtime"] = f"{MACHINES['realtime'] / per_second:.1f}×"
        derived["realtime_cd"] = f"{MACHINES['realtime'] / (per_frame * 44100 / block):.1f}×"   # the same cost at CD rate, stereo
        derived["rt_phone"] = f"{round(MACHINES['rt_phone'] / per_second)}×"
        derived["rt_laptop"] = f"{round(MACHINES['rt_laptop'] / per_second)}×"
        derived["core_phone"] = f"{round(100 * per_second / MACHINES['rt_phone'])}%"
        derived["core_phone_exact"] = f"{100 * per_second / MACHINES['rt_phone']:.1f}%"
        for fid, want in derived.items():
            if fid not in figs:
                fails.append(f"{fid}: derived as {want!r} but figures.json does not define it")
            elif figs[fid]["value"] != want:
                fails.append(f"{fid}: derived {want!r}, figures.json says {figs[fid]['value']!r}")

for f in fails:
    print("RED", f, file=sys.stderr)
if not fails:
    print(f"OK {len(seen)} figures on the page agree with figures.json; {len(derived)} re-derived from the recording and the step counts; " + (f"kernel/ re-taken: {lines:,} lines, {routines} routines" if lines is not None else "kernel/ not vendored (withheld pending licence), lines and routines carried from figures.json"))
sys.exit(len(fails))
