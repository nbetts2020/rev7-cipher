# Historical AMSCO zero-column recovery — focused search

**No complete message or reliable readable region was recovered.** The focused source-derived encode and decode constructions completed without node caps or unresolved long-erasure cases.

The key set contains 45 decimal permutations: insert 0 at every nonleading position of `123456789`, `198346572`, `135624789`, `987654321`, and `135792468`. Thirty-six survive a signed 32-bit integer conversion; nine descending-base cases explicitly assume 64-bit PHP. Each construction includes four observed-text orientations and four orientations between modern encryption and AMSCO.

| Construction | Reconstructed hex lengths | Patterns | Completed checks | Result |
|---|---|---:|---:|---|
| Historical encode used as forward transform | 1170 or 1260 | 720 | 54,720 CFB8 algorithm/IV/language cases; 609,352 DFS nodes | No compatible complete plaintext |
| Historical decode used as forward transform | 1260 or 1262 | 1,440 | 109,440 CFB8 cases | Every case contradicted a provably unaffected plaintext byte/sequence |
| Decode, other modern modes and masked readable regions | 1260 or 1262 | 1,440 | 331,200 mode configurations | No compatible known-region message; maximum safe ASCII run 18 bytes |

Counts overlap across modern families; they are executed instances, not a fraction of the entire construction space.

## The actual loss mechanism

The recovered 2016 AMSCO instructions require consecutive, unrepeated digits but do not explicitly say to start at 1. A nonleading-zero permutation of 0–9 survives the controller's numeric conversion. The encoder labels columns using those digits, but its output loop visits 1 through the width, omitting column 0. Continuous 2/1 cells and width 10 give a sparse loss of 78 nibbles from 1170, or 168 from 1260, leaving the observed 1092. Only those source-identified missing slots were treated as unknown. [Original class](https://github.com/cryptool-org/cto/blob/887e095c586f7dbae805ae40a29e82ce0d565a6f/_ctoLegacy/tools/amsco/class.amsco.php), [instructions](https://github.com/cryptool-org/cto/blob/887e095c586f7dbae805ae40a29e82ce0d565a6f/_ctoLegacy/tools/amsco/infobox.template).

The decode button behaves differently with those keys: missing label 10 makes `getPos` return null; `null+1` selects column 1 and overwrites its earlier assignment. Its matching even input lengths are 1260 and 1262, with a contiguous source chunk erased. Both operation roles were modeled separately. Even lengths were enumerated against the exact projection; missing characters were not arbitrary padding.

## Recovery and validation

Sparse encode holes were solved under CFB8, password `Zombies`, nineteen block primitives and both ASCII-zero/binary-zero IV fills. DFS enumerates missing nibble values and checks plaintext bytes. Failed-state memoization retains position, UTF-8 state and the preceding ciphertext feedback block. Every target case completed below the 50-million-node guard.

Language 0 permits ASCII 32–126 plus tab, CR and LF. Language 1 additionally permits UTF-8 NBSP; en/em dashes, specified curly quotes, bullet, ellipsis and narrow NBSP; and a UTF-8 BOM only at the beginning. This is a curated repertoire, not arbitrary Unicode. Every compatible ending is preserved; no missing punctuation was guessed.

All 152 planted 585/630-byte controls recovered the exact original message **and every missing cipher digit among the candidates**. The 66,113 compatible completions are retained in compressed JSONL; each was independently re-encrypted and passed the legacy forward transformation. Printable constraints do not guarantee a unique natural-language answer.

The unchanged historical PHP source was also executed through PHP-WASM 8.4.25 with 64-bit integers: all 152 planted encode forwards and 230 planted decode forwards matched exactly, with the original source hash preserved. This verifies source behavior in that runtime, not the historical deployment environment.

For contiguous decode loss, dependency masks identify exactly which plaintext bytes are independent of unknown ciphertext. The mode pass covers CFB8/NCFB/ECB/CBC over 19 primitives and 97 cached OFB8/OFB/CTR/RC4 configurations, including both IV fills where relevant. Incomplete ECB/CBC tails are not decrypted or invented. All 230 independent masked-mode controls recovered exact known plaintext regions, and a negative filler-artifact control passed.

The preliminary unmasked zero-fill run produced 4380 artificial hits inside erased spans. The strict masked pass found no safe ASCII run of 32 bytes anywhere; its maximum was 18. Those filler artifacts are not partial solutions.

An independent review found no false-negative defect in the recurrence, memo key or known-region UTF-8 pruning; 66,844 grammar-oracle cases, 760 actual-cipher recurrence/pruning cases and 102 exhaustive memo comparisons passed. See [independent review](../review/ZERO_COLUMN_REVIEW.md).

## Limits and artifacts

The negative applies to these 45 keys, the stated orientations, `Zombies`, and the accepted text classes. Other keys, additional layers, other IV/key conventions, arbitrary Unicode, binary intermediates and trailing NUL padding remain outside it. This focused DFS is CFB8; other feedback/block modes were checked only where erasure-independent bytes could be determined. Broader key enumeration and NCFB erasure recovery are separate tasks.

`RESULTS.json` records exact counts and hashes. `work.py` generates projections and control chains; `recover.cpp` performs sparse recovery; `masked_modes.cpp` checks dependency-safe regions. The compressed control archive preserves all endings and recovered ciphertexts. The original Rev-7 transcription was not changed.
