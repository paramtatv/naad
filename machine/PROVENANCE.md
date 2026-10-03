# Where these two files come from

Both are served from this site and nothing else, as the owner's ruling of 2026-10-02 requires.

| file | octets | md5 | source |
|---|---|---|---|
| `yantra_wasm.wasm` | 105,813 | d048c7aac3de67a4732ad7d9852b0174 | `paramtatv/sansos` trunk at 65736af1, `crates/yantra-wasm`, built with `cargo build -p yantra-wasm --target wasm32-unknown-unknown --release` (rustc stable, `wasm32-unknown-unknown`), on 2026-10-02 |
| `walker.elf` | 107,544 | aab6bf1b4c3c06874cf33b413b02a004 | the Śravaṇa whole-file walker, `kernel/pariksha_i.t1` at main 249e608 with `nihshesha.t1` and `mapana.t1` (the `kernel/` beside this directory is the same decoder at 249e608), compiled by `t1_image` from the sansos tree 34c9712a; the image every `walker_*` figure on the page was taken from. Replaced on 2026-10-02 23:10 EDT with the per-read bound; the earlier image was 98,936 octets, md5 66feb91e… |

The page's "Run it here" block loads these two, cuts the first 87,464 octets off
`grieg-mountain-king.flac`, hands them to the machine through `yantra_input_alloc`, and
holds the result to the page's own figures: the SHA-256 of ffmpeg's decode of those ten
frames and the executed-instruction count `walker_steps10`. Nothing leaves the browser.

Both are AGPL-3.0-only, like the rest of this repository. To update: rebuild from the
commits named in `figures.json`, replace both files, and re-take every figure that names
them, together, in one change.
