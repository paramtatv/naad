#!/usr/bin/env python3
"""Refuse index.html when any figure on it disagrees with figures.json.

Seven checks, each of which can go red on its own:
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
  5. every figure README.md mirrors, marked <!--fig:ID-->VALUE<!--/fig-->, equals
     figures.json, so the repository's front page cannot fall behind the site.
  6. nothing above the engineering divider uses the words the handoff reserves
     for the engineering sections: decoder, codec, integer, instruction,
     bit-exact, frame, runtime, toolchain.
  7. the page and its images load nothing from another origin (hyperlinks are
     allowed, loads are not), use no beacon, socket, frame or import, and every
     local file or anchor they reference exists.

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
        # THE EMBEDDED TEST'S SLOPE (2026-10-04, P7): two measured counts, two derived figures.
        slope = (integer("t10_steps") - integer("t2_steps")) / 8
        derived["timing_retake"] = f"{round(slope):,}"
        derived["ipcs"] = f"{round(slope / 1024):,}"
        # THE MEASURED CLOCK, beside the modelled one (2026-10-03). jetson_wall is the median of
        # three wall-clock decodes of this whole recording on one Jetson core, the decoder
        # running inside the instruction emulator the page ships; jetson_steps is the count
        # those runs executed. From them and this file's own length: how many times longer
        # than the music the decode took, and the emulator's rate in millions per second.
        wall = float(figs["jetson_wall"]["value"])
        derived["jetson_rtf"] = f"{wall / (total / rate):.1f}×"
        derived["jetson_mips"] = f"{round(integer('jetson_steps') / wall / 1e6)}"
        for fid, want in derived.items():
            if fid not in figs:
                fails.append(f"{fid}: derived as {want!r} but figures.json does not define it")
            elif figs[fid]["value"] != want:
                fails.append(f"{fid}: derived {want!r}, figures.json says {figs[fid]['value']!r}")

# 5. README.md is public and mirrors some figures. Each mirrored value is wrapped in
# <!--fig:ID-->VALUE<!--/fig--> (invisible when rendered) and must equal figures.json.
readme = root / "README.md"
mirrored = 0
if readme.exists():
    for m in re.finditer(r"<!--fig:([a-z0-9_]+)-->(.*?)<!--/fig-->", readme.read_text(encoding="utf-8")):
        fid, text = m.group(1), m.group(2)
        mirrored += 1
        if fid not in figs:
            fails.append(f"README.md mirrors {fid!r} which figures.json does not define")
        elif text != figs[fid]["value"]:
            fails.append(f"README.md: {fid} says {text!r}, figures.json says {figs[fid]['value']!r}")
    if not mirrored:
        fails.append("README.md mirrors no figures; its numbers would be unchecked")

# 6. The fan sections, everything above the first ENGINEERING comment, talk like a
# listener (HANDOFF section 1). These words belong below the divider.
cut = html.find("ENGINEERING")
if cut < 0:
    fails.append("no ENGINEERING divider comment in index.html; the fan-voice check has nothing to cut at")
else:
    above = html[html.find("<body"):html.rfind("<!--", 0, cut)]
    above = re.sub(r"<(style|script|svg)\b.*?</\1>", " ", above, flags=re.S)
    above = re.sub(r"<[^>]+>", " ", above)
    for m in re.finditer(r"(?i)\b(decod\w*|codec\w*|integer\w*|instruction\w*|bit-exact|frames?|runtime|toolchain)\b", above):
        fails.append(f"fan section uses {m.group(0)!r}: ...{' '.join(above[max(0, m.start() - 40):m.end() + 20].split())}...")

# 7. Nothing is loaded from another origin, and nothing local is referenced that is not
# shipped. Owner's ruling, 2026-10-02: "No analytics scripts, tracking pixels, telemetry
# beacons, or external third-party assets shall ever be included on the site." A hyperlink
# the reader chooses to follow is not a load; everything else that names another host is.
OWN = "https://paramtatv.github.io/naad/"
ABSOLUTE = r"""(?:https?:)?//[A-Za-z0-9.-]+\.[A-Za-z]{2,}[^\s"'<>)]*"""
ids = set(re.findall(r'\bid="([^"]+)"', html))
hyperlinks = 0
def local(ref, where):
    path = ref.split("#")[0].split("?")[0]
    if path and not (root / path).exists():
        fails.append(f"{where} references {ref!r}, which is not shipped beside the page")
for m in re.finditer(r'<a\b[^>]*\bhref="([^"]*)"', html):
    ref = m.group(1)
    if re.match(r"https?://", ref):
        hyperlinks += 1
    elif ref.startswith("#"):
        if ref[1:] and ref[1:] not in ids:
            fails.append(f"link to {ref!r}, but no element on the page has that id")
    elif not ref.startswith("mailto:"):
        local(ref, "a link")
rest = re.sub(r"<a\b[^>]*>", " ", html)
for m in re.finditer(r'<meta\b[^>]*\b(?:property|name)="(?:og:url|og:image|twitter:image)"[^>]*\bcontent="([^"]*)"[^>]*>', rest):
    if not m.group(1).startswith(OWN):
        fails.append(f"share tag points off this site: {m.group(1)!r}")
    else:
        local(m.group(1)[len(OWN):], "a share tag")
rest = re.sub(r'<meta\b[^>]*\b(?:property|name)="(?:og:url|og:image|twitter:image)"[^>]*>', " ", rest)
rest = re.sub(r'\bxmlns(?::\w+)?="http://www\.w3\.org/[^"]*"', " ", rest)
for m in re.finditer(ABSOLUTE, rest):
    fails.append(f"the page names another host outside a hyperlink: {m.group(0)[:80]!r}")
for m in re.finditer(r'\b(?:src|poster|href)="([^"]+)"', rest):
    if not m.group(1).startswith(("#", "data:")) and not re.match(ABSOLUTE, m.group(1)):
        local(m.group(1), "the page")
for m in re.finditer(r"url\(\s*['\"]?([^'\")]+)", rest):
    if not m.group(1).startswith(("#", "data:")) and not re.match(ABSOLUTE, m.group(1)):
        local(m.group(1), "a stylesheet rule")
for m in re.finditer(r'sendBeacon|XMLHttpRequest|WebSocket|EventSource|<iframe|<object|<embed|http-equiv="refresh"|@import|gtag\(|googletagmanager|google-analytics', html):
    fails.append(f"the page uses {m.group(0)!r}, which this site does not allow")
for svg in sorted(root.glob("*.svg")):
    body = re.sub(r'\bxmlns(?::\w+)?="http://www\.w3\.org/[^"]*"', " ", svg.read_text(encoding="utf-8"))
    for m in re.finditer(ABSOLUTE + r"|<script", body):
        fails.append(f"{svg.name} names another host or carries a script: {m.group(0)[:80]!r}")

for f in fails:
    print("RED", f, file=sys.stderr)
if not fails:
    print(f"OK {len(seen)} figures on the page agree with figures.json; {len(derived)} re-derived from the recording and the step counts; {mirrored} mirrored in README.md; no off-site load, {hyperlinks} hyperlinks; " + (f"kernel/ re-taken: {lines:,} lines, {routines} routines" if lines is not None else "kernel/ not vendored (withheld pending licence), lines and routines carried from figures.json"))
sys.exit(len(fails))
