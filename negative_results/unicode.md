# UTF-16/UTF-32 plaintext detector and bounded attacks

Completed with **zero candidates**. This tests an alternate plaintext/intermediate representation; it is not evidence that a 2016 web tool used UTF-16 or UTF-32 by default.

## Gap and detector

Earlier scanners required contiguous printable ASCII bytes and rejected NUL. `keyword_sweep.py` tested UTF-16/32 **key bytes**, and earlier transposition reports mention Unicode **key ordering**; neither covers a UTF-16/32 plaintext layer. See the explicit ASCII/representation limitations in `RESULTS.md`, `ROUND4_RESULTS.md`, `ECB_FORMAT_RESULTS.md` and `WIKI_KEY_ATTACK_RESULTS.md` at the project root.

The new detector reads actual UTF-16LE/BE and UTF-32LE/BE code units at every possible byte alignment. It seeks at least 40 consecutive characters and at least one ASCII letter. Accepted characters are ASCII space through tilde, tab/CR/LF, U+00A0, U+2013/U+2014, U+2018–U+201F and U+2026. NUL code points, surrogates and other code points break runs. This is an English-compatible character detector, not a general Unicode-printability or semantic-language test.

A 12-byte local screen accepts two consecutive compatible code points in any tested representation/alignment. Leading BOMs are not counted as text, but do not prevent the following characters from passing, including OFB/CTR prefix screens. Block/feedback modes sample offsets 0,64,128,192,256,320,384,448,512. Independent-keystream modes screen offset zero; native streams screen the first 96 bytes. A passing screen triggers a full decryption and the 40-character detector. Candidate logging is capped at 100 records while counting every accepted candidate; all attack counts were zero.

## Completed coverage

| Pass | Scope | Probes | Full checks | Candidates |
|---|---|---:|---:|---:|
| Main seeds | 475 literal UTF-8 keys; 40 byte-input variants; every block alignment | 133,806,529 | 5,975 | 0 |
| Additional reused keys | 25 disjoint historical/reused-key variants; same inputs/alignment scope | 6,679,586 | 243 | 0 |
| Selected transpositions | 2,264 deduplicated key/cipher instances; ordinary alignment | 1,942,236 | 92 | 0 |

The 500-key union includes all capitalization combinations of `Zombies`, the earlier finite lore/format guesses, 154 asset-label keys, repair/extra-key lists, and the reused keys listed in `crossmap_probe.py`. These are literal UTF-8 keys. No new KDF, Unicode key encoding, or ciphertext input decoder was added.

The 40 direct byte-input variants cover both nibble phases, four byte/nibble orientations, and keeping the input or removing one/two bytes from either end. `inputs.json` records exact labels, lengths, hashes and bytes. ECB, CBC and full-block CFB additionally test every initial byte offset up to the primitive's block size minus one. CFB8, OFB8, full-block OFB, CTR and native streams use the listed input variants. Two IV fills are tested: repeated ASCII `0` and zero bytes. There are 19 block primitives/seven modes and three native stream primitives; keys exceeding an algorithm's supported length are explicitly skipped. ECB/CBC ignore incomplete trailing blocks, so this is not a padding-validation claim.

The selected transposition pass reuses the exact recovered historical `135624` AMSCO and `CODE` columnar defaults with inner keys `Zombies`, `ZOMBIES`, `zombies`. It adds 71 distinct column orders: ordinary columnar and continuous 2,1 AMSCO with the small reused-key set/tie alternatives, plus unkeyed columnar widths 2–32. Both directions, four input orientations, output reversal and two nibble phases are included. Additional transpositions use inner key `Zombies`. Whole hexadecimal strings are transposed; digits are not held in place. `build_transpositions.py` and `transposition_inputs.json` preserve the exact scope.

The full 161,354-key corpus was **not scanned** with this detector. A completed 100-key/40-variant benchmark had zero candidates and took 3.443 seconds. Simple linear extrapolation under that workload is about 93 minutes for the corpus, so the bounded extension used the documented small transposition set instead. The 100 benchmark keys are extra finite observations, not a corpus exclusion.

## Validation and reproduction

- 1,200 random/planted byte fixtures match an independent Python-codec decoder oracle exactly.
- 1,064 planted examples cover all 19 block primitives, all seven modes, four encodings, BOM/no-BOM, and both IV fills across the cases. All recover exact original plaintext bytes. Registered primitives use the actual libmcrypt mode encryption; the three extra primitives use their original block encryption functions with independently implemented mode recurrence.
- 24 native-stream examples and eight header/framing examples exercise the all-algorithm scanner path; all recover exact original plaintext. Total exact encrypted controls: 1,096.

```sh
clang++ -O3 -std=c++17 -I mcrypt/include continuation_unicode/scan.cpp -L mcrypt/lib -lmcrypt -o continuation_unicode/scan
python3 -B continuation_unicode/validate.py
python3 -B continuation_unicode/build_inputs.py
ALL_BLOCK_ALIGN=1 ./continuation_unicode/scan scan continuation_unicode/seed_keys.txt
ALL_BLOCK_ALIGN=1 ./continuation_unicode/scan scan continuation_unicode/reused_extra_keys.txt
python3 -B continuation_unicode/build_transpositions.py
./continuation_unicode/scan stdin < continuation_unicode/transposition_inputs.tsv
```

These negatives remain conditional on the tested primitives, keys, IVs, ordering/framing, character repertoire and probe positions. They do not exclude arbitrary Unicode text, binary/compressed intermediates, an untested outer transposition, unknown independent-keystream IVs, or independently unknown layer keys. A printable Unicode candidate would still require coherent content and exact re-encryption before being considered a solution. No candidate was found. Machine-readable counters, source/input hashes and controls are in `RESULTS.json` and the adjacent logs.
