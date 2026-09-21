# Rev-7: ECB, formatting and edge-loss follow-up

**Result: no verified plaintext, readable intermediate layer, or partial-message hit.** All 20 searches below finished. Completed UTC: 2026-09-06T04:41:02.401908+00:00.

The ciphertext remained exactly the supplied 1,092 hexadecimal characters (546 bytes). This run tested hypotheses identified in the literature review; it did not determine the cipher's intended construction.

## Completed searches

| Search | Vocabulary / models | Candidate byte-stream instances | Result |
|---|---|---:|---|
| ECB and CBC after transposition | All 161,354 main and extended keyword variants | 24,391,168 | No text hit |
| Five-character groups, spaces transposed then stripped | All 161,354 variants; CFB8, ECB and CBC | 23,540,832 | No text hit |
| Other literal whitespace layouts | 24,379 focused key variants; three layouts; CFB8, ECB and CBC | 7,216,608 | No text hit |
| Every possible block-byte alignment | 24,379 focused key variants; ECB and CBC | 2,405,536 | No text hit |
| Explicit edge repair before undoing transposition | 24,379 focused key variants; twelve models; ECB and CBC | 28,866,432 | No text hit |
| Separated readable ECB blocks | All 161,354 variants | 23,540,832 | No partial-message hit |

Counts are generated instances, not independent keys or full-message decryptions. They include directions/orientations and alternate nibble alignment. Some instances are equivalent. The main ECB run used separate deduplication for primary and extended lists; the formatting and partial-message runs deduplicated their combined list. The formatting logs increment `candidates` once for ECB/CBC and once for CFB8; the table divides those counters by two so it does not count that same instance twice merely for having both scanners.

## What the models actually tested

All modern decryption used **key `Zombies`** with the same validated libmcrypt short-key handling as the earlier work. All 19 available block primitives were included. Keyword candidates control the outer transposition, not an independently unknown inner encryption key.

Transpositions: ordinary columnar, AMSCO with both starting sizes and two alternating-cell conventions, and repeated-letter Myszkowski. Both tie orders, forward/inverse permutations, Unicode/UTF-8 ordering where different, four input orientations, output reversal and two nibble phases were included.

ECB/CBC probes read intact blocks at byte positions 0, 192 and 384. The broad pass assumed block boundaries at the start of each candidate. The focused alignment pass tried every offset modulo each algorithm's block size. CBC used repeated ASCII `0` for the initial IV; its interior probes do not depend on that IV. No padding was invented to turn a partial ciphertext into a supposedly valid complete message.

Whitespace models operate before the outer transposition: format the hexadecimal text, transpose the characters including whitespace, then strip whitespace and display the compact result. The generated permutation tracks only the surviving hex digits, preserving the effect the removed whitespace had on column/cell positions. In addition to one space per five characters, focused models tested CR/LF in place of the group separator every 70 hex characters and the supplied image transcription's whitespace layout with LF or CR/LF. These are explicit reconstructions, **not a claim that the 2016 tool has been identified or reproduced exactly**.

The focused corpus has 24,379 distinct spellings, built from the entity-supported words plus selected established cipher/lore terms and their case variants. It is narrower than the full corpus; additional case variants can still induce the same permutation.

Edge repairs are applied to the observed compact string **before** undoing transposition. Removing 4, 12 or 36 hex digits from either edge tests possible extra characters. Adding 12, 28 or 60 digits at either edge tests possible missing suffixes/prefixes, producing lengths compatible with the supported block sizes. Added zero digits are explicitly unknown placeholders, not recovered ciphertext. A meaningful hit would need readable unaffected blocks and independent recovery or justification of the missing values.

## Detection and validation

The ECB/CBC text gate requires two complete printable blocks at a sampled location, followed by a full-candidate check for a printable run of at least 32 bytes. The CFB8 gate retains the earlier selected-window scanner. These gates seek English or printable representation layers such as hexadecimal/base64; they are not language proofs.

A second ECB pass relaxes the requirement for contiguous readable text: a printable sampled block triggers decryption of all complete blocks, and at least 64 bytes spread across wholly printable blocks triggers a `PARTIAL` record. It found none. This is a partial-damage detector, not a demonstrated hill-climbing algorithm. It can still miss a candidate whose intact blocks avoid all sampled positions.

Validation checks passed:

- Published Rev-1 RC2/Rijndael ECB layers and Rev-6 Serpent CFB8 were reproduced; the algorithm self-tests passed.
- 432 independently encrypted ECB/CBC examples exercised every byte alignment of the 16 registered block primitives, with extra edge bytes.
- Six independently constructed ECB/CBC examples covered the three extra primitives.
- Three complete keyword/transposition examples exercised exactly Rev-7's length with two extra bytes before transposition.
- Twelve complete formatting examples covered all four whitespace models, columnar/AMSCO and ECB/CFB8.
- Six missing-edge examples verified that placeholder restoration recovers intact original plaintext regions.
- Three controls detected separated intact ECB blocks, and three controls verified odd-nibble framing at exactly Rev-7's hex length.
- The existing historical DE AMSCO and GK-12 controls passed during formatting validation.

## Interpretation

The large ECB/CBC/transposition gap identified in the review is now tested under the stated alignments and key assumptions. The full five-character spacing model is also tested. Neither produced evidence of a solution. The supported next conclusion is **that these particular constructions failed**, not that the ciphertext is impossible or the keyword corpus is exhaustive.

Still outside this pass: two independently unknown layer keys, arbitrary binary intermediate layers, most key derivation conventions, arbitrary interior insertions/deletions, further classical layers, and other formatting/tool implementations. The corpus is current wiki vocabulary, not an authenticated 2016 snapshot. No complete plaintext or reproducible solution chain has been recovered.

## Reproduction and audit

Sources: `ecb_transpose.cpp`, `format_transpose.cpp`, `ecb_partial.cpp`; their generated-source helpers are `make_format_scanner.py` and `make_partial_scanner.py`. Shared primitives and permutations come from `search.cpp`.

Build each scanner with:

```sh
clang++ -O3 -std=c++17 -I mcrypt/include ecb_transpose.cpp -L mcrypt/lib -lmcrypt -o ecb_transpose
clang++ -O3 -std=c++17 -I mcrypt/include format_transpose.cpp -L mcrypt/lib -lmcrypt -o format_transpose
clang++ -O3 -std=c++17 -I mcrypt/include ecb_partial.cpp -L mcrypt/lib -lmcrypt -o ecb_partial
```

Run the main searches from this directory:

```sh
./ecb_transpose wiki_attack_keys.txt
./ecb_transpose wiki_extended_attack_keys.txt
./format_transpose ecb_all_keys.txt
ALL_ALIGN=1 ./ecb_transpose ecb_focused_keys.txt
./ecb_partial ecb_all_keys.txt
python3 -B format_focused_cases.py
python3 -B ecb_edge_cases.py
```

The JSON companion records exact per-run counters and source/input hashes. `ecb_round_report.py` refuses to report a negative result if any search is incomplete or contains a `HIT` / `PARTIAL` record.
