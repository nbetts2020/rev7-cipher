# How the key was found

Verifying the solve needs none of this — `solution/verify_portable.py` is
stdlib-only Python and checks the whole chain on its own. This directory
answers the other question: *how was key `1947038265` discovered, and how were
168 destroyed characters regenerated?*

## The idea

Reversing the paper and inverting the surviving AMSCO columns gives back a
1,260-character layout in which 1,092 characters are known and **168 are
unknown** — the ones the buggy column-0 loop threw away. Those unknowns are not
scattered randomly: for a given key they sit at fixed, computable offsets, two
per 15-character row.

CFB8 is what makes this tractable. Each ciphertext byte depends only on the
preceding ciphertext, so the plaintext can be walked left to right, and any
prefix that decrypts to something outside the allowed text repertoire can be
abandoned before its subtree is ever explored. The unknown nibbles become a
depth-first constraint search with aggressive pruning rather than a
2^672 enumeration.

The allowed repertoire is printable ASCII plus a small set of well-formed UTF-8
typography — the curly quotes and apostrophes that appear in the message. That
gate is in `transition()` in `zero_column/recover.cpp`. **No plaintext crib is
supplied**; the search is never told what the message says.

## Reproducing it

Build the solver first — `lib/BUILD.md` has the exact steps, including the
libmcrypt 2.5.8 configure line and the separately built `extras.dylib`. Then:

```sh
python3 -B search/zero_full/targeted_reproduce.py
```

It runs in under a second, reads `cipher.txt`, projects it back through the
AMSCO layout with column 0 masked, hands the masked pattern to the solver, and
asserts that exactly 64 completions come back — all of them `blowfish-compat`,
IV fill `0x30`, language class 1. It cross-checks them against the recorded
`zero_full/candidates_decoded.json` and writes `targeted_results.json`.

Selecting candidate 18 happens **after** enumeration and is a reading judgment,
not a solver output. The script is explicit about this.

One piece runs with no build at all:

```sh
python3 -I lib/zero_projection.py
```

That is the AMSCO projection's own self-test: 200 randomized cases checked
against `lib/literal_models.py`, a literal Python translation of the 2016 PHP
class, confirming the forward projection and the dropped-column model agree
with the original algorithm.

## What the sweep actually covered

The key was found by sweeping the signed-32-bit-safe subset of 10-digit
non-leading-zero permutations — **416,400 keys** of the **3,265,920** total.
Two workers split it by ordinal parity:

| Worker | Status | Keys guaranteed complete | Cases | Candidates |
|---|---|---:|---:|---:|
| 1 | Completed | 208,200 | 126,585,600 | 64 |
| 0 | Interrupted after the solution was confirmed | 170,000 (last checkpoint) | 103,360,000 | 0 |
| | | **378,200** | **229,945,600** | **64** |

Worker 1 finished in 534 seconds. So 378,200 keys are *guaranteed* swept; at
least 38,200 keys inside the signed-32-bit-safe subset were never reached,
because worker 0 was stopped once the answer was in hand rather than run to
completion.

The remaining **2,849,520** keys exceed signed 32-bit range and were not
searched in this pass at all. Nothing here supports a uniqueness claim over the
full key space, and this pass is not reported as a negative result for the keys
it did not reach.

Independent Python and C++ implementations agree on the enumeration, the
per-shard key sums and the zero-position counts. Five planted keys exercising
both shards were recovered correctly, and unchanged PHP execution confirmed all
five outer encryptions.

## Files

| Path | What it is |
|---|---|
| `zero_full/targeted_reproduce.py` | The reproduction entry point described above |
| `zero_full/targeted_results.json` | Its recorded output |
| `zero_full/candidates_decoded.json` | All 64 candidates as recorded by the original run, used as the cross-check |
| `zero_column/recover.cpp` | The solver: DFS over unknown nibbles with CFB8 pruning, memoization and a text-repertoire gate |
| `zero_column/recovery_support.inc` | Shared helpers for the recovery tools |
| `../lib/search.cpp` | Algorithm registry and CFB8/ECB/CBC probes; compiled into `recover` |
| `../lib/zero_projection.py` | Forward and inverse AMSCO projection, with self-test |
| `../lib/literal_models.py` | Literal Python translation of the 2016 PHP class, used only to check the projection |
| `../lib/BUILD.md` | How to build libmcrypt, `extras.dylib` and the solver |

A final honesty note: this reproduces a construction that matches the paper
exactly. It does not establish which software the original author actually used
to produce it.
