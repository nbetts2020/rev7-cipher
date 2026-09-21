# How the key was found

Verifying the solve needs none of this, as this directory
answers the other question: *how was key `1947038265` discovered, and how were
168 destroyed characters regenerated?*

## Idea

Reversing the paper and inverting the surviving AMSCO columns gives back a
1,26--character layout in which 1,092 characters are known and **168 are
unknown** - the ones the buggy column-0 loop threw away. Those unknowns are fortunately not
scattered randomly. For a given key they sit at fixed, computable offsets, two
per 15-character row.

CFB8 is what makes this tractable. Each ciphertext byte depends only on the
preceding ciphertext, so the plaintext can be walked left to right, and any
prefix that decrypts to something outside the allowed text repertoire can be
abandoned before its subtree is ever explored. The unknown nibbles become a
depth-first constraint search with aggressive pruning.

## What the sweep actually covered

The key was found by sweeping the signed-32-bit-safe subset of 10-digit
non-leading-zero permutations, including **416,400 keys** of the **3,265,920** total.
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
searched in this pass at all.

Independent Python and C++ implementations agree on the enumeration, the
per-shard key sums and the zero-position counts. Five planted keys exercising
both shards were recovered correctly, and unchanged PHP execution confirmed all
five outer encryptions.
