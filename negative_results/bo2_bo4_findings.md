# BO2 / BO4 comparison for Rev-7

Research date: 2026-09-05. No verified Rev-7 plaintext recovered.

## 1. Raw assets can provide evidence absent from the displayed cipher

Richkiller's 2025 BO4 report documents two concrete cases:

- The recovered Voyage texture name `i_t8_zm_zod_cipher_your_charm_c` suggests the opening words “Your charm”.
- IX's Odin inscription repeats its first sentence in the fourth position in-game; the underlying texture contains the correct fourth sentence.

Recovered Blood of the Dead texture names also confirmed the order of document fragments. **Transfer to Rev-7:** inspect the original texture, its filename, material placement, and any alternate versions. This could supply a crib or expose a presentation error. This pass did not obtain Rev-7's original game asset or filename, and there is no evidence yet that either carries such a clue.

[Researchers' report](https://www.reddit.com/r/CODZombies/comments/1ljexxl/a_bo4_update_letters_ciphers_and_decoding_hahes/)

## 2. Extra ciphertext is a demonstrated failure mode

Mob of the Dead's ADFGX ciphertext includes two consecutive `FDGFFG` rows. Removing one fixes the repeated material in the decrypted message. Its key is `ZOMBIE`, and the plaintext is German. I independently reproduced `DRINGENDDERRIESEISTINFRANKREICH` from the corrected input and published substitution mapping.

**Transfer:** include accidental duplication/deletion of extra text in the damage model. Do not force an English plaintext during final language analysis. However, Rev-7 has no repeated whole rows, no repeated five-character groups, and no adjacent identical groups in the supplied transcription. Thus the obvious Mob repair does not apply. The existing ASCII scanner already accepts ASCII German as readily as ASCII English.

[Solver's detailed explanation](https://www.reddit.com/r/CODZombies/comments/9dsk9j/adfgx_solution_for_the_causal_player_answering/)

## 3. Hill ciphers used nonstandard alphabets and automatic key completion

The confirmed Mob cell ciphers are Hill ciphers modulo 41. The linked encoder uses the alphabet `_ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.?,-`. I submitted the harmless control text `TEST` with key `MOBOFTHEDEAD` to that encoder. It produced the published 4×4 key matrix, adding the values for `ABCD` automatically, and output `QU-C`.

The added letters therefore need not have been part of a separately chosen password. This current tool behavior is consistent with the published Mob matrix; it is not independent proof of which historical page version the author used.

**Transfer:** include key construction rules and matrix operations. A matrix operation modulo 16 can transform hex into hex, so the limited visible alphabet does not establish transposition or single-symbol substitution.

[Original verification](https://www.reddit.com/r/CODZombies/comments/49o967/decryption_method_of_motd_cell_ciphers_confirmed/), [linked encoder](https://massey.limfinity.com/207/hillcipher.php). Local response: `hill_padding_control.html`.

## 4. A real BO4 cipher lost information during encryption

The IX Hill cipher used the matrix with entries `2,15,18,22`. Its determinant is −226, equivalent to 8 modulo 26, so it has no inverse modulo 26. The solvers reconstructed the message despite this defect.

**Transfer:** not every plausible layer has a unique inverse. Such candidates require constraints on the forward encryption, rather than an ordinary inverse function. This does not imply Rev-7 is irrecoverable or uses Hill.

A narrow check argues against an intact, direct, singular 2×2 Hill layer modulo 16 under the standard hex alphabet: its output parity pairs would lie in a proper linear subspace, while Rev-7 exhibits all four parity pairs at both pairing offsets. Other alphabets, additional transformations, larger constructions, and damaged data remain outside this check.

[Solvers' correction report](https://www.reddit.com/r/CODZombies/comments/aq7035/cipher_update_revelations_transcripts_new_chaos/)

## 5. Reused passwords do not imply reused full keys

Blood of the Dead's ADFGX confession ciphers reuse `BloodOfTheDead` as the transposition key but use different substitution squares. Thus even recovering a recurring keyword may leave another independent component unknown.

This strengthens the previous BO3 finding rather than introducing a new algorithm. It argues for treating modern keys, transposition permutations, and substitution alphabets as separate unknowns.

[Original three-cipher solve](https://www.reddit.com/r/CODZombies/comments/9q301p/3_adfgx_ciphers_from_botd_solved_sals_confessions/)

## Targeted Rev-7 test

`bo2_bo4_probe.py` enumerates all **24,576 invertible 2×2 matrices modulo 16**. Every transformation table was checked against its computed inverse. Original/reversed input and both nibble pairing offsets produce 98,304 generated matrix/input instances. The scanner's additional nibble-phase alternatives produce 196,608 tested instances per algorithm build.

These transformations were tested before the existing CFB8 and ECB checks, with modern key `Zombies`, using the 16 registered block algorithms plus the three separately loaded extras. **No candidate met the readable-span threshold.** This is exhaustive over the specified matrix family, not over Hill ciphers generally or arbitrary layer chains.

Files: `bo2_bo4_probe.py`, `bo2_bo4_audit.log`, `bo2_bo4_hill.log`, `bo2_bo4_hill_extras.log`, and the corresponding validation logs.

## Priority

The highest-value new evidence would be Rev-7's raw asset and metadata. The next computational ideas are forward constraints for more complex hex-preserving transformations and a broader damage model including extra text. BO4 supplies evidence of recurring practices, but a tool or key used in 2018 should not automatically be assumed available or intended for a 2016 puzzle.
