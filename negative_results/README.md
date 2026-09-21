# Negative results

Reports from the approaches that did not solve Rev-7. They are kept because the
bounds they establish are part of the evidence: each one states what was tested
and, importantly, what was *not*.

Only the markdown reports are here. The logs, binaries, keyspace dumps and
intermediate data they reference stayed in the original research workspace and
are not part of this repository, so paths quoted inside these files will not
resolve here.

| Report | What it rules out |
|---|---|
| `sources_CURRENT_SOURCE_REVIEW.md` | Current-generation CrypTool sources as the construction |
| `sources_PRESERVED_POSITION.md` | Position-preserving transforms |
| `sources_XXTEA.md`, `sources_TEA_FAMILY.md` | XXTEA and the TEA family |
| `structure.md` | Structural/layout hypotheses for the missing characters |
| `substitution.md`, `substitution_mixed.md` | Hex substitution layers, alone and mixed |
| `aesctr.md`, `aesctr_nonce.md`, `aesctr_structure.md` | AES-CTR with assorted nonce and structure models |
| `filtered_routes.md` | Route transpositions under filtering |
| `partialhex.md`, `partialhex_key_search.md` | Partial-hex models and their key searches |
| `window_bounds.md` | Sliding-window insertion models |
| `numeric_amsco.md` | Numeric AMSCO variants — the branch the zero-column model grew out of |
| `byte_keys.md` | Raw byte keys rather than ASCII |
| `unicode.md` | Unicode-aware plaintext repertoires |
| `mixed_classical.md` | Mixed classical layer chains |
| `embedded_iv.md` | IV material embedded in the ciphertext |
| `bo2_bo4_findings.md`, `cross_map_findings.md` | Keys and constructions borrowed from other maps |
| `ecb_format.md`, `round4.md`, `wiki_key_attack.md` | ECB formats, round-4 crib attack, wiki-derived key lists |
| `treyarch_comment_review.md` | Developer comments mined as key material |
| `literature_review.md` | Provenance of the paper texture and published transcriptions |
| `audit_REPORT.md`, `audit_ROOT_REVIEW.md`, `audit_MEMO_REVIEW.md` | Audits of the search infrastructure itself |
