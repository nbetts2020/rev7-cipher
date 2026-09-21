# Arbitrary hex-symbol substitution continuation

No hit. Five completed searches each enumerated the stated bijective 16-symbol substitutions before known-key feedback decryption. None reached its node cap.

Key: `Zombies`; 19 block primitives; CFB8 and full-block CFB; ASCII `0` and zero-valued IV fills; normal/reversed/nibble-swapped/byte-reversed orientations. Each class had 304 algorithm/mode/IV/orientation trials.

| Restricted early plaintext alphabet | Completed search nodes | Capped trials | Hits |
|---|---:|---:|---:|
| Uppercase hex, whitespace | 586,414 | 0 | 0 |
| Lowercase hex, whitespace | 580,004 | 0 | 0 |
| Lowercase letters, specified punctuation/whitespace | 17,009,490 | 0 | 0 |
| Uppercase letters, specified punctuation/whitespace | 18,370,309 | 0 | 0 |
| Base64 characters, equals sign and CR/LF | 1,235,061,549 | 0 | 0 |

A class constrains plaintext bytes until every hex symbol has an assigned value. The scanner then decodes the whole message and requires a printable run of 80 bytes. Thus a correctly modeled, entirely class-restricted plaintext of this length would be found; the search can miss a mixed-case or otherwise unrestricted early plaintext, wrong key/IV, missing digits, further binary layers, non-bijective or position-dependent substitution. No claim is made that arbitrary substitution plus unrestricted English is exhausted.

64 independently encrypted synthetic controls (all 16 registered block algorithms, both feedback modes and IV fills) with random bijective hex substitutions recovered exact complete plaintexts without hitting the cap. The three extra primitive self-tests pass, but they were not separately included in those 64 end-to-end controls.

Run `python3 continuation_substitution/validate.py`, then `./continuation_substitution/substitute scan 50000000 CLASS`, where CLASS is hex, hexlower, lower, upper, or base64. Logs and source are in this directory.
