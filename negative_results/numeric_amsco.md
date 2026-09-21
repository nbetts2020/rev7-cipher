# Exact historical numeric AMSCO verification

No Rev-7 solution or candidate meeting the recorded plaintext gates was recovered. The search completed **all 409,112 valid numeric column-label permutations of widths 2–9** with the inner key `Zombies`.

This independently checks a previously attempted family. [Randomiser's April 11 report](https://www.reddit.com/r/CODZombies/comments/1sims97/another_revelations_cipher_solved_and_notes_on/) already says AMSCO keys through length nine were brute-forced using mcrypt. The earlier search code was unavailable for comparing its exact conventions or mode coverage.

The outer transform follows the [official pre-release 2016 PHP source](https://github.com/cryptool-org/cto/tree/887e095c586f7dbae805ae40a29e82ce0d565a6f/_ctoLegacy/tools/amsco): continuous cells of 2,1 characters, numeric column labels, uppercase text with PHP whitespace trimming, and retained decimal digits. The first cell has two characters; alternation continues across rows. Keys are permutations of `1..width`, excluding zero, duplicate, and out-of-range labels.

| Width | Keys completed |
|---|---:|
| 2 | 2 |
| 3 | 6 |
| 4 | 24 |
| 5 | 120 |
| 6 | 720 |
| 7 | 5,040 |
| 8 | 40,320 |
| 9 | 362,880 |
| Total | 409,112 |

Each key was applied to normal, reversed-hex, reversed-byte, and swapped-nibble input, in both transform directions, with both output directions and both nibble phases. This makes 13,091,584 phase instances. The benchmark completed the first 1,000 keys; four disjoint partitions covered the remaining 408,112 keys without repeating them.

| Inner-mode checks | Sampled windows | Hits |
|---|---:|---:|
| ECB and CBC, sharing block decryptions | 746,220,288 | 0 |
| CFB8 | 1,741,180,672 | 0 |
| Full-block CFB (NCFB) | 1,243,700,480 | 0 |
| OFB8, full-block OFB, CTR, and RC4 | 3,207,438,080 | 0 |

CFB8, NCFB, ECB and CBC cover 19 block primitives. The cached streams cover the 16 registered mcrypt block primitives in three modes, plus RC4. The key is `Zombies`; applicable IV bytes are ASCII `0`. The counters count attempted windows, including fast rejections, rather than full-message decryptions. ECB/CBC together made 746,493,242 primitive block calls. The four workers took approximately 410 seconds each after the 4.45-second benchmark.

Detection requires ASCII bytes 32–126 or tab/CR/LF. CFB8 checks 16-byte windows beginning at offsets 0,48,112,208,304,400,496 and then a full-message printable run of at least 32. NCFB and cached streams check 24-byte windows at 0,64,192,320,448 and require a full-message run of at least 40. ECB/CBC check two adjacent blocks at aligned offsets 0,192,384 and then a run of at least 32. Incomplete trailing blocks are retained as untrusted bytes in the diagnostic buffer; they are not padded or decrypted. The second nibble phase drops the first nibble and any final unpaired nibble explicitly.

Validation passed 898 comparisons against a separately written literal translation of the historical PHP, including the `135624` fixture and ragged lengths. Those controls did not execute PHP. A later independent run of the unchanged original class in PHP 8.4.25 passed 1,180 additional comparisons, including valid and malformed keys; see `../continuation_php_runtime/RESULTS.md`. Nine independently encrypted full chains recovered the exact expected plaintext, covering Serpent CFB8, NCFB, CBC, OFB8, full-block OFB and CTR, RC2 and Rijndael-256 ECB, and RC4. Every control used the outer key `593168247`.

These negatives are conditional on the recorded modes, key, IV, orientation, framing and ASCII detection gates. They do not exclude another inner key, binary intermediate layers, damage, unsampled block alignments, or invalid numeric keys that erase data. The separately derived zero-column projections are in `zero_projection.py`; they are hypotheses about an implementation defect, not evidence that Rev-7 used one.

Reproduction and evidence: `numeric_amsco.cpp`, `validate.py`, `RESULTS.json`, `validation_results.json`, `keyspace_count.log`, `benchmark{,_stats}.log`, `part0{,_stats}.log` through `part3{,_stats}.log`, and the full-chain `control_*` files. The compact observed ciphertext SHA-256 is `5c50001013a2dd862e13c38d314a0ba6d7303794287a05cc999018cf82cf4b1c`.

The invalid-key decode direction has its own source-semantic defect: when label 10 is absent from a nonleading-zero permutation of `0..9`, `getPos(10)` returns null, and `null+1` selects column 1, overwriting its earlier contents. `zero_decode_projection.py` models that direction separately and passed 750 comparisons against an independent literal string-operation translation. All four tested safe 32-bit keys produce 1,092 output characters from either 1,260 or 1,262 input characters. These maps are handed to the separate erasure-recovery search; they are not included in the valid-key exhaustive counts above. The later PHP execution described above independently confirmed both projection directions.
