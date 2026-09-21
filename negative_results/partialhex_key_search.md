# Independent inner-key search with fixed digits

No hit. All four restricted-alphabet scans completed with no capped trials. The key is independently unknown:161,354 main/extended corpus keys plus157 previously tested asset/focused keys absent from that corpus. There is no assumed transposition keyword; each A-F nibble may independently vary over A-F, so this covers a superset of letter-only transpositions and substitutions. Digits remain fixed.

For each main-corpus character class, the scan executed2,814,438 valid key/algorithm configurations and67,546,512 input/key/algorithm/IV trials. Twelve orientations, phases and leading-byte-removal variants are explicit in the shared input generator. Modes:CFB8 only;19 block primitives;ASCII-zero and binary-zero IVs. Literal UTF-8 keys use validated mcrypt supported-size zero-padding and length limits. No hashing or silently truncating long keys is assumed.

The four classes are uppercase hex, lowercase hex, lowercase letters plus specified punctuation/whitespace, and uppercase letters plus the same punctuation/whitespace. Each class is required throughout the entire reconstructed message. Opposite-case letters, numbers in the letter classes, arbitrary prefix corruption/IVs, and binary intermediates remain outside these results. This model may be computationally useful but is not asserted to be the2016 tool's behavior; recovered historical Skytale code actually discarded digits.

Ten independently encrypted controls with a non-default inner key, Group935, recovered exact complete plaintexts after arbitrary A-F rearrangement. Because the relaxation permits alternative endings, multiple candidate reconstructions can satisfy a control; the known plaintext was among them. Candidate emission is capped, but the hit counter continues.

A separate2,000-key Base64 benchmark was bounded and reached4,078 caps; it is not part of the completed four-class result. No full Base64 corpus search was claimed.

Scripts:keyscan.cpp,validate_keys.py. Exact counters:KEY_SEARCH_RESULTS.json. Logs:keys_CLASS.log and extra_keys_CLASS.log. Run from parent directory with `./continuation_partialhex/keyscan CLASS continuation_aesctr/all_keys.txt 10000`.
