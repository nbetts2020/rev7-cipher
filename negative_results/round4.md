# Rev-7 — additional attack results, 2026-09-05

**No verified plaintext or credible intermediate message was recovered.** These are completed searches on the supplied transcription, not proposed work. Counts below are candidate instances, often including duplicates; they do not measure the fraction of all possible solutions covered.

| Attack | Completed scope | Result |
|---|---|---|
| Extra text before an unkeyed columnar/Scytale transformation | Remove 1–8 consecutive hex characters at positions spaced five characters apart; widths 2 through half the remaining length; forward/inverse transposition, reversals, both nibble alignments. 15,146,672 instances. | No CFB8 text hit across 19 block algorithms. |
| Extra text before keyed columnar/AMSCO transformation | Remove 1–16 consecutive hex characters at every position; keys ZOMBIES, ZOMBIE, 198346572, TRYTHIS, ZOMBIESAREEVERYWHERE; ordinary columnar and six AMSCO conventions, with reversals/alignment variants. 9,717,120 instances. | No CFB8 text hit across 19 block algorithms. |
| Hex-coordinate fractionation | Split each digit into two 2-bit coordinates or four 1-bit coordinates; gather/interleave coordinates over periods 2–1092, both directions, 14 explicit alphabets, reversals and nibble alignments. 488,768 instances. | No hit in the expanded mode scanner. This hex adaptation is a hypothesis, not a documented Treyarch method. |
| Older-map transformations with additional encryption modes | Rechecked the cross-map transformation generator, including spacing-aware permutations and double columnar routes. 67,968 instances. | No hit in the expanded mode scanner. |
| Consecutive binary encryption layers | 2,784 two-layer instances and 184,832 three-layer instances. First two layers of the three-layer search restricted to CFB8/full-block CFB; byte/nibble orientations between layers. Principal key Zombies. | No readable final layer. Two-layer first stages also included independent-keystream modes. |
| Key construction | 463 literal keys generated with alphabetic, numeric, space and PKCS-style padding, plus selected seed words. 301,872 direct decryptions. | No hit. These padding rules are hypotheses, not established Rev-7 settings. |
| Autokey and differential encoding | Plaintext/ciphertext autokey, repeating-key controls, add/subtract/Beaufort/XOR in mod 16 and mod 256, selected seed keys; physical-line restarts for hex; differences/recurrences at lags 1–128. 90,112 instances. | No hit in the expanded mode scanner. |
| Hill matrices derived from guessed openings | 3×3 and 4×4 matrices modulo 16; four input orientations; 19 CFB8 algorithms; ASCII-zero IV and key Zombies. 64,706,685 algorithm/orientation/opening trials drawn from 995,409 generated opening strings, shortened and deduplicated separately for each case. | 8,366 candidate matrices fit their proposed opening, but none passed the full-message printable-run check. A fitted opening alone is not evidence of a solution. |

## What was validated

- 81 independent mode controls: encrypt synthetic plaintext with libmcrypt, decrypt it back, and require the scanner to recover the exact complete plaintext. OFB/CTR/RC4 keystream assumptions were checked against encryption, not simply assumed.
- Six full search controls recovered exact synthetic messages: an extra-character/Scytale case, two coordinate-fractionation cases, a three-layer binary chain with intervening reversals, and 3×3/4×4 Hill cases with matrices recovered from an opening.
- Coordinate-transform inverses and all autokey operation/feed combinations passed round-trip checks. The fractionation fixture `0123 → 001B` was checked directly from 2-bit coordinates.
- The existing original-libmcrypt validation includes algorithm self-tests and exact reproduction of published Rev-1 and Rev-6 encryption layers; see `crypto.py` and the earlier results.

The expanded scanner checks CFB8, full-block CFB and ECB for 19 block primitives, plus libmcrypt OFB, full-block OFB and CTR for its 16 registered block algorithms, and RC4. It does **not** add a comprehensive CBC search in this pass. Previous CBC checks are documented separately.

## Limits

Most structural searches still depend on key `Zombies` and the other Revelations settings. The scanners probe selected positions, then require a printable run of 32 or 40 bytes; they can miss short fragments, non-ASCII text, compressed data, or additional untested binary layers. The Hill search requires a correct opening in its finite dictionary and the tested modern cipher/IV; it is not an exhaustive matrix-key search. Extra-character removal is a specific damage model, not an audit of the original game asset. No claim is made that all keys, transpositions, cipher compositions or transcription errors have been excluded.

## Reproduction and logs

From this directory:

```sh
clang++ -O3 -std=c++17 -I mcrypt/include round4.cpp -L mcrypt/lib -lmcrypt -o round4
./round4 extra Zombies 8
./round4 keyextra
./round4 fraction
python3 crossmap_probe.py | ./round4 stdin
./round4 layers
python3 round4_keypadding.py
python3 round4_autokey.py | ./round4 stdin
python3 round4_make_cribs.py
./round4 hillcrib
```

The opening generator uses macOS `/usr/share/dict/words`; the exact generated candidates used here are saved in `round4_cribs.txt`. Principal logs: `round4_extra.log`, `round4_keyextra.log`, `round4_fraction.log`, `round4_crossmodes.log`, `round4_layers.log`, `round4_keypadding.log`, `round4_autokey.log`, and `round4_hillcrib.log`. Validation logs: `round4_controls.log`, `round4_end_to_end.log`, and `round4_hill_controls.log`.

No newly tested family supplied a convincing lead. Independent access to the original Rev-7 texture/asset and its metadata remains useful evidence to seek; the searches here cannot determine whether the supplied text is exactly what the puzzle author intended.
