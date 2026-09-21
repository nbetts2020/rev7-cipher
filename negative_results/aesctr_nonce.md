# Dated AESCTR nonce with arbitrary hexadecimal substitution

No complete printable plaintext was recovered. Both bounded searches finished: **318,407,328 nonce contexts /2,865,665,952 AES key-context checks**, across twelve input orientations/framing variants. No target candidate required a language judgment.

| Encoded timestamp range (UTC) | Nonce contexts | AES checks |
|---|---:|---:|
| 2016-01-01 through 2016-12-31 | 60,185,472 | 541,669,248 |
| 2010-01-01 through 2015-12-31 | 258,221,856 | 2,323,996,704 |

## Exact conditional construction

This models the parent task's independently verified Movable Type AESCTR implementation followed by a bijective substitution of all sixteen hex symbols. Its eight-byte prefix is interpreted as two little-endian millisecond bytes (0–999), two random bytes, and four little-endian epoch-second bytes. **The encoded timestamp is assumed to lie in 2010–2016.** This assumption is not evidence that Rev-7 uses this method. The timestamp ranges include dates after the map's release as a conservative extension.

Modern passwords are `Zombies`, `ZOMBIES`, and `zombies`, each at 128/192/256 bits. Nine separately cached AES contexts use the original construction's AES-based password expansion and counter layout. No independent transposition is combined with the arbitrary symbol substitution in this pass.

The twelve input variants use four whole-byte/nibble orientations at either nibble phase, plus four orientations after removing the leading `83` byte. These are explicit framing alternatives. The unchanged transcription's hash was checked.

## Enumeration and detection

For each epoch second, a partial bijection is derived from nonce bytes 4–7. Legal millisecond values are merged with that partial map. Assignments for every remaining symbol present in the nonce are enumerated; the same nonce context is then checked under all nine fixed keys. Dates and mappings are reused within each loop, and candidate contexts are streamed rather than materialized to disk.

Once the nonce is fixed, the keystream is known. Printable-byte constraints prune remaining symbol assignments using 64 plaintext bytes, followed by a check of the entire plaintext. Every mapping is bijective, there is no search-node cap, and no guessed opening is used. The allowed plaintext bytes are ASCII 32–126, tab, CR and LF. Binary layers, compressed data, non-ASCII messages, different nonce/KDF conventions and other passwords remain outside the result. Allowing random nonce value 65535 slightly enlarges the original JavaScript's range and cannot cause a false negative.

Count-only enumeration and the completed decryption passes agree exactly. The first 2016 log retains an inherited generic cache banner from the unrestricted AES backend; the nonce enumerator itself imposes the date/ms/bijection constraints stated here. The later range executable labels those constraints explicitly.

## Independent controls

The original JavaScript encrypted nine 538-byte messages under all nine key contexts using three fixed 2016 dates. A deterministic random permutation then substituted all 16 hex symbols. The solver recovered the exact expected inverse alphabet and entire original plaintext in every case. Both executable versions passed these controls.

The controls also produced twelve additional fully printable sibling mappings containing altered, garbled text. This demonstrates why printable text alone is not proof of a solution. No such candidate occurred on Rev-7. Candidate output labels were changed from `SOLUTION` in the original executable to `PRINTABLE_CANDIDATE` in the range executable to avoid overstating that gate.

Scripts, controls, complete logs, per-variant counts, timings and hashes are alongside this report. Reproduce from the Rev-7 directory:

```sh
continuation_aesctr_nonce/nonce scan
continuation_aesctr_nonce/nonce_range scan all 1262304000 1451606400
python3 -B continuation_aesctr_nonce/report.py
```

`nonce_2016.cpp` preserves the first executable's source; `nonce.cpp` adds explicit timestamp-range arguments and clearer logging without changing the search algorithm. These negative results are conditional exclusions, not a recovered solution or an impossibility proof.
