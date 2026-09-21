# Rev-7 literature review and implications for the completed searches

**Result:** no new plaintext was found. The review did identify a concrete coverage gap, recover a contemporaneous texture source, and experimentally explain why a nearly correct transposition can still look unsuccessful.

This is a focused technical review of original solver reports, tool documentation/source, NIST's mode specification, and research on transposition cryptanalysis. It is not a systematic review of every publication. Claims about Rev-7's intended construction remain hypotheses unless demonstrated by a reproducible solution.

## 1. Most actionable computational gap: the large transposition pass was CFB8-only

Randomiser's 2026 Rev-1 solution uses a Beaufort layer, RC2 in **ECB**, reversal, and Rijndael-256 in **ECB**. Its unusual case-sensitive alphabet was also essential. Thus a solved Revelations cipher already supplies a counterexample to treating CFB8 as universal. [Original Rev-1 solver report](https://www.reddit.com/r/CODZombies/comments/1sims97/another_revelations_cipher_solved_and_notes_on/).

Our code audit confirms that `wiki_transpose.cpp` passed its approximately 24.4 million main/extended candidate instances to the CFB8 scanner only. We did test ECB/CBC in direct-key searches and smaller structural sweeps; we did **not** run the whole large transposition family through those modes. This is a specific untested combination, not a claim that ECB was never tried.

Length matters: Rev-7 decodes to 546 bytes, which is not a whole number of blocks for the tested block sizes. An ECB hypothesis therefore needs an explicit, justified framing/conversion/damage model. Silently padding the input would not establish a solution.

## 2. A contemporaneous texture source has now been recovered

DragonGJY's October 7, 2016 post describes exports from PC textures and labels this image **`ori_trench_paper`**. The linked 1024×512 PNG remains retrievable. It visually matches the supplied cipher, including the leading `83` and the five-character grouping. This gives us a contemporaneous comparison source and a reported asset label, rather than just a later wiki screenshot. [2016 texture-export thread](https://www.callofdutyzombies.com/topic/183529-all-revelations-ciphers-texture-files/).

The PNG is saved as `literature_review/ori_trench_paper_2016.png`. Its SHA-256 is `e8b277bee96433eb35860a1d22fdcba9ef29fc9b7209bf4367b4c7997ca5ac54`. It contains no PNG textual metadata chunks. The forum label is not an authenticated full game-bundle path. I have not recovered the thread's attached transcription ZIP or completed an independent character-by-character transcription audit from it.

I tested 154 variants of the reported labels as direct encryption keys and as transposition keys: no hit. Logs are in `literature_review/asset_label_keyscan.log` and `asset_label_transpose.log`. The main value of this find is provenance, not evidence that the label is a password.

