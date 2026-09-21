# Failed-state memoization review and mixed-case follow-up

**Result:** the failed-state cache is safe for the intended interior search when its printable-suffix invariant is enforced. A generic reuse without that invariant can produce a false negative. The default-off guard in `memo_review/MEMO_GUARD.patch` fixes that reuse hazard. The subsequent bounded mixed-case Rev-7 search found no hits; 35 cases remain capped.

## Why the cache key is sufficient in its intended scope

With `conserve=false`, fixed key/primitive, fixed observed ciphertext and fixed alphabet, a CFB8 continuation depends only on its current position and preceding full ciphertext block. Remaining A–F counts are deliberately ignored. CFB8 does not need `priorstream`, and caching is restricted to positions after a full feedback block, where the IV no longer matters. The binary cache key has fixed-width block and position components and is local to one reconstruction object.

Failure is cached only after the entire subtree returns without a cap and without increasing the hit counter. Successful subtrees are not cached. Filling the 250,000-entry cache stops further insertion; it does not discard unexplored branches. Cache hits occur before the DFS node counter increments, so reported node caps count uncached expansions rather than every recursive call.

The terminal `run(plaintext) >= 80` test is the important qualification: in general, acceptance can depend on plaintext before the cached context. The interior caller removes that dependency by starting with at least 80 remaining bytes and allowing only printable alphabet bytes. Every complete continuation must therefore pass the terminal gate, regardless of its fabricated prefix.

The proposed guard defaults `memo_enabled` to false. The interior caller enables it only when its start is in bounds, at least 80 bytes remain, and every alphabet byte is printable. The cache also still requires `conserve=false`, CFB8 and a complete preceding block. Root-owned sources were not modified by this review; the patch and independently compilable guarded copies are supplied.

## Concrete regression and controls

A deliberately simple **bijective identity block permutation** demonstrates the generic hazard. Two permitted A–F prefix histories reach the same position and preceding block with only ten suffix bytes left. One full decryption has only 18 consecutive printable bytes; the other has 90. The naive solver finds the second, while the original unguarded memo solver suppresses it after remembering the first failure. The guarded default-off version agrees with the naive solver. This is a program regression fixture, not a Rev-7 candidate. Sources and logs: `memo_review/generic_plain.*`, `generic_memo.*`, `generic_guarded.*`.

Additional comparison results:

- **96 real-primitive fixtures**, covering all 16 registered block algorithms, 80–128-byte suffixes, planted valid ciphertexts and controlled mutations: identical ordered hit records between naive and guarded versions, no caps, and every unmutated expected suffix recovered. These tight fixtures did not produce cache hits; their purpose is baseline equivalence and guard validation.
- A constructed convergent failure fixture exercised the cache: **2,880 naive expansions versus 115 memo expansions**, with 35 cache hits and identical zero-success results.
- A corresponding positive fixture retained **all 36 successes** in both versions and cached no failures.
- A deliberately capped fixture stopped at six expansions for a five-node cap and cached nothing.

The convergence fixtures use toy transition functions to force repeated states. They supplement, rather than replace, the actual-primitive controls and the state-dependence argument. Fixtures, exact comparison data and logs are under `memo_review/`; `compare.py` reproduces the 96 real-primitive comparisons.

## Bounded mixed-case search

The guarded search used key `Zombies`, CFB8, all four orientations and both nibble phases. It reconstructs arbitrary A–F values at letter positions while preserving numeric positions; it does not enforce the A–F histogram or identify a transposition. The 24- and 32-byte Rijndael block variants were skipped for the same context-size limit as the earlier interior pass.

The alphabet contains exactly **63 bytes**: uppercase and lowercase ASCII letters, space, CR, LF, and `.,'!?-:;`. It excludes digits, tab, other punctuation and non-ASCII characters. The **entire chosen suffix through the final byte** must stay in this alphabet. Thus even a late `1` in `115`, after a long readable English passage, is outside the tested model; the search does not merely require an early English span.

| Outcome | Count |
|---|---:|
| Included cases | 136 |
| Fully exhausted cases | 101 |
| Cases reaching the 2,000,000-node cap | 35 |
| Skipped primitive/orientation/phase combinations | 16 |
| Uncached DFS expansions | 76,329,834 |
| Reused failed states | 496,022 |
| Reported hits | 0 |

The scheduled run completed in about 68 seconds. Completion of that loop does not make the 35 capped trees exhaustive. No candidate output arose for interpretation. If a future permissive search does emit printable suffixes, they remain underconstrained until their prefixes, letter counts, outer transformation and coherent complete message are established.

Reproduce from the project root:

```sh
clang++ -O3 -std=c++17 -I mcrypt/include continuation_audit/memo_review/interior_guarded.cpp -L mcrypt/lib -lmcrypt -o continuation_audit/memo_review/interior_guarded
./continuation_audit/memo_review/interior_guarded scan mixed 2000000
```

Exact per-case limits, outcomes, input/source hashes and alphabet are in `memo_review/mixed_results.json`; the completed scan is `memo_review/mixed.log`. This result neither solves Rev-7 nor excludes general mixed-case English.
