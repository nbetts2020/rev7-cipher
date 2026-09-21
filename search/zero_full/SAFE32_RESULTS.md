# Complete signed-32-bit zero-column encode search

**A coherent solution was recovered and verified.** Worker 1 completed its 208,200 keys and returned 64 compatible plaintexts for one pipeline. Worker 0 was interrupted after verification, at the parent's direction, with its last complete checkpoint at 170,000 keys. The complete 416,400-key space was not exhausted, and this pass is not reported as a negative.

The discovered pipeline is **libmcrypt `blowfish-compat` in CFB8 mode, key `Zombies`, IV `3030303030303030`; encode its output as uppercase hexadecimal; apply the original historical AMSCO encode with numeric key `1947038265`; then reverse all hexadecimal characters**. AMSCO's key contains a zero in the fifth input column (index 4), so its output loop discards 168 of the 1,260 hex characters. This exactly explains the observed 1,092-character length.

All 64 candidates re-encrypt exactly through libmcrypt and reproduce every observed hex character through actual execution of the unchanged historical PHP class. Candidate 18, indexed from zero, contains coherent prose throughout, beginning `MI-8 transcript. Field Report 1918: Corporal Dempsey is still at large in France.` and ending `I better be careful.` followed by four line feeds. Its bytes are in `candidate18_plaintext_utf8.txt`.

Erasure prevents a mathematical uniqueness claim. Across the recorded 64 language-constrained completions, 596 of 630 plaintext bytes are invariant. Three short regions each have a coherent reading and a gibberish alternative; the final five bytes have eight alternatives. Candidate 18 is the post-search semantic selection. These alternatives were enumerated without a plaintext crib, and `candidate_ambiguity.json` preserves every differing region.

| Worker | Status | Guaranteed completed keys | Completed cases | Candidates | Caps |
|---|---|---:|---:|---:|---:|
| 0 | Interrupted, exit 130 | 170,000 | 103,360,000 | 0 at last checkpoint | 0 at last checkpoint |
| 1 | Complete | 208,200 | 126,585,600 | 64 | 0 |
| Total counted | Partial keyspace | 378,200 | 229,945,600 | 64 | 0 recorded |

Worker 1 completed in 533.639 seconds. Worker 0's last complete checkpoint was at 682.252 seconds; subsequent unlogged work is not counted. At least 38,200 safe keys remain outside the completed checkpoints. The workers were disjoint by ordinal parity. No capped or long-erasure case was recorded. Worker 0's interrupted gzip file is empty and is not treated as a complete gzip stream; it reported no candidates. Worker 1's 64 records are preserved intact.

The complete enumeration, per-shard numeric-key sums, ordinal sums, and zero-position counts match independent Python and C++ implementations. Five planted keys exercise both shards; the recovered ciphertext/plaintext pairs match the originals, and unchanged PHP execution independently confirms all five outer encryptions. Evidence: `shard_counts.log`, `safe32_validation_results.json`, `safe32_controls.log`, and `safe32_php_controls.json`.

Worker evidence is in `safe32_part0_stats.log` and `safe32_part1_stats.log`; all recovered records are in `safe32_part1_candidates.txt.gz` and `candidates_decoded.json`. Exact-chain checks are in `candidate_validation.json` and `candidate_php_validation.json`. Machine-readable final accounting is in `SAFE32_RESULTS.json`. `aggregate_safe32.py` intentionally refuses to label the interrupted run complete.

Targeted reproduction uses the original recovery executable and supplies no plaintext to its search:

```sh
python3 -B continuation_zero_full/targeted_reproduce.py
```

It reproduces all 64 records in the same order and explicitly selects candidate 18 afterward. Results are in `targeted_results.json`, `targeted_original_recover.log`, `targeted_all64_candidates.txt.gz`, and `targeted_selected_plaintext_utf8.txt`.

The other 2,849,520 nonleading-zero keys exceed signed 32-bit range and were not searched in this pass. The recovered pipeline is verified against the observed ciphertext; the author's exact historical sequence of tools is not independently documented.
