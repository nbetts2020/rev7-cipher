# Movable Type AES-CTR wrapper: direct-key search

No hit. The completed scan tested all 161,354 main/extended literal wiki keys, 40 distinct direct byte-input interpretations, and AES-128/192/256: **19,362,480 input/key/size instances**.

This models the [original tool's AES-CTR wrapper](https://www.movable-type.co.uk/scripts/aes.html), not just raw AES: UTF-8 password bytes truncated/zero-padded to the selected key size; AES encryption of the first16 password bytes using that padded password as the seed key; repetition of the resulting16-byte block to fill a24/32-byte key; an8-byte nonce prefix and a big-endian8-byte block counter. No date/nonce-value filter was used.

Inputs include compact hex decoding, literal ASCII hex, base64 interpretation, normal/reversed/nibble/byte orientations, optional removal of leading/trailing83-sized two-digit groups, and odd nibble phases. These are explicit framing hypotheses. Search probes16-byte printable blocks at four offsets, followed by a full decryption requiring an80-byte printable run. Compressed/binary intermediates, short fragments, other keys, and wrapper conventions remain outside this result.

Validation: the published `big secret` / Unicode-password example decrypted exactly. Eighteen independently encrypted messages produced by the downloaded original JavaScript implementation recovered their exact plaintext, covering all key sizes, Unicode keys, and short/long messages. Original source retained in `aes.js` / `aes-ctr.js`, including its copyright and license notices.

Reproduce with `node continuation_aesctr/validate.js`, the C++ scanner's `stdin` control mode, and `./continuation_aesctr/scan direct continuation_aesctr/direct_inputs.tsv continuation_aesctr/all_keys.txt`. See `direct.log` for the completed count. Structural follow-up has its own report in `continuation_aesctr_structure/RESULTS.md`.
