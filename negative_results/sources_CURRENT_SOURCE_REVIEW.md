# Current sources and independently verified transfer work

Checked 2026-09-07. No verified Rev-7 solution was found in the reviewed current public sources.

## New same-day result: TheGiant

Community participant `irebase` reported TheGiant solved by `u/Icy_Sheepherder_9444` on September 7, 2026. The post identifies one XXTEA layer with key `TheGiant`, using the [Movable Type tool](https://www.movable-type.co.uk/scripts/tea-block.html), and supplies a corrected transcription. It also explicitly calls Rev-7 the remaining BO3 cipher. [Original report](https://www.reddit.com/r/CODZombies/comments/1w9e5ib/solved_thegiant_cipher_solved_after_3958_days/).

I independently decrypted the published ciphertext and re-encrypted the resulting **144-byte UTF-8 plaintext** to exactly the same ciphertext. This includes the three Unicode ellipses; replacing them with three periods would change the ciphertext. Reproduction: `python3 -B xxtea_control.py`. The exact source ciphertext, recovered plaintext and result are preserved in `xxtea_control.json`. `xxtea_scanner_control.log` verifies the separate C++ search implementation recognizes the same plaintext.

The confirmed settings are corrected block TEA (XXTEA), 32-bit little-endian words, the first 16 UTF-8 key bytes right-padded with zero bytes, and the standard `6 + floor(52/n)` rounds for `n` words. XXTEA is different from the XTEA primitive in libmcrypt.

**Do not infer a verified difference in mcrypt key handling from this post.** Its comparison describes Tools4Noobs as repeating keys, but Randomiser's earlier [seven-cipher report](https://www.reddit.com/r/CODZombies/comments/1rbpx86/seven_revelations_ciphers_finally_solved/) explicitly says short fixed-size mcrypt keys are zero-padded. The existing local implementations also use that padding. I verified TheGiant's null padding; I did not verify the post's Tools4Noobs comparison.

The original [Movable Type source](https://github.com/chrisveness/crypto/blob/master/tea-block.js) agrees with the independently reproduced settings. The author's page dates its relevant UTF-8 update to 2009 and base64 update to 2014. This makes the implementation a plausible historical source, but exact ciphertext agreement alone cannot prove which copied instance of the algorithm was used.

## Another same-day result: IX #3

The same community participant reports IX #3 solved by `sunny.day.blue.sky`, with key alphabet supplied by `u/JessesOcean`: Bifid, period 8, alphabet `AFKTSNDZOXVIEHBMLPUQYWCGR`. The report continues to describe the final Revelations cipher as unsolved. [Original report](https://www.reddit.com/r/CODZombies/comments/1w9rena/solved_ix3_cipher_solved_after_2887_days/).

I independently verified this plaintext and exact re-encryption; the values are saved in `ix3_control.json`. This is current status evidence, not a Rev-7 algorithm clue. The post's characterization of a keyed Bifid alphabet as effectively a one-time pad is not adopted here.

## Most recent original Revelations solution located

Randomiser's April 11, 2026 [Rev-1 report](https://www.reddit.com/r/CODZombies/comments/1sims97/another_revelations_cipher_solved_and_notes_on/) remains the newest verified Revelations solve located. Its complete sequence is case-sensitive 52-letter Beaufort with `ZOMBIES` → RC2 ECB with `Zombies` → reverse → Rijndael-256 ECB with `Zombies`. The preexisting local `crypto.py` already verifies those modern layers and exact newline details.

That report's Rev-7 remarks are hypotheses: reverse the text, possibly AMSCO or Scytale, perhaps missing ciphertext or an additional classical layer. The report says Scytale and AMSCO keys through length 9 had been tried. It does not supply a verified Rev-7 plaintext or key.

## Additional concrete implementation lead

The same author's [AES-CTR wrapper](https://www.movable-type.co.uk/scripts/aes.html) uses an eight-byte nonce prefix and a password derivation that encrypts password bytes with AES before repeating the derived block to key length. This differs from simply giving literal `Zombies` to a standard AES mode. It accepts arbitrary message lengths and therefore deserves an exact wrapper check without assuming Rev-7 has a length error. The parent agent owns that test.

The author's [older `tea.html`](https://www.movable-type.co.uk/scripts/tea.html) actually implements XTEA ECB, not original TEA. It zero-pads the first 16 key characters and packs little-endian words, with legacy escape/unescape of text. We separately check original TEA and the 1997 uncorrected variable-width Block TEA from the authors' [TEA paper](https://www.cl.cam.ac.uk/ftp/papers/djw-rmn/djw-rmn-tea.html) and [Tea extensions paper](https://www.movable-type.co.uk/scripts/xtea.pdf).

## Later historical-source correction

An independent audit subsequently recovered CrypTool Online's pre-release 2016 source, including the [September 2 snapshot](https://github.com/cryptool-org/cto/tree/887e095c586f7dbae805ae40a29e82ce0d565a6f). The historical PHP Skytale removes decimal digits, unlike the current JavaScript implementation's optional preservation of nonalphabet characters. Historical files are preserved under `../continuation_historical_tools/`. Do not infer that today's preserved-digit Skytale behavior was the 2016 behavior. The preserved-position search remains a conditional family test; it is not a demonstrated historical attribution.
