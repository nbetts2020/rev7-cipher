# Bounded full-keyspace zero-column benchmark

This report records the initial benchmark. The subsequently authorized complete signed-32-bit search is tracked separately in `SAFE32_RESULTS.md`; its results must not be inferred from the benchmark.

The optimized in-memory encode search completed **10,000 sampled numeric keys in 30.7137 seconds**, with **zero candidates and no capped cases**. No full-keyspace or multi-hour run was launched.

There are **3,265,920** nonleading-zero permutations of `0..9`: nine choices for the first digit and `9!` permutations of the rest. Of these, **416,400** fit a signed 32-bit integer: 362,880 begin with `1`, and 53,520 begin with `2`. Both counts were checked by complete enumeration. This is the malformed-key family confirmed by actual PHP execution in `../continuation_php_runtime/RESULTS.md`.

The benchmark selected permutation ordinals `floor(i * 3265920 / 10000)` for `i=0..9999`, after excluding leading-zero keys. It covers all nine possible zero-column positions, with 1,068–1,134 sampled keys at each position; 1,275 sampled keys are signed-32-bit-safe. It is not a lexicographic prefix and does not exhaust the safe subset.

| Completed check | Count |
|---|---:|
| Distinct sampled keys | 10,000 |
| Pre/post orientation combinations per key | 16 |
| CFB8 block primitives | 19 |
| IVs per primitive | 2 |
| Algorithm/orientation/IV cases | 6,080,000 |
| Cases rejected by fully determined plaintext bytes | 4,812,985 |
| DFS nodes in remaining cases | 70,146,718 |
| Full compatible candidates | 0 |
| Node-capped cases | 0 |
| Cases skipped for long contiguous erasure | 0 |

Every case uses inner key `Zombies`. IVs contain either zero bytes or ASCII `0` bytes. Pre/post orientations independently cover unchanged text, reversed hex characters, reversed byte order and swapped nibbles. The source is the observed 1,092-character uppercase hexadecimal text. An odd zero-column index omits one character per 15-character row and reconstructs a 1,170-character input; an even index omits two and reconstructs 1,260. Unknown positions remain unrestricted nibble erasures. No ciphertext digits are invented or fixed from a guessed plaintext.

One language pass includes printable ASCII plus tab/CR/LF, nonbreaking space, a specified set of UTF-8 punctuation sequences and an optional initial UTF-8 BOM. It contains the previous strict-ASCII language, so a negative does not need a redundant ASCII pass. It is **not all valid UTF-8**. The exact added sequences are `C2 A0`, `E2 80` followed by one of `93,94,98,99,9A,9B,9C,9D,9E,9F,A2,A6,AF`, and `EF BB BF` only at positions 0–2.

The implementation includes the existing recovery code unchanged for regression comparison. Its optimizations are:

- Construct the 16 masked input patterns directly in memory for each key, using the PHP-verified continuous 2,1 cell geometry.
- Precompute fully determined CFB positions for each zero-position/orientation/block-size layout. Check these positions sequentially and stop on the first impossible language transition. Unknown history uses the same relaxed language-state set as the original code.
- Delay copying an entire candidate into the DFS buffer until the necessary known-byte check passes.
- Enumerate only ciphertext byte values allowed by the nibble mask, in the same ascending order as the original 0–255 scan.

The DFS acceptance condition, memo key, key schedules, language transitions and 50-million-node per-case limit remain unchanged. Only fully explored failed states are cached. No cross-key rejection cache or unproven symmetry reduction is used. All sixteen orientations are retained even where a narrower equivalence might exist.

Validation passed **2,712 exact projection comparisons** against the independent PHP-validated Python index model. It also recovered every planted ciphertext and plaintext in **152 full-chain controls**. The original and optimized implementations emitted 66,113 complete compatible records with matching byte counts and two independently accumulated 64-bit stream digests, covering 171,004,033 output bytes without retaining that large stream. Those planted outer encryptions had already matched the unchanged original PHP in all 152 cases. The controls exercise every supported primitive, both IVs, both message geometries and ASCII/typographic plaintexts. Evidence is in `validation_results.json`, `controls.log`, and `../continuation_zero_column/php_planted_results.json`.

Linear extrapolation from this run is **10,030.8 seconds (2.79 hours)** for all nonleading-zero keys or **1,278.9 seconds (21.3 minutes)** for the safe 32-bit subset on one worker. Four workers would ideally reduce those to approximately 42 minutes and 5.3 minutes respectively, before contention and scheduling overhead. These are estimates, not measured full runs; the safe subset has a different zero-position distribution and throughput varied during the benchmark. The observed 10,000-key sample alone is excluded under the recorded assumptions.

The safe subset is a concrete next bounded target because it removes integer-width ambiguity and can be split into disjoint key ordinals. The full keyspace also includes keys whose historical integer conversion depends on the production PHP architecture. Neither the malformed-key construction nor any inner algorithm has been established for Rev-7.

At benchmark completion the directory occupied approximately 720 KiB and its candidate log was empty. There is no large input TSV. The exact benchmark source is preserved in `benchmark_10000_snapshot.cpp`, matching the hash recorded in `RESULTS.json`. A subsequent explicit `safe32` mode was added for the authorized 416,400-key pass; the benchmark mode retains its 10,000-key cap and the larger integer-width-dependent keyspace is not enabled.

Reproduce from the project root:

```sh
clang++ -O3 -std=c++17 -I mcrypt/include continuation_zero_full/benchmark.cpp -L mcrypt/lib -lmcrypt -o continuation_zero_full/benchmark
continuation_zero_full/benchmark count > continuation_zero_full/keyspace_counts.log
python3 -B continuation_zero_full/validate.py > continuation_zero_full/validation.log
continuation_zero_full/benchmark benchmark 10000 > continuation_zero_full/benchmark_candidates.log 2> continuation_zero_full/benchmark_stats.log
```

Machine-readable counts, source hashes, and assumptions are in `RESULTS.json`. The exact historical source is [CrypTool's 2016 `class.amsco.php`](https://github.com/cryptool-org/cto/blob/887e095c586f7dbae805ae40a29e82ce0d565a6f/_ctoLegacy/tools/amsco/class.amsco.php).
