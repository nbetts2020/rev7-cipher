# Alphabet-filtered routes and rail fence

No readable intermediate layer was recovered. The complete pass generated **161,776 unique hexadecimal streams /323,552 phased byte-stream instances**.

| Scope | Unique hex streams | Bounds |
|---|---:|---|
| Transform A–F while preserving digit positions | 99,264 | Matrix widths and rail counts 2 through half the 402-letter subsequence; every rail starting phase through 32 rails, then phases 0,1,rails−1; every coprime skip |
| Transform digits while preserving A–F positions | 30,540 | Matrix widths and rail counts 2–64; every rail phase through 16, then three selected phases; every coprime skip |
| Transform both subsequences independently with common route parameters | 31,972 | Focused bounds as for digits, with coprime skips valid for both lengths |

Matrix families include ordinary columns, row/column snakes, diagonals, alternating diagonals, and two spiral traversals from all four corners. Forward/inverse maps, four whole-input orientations and output reversal were included. Counts are deduplicated across this generator but not against earlier searches. There is no removal/insertion of characters in this pass. The excluded characters stay in their existing slots relative to each oriented input.

The modern layer uses the existing `round4` scanner with password `Zombies`, CFB8/full-block CFB/ECB over 19 block algorithms, OFB8/full-block OFB/CTR over 16 registered block algorithms, and RC4. Both nibble phases are tested. This is not a comprehensive CBC search. It detects sufficiently long printable regions and can miss binary layers, compressed data, non-ASCII plaintext or short fragments.

The same 323,552 phased streams were also checked under the independently validated Movable Type AESCTR construction: nine cached contexts (`Zombies`, `ZOMBIES`, `zombies` at 128/192/256 bits), for **2,911,968 checks**, with no hit. This pass imposed no nonce-date or millisecond-value filter. Its detector requires an 80-byte printable run after a sampled 16-byte window. Twenty-seven original-JavaScript AESCTR / filtered-rail / inverse controls recovered their exact 538-byte messages. See `aesctr.log` and `aesctr_controls.log`.

## Grounding and controls

The current CTO shared driver calls the transformation only on characters in the configured alphabet and otherwise retains them unless its deletion option is selected. Its Skytale implementation transposes only the filtered message. We executed 36 exact encrypt/decrypt comparisons against that original JavaScript under the 52-letter alphabet, using six widths and three messages including Rev-7. This verifies the modeled behavior for that source/configuration; it does not authenticate a 2016 version. [Original shared driver](https://raw.githubusercontent.com/cryptool-org/cto/master/_ctoApps/railfence/src/common/crypt.js), [original Skytale](https://raw.githubusercontent.com/cryptool-org/cto/master/_ctoApps/railfence/src/common/skytale.js).

A hand-derived rail-3 control verifies `A1B2C3D4E5F6 → A1E2B3D4F5C6`. Nine transformation/inverse controls using independently generated Serpent-CFB8 ciphertext recovered the exact 546-byte message through the scanner, covering rail, spiral and skip across all three scopes. The final audit checked all exact control plaintexts, source comparisons, complete counters and absence of target hits.

```sh
python3 -B continuation_filtered_routes/generate.py | ./round4 stdin
python3 -B continuation_filtered_routes/source_controls.py
node continuation_filtered_routes/source_controls.js
```

Run from the parent Rev-7 directory. Scripts, complete logs and counts are alongside this report. This negative result excludes the stated finite transformations and settings; it is not a recovered solution.
