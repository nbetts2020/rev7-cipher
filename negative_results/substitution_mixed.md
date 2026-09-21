# Mixed-case hexadecimal substitution follow-up

No candidate was recovered. All **304** algorithm/mode/IV/orientation trials exhausted their search trees, with **781,752,551 nodes and no caps**, in 297 seconds. Eight independently encrypted Serpent/RC2 CFB8/NCFB controls, with both IV fills, recovered their exact complete plaintexts.

This extends the earlier uppercase-only and lowercase-only prose searches to both letter cases, spaces, CR/LF, and `.,\'!?-:;`. It includes ordinary mixed-case prose in the constrained opening. Digits, other punctuation, and arbitrary UTF-8 remain outside that opening alphabet.

The model is an arbitrary bijective mapping of all 16 hexadecimal symbols applied before decryption, modern key `Zombies`, all 19 block primitives, CFB8 and NCFB, repeated ASCII-zero or binary-zero IVs, and four input orientations. Once all 16 symbols are assigned, the complete decryption must contain an ASCII run of at least 80 bytes. This is a candidate detector, not proof of English; no candidate reached it here.

Reproduce with `./continuation_substitution/substitute scan 500000000 mixed`. Controls: `python3 -B continuation_substitution/validate_mixed.py`. Machine counters are in `MIXED_RESULTS.json`.
