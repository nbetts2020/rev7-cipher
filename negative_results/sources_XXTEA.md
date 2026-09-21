# XXTEA transfer results

The independently reproduced September 7, 2026 TheGiant solution introduced a genuine primitive not previously present in the libmcrypt scanner. All completed transfers below produced **zero hits**. These are bounded hypothesis tests, not a disproof of XXTEA in a deeper pipeline.

| Completed search | Exact decryptions | Result |
|---|---:|---|
| 424 unique direct/framed inputs, 18 keys, four data/key endian combinations | 30,528 | No hit |
| 24 explicit hex edge-framing cases, 159,223 distinct padded/truncated key values, standard little-endian | 3,821,352 | No hit |
| All 65,536 two-byte values split across either/both ends, four orientations, six keys, standard little-endian | 4,718,592 | No hit |
| 354,988 unique framed Scytale/columnar/AMSCO candidates, 18 keys, four data/key endian combinations | 25,559,136 | No hit |
| **Total completed** | **34,129,608** | **No hit** |

The actual 546-byte hex input is not a multiple of XXTEA's four-byte word size. Frames explicitly model discarding up to a partial word at either/both edges, or appending/prepending zero, ASCII `0`, space, or PKCS-sized byte values. None of those changes is treated as established fact. The broad dictionary pass uses only 24 distinct hex cases: four orientations, two-byte edge deletion or zero-byte edge padding, and all three left/right splits. Only the separate six-key repair pass exhaustively tests unknown two-byte values.

The focused direct/transposition generator also checks the compact input as ASCII uppercase/lowercase and as base64. This includes interpreting the 1,092 characters as base64 giving 819 bytes, and explicit padding to 820. Direct cases include literal source whitespace, normal/reversed input, byte reversal, the experimental removal of leading `83`, and removal of two trailing hex digits.

Transposition coverage: all ordinary Scytale widths 2 through half the input length; columnar and six AMSCO variants under the named keys in `xxtea_candidates.py` (earlier solved keys plus `THEGIANT`, `REVELATIONS`, `ORIGINSTRENCH`, `ORIGINS`, `TRENCH`, `ORITRENCHPAPER`); stable/reversed duplicate-letter ranking; both permutation directions. The deduplication occurs on final framed byte strings.

The 18 focused keys are in `focused_keys.txt`. The six exhaustive repair keys are in `repair_keys.txt`. Key truncation/padding equivalence is explicit: take the first 16 UTF-8 bytes and pad with zeroes. No cryptographic key cracking is implied by dictionary coverage.

The hit criterion was at least 85% printable ASCII/tab/CR/LF or one printable run of 64 bytes. It recognizes ordinary text and printable intermediate encodings such as hex/base64. It can miss binary intermediate layers, compressed data, and a badly corrupted plaintext. XXTEA avalanches over the whole message, so unlike CFB8 it supplies no expectation of a readable unchanged suffix after local ciphertext damage.

An initial all-dictionary pass across all 424 frames was **interrupted** to prioritize supported framing cases. `xxtea_dictionary.log` and `xxtea_dictionary_stats.log` are incomplete and excluded from every count above.

Controls: published TheGiant ciphertext decrypts exactly and re-encrypts identically in `xxtea_control.py`; the independent C++ scanner detects it in `xxtea_scanner_control.log`. Result logs ending `_stats.log` contain the completed counts.

## Reproduction from this directory

```sh
clang++ -O3 -std=c++17 xxtea_scan.cpp -o xxtea_scan
python3 -B xxtea_control.py
python3 -B xxtea_candidates.py direct | ./xxtea_scan focused_keys.txt
STRICT_ENDIAN=1 ./xxtea_scan dictionary_keys.txt < xxtea_dictionary_inputs.tsv
STRICT_ENDIAN=1 ./xxtea_scan repair_keys.txt repair2 < repair_inputs.tsv
python3 -B xxtea_candidates.py transposes | ./xxtea_scan focused_keys.txt
```
