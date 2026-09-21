# Recovered 2016 CrypTool Online implementations

**Result:** authentic historical source was recovered from the official repository's old directory tree. Its filtering behavior differs materially from today's plugins. Exact historical defaults and a complete corpus pass through five historical columnar key configurations found no plaintext hit.

## Provenance and chronology

The earlier path-specific lookup missed `_ctoLegacy`. Whole-repository history reaches an August 5, 2016 initial commit. The August 12 commit [“legacy tools added”](https://github.com/cryptool-org/cto/commit/4fc443f0d87c0e86815695a47ab2d6174c725f82) adds the PHP AMSCO/Skytale tools and JavaScript columnar tool. The [September 2, 2016 snapshot](https://github.com/cryptool-org/cto/tree/887e095c586f7dbae805ae40a29e82ce0d565a6f) preserves those files unchanged. Author and committer timestamps agree. All 11 downloaded source files match their recorded Git blob hashes; both historical tree responses are untruncated.

The current GitHub repository was created in 2018 but contains this older Git history. These are verifiable source snapshots, not authenticated web-deployment captures. They do not prove which tool the puzzle author used. Exact URLs, file hashes and the Git identities are in `SOURCE_INDEX.json`; API responses and retrieval records are retained here.

The current `_ctoApps/railfence` lineage first appears in [June 15, 2017](https://github.com/cryptool-org/cto/commit/4ff37f0119b3dc208be9c8731128a85cab3ba349), and its Skytale addition is dated [June 25, 2017](https://github.com/cryptool-org/cto/commit/ef6f52c0b8fea2bbee3d498bdc424a4ef2fcbcff). No railfence implementation appears in the inspected complete 2016 tree. This establishes the chronology of this code lineage; it does not prove that no separate railfence page ever existed.

## Material behavior differences

**Historical AMSCO retains hexadecimal digits.** `setText` uppercases input; the encoder and decoder trim each whitespace character but do not alphabet-filter the data. Cells alternate 2,1 continuously across row boundaries. Numeric key digits label input columns, which are then read in numerical order. The controller's default is `135624`, and output is grouped in fives. The accompanying instructions require consecutive, unrepeated digits in arbitrary order. [Class](https://github.com/cryptool-org/cto/blob/887e095c586f7dbae805ae40a29e82ce0d565a6f/_ctoLegacy/tools/amsco/class.amsco.php), [controller/default](https://github.com/cryptool-org/cto/blob/887e095c586f7dbae805ae40a29e82ce0d565a6f/_ctoLegacy/tools/amsco/default_tool.php), [key instructions](https://github.com/cryptool-org/cto/blob/887e095c586f7dbae805ae40a29e82ce0d565a6f/_ctoLegacy/tools/amsco/infobox.template).

For a valid permutation of 1 through its width, that numeric convention equals sorting the positions by their numeric labels. Invalid numeric keys are not reliably rejected: duplicate labels overwrite cells and out-of-range labels can drop columns. Leading zeros are removed by the integer conversion. Those lossy inputs are not part of an exhaustive *valid-key* claim and are not evidence of deliberate Rev-7 corruption.

**Historical Skytale removes digits.** Its controller always uppercases and calls `check`; `check` accepts letters from its fixed alphabet, with no displayed option that enables digits. For the supplied hexadecimal text, all 690 numeric characters disappear and only 402 A–F characters survive. This unmodified wrapper therefore cannot directly be the outer stage producing the observed 1,092-character mixed hex string. The regular-expression checker has metacharacter quirks, but they do not make decimal digits pass. [Controller](https://github.com/cryptool-org/cto/blob/887e095c586f7dbae805ae40a29e82ce0d565a6f/_ctoLegacy/tools/skytale/default_tool.php), [filter and transform](https://github.com/cryptool-org/cto/blob/887e095c586f7dbae805ae40a29e82ce0d565a6f/_ctoLegacy/tools/skytale/fkt_coder.php), [form](https://github.com/cryptool-org/cto/blob/887e095c586f7dbae805ae40a29e82ce0d565a6f/_ctoLegacy/tools/skytale/form.template).

Skytale's default width is 5, with five-character output spacing. Its incomplete-row decoder inserts literal spaces. Once those filler spaces are removed, its permutation is ordinary inverse columnar transposition at effective width `ceil(N / ceil(N / requested_width))`. This can differ from the requested width for short/wide layouts, but the checked behavior does not reveal a new family of dropped-symbol permutations. The per-algorithm filtering distinction matters more than the filler implementation.

**Historical columnar transposition moves the complete input, including digits, spaces and line breaks.** Its alphabet settings normalize/filter the *key*, not the data. Default key is `CODE`. Uppercase-only mode folds the key to uppercase; enabling lowercase preserves mixed case. Checking the digits option after the initial uppercase setting appends `0123456789` after A–Z, changing alphanumeric key ordering relative to ASCII sorting. The order of option activation can itself change alphabet-group order. [Original JavaScript](https://github.com/cryptool-org/cto/blob/887e095c586f7dbae805ae40a29e82ce0d565a6f/_ctoLegacy/js/transposition.js), [shared key-alphabet library](https://github.com/cryptool-org/cto/blob/887e095c586f7dbae805ae40a29e82ce0d565a6f/_ctoLegacy/js/ctolib.js), [defaults/form](https://github.com/cryptool-org/cto/blob/887e095c586f7dbae805ae40a29e82ce0d565a6f/_ctoLegacy/tools/transposition/default_tool.php).

A direct source execution illustrates this: alphabet A–Z then digits, key `A1B2`, and input `0123456789ABCDEF` produce `048C26AE159D37BF`; ASCII key sorting produces `159D37BF048C26AE`. Thus neither a universal digit-preserving rule nor a universal letter-filtering rule describes these 2016 tools.

## Reproduction and completed checks

At the time of this historical-source pass, no native PHP executable was available in PATH; its PHP routines were translated and were not claimed to have run in their original runtime. A subsequent independent agent executed the unchanged AMSCO class under official PHP-WASM 8.4.25: 1,180 cases, including malformed keys, matched the independent projection models with zero mismatches. See `../continuation_php_runtime/RESULTS.md`; that follow-up does not imply the original web wrapper was executed. The AMSCO translation matched 1,098 independent **valid-key** permutation/round-trip fixtures, including target lengths. A later audit corrected the port's missing-label fallback for invalid numeric keys: the original PHP uses column 1 when a label is absent and compares labels against single key characters. The validated/default results use valid keys and are unchanged; they do not claim malformed-key coverage. The Skytale shape/filler translation matched 8,754 comparisons, including every width for lengths 402 and 1,092. The existing historical DE `198346572` control was also checked. The recovered JavaScript was executed directly under Node: 880 algorithm fixtures and 40 actual GUI/library key-normalization fixtures passed.

The exact default checks covered both directions, four input orientations, output reversal and both nibble phases. Each used `Zombies`, `ZOMBIES` and `zombies` with 19 block primitives/seven modes and three native streams. Both `135624` AMSCO and `CODE` columnar completed 96 key/input instances and 82,368 probes with zero hits. The numeric AMSCO fixture and literal models are in `validation_attack_results.json` and `literal_models.py`.

The larger pass derived keys from **all 161,354 corpus entries** using five option orders: A–Z; A–Z/a–z; A–Z/digits; A–Z/a–z/digits; A–Z/digits/a–z. The original key-cleaning library and JavaScript case folding were used. Equivalent column orders were deduplicated across settings and source keys, yielding **44,562 orders**. The complete 1,092 hex characters were transposed without data filtering.

That run used inner key `Zombies`, 19 block primitives in CFB8, full-block CFB, ECB, CBC, OFB8, full-block OFB and CTR, plus RC4. OFB/CTR tested ASCII-zero and binary-zero IV fills; feedback probes use interior context. Eight independent complete-chain controls used original 2016 JavaScript for the outer encryption and passed all seven block modes plus RC4 at Rev-7's length.

Completed totals: **1,425,984 candidate byte-string instances**, **407,831,424 probe checks**, 49 longer checks, **0 hits**, approximately 122.9 seconds. These are instances, not a fraction of the key/construction space. The scanner requires a 40-byte printable run after selected-window probes, ignores incomplete ECB/CBC tails for detection, and does not cover binary intermediates, arbitrary damage, other key alphabets, or an independently unknown modern key. WAKE/Enigma were included only in the small default checks.

Reproduce from the project root:

```sh
python3 -B continuation_historical_tools/validate_and_attack.py
node continuation_historical_tools/validate_columnar.cjs
node continuation_historical_tools/derive_columnar_keys.cjs
clang++ -O3 -std=c++17 -I mcrypt/include continuation_historical_tools/historical_columnar.cpp -L mcrypt/lib -lmcrypt -o continuation_historical_tools/historical_columnar
python3 -B continuation_historical_tools/columnar_chain_controls.py
./continuation_historical_tools/historical_columnar continuation_historical_tools/historical_columnar_orders.tsv
```

## Bounded search outcome

The official 2016 Git snapshots supplied the requested historical AMSCO, Skytale and columnar implementations, so no archive replay is being substituted for source recovery. The official organization inventory did not reveal another older CTO repository; the obsolete `ct-online` organization API returned 404. The recovered history resolves the earlier failed current-path lookup. Pre-2017 railfence remains unverified beyond the negative 2016-tree check and documented 2017 introduction.

The strongest result is a correction to tool provenance and filtering assumptions, plus completed exact-source/default/key-order checks. No result here identifies a Rev-7 plaintext or justifies inventing another cipher layer.
