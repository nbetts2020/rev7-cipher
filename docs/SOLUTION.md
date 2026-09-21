# Rev-7

**The message is recovered.** The reconstruction reproduces every one of the
paper's 1,092 hexadecimal characters and all 219 printed groups. I did not
change the original transcription.

> MI-8 transcript. Field Report 1918: Corporal Dempsey is still at large in
> France. My orders are to bring him back to US intelligence to face charges and
> find out who he is working for. I almost had him in Calais, but my cover was
> blown and he evaded capture. He retreated deep behind enemy lines somewhere in
> northern France. He did leave behind some cryptic intel though. A handwritten
> note. It reads: ‘I am not a monster. He is the monster. The secret is in the
> mound. I must go to the mound. Remember that! Why can’t I ever remember that.’
> Not only is Dempsey a traitor, but he has lost his mind. I better be careful.

That file is exactly **630 UTF-8 bytes**, including the curly quotes and
apostrophes and **four line feeds after the final period**. The bytes are in
`solution/plaintext.txt`. Don't let an editor normalize them.

## The chain

| # | Layer, in encryption order | Exact settings |
|---|---|---|
| 1 | Block cipher | libmcrypt `blowfish-compat`, CFB8. Raw ASCII key `Zombies`, 7 bytes / 56 bits. IV `3030303030303030`, which is eight ASCII zero characters, not eight zero bytes |
| 2 | Representation | Uppercase hexadecimal. 630 encrypted bytes become 1,260 characters |
| 3 | Historical AMSCO | Numeric key `1947038265`. Continuous two-character / one-character cells, starting with two. Reproduce the omission of the column labeled `0` |
| 4 | Presentation | Group in fives, then reverse the whole grouped string. The paper adds its own line wrapping |

## The bug

**The zero in the key sits in the fifth column.** That column holds two
hexadecimal characters per 15-character row. Across 84 rows it drops 168:

```
1,260 - 168 = 1,092
```

which is the count on the paper. Reversing the grouped output is also what
leaves the stray two-character group `83` at the front.

You can read the defect yourself in the [pinned 2016 source](https://github.com/cryptool-org/cto/blob/887e095c586f7dbae805ae40a29e82ce0d565a6f/_ctoLegacy/tools/amsco/class.amsco.php).
Its output loop reads labels 1 through the key length, so it never emits label
`0`. The key also fits inside a signed 32-bit integer, which matters because the
PHP wrapper casts it. Running that unchanged class under PHP 8.4.25 reproduces
the paper exactly.

That proves the construction matches. It does not prove which copy of the
software the author actually used.

## How the missing characters came back

**Reverse the paper, invert the surviving AMSCO columns, and you get a
1,260-character pattern with 168 unknown nibbles.** A CFB8 constraint search
fills those in, allowing only ASCII text or a small specified repertoire of
well-formed UTF-8 typography. The broad key sweep found the key above. A fresh,
targeted run with that key, algorithm and IV, **with no plaintext crib supplied
to the search**, returned all 64 compatible completions.

## What is ambiguous

**Because a column is erased, the original bytes are not mathematically
unique.** Under the tested text repertoire there are 64 complete candidates.
596 of the 630 bytes are identical across all of them. Four spans differ,
admitting 2 × 2 × 2 × 8 alternatives between them.

Candidate 18, counting from zero, is the coherent reading in all four:
`psey is s`, `cover was `, `s: ‘I am`, and a final period followed by four
newlines. The others give nonsense. The message quoted above is that candidate
with **nothing corrected and no words inserted**.

Every alternative is kept in `solution/all_64_candidates.txt.gz`, and
`solution/ambiguity.json` maps the regions that differ.

## Check it yourself

```sh
python3 -I solution/verify_portable.py
```

Stock Python 3, standard library only. No native crypto library, no network, no
dependencies. It checks the recovered ciphertext and plaintext, both encryption
layers, the omitted column, the original compact ciphertext and the grouping.

All 64 candidates were also re-encrypted with libmcrypt back to their
reconstructed ciphertexts, then pushed through both an independently written
AMSCO projection and the unchanged PHP class, and all 64 reproduce the paper.
The selected candidate matches every printed five-character token, differing
only in line-wrap whitespace.

## Re-run the search

```sh
python3 -B search/zero_full/targeted_reproduce.py
```

This runs a native CFB8 constraint solver against the observed paper and the
masked AMSCO layout, linked against a locally built libmcrypt 2.5.8, with no
plaintext crib. It returns exactly 64 completions, all of them
`blowfish-compat` with the IV fill above. Picking candidate 18 happens after
enumeration and is a reading judgment, not a solver output.

Build instructions are in `lib/BUILD.md`. `search/README.md` explains the method
and states exactly how much of the key space was covered, which is less than all
of it.

## Hashes

| Thing | SHA-256 |
|---|---|
| Selected plaintext, 630 bytes | `35e58315c1edbfeb73a244c0a8075dc8e07709a2c554736726e45ce756c9d280` |
| Original compact uppercase ciphertext | `5c50001013a2dd862e13c38d314a0ba6d7303794287a05cc999018cf82cf4b1c` |
