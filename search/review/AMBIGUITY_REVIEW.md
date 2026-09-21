# Independent inspection of the 64 complete candidates

The nineteenth archived record (index 18) is a complete coherent message already present in the exhaustive output. No characters were inserted, deleted or corrected. Its exact 630 bytes include four final newline bytes after the last period.

All 64 candidates share every byte outside the four ranges below. The alternatives form the complete Cartesian product 2 × 2 × 2 × 8 = 64; cryptographic compatibility alone does not select one of them. The natural-language reading selects index 18.

| Byte range, zero-based inclusive | Existing alternatives (JSON-escaped strings) | Selected |
|---|---|---|
| 48–56 | `"<>1W$9@6i"`, `"psey is s"` | `"psey is s"` |
| 220–229 | `"a*rqL:x2i'"`, `"cover was "` | `"cover was "` |
| 400–409 | `"qF*\u0060-YXp#x"`, `"s: ‘I am"` | `"s: ‘I am"` |
| 625–629 | `" gN0y"`, `"\"EZX\\"`, `"&q3_r"`, `"*'Efs"`, `",@Cp{"`, `".\n\n\n\n"`, `".Zp(^"`, `"/<sG2"` | `".\n\n\n\n"` |

The selected bytes were independently encrypted and decrypted through libmcrypt `blowfish-compat` CFB8, password `Zombies`, eight ASCII `0` IV bytes. Encryption reproduced the archived 630-byte ciphertext exactly. Historical AMSCO encode with numeric key `1947038265`, followed by reversing all hex characters, reproduced the original 1,092-character Rev-7 transcription exactly. This local check used the previously PHP-validated literal encoder; the other verification agent is executing the original unchanged PHP separately.

The three internal choices read “Dempsey is still”, “but my cover was blown”, and “It reads: ‘I am not”. Their alternatives are unrelated printable gibberish. The eighth-way ending choice yields a period followed by four newlines; the other seven endings contain unrelated punctuation and letters.

Exact plaintext SHA-256: `35e58315c1edbfeb73a244c0a8075dc8e07709a2c554736726e45ce756c9d280`.
Exact recovered ciphertext-byte SHA-256: `2f7ff5dfff2d7de31556da56f941bb7f6f7d1299fb3b8540df85791c727ce13a`.

[Untouched plaintext](selected_plaintext.txt), [full recovered ciphertext hex](selected_cipher.hex), [machine-readable ambiguity table](ambiguity.json), [all 64 plaintexts](all_candidate_plaintexts.json).
