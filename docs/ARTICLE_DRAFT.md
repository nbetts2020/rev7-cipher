# The Missing Column: Recovering Revelations’ Origins Trench Cipher

The Origins Trench paper in *Call of Duty: Black Ops III — Revelations* contains a report about Corporal Dempsey in France in 1918. I have recovered a coherent reading of that report and a construction that reproduces every hexadecimal character printed on the paper.

The decisive discovery was a behavior in an old cipher tool: under the key used in the successful reconstruction, it silently discarded an entire column of characters.

Here is the recovered message:

> MI-8 transcript. Field Report 1918: Corporal Dempsey is still at large in France. My orders are to bring him back to US intelligence to face charges and find out who he is working for. I almost had him in Calais, but my cover was blown and he evaded capture. He retreated deep behind enemy lines somewhere in northern France. He did leave behind some cryptic intel though. A handwritten note. It reads: ‘I am not a monster. He is the monster. The secret is in the mound. I must go to the mound. Remember that! Why can’t I ever remember that.’ Not only is Dempsey a traitor, but he has lost his mind. I better be careful.

This investigation builds on substantial community work. Randomiser’s published Revelations solutions established the importance of the old mcrypt encryption library, the case-sensitive password `Zombies`, and specific encryption settings. That report also credited JessesOcean and the community for the Rev-10 discovery that helped establish `Zombies` as a candidate key. Those findings gave this search a foundation. [Earlier Revelations solutions](https://www.reddit.com/r/CODZombies/comments/1rbpx86/seven_revelations_ciphers_finally_solved/)

Randomiser’s later Rev-7 notes were especially relevant. The paper uses uppercase hexadecimal arranged in groups of five, except for the opening `83`. That unusual first group suggested reversal. The notes also identified CrypTool, AMSCO and Scytale as promising leads, documented unsuccessful AMSCO searches through nine-digit keys, and raised missing ciphertext as a possible explanation. [Rev-7 research notes](https://www.reddit.com/r/CODZombies/comments/1sims97/another_revelations_cipher_solved_and_notes_on/)

I continued the investigation with Codex, using it to help examine historical source code, build and run searches, and verify the results. The process included many unsuccessful tests. Trying a cipher name and a plausible password was not enough; the implementation details and the condition of the surviving text mattered.

The productive turn came from examining a version of CrypTool’s AMSCO code that existed before Revelations’ release. AMSCO is a transposition cipher: it rearranges characters by placing them in columns and reading those columns in a key-controlled order. This implementation filled its cells with alternating groups of two characters and one character.

Its handling of the digit zero was the crucial detail. The code could assign characters to a column labeled `0`, but its output loop started at column `1`. Anything stored in the zero-labeled column disappeared from the result. The surviving text therefore had holes that an ordinary reversal of the transposition could not restore. [Historical AMSCO source](https://github.com/cryptool-org/cto/blob/887e095c586f7dbae805ae40a29e82ce0d565a6f/_ctoLegacy/tools/amsco/class.amsco.php)

That gave the search a concrete new task. For each candidate numbered key, the program reversed the paper’s text, placed the surviving characters back into their proposed positions, and marked the missing positions as unknown. It then tried possible values for those missing hexadecimal digits while decrypting. Branches that could not produce text within the search’s allowed character set were rejected.

The successful key was **`1947038265`**. The modern encryption layer was **`blowfish-compat` in CFB8 mode**, with the password **`Zombies`** and an initialization vector consisting of eight ASCII zero characters.

With that AMSCO key, zero labels the fifth column. It holds two characters in each of 84 rows, so the tool omits 168 hexadecimal characters. The recovered encrypted message contains 1,260 hex characters before AMSCO. Subtracting the omitted column leaves exactly the 1,092 characters on the paper.

The first complete candidates contained long passages of recognizable prose: an MI-8 transcript, Dempsey evading capture in Calais, and a handwritten note about the mound. The search had not been supplied with those words or an expected opening. They emerged from the reconstruction.

Readable prose was the beginning of verification. The recovered message was encrypted again, converted to uppercase hexadecimal, passed through the unchanged historical AMSCO class, grouped in fives, and reversed. That process reproduced every surviving character. It also reproduced all 219 printed groups, including the initial `83`.

There is an important limit to the result. Because the tool discarded information, the paper does not uniquely determine every original byte. Under the tested text constraints, the recovery produced 64 complete candidates. They share 596 of their 630 bytes, with alternatives confined to four small regions. One candidate reads coherently throughout; the other combinations introduce garbled passages or endings. The message quoted above is that coherent candidate, without corrections or inserted words.

The exact file preserves its curly punctuation and four newline bytes after the final period. All 64 candidates are retained so that the remaining ambiguity can be inspected directly. A fresh targeted search reproduced them without a plaintext hint, and a separate Python implementation verified the selected message against the paper.

The report places Dempsey under pursuit by someone ordered to return him to US intelligence. It also gives us his note about a monster, the mound, and his difficulty remembering. Those are the statements recovered from the cipher; identifying the report’s author or settling the meaning of every line would require further evidence.

The accompanying [verification package](../solution/) contains the exact plaintext, reconstructed ciphertext, original transcription, all 64 candidates, and a verifier that runs with Python’s standard library. The [technical report](SOLUTION.md) records the settings, the missing-column behavior, the ambiguity, and the steps needed to repeat the recovery.
