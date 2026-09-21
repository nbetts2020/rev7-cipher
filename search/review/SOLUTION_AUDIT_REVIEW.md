# Independent confirmation of the Rev-7 recovered message

**Candidate 18 is a coherent, unedited recovered plaintext and exactly regenerates every observed hexadecimal character.** Its plaintext SHA-256 is `35e58315c1edbfeb73a244c0a8075dc8e07709a2c554736726e45ce756c9d280`.

The exact forward chain is:

1. UTF-8 plaintext bytes, including the selected record's terminal period and four LF bytes.
2. libmcrypt `blowfish-compat`, mode `cfb` (CFB8), literal key `Zombies`, eight-byte IV `3030303030303030` (ASCII zero characters).
3. Convert the 630 encrypted bytes to 1,260 uppercase hex characters.
4. Execute the recovered original AMSCO implementation with numeric key `1947038265`. Cells alternate 2,1 continuously. This malformed ten-column key assigns label zero to one column; the implementation emits labels 1–10, so column zero's 168 hex characters disappear.
5. Reverse the entire resulting 1,092-character hexadecimal string. Ignore display grouping/whitespace when comparing to the paper.

The numeric key is below the signed 32-bit limit. This result does not depend on a 64-bit-only integer value, although the available original-source execution used PHP-WASM 8.4.25 with 64-bit integers. The exact original class bytes were loaded unchanged, with SHA-256 `132d61ff8b794ab9717a0ce284d7bf21f82c8dbfe39bf9f1a3b5f7aa7eb91e4f`.

Independent checks completed for **all 64 emitted candidates**:

- Original libmcrypt API decrypts each complete recovered ciphertext to its recorded plaintext exactly.
- Original libmcrypt API re-encrypts each recorded plaintext to its recovered ciphertext exactly.
- A separately written explicit cell/column-index loop recreates the observed 1,092 hexadecimal characters exactly.
- Executing the unchanged historical PHP class also recreates those 1,092 characters exactly after reversal.

These checks use the actual modern library and original historical source, rather than relying only on the recovery solver's own recurrence. The original PHP interpreter receives recovered ciphertexts and keys but no expected output; the caller compares its returned output afterward.

The erased column makes the transformation lossy. The 64 completions in the solver's finite character repertoire form exactly `2 × 2 × 2 × 8` choices at four spans. Three choices distinguish intelligible clauses from gibberish:

| Zero-based plaintext byte span | Coherent alternative | Other alternative |
|---|---|---|
| 48–56 | `psey is s` | `<>1W$9@6i` |
| 220–229 | `cover was ` | `a*rqL:x2i'` |
| 400–409 | `s: ‘I am` | ``qF*`-YXp#x`` |

The final five bytes have eight exact alternatives. Candidate 18 contains `.` followed by four LF bytes; the other endings contain unrelated punctuation/letters. The main-message clauses and natural ending therefore identify candidate 18 by English coherence, not by pretending that the lossy ciphertext uniquely determines every possible plaintext. Its contents were not edited to create this match. `RESULTS.json` preserves all alternatives, including the trailing-byte ambiguity.

Files:

- `recovered_plaintext.txt`: exact candidate 18 UTF-8 bytes.
- `selected.json`: exact solver record and recovered full ciphertext.
- `RESULTS.json`: independent checks, hashes and ambiguity sets.
- `php_results.json`: original-source execution evidence.
- `verify.py`, `verify_php.mjs`: reproducible independent checks.

```sh
node continuation_audit/rev7_solution_audit/verify_php.mjs
python3 -B continuation_audit/rev7_solution_audit/verify.py
```

This verifies the recovered message and construction. It does not establish whether using a zero-labelled key was an authoring mistake or an intentional difficulty choice.
