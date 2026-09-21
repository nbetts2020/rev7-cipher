# Keyed transposition of decoded bytes

No readable plaintext or intermediate layer was recovered. The full **161,354-key corpus** completed in two deterministic partitions: **735,651 permutations /11,770,416 candidate byte-stream instances**.

## Confirmed coverage gap

The earlier `wiki_transpose.cpp`, `ecb_transpose.cpp`, `format_transpose.cpp` and AESCTR corpus scanner construct their permutations over the 1,092 hexadecimal characters. Their “bytes” labels concern keyword ordering, not ciphertext units. The earlier route work did permute bytes, but without the complete keyed columnar/AMSCO/Myszkowski corpus. This pass fills that distinct combination; it does not claim a known historical encoder behaved this way.

The ciphertext is decoded to 546 bytes **before** constructing the permutation. Each byte's two hex digits remain together during transposition. Ordinary columnar, four AMSCO conventions and repeated-letter Myszkowski are included, with both repeated-key tie directions and Unicode/UTF-8 keyword ordering where different. Four input orientations cover the original stream, byte reversal, nibble swapping and complete hex reversal. Forward/inverse permutations and whole-byte output reversal are included. The unit pairing starts at the original even nibble phase; it is not repaired by adding or dropping a nibble.

Equivalent keyword orders/group signatures are deduplicated across the full corpus. Candidate instances are not all globally distinct byte strings. The two partitions assign alternating permutation indices; their counts sum to the complete enumeration.

## Modern layer and partial blocks

The inner password is the literal `Zombies`. Tests cover CFB8, full-block CFB, ECB and CBC across 19 block primitives. Another 97 cached XOR-keystream configurations cover OFB8, full-block OFB and CTR for 16 registered block algorithms with both ASCII-zero and binary-zero IV fills, plus RC4. These cached configurations were independently checked against library encryption. Native WAKE and Enigma are not included in this pass.

Feedback/CBC checks use the established ASCII-zero IV; interior CFB/CBC probes are not dependent on its initial value. ECB/CBC inspect complete blocks at their ordinary start alignment and ignore a trailing incomplete block. No padding or missing ciphertext is fabricated. Other byte offsets, damaged transposition lengths, independently unknown inner passwords and additional layers remain outside the result.

The scanner tests selected printable windows, then checks full decryption for a printable run of 32 or 40 bytes, depending on the mode. It can miss short fragments, compressed/binary intermediates and non-ASCII text. A hit would still need complete interpretation and a reproducible forward construction.

## Validation

All 173 independently generated complete-chain controls passed: 19 primitives × four feedback/block modes, plus 97 cached stream configurations. Python constructs the modern ciphertext and forward byte transposition; the C++ implementation reverses the orientation and byte permutation before scanning. Controls cover columnar, all four AMSCO variants, Myszkowski, Unicode keywords and all four input orientations.

Every observed control input has exactly 546 bytes. Stream/feedback controls recover the whole 546-byte plaintext. ECB/CBC controls first encrypt a whole number of blocks, then append an explicitly known synthetic extra tail of 2, 6 or 18 bytes before transposition; after inversion, the exact valid plaintext region is recovered. That tail is a modeled defect, not encryption padding or a claim about the actual puzzle.

The final audit checked exact control plaintext regions, completed partition totals, zero target-hit records and the unchanged input hash. Full logs, source/corpus hashes and counters are alongside this report.

```sh
python3 -B continuation_byte_keys/controls.py
continuation_byte_keys/scan scan continuation_aesctr/all_keys.txt 2 0
continuation_byte_keys/scan scan continuation_aesctr/all_keys.txt 2 1
python3 -B continuation_byte_keys/report.py
```

Run from the parent Rev-7 directory. These completed finite tests are negative evidence for their stated constructions and settings, not a recovered solution or an impossibility proof.
