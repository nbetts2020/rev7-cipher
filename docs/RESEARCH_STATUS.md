# Rev-7 — recovered

The active work has recovered a coherent message and a reproducible encryption construction. See [SOLUTION.md](SOLUTION.md).

Settings: `blowfish-compat` CFB8, key `Zombies`, IV eight ASCII zeros; uppercase hex; historical AMSCO key `1947038265` with the zero-column omission; reverse the grouped output.

The unedited 630-byte plaintext is `solution/plaintext.txt`. Candidate18 is the coherent choice among64 complete text-compatible reconstructions; data loss prevents mathematical uniqueness. Every reconstruction re-encrypts to the unchanged original1,092hexcharacters. Three independent reviews and unchanged originalPHP confirmed the chain; all219 printedtokens match.

The broad safe32 search was stopped after verification. Partition1 completed208,200keys and found64candidates; partition0 was interrupted with170,000keys at its last complete checkpoint. Remaining speculative searches were stopped or had completed; none is required for the recovered solution. Historical negative reports and capped controls are preserved with their original limits.

The portable standard-library verifier passed independent native-library comparisons and standalone execution. The completed package is `rev7_solution.zip`; the research goal is fulfilled.
