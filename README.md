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
message, encrypted it, and got 1,260 characters. They ran that through a free
online scrambling tool to shuffle it. The tool handed back 1,092 characters — it
had silently deleted 168 of them and reported no error. That output is what went
into the game.

So 13% of the ciphertext isn't on the paper, and never was. **It was not
solvable as designed.** No amount of cleverness would decrypt it, because part
of it does not exist.

**That is also why every attempt stalled.** A shuffling cipher normally
preserves length: 1,092 characters in, 1,092 out. So people reasonably treated
the 1,092 characters on the paper as the complete message and searched for the
shuffle that unscrambles them. That search cannot succeed — the real message was
1,260 characters. It was never a matter of searching harder; the answer was
outside the space being searched.

**How it came apart.** Rather than guess at the cipher, this work went and
fetched the actual source code of the 2016 tool, pinned to the version that was
live when the game shipped, and read it. The bug is right there in the file: the
tool labels its columns with the digits of your key, then prints out columns `1`
through `N`. If your key contains a `0`, that column gets built, gets filled,
and never gets printed. Everything in it is discarded.

That turns the missing characters from a mystery into arithmetic:

```
1,260 − 1,092 = 168 = 2 × 84
```

168 characters gone, two from each of 84 rows — the exact shape of one dropped
column. The size of the hole tells you the key contains a `0` and roughly where
it sits. That is what collapsed millions of candidate keys into a searchable
set, and `1947038265` is the one that fits. Running the unmodified 2016 file
today reproduces the paper exactly, which confirms the construction — though not
which copy of the tool the author actually used.

**The missing text was rebuilt, not recovered.** Those 168 characters are gone
for good. What made them reconstructable is the underlying cipher: each byte
depends only on the handful before it, so damage stays local and readable text
re-synchronizes around the gaps. A search rebuilt them from context, pinning 596
of the 630 bytes to a single possible value. Four small spots admit more than
one reading; one version is coherent English and the rest are gibberish, so the
message itself is not in doubt — but this is a reconstruction, not a decryption.
That distinction is why the caveats below are worth reading.

## Credits

The key `Zombies` was not discovered here. It was established from the other
*Revelations* ciphers by **Randomiser** and the community, crediting
**JessesOcean** for the Rev-10 discovery. Randomiser's April and later Rev-7
notes identified CrypTool and AMSCO as leads, documented failed AMSCO searches
through nine-digit keys, and raised missing ciphertext as a possible
explanation — the thread this solve pulled on.

The solve itself was carried out with OpenAI Codex (gpt-6-astra).

