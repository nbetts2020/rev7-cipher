# Rev-7 — completed wiki keyword attack

**Result: no verified plaintext or credible intermediate message.** All five searches below completed, with no `HIT` records. Completed UTC: 2026-09-06T03:35:10.873552+00:00.

## Tested inputs

- 138,036 distinct candidates from the primary wiki corpus. The first 75,340 were the BO3-associated subset.
- 23,318 additional case/spelling variants derived from the 6,942 extended-only words, excluding candidates already in the main list.
- 111,878 additional byte-prefix variants to check possible encoder truncation. These were tested only with algorithms whose maximum key length matched that prefix length.
- Total: 161,354 word/phrase/spelling candidates, plus 111,878 distinct shortened-key candidates. Prefix truncation is a separate hypothesis, not the original libmcrypt behavior; libmcrypt rejects overlength keys.
- Ciphertext unchanged: 1,092 hex characters; SHA-256 of compact uppercase ASCII `5c50001013a2dd862e13c38d314a0ba6d7303794287a05cc999018cf82cf4b1c`.

## Direct encryption-key tests

The principal scan tried the literal UTF-8 candidate bytes with all 19 available block primitives and the three native stream algorithms (RC4, WAKE and Enigma), subject to each algorithm's key-length limit. It used libmcrypt's supported-size zero padding for accepted short keys. It did not silently truncate oversized keys in this pass; the separate truncation pass handles that explicit hypothesis.

Block modes: CFB8, full-block CFB, ECB, CBC, OFB8, full-block OFB and CTR. Both repeated ASCII `0` bytes and zero-valued bytes were tested as IVs where relevant. Native stream algorithms in this library have no IV.

Twelve byte-input variants covered normal order, byte reversal, hex-digit reversal, nibble swapping, an alternate nibble alignment, and the hypothesis that the first byte `83` is a header to remove. Feedback/block checks sampled nine positions; the changed-IV checks avoid redundant interior probes. OFB/CTR checks screened the beginning, while native stream checks inspected the first 96 bytes. An apparent match triggered decryption of the remaining data and a minimum 40-byte printable-run check. Partial trailing blocks are ignored for ECB/CBC, so those tests allow trailing ciphertext damage but do not establish valid padding.

Across the three direct passes: **3,466,230 valid key/algorithm configurations**. Probe counts in the JSON/logs are short-window checks, not full-message decryptions and not statistically independent trials. All preliminary candidates failed the longer-text gate.

## Transposition-key tests

All 161,354 main/extended source candidates were also tried as keys for:

- Ordinary keyed columnar transposition.
- AMSCO with both starting cell sizes and distinct alternating-cell conventions.
- Myszkowski transposition, which treats repeated key letters as shared column groups.

Both tie directions, encryption/inverse directions, input/output reversals and both nibble alignments were checked. Unicode code-point ordering and UTF-8 byte ordering were both included when different. Equivalent key orders were deduplicated within each pass. Modern decryption after rearrangement used **CFB8, key `Zombies`, across 19 block primitives**.

These produced **24,391,168 candidate byte-string instances**. Some instances are equivalent, and deduplication was not shared between the main and extended runs. None produced a text hit.

## Validation

- Existing published Rev-1 and Rev-6 layers were reproduced, and algorithm self-tests passed.
- 818 independently encrypted controls recovered exact full plaintexts across registered algorithms, modes, key lengths, UTF-8 keys and IVs (`wiki_keyscan_controls.log`).
- Twelve independently constructed CFB8 controls passed for Threeway and the two additional SAFER primitives (`wiki_extra_controls.log`).
- Four planted transposition examples recovered exact plaintext, covering ordinary columnar, AMSCO, repeated-letter Myszkowski and a Unicode keyword (`wiki_transpose_controls.log`). The historical DE AMSCO and GK-12 controls also passed.
- Two additional controls exercised the maximum-key-length restriction for DES and native Enigma before the truncation run.

## What remains outside this result

This is not an exhaustive test of every possible use of each word. It does not rule out hashes/KDFs, unknown IVs in independent-keystream modes, two independently unknown layer keys, using the new word simultaneously as both encryption and transposition key, additional layers, untested cipher families, spacing/padding rules, or different ciphertext damage. Selected-window printable-text screening can miss short fragments, non-ASCII plaintext, compressed content and additional binary layers. The corpus is current wiki vocabulary, not an authenticated 2016 snapshot.

An exact re-encryption by itself would not prove a guessed key: ordinary decrypt/encrypt round trips work for wrong keys too. Any future hit still needs a coherent complete message and a reproducible chain. No candidate reached that stage here.

## Files and reproduction

Source: `wiki_keyscan.cpp`, `wiki_transpose.cpp`. Exact ordered inputs and hashes are recorded in `WIKI_KEY_ATTACK_RESULTS.json`. Truncated byte strings may not be valid UTF-8; `wiki_truncated_key_terms.tsv` records their derivations in hex.

```sh
clang++ -O3 -std=c++17 -I mcrypt/include wiki_keyscan.cpp -L mcrypt/lib -lmcrypt -o wiki_keyscan
clang++ -O3 -std=c++17 -I mcrypt/include wiki_transpose.cpp -L mcrypt/lib -lmcrypt -o wiki_transpose
./wiki_keyscan scan wiki_attack_keys.txt
./wiki_keyscan scan wiki_extended_attack_keys.txt
./wiki_keyscan truncated wiki_truncated_attack_keys.txt
./wiki_transpose wiki_attack_keys.txt
./wiki_transpose wiki_extended_attack_keys.txt
```

Completed logs: `wiki_keyscan.log`, `wiki_extended_keyscan.log`, `wiki_truncated_keyscan.log`, `wiki_transpose.log`, `wiki_extended_transpose.log`.
