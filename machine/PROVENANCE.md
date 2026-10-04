# Where these two files come from

Both are served from this site and nothing else, as the owner's ruling of 2026-10-02 requires.

| file | octets | md5 | source |
|---|---|---|---|
| `yantra_wasm.wasm` | 106,007 | 3131f4507b1ac65b4854603089594158 | `paramtatv/sansos` trunk at f985af41 (loader RAM floor = file-backed extent, stores bounded on the budget, W-363; earlier copy 105,813 octets from 65736af1), `crates/yantra-wasm`, built with `cargo build -p yantra-wasm --target wasm32-unknown-unknown --release` (rustc stable, `wasm32-unknown-unknown`), on 2026-10-02 |
| `walker.elf` | 103,696 | 6c95b378f44f124f3185a9a9916b8b26 | the Śravaṇa whole-file walker from sravan main eff3245 (`kernel/pariksha_i.t1` with `nihshesha.t1` and `mapana.t1`; the `kernel/` beside this directory is the same commit), built by sravan's own `tools/build-walker.sh` invocation (the compiler supplies `ashtaka`) with `t1_image` from sansos 3309cb42, the pin in sravan's `tools/PIN`; built identically by two lanes on 2026-10-04. Replaced r58's image (107,544 octets, md5 aab6bf1b…, sravan 249e608 under 34c9712a) at r59. Every `walker_*` and `jetson_*` figure on the page was taken from this image; in this page's machine it runs at 32 MiB to the same 202,190,979 instructions as natively |

The page's "Run it here" block loads these two, cuts the first 87,464 octets off
`grieg-mountain-king.flac`, hands them to the machine through `yantra_input_alloc`, and
holds the result to the page's own figures: the SHA-256 of ffmpeg's decode of those ten
frames and the executed-instruction count `walker_steps10`. Nothing leaves the browser.

Both are AGPL-3.0-only, like the rest of this repository. To update: rebuild from the
commits named in `figures.json`, replace both files, and re-take every figure that names
them, together, in one change.
