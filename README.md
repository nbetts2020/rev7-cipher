## Rev-7 Cipher

<img width="1000" height="500" alt="image" src="https://github.com/user-attachments/assets/0288956c-5cfb-44d5-a92a-bd2fda4b3af0" />

The last unsolved cipher from *Call of Duty: Black Ops III*, the **Origins Trench
paper** in *Revelations*, is solved.

This repo contains the transcription, the recovered plaintext, and everything necessary to recreate the solve.

## Message

> MI-8 transcript. Field Report 1918: Corporal Dempsey is still at large in
> France. My orders are to bring him back to US intelligence to face charges and
> find out who he is working for. I almost had him in Calais, but my cover was
> blown and he evaded capture. He retreated deep behind enemy lines somewhere in
> northern France. He did leave behind some cryptic intel though. A handwritten
> note. It reads: ‘I am not a monster. He is the monster. The secret is in the
> mound. I must go to the mound. Remember that! Why can’t I ever remember that.’
> Not only is Dempsey a traitor, but he has lost his mind. I better be careful.

## Solve

**Biggest Finding: the cipher was almost unsolvable because...it was broken.** In 2016, Treyarch wrote the
message, encrypted it, and got 1,260 characters. To shuffle those, they likely ran them
through an **AMSCO** transposition tool built on code from **CrypTool-Online**,
the free browser edition of CrypTool, which back then lived at `cryptool-online.org`. The tool
handed back 1,092 characters. It had silently deleted 168 of them and reported
no error. That output is what went into the game.

**That is also why every attempt stalled.** A shuffling cipher normally
preserves length: 1,092 characters in, 1,092 out. So a reasonable assumption treated
the 1,092 characters on the paper as the complete message and searched for the
shuffle that unscrambles them. That search cannot succeed, as the real message was
1,260 characters.

**Breakthrough.** Rather than continuing to hack away at the cipher itself, I
fetched CrypTool-Online's source — the file `class.amsco.php`, pinned to the
version that was live when the game shipped, and read it. The bug is
unmistakable - the tool labels its columns with the digits of your key, then
prints out columns `1` through `N`. If your key contains a `0`, that column gets
built, gets filled, and never gets printed. Everything in it is discarded.

CrypTool never fixed this. The file was quietly deleted in 2020 as part of a
legacy refactor, and no public bug
report or fix was ever filed against it. The modern site has no AMSCO tool. But
the bug itself was never corrected — byte-identical copies of that file were
still sitting in eleven public repositories as of September 2026.

Thus:

```
1,260 - 1,092 = 168 = 2 × 84
```

168 characters gone, two from each of 84 rows — the exact shape of one dropped
column. The size of the hole tells you the key contains a `0` and roughly where
it sits. That changed what to search for. Sweeping the keys that could leave a gap this
size turned up `1947038265`. Running the unmodified 2016 file
today reproduces the paper exactly.

**The missing text was rebuilt, not recovered.** Those 168 characters are gone
for good. What made them reconstructable is the underlying cipher, wherein each byte
depends only on the handful before it, so damage stays local and readable text
re-synchronizes around the gaps. A search rebuilt them from context, pinning 596
of the 630 bytes to a single possible value. Four small spots admit more than
one reading; one version is coherent English and the rest are gibberish, so the
message itself is not in doubt — but this is a reconstruction, not a decryption.

## Credits

The key `Zombies` was not discovered here. It was established from the other
*Revelations* ciphers by **Randomiser** and the community, crediting
**JessesOcean** for the Rev-10 discovery. Randomiser's April and later Rev-7
notes identified CrypTool and AMSCO as leads, documented failed AMSCO searches
through nine-digit keys, and raised missing ciphertext as a possible
explanation — the thread this solve pulled on.

**AI Disclaimer.** Research and discovery was aided in part by GPT-6 Astra Ultra.

