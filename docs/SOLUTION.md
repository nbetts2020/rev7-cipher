# Revelations Rev-7 / Origins Trench — recovered September 7, 2026

_All paths in this document are relative to the repository root._

**The message is recovered.** The coherent completion reproduces every one of the paper's 1,092 hexadecimal characters and all 219 printed groups. The original ciphertext transcription was not changed.

> MI-8 transcript. Field Report 1918: Corporal Dempsey is still at large in France. My orders are to bring him back to US intelligence to face charges and find out who he is working for. I almost had him in Calais, but my cover was blown and he evaded capture. He retreated deep behind enemy lines somewhere in northern France. He did leave behind some cryptic intel though. A handwritten note. It reads: ‘I am not a monster. He is the monster. The secret is in the mound. I must go to the mound. Remember that! Why can’t I ever remember that.’ Not only is Dempsey a traitor, but he has lost his mind. I better be careful.

The exact file contains **630 UTF-8 bytes**, including the curly quotation marks/apostrophe and **four LF bytes after the final period**. Those bytes are preserved in `solution/plaintext.txt`.

| Layer, in encryption order | Exact settings |
|---|---|
| Modern encryption | libmcrypt `blowfish-compat`, CFB8; raw ASCII key `Zombies` (7 bytes / 56 bits); IV `3030303030303030` (eight ASCII zero characters) |
| Representation | Uppercase hexadecimal: 630 encrypted bytes become 1,260 characters |
| Historical AMSCO | Numeric key `1947038265`; continuous two-character/one-character cells, starting with two; reproduce the historical omission of the column labeled `0` |
| Final operation | Group in fives, then reverse the entire grouped string; the paper adds its visual line wrapping |

The essential discovery was **data loss in the historical AMSCO implementation**. The zero is in the fifth column. That column holds two hexadecimal characters per 15-character row. Across 84 rows, it drops 168 characters: **1,260 − 168 = 1,092**. Reversing the grouped result also explains the leading two-character group `83`.

This behavior is present in the authenticated pre-release [CrypTool AMSCO source](https://github.com/cryptool-org/cto/blob/887e095c586f7dbae805ae40a29e82ce0d565a6f/_ctoLegacy/tools/amsco/class.amsco.php). Its output loop reads labels 1 through the key length, so it never emits label 0. The numeric key fits a signed 32-bit integer. Executing the unchanged historical class in PHP 8.4.25 reproduced the paper exactly. This verifies a matching construction; it does not establish which software deployment the original author used.

**How the recovery was obtained.** Reversing the paper and inverting the surviving AMSCO columns gives a 1,260-character pattern with 168 unknown nibbles. A CFB8 constraint search reconstructs those nibbles while requiring ASCII text or a specified small repertoire of well-formed UTF-8 typography. The broad zero-key search found the key above. A fresh, targeted run with that key, algorithm and IV, **without supplying a plaintext crib**, reproduced all 64 compatible completions.

**The ambiguity is explicit.** Because a column is erased, the original bytes are not mathematically unique. Under the tested text repertoire, there are 64 complete candidates: 596 of 630 bytes are identical, while four spans admit 2 × 2 × 2 × 8 alternatives. Candidate 18 (zero-based) is the coherent reading throughout: `psey is s`, `cover was `, `s: ‘I am`, and a final period plus four newlines. The other choices contain nonsensical character sequences. The quoted message is that candidate **without corrections or inserted words**. All alternatives are retained in `solution/all_64_candidates.txt.gz` and explained in `solution/ambiguity.json`.

**Verification.** Three independent reviews checked the plaintext and ciphertext. All 64 candidates re-encrypt with libmcrypt to their corresponding reconstructed ciphertext and then reproduce the original paper through both independently written AMSCO projections and the unchanged PHP class. The selected candidate also matches every printed five-character token, allowing only line-wrap whitespace differences.

Run the portable forward/decryption verifier from this project:

```sh
python3 -I solution/verify_portable.py
```

It uses Python's standard library and the small files in `solution/`; it requires no native crypto library or network. It verifies the recovered ciphertext and plaintext, both encryption layers, the omitted column, original compact ciphertext, and grouping.

To repeat the missing-nibble search itself:

```sh
python3 -B search/zero_full/targeted_reproduce.py
```

This runs a native CFB8 constraint solver, linked against a locally built libmcrypt 2.5.8, against the observed paper and the masked AMSCO layout, with no plaintext crib supplied. It returns exactly 64 completions, all of them `blowfish-compat` with the IV fill above. The post-search selection of candidate 18 is a reading judgment, recorded explicitly as such. Build instructions are in `lib/BUILD.md`, and `search/README.md` explains the method and states exactly how much of the key space was covered.

Exact selected plaintext SHA-256:

`35e58315c1edbfeb73a244c0a8075dc8e07709a2c554736726e45ce756c9d280`

Original compact uppercase ciphertext SHA-256:

`5c50001013a2dd862e13c38d314a0ba6d7303794287a05cc999018cf82cf4b1c`

The earlier negative search reports are historical records superseded by this recovery.
