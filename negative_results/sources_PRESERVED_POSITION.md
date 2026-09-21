# Transposition preserving excluded characters

## Source-supported implementation behavior

The current CrypTool Online [shared transformation driver](https://raw.githubusercontent.com/cryptool-org/cto/master/_ctoApps/railfence/src/common/crypt.js) only calls the algorithm for characters in the selected alphabet. Characters outside that alphabet remain in place unless the option to delete them is selected. Five-character grouping occurs afterward. Its [Skytale implementation](https://raw.githubusercontent.com/cryptool-org/cto/master/_ctoApps/railfence/src/common/skytale.js) filters the input to the selected alphabet before computing the permutation, then returns the next transformed alphabet character to that driver.

The [current default alphabet](https://raw.githubusercontent.com/cryptool-org/cto/master/_ctoApps/railfence/src/common/alphabets.html) is the 52-letter uppercase/lowercase alphabet, excluding digits. Therefore, when the selected alphabet contains letters but not digits, the combined implementation can permute the A–F subsequence of hex while keeping every digit in its original position. Rev-7 has **402 A–F characters and 690 digits**. This behavior preserves the all-hex alphabet and is a concrete coverage gap relative to transposing the entire compact ciphertext.

**Historical-source correction:** a later independent audit recovered the actual pre-release 2016 PHP implementation. Its Skytale wrapper uppercases the input and calls `check()`, whose alphabet excludes decimal digits. It therefore removes digits rather than preserving their positions. See the [2016 source snapshot](https://github.com/cryptool-org/cto/tree/887e095c586f7dbae805ae40a29e82ce0d565a6f/_ctoLegacy/tools/skytale) and the files under `../continuation_historical_tools/`. The verified present-JavaScript behavior must not be presented as a historically established Rev-7 construction. The searches and conditional bounds remain valid tests of a possible family, but the newly recovered history weakens this particular tool attribution. Digits-only, separate transforms of each class, and AMSCO remain separate hypotheses; the historical AMSCO implementation is being audited directly.

## Completed focused pass

The generator produced **62,288 unique hex strings**. It tested A–F-only, digits-only, and both classes independently under the same permutation settings; all Scytale widths through the relevant subsequence length; 19 named key strings under columnar and six AMSCO variants; stable/reversed equal-key ranking; both permutation directions; four input orientations; output reversal; and preserving or experimentally removing the leading `83`.

The expanded existing scanner checked **124,576 nibble-phase candidate instances**, **107,758,240 main windows** and **42,355,840 additional-mode windows**. It returned **zero hits** in 54.97 seconds. This covers CFB8, partial ECB, full-block feedback, OFB/CTR variants and RC4 under the existing `Zombies` settings, subject to the scanner's documented sampled-printable-window limitations. It does not exhaust every key or binary intermediate.

Controls passed: independently encrypt a long message with Serpent CFB8, apply/invert the filtered transposition while checking excluded positions remain unchanged, recover the exact message through libmcrypt, then confirm the expanded scanner finds it. A separate C++ versus Python comparison checks the full-corpus generator's transformations across both orientations and all class/pattern/direction cases. An independent agent also ran the actual current CrypTool JavaScript under a mocked DOM: 36 exact encrypt/decrypt comparisons across three texts (including Rev-7) and six widths matched the filtered model. Those controls are saved in `../continuation_filtered_routes/source_controls.log`.

Files: `preserved_transposes.py`, `preserved_control.log`, `preserved_cpp_control.log`, `preserved_focused_generation.log`, `preserved_focused_scan_stats.log`.

## Full-corpus extension

Both full-corpus passes completed with zero hits. They read **161,354 keyword strings**, deduplicate to **119,678 distinct stable/reversed-tie keyword orders**, and apply columnar plus four AMSCO parity variants to the A–F subsequence only. All 1,092 characters are retained, with digits fixed; four input orientations, both permutation directions, output reversal and both nibble phases are tested. The inner key is `Zombies` across 16 registered block primitives plus three extra primitives (19 total).

| Completed full-corpus pass | Candidate phase instances | Windows | Hits |
|---|---:|---:|---:|
| CFB8 | 19,148,480 | 2,546,747,840 | 0 |
| ECB/CBC at block-aligned sampled windows | 19,148,480 | 1,091,463,360 | 0 |
| NCFB at standard block origin | same 19,148,480 | 1,819,105,600 | 0 |

These counts are candidate instances, **not unique ciphertexts**. ECB/CBC decrypt only complete blocks and retain/ignore the explicit partial trailing block, without inventing padding. The default full pass does not enumerate every byte alignment. A separate focused all-byte-alignment ECB/CBC check completed **124,576 phase instances / 91,189,632 windows**, also with no hit.

The CFB8 pass completed in 1,290.41 seconds. The mode follow-up records a completed first-10,000-key checkpoint (9,320 orders), then processes the remaining global order ordinals in three disjoint modulo-3 partitions. Each partition selected 36,786 orders; 9,320 + 3×36,786 = 119,678. The interrupted initial process's unlogged work is excluded. `RESULTS_INDEX.json` verifies the summed phase and window counts. An optimized NCFB gate stops at the first nonprintable byte with the same acceptance condition; independent controls pass before and after the change.

The corpus uses Unicode-codepoint keyword ordering, not an additional UTF-8-byte-order variant; it does not include Myszkowski. It does not establish a unique possible classical layer or cover arbitrary keys for the inner modern cipher.

Code: `preserved_dictionary.cpp`, `preserved_dictionary_modes.cpp`. Logs: `preserved_dictionary_letters_stats.log`, `preserved_modes_checkpoint.json`, `preserved_modes_part0_stats.log`, `preserved_modes_part1_stats.log`, `preserved_modes_part2_stats.log`, `preserved_alignment_scan_stats.log`. Independent four-mode controls: `preserved_modes_control.log`, `preserved_modes_optimized_control.log`.

## Exact relaxed upper bound for keystream modes

`fixed_digit_stream_bounds.py` permits each observed A–F nibble to take **any** A–F value independently, with all digit positions fixed. This deliberately drops the requirement that values form a permutation, so every A–F-only transposition is contained in the relaxed set. For a fixed XOR keystream, each output position can then be checked independently for whether **any** permitted ciphertext byte makes it printable. A run of such possible positions gives an upper bound on every attainable printable run.

Across **7,664 cases**, the maximum possible printable run is **15 bytes**, and the maximum possible printable proportion is **50.4%**. Thus no A–F-only transformation under these exact settings can produce a long ASCII, hex, or base64 layer anywhere in the message. This bound does not assume the first bytes are readable; it examines the entire output.

Coverage: all supported registered block algorithms in libmcrypt's `ofb`, `nofb`, and `ctr` modes, with zero-byte and repeated-ASCII-`0` IVs, plus RC4; keys `Zombies`, `ZOMBIES`, `zombies`, `TheGiant`, `Revelations`; four source orientations; both nibble phases; keep/drop leading `83`. Unsupported oversized-key configurations are omitted, not silently truncated. There were **479 distinct valid cipher/key/mode/IV configurations**. Each passed an independent encryption test proving its ciphertext equals plaintext XOR the computed keystream, plus an A–F-reordered control whose full known plaintext remained feasible under the bound.

The RC4-only portion has 80 cases and a maximum possible printable run of nine bytes. This is preserved separately in the log for comparison.

This conditional exclusion does **not** cover CFB (whose keystream depends on ciphertext), unknown keys or IVs, digit-changing transformations, or binary/compressed next layers. The full CFB8 keyword pass therefore remains complementary.

The 71.9 MB completed focused input TSV was removed after verification to conserve disk space. It can be recreated exactly with `python3 -B preserved_transposes.py`; result counts and controls are retained.
