# Complete IV stored at the packet's beginning or end

**No candidate found.** This is a wrapper hypothesis, not authenticated evidence that the original puzzle author used a particular tool or stored an IV this way.

## Prior coverage and exact construction

The earlier direct/same-key scans used repeated ASCII `0` or zero-byte IVs. The separate Movable Type AESCTR work uses an eight-byte nonce and its own password expansion. Source/report review found no prior pass treating a complete primitive-block-sized prefix or suffix as the raw IV for these three mcrypt modes.

For every candidate packet, the scanner takes exactly one block from the beginning or end as the IV and removes those bytes from the ciphertext body. The body is decrypted in full. No missing bytes or zero placeholders are inserted.

The recurrence follows the local original libmcrypt 2.5.8 sources:

| Mode | Initial state | Keystream and update |
|---|---|---|
| OFB8 (`ofb`) | Complete IV | Encrypt the state, XOR its first output byte, shift the state left one byte and append that output byte |
| Full-block OFB (`nofb`) | Complete IV | Encrypt the state, XOR the resulting block, and use that encrypted block as the next state |
| CTR (`ctr`) | Complete IV as a big-endian integer | Encrypt the counter, XOR the resulting block, then increment the entire counter modulo the block width |

Primary implementation files are `libmcrypt-2.5.8/modules/modes/ofb.c`, `nofb.c` and `ctr.c`. Their exact hashes are recorded in `validation.json`. The arbitrary IV bytes are used directly; there is no date filter, IV KDF, guessed textual IV, or Movable Type password expansion in this branch.

## Completed tests

| Pass | Distinct literal keys | Key/packet instances | Full decryptions | Candidates |
|---|---:|---:|---:|---:|
| Initial direct benchmark | 3 | 120 | 13,680 | 0 |
| Focused direct pass | 500 | 20,000 | 2,138,880 | 0 |
| Selected transpositions | 3 | 6,408 | 730,512 | 0 |

The initial keys are `Zombies`, `ZOMBIES` and `zombies`. The 500-key pass includes those three and the earlier seed/reused/asset-key union, so the benchmark is a repeated subset. All keys are literal UTF-8 bytes, with standard mcrypt-compatible key setup. Overlong keys are explicitly skipped per primitive; this pass records 588 such skips among 9,500 key/primitive pairings.

All passes use 19 block primitives, all three modes and both IV placements. The direct inputs are the 40 previously documented hexadecimal-byte variants: both nibble phases, four byte/nibble orientations, and keeping the packet or removing one/two bytes from either end. IV extraction happens after these input transformations. Exact packets and labels are in the small `direct_inputs.tsv` file, sourced from `continuation_unicode/inputs.json`.

The transposition pass streams the documented small historical/reused-key set from the preceding Unicode task: recovered historical AMSCO `135624` and columnar `CODE` defaults, 71 additional distinct column orders from reused keywords/tie alternatives and unkeyed widths 2–32, both directions, four input orientations, output reversal and both nibble phases. Every distinct resulting packet is checked with each of the three literal modern keys. The entire IV-plus-ciphertext packet is the hypothesized transformed data. Exact source identity and streamed-input hash are in `transposition_manifest.json`; no new large transformed-ciphertext file was created.

The three-key direct benchmark took 0.874 seconds and justified the focused pass, which finished in 126.421 seconds. The full 161,354-key corpus was not run. There are no capped or partially sampled searches hidden in these counts: every listed packet/mode/IV-placement instance was fully decrypted.

## Detection and validation

The detector scans the full decrypted body. It requires either an 80-character ASCII/curated-UTF-8 run or a 40-character UTF-16LE/BE or UTF-32LE/BE run, with at least one ASCII letter. Wide encodings are checked at every code-unit byte alignment. The finite character repertoire is ASCII space through tilde plus tab/CR/LF, NBSP, U+2013/U+2014, U+2018–U+201F and U+2026. BOMs break a run but do not prevent the following long text from being detected. Binary bytes outside a surviving long run are permitted. This seeks English-compatible text or representation layers, not arbitrary Unicode or compressed/binary plaintext. Candidates would still need coherent content and exact re-encryption; none occurred.

Validation passed **2,052 exact plaintext controls and 4,104 packet-placement controls**, covering all 19 primitives, all three modes, three literal keys and six encoding forms. Every full packet has the observed 546-byte length. IVs are nonrepeated random blocks, with additional cases ending in `FFFF` to test multi-byte CTR carry. Controls include BOMs and binary prefix/suffix bytes around an otherwise long text run.

The 16 registered primitives were encrypted with the actual libmcrypt library modes. For the three extra primitives, the unchanged original `ofb.c`, `nofb.c` and `ctr.c` were compiled directly and invoked with the original primitive block-encryption functions. Thus the new handwritten decoder was checked against original mode implementations for every primitive, rather than only against another transcription of the recurrence. Compressed input fixtures and the bounded control log are retained.

```sh
clang -O2 -std=gnu99 -dynamiclib -DHAVE_CONFIG_H -I libmcrypt-2.5.8 -I libmcrypt-2.5.8/lib -I libmcrypt-2.5.8/libltdl libmcrypt-2.5.8/modules/modes/ofb.c libmcrypt-2.5.8/modules/modes/nofb.c libmcrypt-2.5.8/modules/modes/ctr.c -o continuation_embedded_iv/original_modes.dylib
clang++ -O3 -std=c++17 -I mcrypt/include continuation_embedded_iv/scan.cpp -L mcrypt/lib -lmcrypt -o continuation_embedded_iv/scan
python3 -B continuation_embedded_iv/validate.py
python3 -B continuation_embedded_iv/build_inputs.py
./continuation_embedded_iv/scan direct continuation_embedded_iv/direct_inputs.tsv continuation_embedded_iv/focused_keys.txt
python3 -B continuation_embedded_iv/stream_transpositions.py
```

The result does not exclude untested passwords, shorter nonce/counter wrappers, separately encoded or transformed IVs, an IV stored elsewhere, different counter layouts, untested transpositions, damaged data that destroys every qualifying text run, or additional binary layers. It supplies a bounded negative for the complete-IV prefix/suffix construction above. Machine-readable results and hashes are in `RESULTS.json`.
