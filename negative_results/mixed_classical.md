# Mixed classical layers

No candidate passed the text detector. The completed pass covered **1,353,216 byte-stream instances** from 5,286 ordered layer pairs in 137 seconds.

The fixed layers were historical AMSCO with `135624` (the recovered default), AMSCO with the published DE key `198346572`, and columnar transposition with `CODE` (the recovered columnar default). Each was paired in both layer orders with 881 distinct target permutations: ASCII keys from the 475-entry focused file, six valid numeric AMSCO keys, and unkeyed column widths 2–546. The count is after exact target permutation deduplication; equivalent composed transformations can remain.

Both directions of each layer were tested independently, with four input orientations, an optional reversal between the layers, four output orientations, and two hexadecimal byte phases. The modern key was `Zombies`. Detection covered all 19 block primitives under CFB8, NCFB, ECB and CBC, plus 97 cached OFB8/NOFB/CTR/RC4 configurations. Feedback/block modes used repeated ASCII `0`; cached independent streams included ASCII and binary-zero IVs. Incomplete ECB/CBC tails were not invented or treated as plaintext.

All **115 independently encrypted control chains** recovered the exact pre-transposition ciphertext and complete expected plaintext. These used literal historical AMSCO operations, separate direct row/column assignment, and libmcrypt encryption. Shared modern scanners already had independent mode controls.

This is a conditional search of specified layer pairs, not evidence that Rev-7 used either historical default. Generic target keys use stable ASCII sorting and are not claimed to reproduce every historical alphabet-normalization option. The detector looks for long ASCII spans at sampled positions; it can miss nontext intermediates, distributed damage, or a different modern key. No plaintext was recovered.

Sources and reproduction: `scan.cpp`, `support.inc`, `controls.py`; run `python3 -B continuation_mixed_classical/controls.py` then `./continuation_mixed_classical/scan scan continuation_unicode/seed_keys.txt` from the project root. Historical source authentication is documented in `../continuation_historical_tools/FINDINGS.md`.
