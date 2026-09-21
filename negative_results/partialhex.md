# Fixed-digit, freely varying A-F reconstruction

No verified plaintext or useful intermediate was recovered. These tests relax every observed A-F nibble independently to any A-F value while leaving numeric digits fixed. This is a superset of letter-only transpositions; a negative result can reject the stated construction without guessing a transposition key. Positive outputs from this relaxation require further evidence because the relaxed model need not correspond to a real transposition.

## Completed strict searches

The fixed key is `Zombies`. Clean-prefix CFB8 searches covered 19 block primitives, ASCII-zero and binary-zero IVs, and four orientations. Each of uppercase hex, lowercase hex, lowercase letters plus listed punctuation, uppercase letters plus listed punctuation, and Base64 completed all152 cases without caps or candidates. Full-block CFB with uppercase hex also completed152 cases without caps/hits. These clean-prefix tests assume the IV and the restricted alphabet from the first byte.

The IV-independent interior CFB8 version enumerates A-F values in a preceding full feedback block, then searches the entire remaining suffix. It selects a context with at most7 unknown nibbles and at least80 suffix bytes. On Rev7 the selected contexts actually have at most5 unknown nibbles. Each of four strict alphabets (upper/lower hex, lower/upper letters plus punctuation) completed136 cases with no caps/hits;16 cases using24/32-byte Rijndael blocks were skipped. Four orientations and both nibble phases are included. This permits an unknown IV or earlier damage; damage within the selected context or suffix, a character outside the tested alphabet, another key or another mode remains outside the exclusion.

The memoized Base64 interior pass completed its scheduled cases but reached the5-million-node cap in62 cases; it is inconclusive for those cases. Failed-state caching uses position and preceding CFB8 block only under an explicit invariant ensuring every accepted suffix independently meets the80-byte text gate. Its correctness was independently reviewed.

## General printable alphabet is insufficient

The clean-prefix general-printable run hit its cap in4 cases. General-printable interior reconstruction admitted many arbitraryASCII suffixes and was aborted. These are not proposed plaintexts. Its large diagnostic log was reduced to counts, three examples and progress metadata. The original naive Base64 interior run was also interrupted after node caps; the memoized result is recorded separately.

## Validation

32 independently encrypted and A-F-shuffled CFB8 controls recovered exact full plaintexts.28 interior controls recovered exact suffixes without using the generating IV. The memoized implementation recovered those same controls. An independent review added extra-primitive fixtures and nonuniform random-IV controls; see `../continuation_audit/ROOT_REVIEW.md`. A further10 controls using key `Group935` validate the new dictionary-key reconstruction scanner. The separate dictionary-key scans are still in progress and are not included in these completed counts.

Character classes are literal strings in the source. Lowercase/uppercase letter classes exclude the opposite case and digits; Base64 includes CR/LF and equals signs but no spaces. Counts and terminal log lines are saved in RESULTS.json.
