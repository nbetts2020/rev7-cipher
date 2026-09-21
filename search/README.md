# The search

## `zero_full/` — the run that found it

`targeted_reproduce.py` is the reproduction entry point. It reads `cipher.txt`,
projects it back through the AMSCO layout for key `1947038265` with the dropped
column masked out, and hands the resulting 1,260-character pattern — 168 of
them unknown — to the native recovery binary with **no plaintext crib**. Exactly
64 completions come back. Build the binary first; see `lib/BUILD.md`.

`SAFE32_RESULTS.md` and `RESULTS.md` document the broad sweep that discovered
the key: 416,400 signed-32-bit-safe keys out of 3,265,920 non-leading-zero
permutations. Partition 1 completed its 208,200 keys and produced the 64
candidates; partition 0 was interrupted at 170,000 keys once the solution was
confirmed. `safe32_control_*` are the planted-solution controls that establish
the sweep would have found a hit had one been there.

## `zero_column/` — the precursor

The focused search that first established the zero-column model.
`recover.cpp` + `recovery_support.inc` are the sparse CFB8 constraint solver;
`masked_modes.cpp` checks dependency-safe regions; `work.py` generates the
projections and control chains.

## `review/` — independent audits

Three reviews ran against the solve. `ZERO_COLUMN_REVIEW.md` audits
`recover.cpp` for false negatives with an independently written harness.
`SOLUTION_AUDIT_REVIEW.md` checks the plaintext and ciphertext.
`AMBIGUITY_REVIEW.md` checks the 64-candidate enumeration and the
candidate-18 selection.

## A note on the other scripts here

`validate.py`, `aggregate_safe32.py` and `checks.py` are archival records of
runs in the original research workspace. They embed paths from that workspace's
directory layout and will not run unmodified here; their recorded outputs
(`*_RESULTS.json`, `validation_results.json`, `candidate_validation.json`) are
the evidence. `targeted_reproduce.py` is the one search script that has been
adapted to this repository's layout and is expected to run.
