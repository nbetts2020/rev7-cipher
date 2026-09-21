# Structural and compressed-layer continuation

No readable intermediate or valid compressed output was recovered. The original ciphertext remains unchanged.

## Completed searches

| Search | Executed scope | Result |
|---|---|---|
| Matrix routes, rail fence, skip and physical row permutations | 603,918 unique hexadecimal streams; 1,207,836 instances with both nibble phases | No hit |
| Inversion with variable-length five-character groups and physical rows | 35,082 unique streams; 70,164 phased instances | No hit |
| Direct modern decryption followed by decompression | 401 seed/key variants; 16 distinct input streams; 1,288,064 decryptions | No valid compressed output |

Unique counts are deduplicated within each route pass, not between passes. Counts do not measure the fraction of all constructions excluded.

## Route models

The first pass used nibbles, bytes, five-character groups aligned at either end, and physical rows as units. It tested ordinary columns, row/column snakes, diagonals, diagonal snakes and spirals from all four corners; forward and inverse index maps; normal/reversed input and output; all widths from 2 through half the unit count. Rail fence used all rail counts through half the unit count, every starting phase through 32 rails and phases 0, 1 and rails−1 beyond that. Skip tested every coprime step. The original input and inputs with two leading/trailing hex digits removed were included as explicit framing hypotheses.

The supplemental pass addresses discarded group boundaries: when a short group or variable-length row moves, inverse transposition must split the observed text using the sizes of the moved slots. This was tested separately. It also uses the actual displayed groups within physical rows; the first pass's physical-row model regroups from each row start.

Modern decryption used the existing validated `round4` scanner and key `Zombies`: CFB8, full-block CFB and ECB across 19 block primitives; OFB8/full-block OFB/CTR for 16 registered block primitives; RC4. Both nibble phases were included. The expanded scanner does not include a comprehensive CBC pass. It detects sufficiently long printable regions, so binary intermediates or short intact fragments can be missed.

## Compression models

The separate direct sweep checked registered libmcrypt block algorithms and native streams, accepted short-key handling, seven block modes, ASCII-zero and binary-zero IV fills where relevant, four byte/nibble orientations, and leading-byte removal/odd-nibble alignment. Literal lore/previous-cipher seeds, all capitalizations of Zombies, selected suffixes/encodings, padding, and MD5/SHA1/SHA256 derivations yielded 401 keys. It did not apply the large wiki dictionary or transpositions before this compression check.

The detector accepts complete zlib/gzip, raw DEFLATE, bzip2, XZ or conventional LZMA-Alone streams, requires at least 32 decompressed bytes, and permits fewer than 32 trailing zero padding bytes. Decompressed output is capped at 100,000 bytes, and LZMA memory at 64 MiB. No format-valid candidate was found, including direct decompression of the input variants. The three separately loaded extra block primitives were not included in this Python sweep. Wrong-IV damage to a compressed header remains outside its complete-stream model.

## Validation and reproduction

Four independent Serpent-CFB8 controls of exactly 546 bytes recovered their exact complete plaintext through the route scanner. Every one of the 28 route maps at width 17 and the rail-fence map was checked for inversion in four token layouts. Hand-calculated spiral, rail-fence and ragged-slot examples passed. Variable-length inverses were checked after ciphertext group boundaries were flattened, rather than retaining the original token list. Twelve independently compressed/encrypted controls passed: six formats under CFB8 and ECB with zero padding.

The final audit checked the unchanged ciphertext SHA-256, all exact control plaintexts, completed search counters, and absence of hit records.

Run from the parent directory:

```sh
python3 -B continuation_structure/routes.py | ./round4 stdin
python3 -B continuation_structure/variable_units.py | ./round4 stdin
python3 -B continuation_structure/compression.py
```

Logs and JSON counts are beside these scripts. These negative results exclude only the stated finite constructions and keys; they are not a solution or proof that Rev-7 is unsolvable.
