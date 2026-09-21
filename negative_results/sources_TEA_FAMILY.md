# Original TEA and original Block TEA checks

No hit was found. These algorithms were tested separately from XTEA and corrected block TEA (XXTEA).

The original TEA implementation follows [Wheeler and Needham's 1994 paper](https://www.cl.cam.ac.uk/ftp/papers/djw-rmn/djw-rmn-tea.html). It passes two independently published [Crypto++ TEA vectors](https://raw.githubusercontent.com/weidai11/cryptopp/master/TestVectors/tea.txt) in both directions. The 1997 original variable-width Block TEA follows the authors' [Tea extensions paper](https://www.movable-type.co.uk/scripts/xtea.pdf), before the XXTEA correction. Its encryption matches a separate Python transcription of that paper, and the C++ search implementation recognizes a control produced by the separate implementation.

| Completed pass | Decryptions | Hits |
|---|---:|---:|
| Original TEA ECB | 11,520 | 0 |
| Original TEA CBC | 34,560 | 0 |
| Original TEA CFB8 | 34,560 | 0 |
| Original TEA CFB64 | 34,560 | 0 |
| Original TEA OFB | 34,560 | 0 |
| Original TEA CTR, big-endian counter increment | 34,560 | 0 |
| Original Block TEA direct | 11,520 | 0 |
| Original Block TEA dictionary | 3,821,352 | 0 |
| Original Block TEA transposition extension | 8,519,712 | 0 |

The seven-mode direct pass used 160 unique inputs, 18 focused keys, both data endianness and key endianness, input orientations and byte offsets 0–7. Representations were raw hex bytes, literal uppercase/lowercase ASCII hex, and base64 interpretation of the observed characters; the experimental leading `83` removal was included. IVs where applicable were all-zero bytes, repeated ASCII `0`, and the first eight ciphertext bytes as a prefixed IV. ECB/CBC ignored an explicit incomplete trailing block; original Block TEA zero-filled its final partial word. These framing choices are hypotheses.

The dictionary extension used the same 24 explicit hex frames and 159,223 distinct effective keys as the XXTEA dictionary test, with standard little-endian words and key words. The transposition extension used the 354,988 framed inputs documented in `XXTEA_RESULTS.md`, six focused keys (`repair_keys.txt`), and four data/key endian combinations. Its count is 354,988 × 6 × 4.

Direct hits required 85% ASCII printable/tab/CR/LF bytes; the extended C++ scans also accepted any 64-byte printable run. Binary intermediate layers are outside that detector's guarantees.

Scripts: `tea_family.cpp`, `tea_family_probe.py`, `original_block_scan.cpp`. Evidence: `tea_family.log`, `tea_family_results.json`, `original_block_control.log`, `original_block_dictionary_stats.log`, `original_block_transposes_stats.log`.

```sh
clang++ -O3 -std=c++17 -shared -fPIC tea_family.cpp -o tea_family.dylib
python3 -B tea_family_probe.py
clang++ -O3 -std=c++17 original_block_scan.cpp -o original_block_scan
STRICT_ENDIAN=1 ./original_block_scan dictionary_keys.txt < xxtea_dictionary_inputs.tsv
python3 -B xxtea_candidates.py transposes | ./original_block_scan repair_keys.txt
```
