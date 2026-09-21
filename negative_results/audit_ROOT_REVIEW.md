# Independent review of the substitution, partial-hex and AES-CTR continuations

**Finding:** I found no demonstrated false-negative implementation bug in the completed restricted searches. Their negative results are valid only under the stated key, mode, representation and plaintext-alphabet assumptions. They do not establish that Rev-7 is unsolvable or exclude unrestricted English.

## Arbitrary bijective hex substitution

The DFS in `continuation_substitution/substitute.cpp` correctly enforces a one-to-one mapping of all 16 hex symbols. Its full-block CFB look-ahead checks necessary conditions for each remaining pair in the current block; it does not incorrectly commit unknown mappings during that check. Backtracking restores both the mapping and used-value mask.

All five recorded classes completed their 304 algorithm/mode/IV/orientation cases without a node cap or hit. The restricted alphabet applies until all 16 mapping values are assigned; afterward, the whole message is decrypted and must contain an 80-byte printable run. Therefore an entirely class-restricted plaintext of the observed length would pass the gate, if its other assumptions are correct. This is not an exhaustive test of mixed-case English: the lower/upper classes exclude the opposite case and decimal digits, and each permits only its explicitly listed punctuation. Base64 permits letters, digits, `+`, `/`, `=`, CR and LF, but no spaces.

The existing 64 controls cover the registered primitives. I added 12 independent raw-primitive controls covering Threeway and both extra SAFER implementations, each in CFB8/full-block CFB with both IV fills. Every exact plaintext was recovered without a cap. Supplementary fixtures and results: `root_review/extra_substitution.*`.

## Digit-preserved, A–F reconstruction

`reconstruct.cpp` keeps each numeric nibble fixed, permits A–F values at letter positions, and correctly accounts for their remaining counts, including when both nibbles of a byte consume the same letter. Its complete-message terminal test enforces the original A–F histogram.

The five strict CFB8 classes and the uppercase-hex full-block CFB run each completed 152 cases with no caps or hits. These results assume key `Zombies`, the tested orientations, and either repeated ASCII `0` or zero-valued IV bytes. The separate general-printable CFB8 run has four capped cases. Its `DONE` line means the scheduled loop finished, not that all 152 search trees were exhausted.

I added six exact full-message reconstruction controls for the three extra primitives and both IV fills; all passed.

## Interior reconstruction without knowing the IV

The CFB8 interior method is sound for its restricted negative conclusions:

1. It chooses one full preceding ciphertext block whose numeric nibbles are known and whose A–F nibbles are enumerated.
2. Every possible A–F value assignment for that context is tried, unless the node cap is reached.
3. Once this preceding block is supplied, subsequent CFB8 output no longer depends on the initial IV.
4. The subsequent DFS deliberately drops histogram conservation. Its possibilities are consequently a **superset** of actual A–F-only permutations. Failing to find a class-restricted suffix in that larger set excludes one in the smaller set under the same remaining assumptions.

Each of the four strict interior logs contains 136 completed cases: 17 primitives × four orientations × two nibble phases. None capped or hit. The 16 skipped combinations belong to Rijndael-192 and Rijndael-256, whose **block sizes** are 24 and 32 bytes. This is not a statement about AES-192/256 key sizes. The configured maximum is seven unknown context nibbles; the included Rev-7 cases actually have at most five. Every chosen start leaves at least 80 suffix bytes, so an entirely class-restricted suffix cannot be lost merely because of the 80-byte gate.

The four classes are uppercase hex, lowercase hex, lowercase letters with specified punctuation, and uppercase letters with specified punctuation. There is no completed IV-independent base64 or unrestricted-printable exclusion here. A valid construction whose suffix leaves its tested alphabet is outside these results.

I independently encrypted controls with **nonuniform random IVs** for all 17 included primitives, shuffled only their A–F symbols, and recovered every exact suffix without supplying those IVs to the solver. This adds 17 controls beyond the original 28 tests using uniform IV fills. See `root_review/random_iv_interior.*` and `feedback_checks.json`.

The permissive interior-print run must remain marked **aborted and inconclusive**. Its retained log has 35 completed CASE lines, 26 capped cases, no DONE line, and a final cumulative hit count of 662,384. Only three illustrative HIT records remain after the stated trimming. Those are constructed printable suffixes: the prefix is not reconstructed, the letter histogram is not enforced, and no outer permutation or coherent message is established. They are not cipher solutions. The current output limit in `support.inc` limits printed records, not the hit counter; strict no-hit claims are supported by the CASE counters, not merely by counting printed records.

## Chris Veness AES-CTR wrapper

The C++ implementation matches the supplied JavaScript at the byte level:

- Passwords are UTF-8 encoded, then truncated or zero-padded to 16, 24 or 32 bytes.
- AES encrypts the first 16 password bytes under that password-derived key; the resulting block is repeated as needed for the working key.
- The first eight ciphertext bytes form the nonce; the remaining counter bytes hold the block number in big-endian order.

The recorded direct scan used the exact 161,354-key corpus, 40 distinct byte inputs and all three AES key lengths: **19,362,480 candidate instances**, with no hit. This is a wrapper-specific password test, not an exclusion of AES generally. Its 80-byte printable-run gate can miss binary or non-ASCII layers, and it assumes the nonce is represented by the first eight bytes of the tested input.

The original 18 JavaScript controls passed. I generated 15 additional vectors from that same JavaScript using long passwords, truncation inside UTF-8 characters, and astral characters. Every complete decryption matched, and every long-message vector was also recovered through the actual `direct` search gate. These supplement the original controls, which exercise the direct decryption function rather than that gate. See `root_review/aes_edges.cjs`, `aes_edges.txt`, `aes_edges.log`, `aes_gate.log` and `aes_checks.json`.

## Review boundaries and reproduction

This review reads the local source and captured logs; it does not authenticate the supplied JavaScript as the exact version used in 2016. It does not turn any constructed printable output into a solution. Root-owned files were left unchanged.

Run the supplementary checks from the project root:

```sh
python3 -B continuation_audit/root_review/feedback_checks.py
node continuation_audit/root_review/aes_edges.cjs > continuation_audit/root_review/aes_edges.txt
./continuation_aesctr/scan stdin < continuation_audit/root_review/aes_edges.txt
```

The additional AES direct-gate fixtures are `root_review/aes_inputs.tsv` and `root_review/aes_keys.txt`; run them with `./continuation_aesctr/scan direct` followed by those two paths. All supplementary feedback checks assert exact full messages or exact suffixes, as applicable, and reject capped controls.

Further failed-state caching review and bounded mixed-case follow-up: [MEMO_REVIEW.md](audit_MEMO_REVIEW.md).
