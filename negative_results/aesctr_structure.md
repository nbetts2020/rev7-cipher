# AESCTR after structural transformations

No readable plaintext or intermediate layer was recovered. All three searches completed.

This pass tests the Movable Type AESCTR construction implemented and independently checked by the parent task: eight nonce bytes prefixed to the ciphertext, AES-based password expansion, and a big-endian counter in the final eight bytes of the AES input block. It uses three literal passwords (`Zombies`, `ZOMBIES`, `zombies`) at 128/192/256 bits, stored in nine independent cached AES contexts. **No date, millisecond or other nonce-value filter was applied.** Arbitrary eight-byte nonces are included.

| Search | Byte-stream instances | AESCTR checks | Result |
|---|---:|---:|---|
| Nibble/byte/five-group matrix routes, rail fence, skip, physical-row variants | 1,207,836 | 10,870,524 | No hit |
| Variable-length group/row inverse reconstruction | 70,164 | 631,476 | No hit |
| Full keyword columnar/AMSCO/Myszkowski corpus | 23,540,832 | 211,867,488 | No hit |

Every stream instance includes its specific nibble phase. These counts are candidate instances, not globally distinct ciphertexts. The route generators deduplicate their own hexadecimal strings before the two phases; the keyword pass deduplicates key-order/group signatures. There is no deduplication between these three passes.

The keyword pass read 161,354 candidates, generated 120,925 distinct ordinary orders and 131,026 repeated-letter groups, and tested 735,651 permutations. It includes ordinary columnar, four AMSCO conventions, and repeated-letter Myszkowski, four input orientations, both directions and output reversal. Candidate words control the transposition only; the modern password remains one of the three literals above.

The route passes reuse the completed structural families from `../continuation_structure/RESULTS.md`: all-width diagonal/spiral/snake routes, bounded rail-fence starting phases, coprime skip steps, both five-digit alignments, explicit leading/trailing two-digit removal, and physical rows. Supplemental inverses account for short groups/variable rows after boundaries are discarded. They do not incorporate every dictionary key into these routes.

Detection probes 16-byte printable windows at plaintext positions 0, 128, 256 and 384, then requires an 80-byte printable run in the complete decryption. It can miss binary layers, compression, non-ASCII messages, short surviving fragments and constructions with a different framing/counter/KDF convention. No source-date assumption was used to prune candidates.

## Validation

The original JavaScript independently encrypted nine messages, one per cached key context, each giving exactly Rev-7's 546-byte ciphertext length including the eight-byte nonce. All nine recovered the complete 538-byte plaintext exactly. Another 54 controls exercised independent Python forward columnar/AMSCO/Myszkowski transformations followed by the C++ inverse maps and AESCTR decryption. Twenty-seven controls exercised flattened nibble, byte and five-digit route transformations and their inverse reconstruction. Every complete chain recovered the exact message and triggered the scanner.

The report generator checks completed counters, zero target-hit records, all 90 exact control plaintexts, and the unchanged input hash. Source and corpus hashes are recorded in `RESULTS.json`.

```sh
python3 -B continuation_aesctr_structure/routes.py | continuation_aesctr_structure/scan stdin
python3 -B continuation_aesctr_structure/variable_units.py | continuation_aesctr_structure/scan stdin
continuation_aesctr_structure/scan keyed continuation_aesctr/all_keys.txt
```

Run from the Rev-7 directory. Full logs and control sources are alongside this report. These are negative results for the stated construction and keys, not a recovered solution or an impossibility proof.