There is a relevant precedent for metadata: Richkiller and collaborators recovered BO4 asset names that exposed a possible message opening and confirmed fragment order; they also found an IX texture line that differed from its displayed in-game version. This supports asset comparison as a method, but does not prove a similar discrepancy in Rev-7. [BO4 researchers' report](https://www.reddit.com/r/CODZombies/comments/1ljexxl/a_bo4_update_letters_ciphers_and_decoding_hahes/).

## 3. Formatting between layers deserves a more exact reconstruction

Rumkin documents separate treatment of spaces and warns about leading, trailing and doubled spaces when spaces are moved with the text. Those choices change the permutation being inverted. [Tool author's documentation](https://rumkin.com/tools/cipher/columnar-transposition/).

The Gorod Krovi Reporter solution demonstrates two distinct transposition permutations. The technical follow-up also identifies reversed key order in the Rumkin reproduction and discusses a historical bug, while explicitly saying that this particular solution was unaffected. [Original solver and technical follow-up](https://www.reddit.com/r/CODZombies/comments/n0edsb/gorod_krovi_reporter_cipher_solved/).

The 2016 texture thread additionally records a different Revelations cipher ending in decimal `013 010`, a concrete CR/LF artifact in a representation layer. It does not establish a CR/LF suffix in Rev-7. [Contemporaneous discussion](https://www.callofdutyzombies.com/topic/183529-all-revelations-ciphers-texture-files/).

**Implication for our search:** model formatting at the stage where it occurred. Transpose a spaced hex rendering and then remove spaces is different from transposing its compact hex digits. Our earlier spacing-aware pass covered selected keys and group sizes, not the complete wiki-key corpus. This is more grounded than treating every hypothetical repair as a missing run of hex digits.

The present CrypTool-Online repository is useful source material, but it cannot automatically be treated as the 2016 implementation. A pre-release history query for the current Scytale path returned no commits; the linked historical AMSCO snapshot could not be retrieved in this review. Neither fact proves that all historical code is unavailable. [Official CTO repository](https://github.com/cryptool-org/cto).

## 4. Classical hill-climbing literature needs adaptation here

Lasry, Kopal and Wacker's 2016 paper attacks long-key columnar transposition using a two-stage search and a specialized fitness score. Its impressive benchmarks concern its stated classical-cipher problem; they are not a demonstrated attack on transposed modern ciphertext. [Published paper and abstract](https://www.tandfonline.com/doi/abs/10.1080/01611194.2015.1087074).

Lasry's thesis, especially §3.2.4 and the methodology chapter, explains why a useful score must retain a relationship to key accuracy despite key errors. It recommends studying that relationship experimentally rather than assuming that a high-order language score will work from arbitrary starting keys. [University-published thesis, 2018](https://www.uni-kassel.de/upress/online/OpenAccess/978-3-7376-0458-1.OpenAccess.pdf).

I applied that diagnostic to synthetic messages with exactly Rev-7's 1,092-hex-character length: English plaintext → known modern CFB8 encryption → keyed columnar transposition. I then exchanged two columns of the correct transposition key and measured recovery over 100 trials per condition.

| Inner cipher | Columns | Mean hex positions still correct | Mean printable output | Median longest printable run |
|---|---:|---:|---:|---:|
| Serpent CFB8 | 7 | 73.2% | 39.0% | 5.5 bytes |
| Serpent CFB8 | 26 | 92.7% | 40.3% | 8 bytes |
| Serpent CFB8 | 84 | 97.8% | 62.6% | 41.5 bytes |
| Rijndael-256 CFB8 | 26 | 92.8% | 38.9% | 7 bytes |
| Rijndael-256 CFB8 | 84 | 97.8% | 46.4% | 35 bytes |

For comparison, the accepted printable-byte set occupies 98/256 ≈ 38.3% of byte values. Coincidentally matching hex digits are included in the reported position accuracy. These are synthetic diagnostics, **not observations of partial Rev-7 solutions**. Wider layouts sometimes retain more signal; the experiment does not prove that every possible heuristic fails.

The practical lesson is that our hit gates can recognize a successful decryption while giving almost no indication that a short-column permutation is nearly right. Before investing in a hill climber, demonstrate a usable scoring gradient on matching synthetic layered examples. Script, complete 4,000-trial results and logs: `literature_review/fitness_controls.py`, `fitness_controls.json`, `fitness_controls.log`.

## 5. Wrong IV alone is a weaker explanation under CFB8

NIST specifies CFB with a segment size, including 8-bit segments; CFB8 itself is standardized, not proprietary to mcrypt. Its feedback equation also bounds propagation: an incorrect IV affects the initial feedback window, and a changed ciphertext byte affects that byte and the next block's worth of byte segments. [NIST SP 800-38A, §6.3 and Appendix D](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38a.pdf).

I verified the relevant behavior with libmcrypt controls for 8-, 16- and 32-byte block sizes. Wrong-IV decryption recovered the unchanged suffix after one block; a flipped byte had bounded damage; a **whole-byte** deletion also recovered after the feedback window when compared with the appropriately shifted plaintext. Arbitrary bit/nibble insertions require separate alignment handling.

Consequently, a wrong IV or a few isolated typos alone should not conceal every long readable region of an otherwise correctly ordered CFB8 message. This reasoning does not apply unchanged to OFB, to incorrect transposition, to distributed errors, or to non-text intermediate data. More arbitrary-IV guessing is therefore a lower priority under the current CFB8 hypothesis.

## Recommended order of work

1. **Close the mode/structure coverage gap:** test ECB after the supported transposition families, with explicit length/framing hypotheses. CBC can be a secondary check, but the direct same-map precedent here is ECB.
2. **Reconstruct historical formatting:** use solved examples as controls for spaces, line endings, grouping, case conversion and layer order. Do not equate modern tool defaults with old ones.
3. **Complete the source audit:** independently transcribe the recovered export and seek the full asset/material identity and alternate versions. Its reported label alone is not an opening crib.
4. **Develop a measured heuristic:** only expand local-search attacks after synthetic trials show that their scores improve toward the correct layered construction.

The broad dictionary work remains useful negative evidence about its tested constructions. It does not outweigh the positive evidence for reused settings, representation layers and implementation conventions in actual solved ciphers. Randomiser's seven-cipher report is the principal basis for those reused modern settings. [Original seven-cipher report](https://www.reddit.com/r/CODZombies/comments/1rbpx86/seven_revelations_ciphers_finally_solved/).

## Screened-out literature

Chhatrapati's *On the Construction and Cryptanalysis of Multi-Ciphers* concerns concealing multiple messages in one ciphertext. Despite the title, it is not a general method for peeling successive modern/classical encryption layers, so it does not currently supply a targeted Rev-7 attack. [Author's IACR preprint, 2021](https://eprint.iacr.org/2021/1005).

No source reviewed supplies a verified Rev-7 plaintext, and none of the new small checks in this review recovered one.

## Follow-up execution

The recommended ECB and formatting follow-up has now completed. All 20 defined searches returned no hit. The full corpus was tested after transposition in ECB/CBC and under the five-character spacing model; focused passes covered other layouts, byte alignments and explicit edge-loss models. See [completed follow-up results](ecb_format.md) for exact coverage and limitations.
