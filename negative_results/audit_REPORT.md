# Independent same-key audit and continuation

**Status:** No candidate passed the 40-byte printable-run gate in these completed scopes.

The original reports accurately acknowledge their main assumptions. I found no demonstrated bug that invalidates the completed searches. The material gap addressed here is using the same dictionary word for both an outer classical transposition and the modern encryption key; previous broad outer-key scans held the inner key fixed to `Zombies`.

The source corpus contains 161,354 literal UTF-8 keys. Each is tested with the same literal outer key, then with additional permutations induced by normalizing ASCII letter case only in the outer key. The latter pass skips all permutations already tested for that literal key. Per-key deduplication is essential: global transposition deduplication would incorrectly omit different modern keys.

Outer families: columnar, AMSCO with both starting sizes and row-alternating/fixed-column patterns, and repeated-letter Myszkowski; both tie directions; code point and UTF-8 ordering where distinct; input hex reversal, byte reversal, nibble swap; forward/inverse transformation; output reversal; two nibble phases. These permutations move all hex symbols; they do not test holding digits fixed while moving only A–F. No damage or whitespace reconstruction is added.

Inner families: 19 block primitives, with libmcrypt-supported literal key sizes and zero padding. Seven modes are CFB8, full-block CFB, ECB, CBC, OFB8, full-block OFB, and CTR. OFB/CTR use both ASCII `0` and zero-valued IV fills. Feedback-mode checks probe interior positions independent of the IV and render candidates with ASCII `0` IV. Native RC4/WAKE/Enigma are outside this pass. ECB/CBC ignore incomplete trailing blocks when detecting readable text; this does not supply a valid padding or framing explanation for the 546-byte input.

CFB8/full-block CFB probe 16-byte windows near offsets 48, 192 and 384. ECB/CBC probe two full blocks at the corresponding block-aligned positions. OFB/CTR probe the first 16 bytes using precomputed keystream prefixes. A promising candidate must subsequently have a printable run of at least 40 bytes. This can miss compressed/binary layers, short surviving fragments, and some corruption patterns.

Validation: 64 independently encrypted full-chain controls cover 16 registered primitives × four feedback/block modes. Another 48 cover OFB8/OFB/CTR. Another 30 cover all three extra primitives × seven modes and nine zero-IV/UTF-8 combinations. Seven additional exact-plaintext controls exercise a case-normalized outer keyword. These are 149 controls, separate from attack counts.

Recorded attack instances: 322,708 key/pass instances; 2,166,435 permutations; 69,325,920 candidate byte-string instances; 17,811,571,200 probe checks; 0 hits. Key instances can occur in both case passes. Counts include equivalent orientations and are not a fraction of the possible construction space. Complete: True.

`focused.log` and `full_corpus.log` were deliberately interrupted because the four `full_part*.log` runs supersede them. Their counters are excluded. `benchmark.log` and `expanded_benchmark.log` are also excluded.

Reproduce from the parent folder:

```sh
clang++ -O3 -std=c++17 -I mcrypt/include continuation_audit/same_key.cpp -L mcrypt/lib -lmcrypt -o continuation_audit/same_key_expanded
clang++ -O3 -std=c++17 -I mcrypt/include continuation_audit/same_key_case.cpp -L mcrypt/lib -lmcrypt -o continuation_audit/same_key_case
python3 -B continuation_audit/controls.py
python3 -B continuation_audit/expanded_controls.py
python3 -B continuation_audit/extra_controls.py
python3 -B continuation_audit/case_controls.py
for part in 0 1 2 3
do
  ./continuation_audit/same_key_expanded continuation_audit/keys_part${part}.txt > continuation_audit/full_part${part}.log 2>&1
  ./continuation_audit/same_key_case continuation_audit/keys_part${part}.txt > continuation_audit/case_part${part}.log 2>&1
done
python3 -B continuation_audit/report.py
```

The four partition files preserve every fourth corpus line, with hashes in `partitions.json`. Source/input hashes and per-run counters are in `STATUS.json`. Neither exact decrypt/encrypt round trips nor printable bytes alone establish a solution; any hit still needs a coherent message and reproducible full chain.
