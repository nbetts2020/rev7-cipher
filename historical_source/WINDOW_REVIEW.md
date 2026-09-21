# Independent review of the local-window feasibility bound

Reviewed `continuation_window_bounds/window.cpp`, its validation code, completed attack logs and recorded controls. I found no demonstrated false-negative bug in the stated conditional exclusions.

The failed-state cache is sound here without the earlier 80-byte-suffix guard: a terminal state accepts completion of the selected window itself, with no predicate that depends on an earlier plaintext prefix. For a fixed trial, remaining transitions depend only on position and the preceding full CFB8 ciphertext block. The observed mask, primitive, key and alphabet are fixed. Counts of A–F symbols are intentionally not conserved. Capped branches return before failed-state insertion; cache saturation merely stops insertion.

Every initial context allowed by the digit/A–F mask is enumerated. A numeric nibble remains fixed, while each A–F position permits any A–F nibble. A feasible complete window therefore includes an explicit context and ciphertext witness. The heuristic selects which local windows to test, but it does not invalidate a negative result: any genuine complete construction within the stated model would necessarily supply a feasible assignment for each selected window. One fully exhausted infeasible window is enough for a conditional exclusion.

Conversely, feasibility of all selected windows does not establish a global construction. The witnesses can disagree where they overlap; no global A–F histogram, outer permutation or coherent full message is imposed. The 50 printable cases with feasible selected windows remain open, not solved.

The completed logs are internally consistent:

- Base64: 136 included cases each yielded an excluded window; 16 combinations were skipped; no caps.
- Printable ASCII: 86 cases were conditionally excluded, 50 had feasible selected windows, and 16 were skipped; no caps. Only the first 60 witnesses were printed, so printed witness count is not total feasibility count.
- Controls: 14 registered primitives per class, all three selected window lengths, 42 emitted witnesses per class. All 84 were independently decrypted and checked against both the alphabet and the nibble mask. Control logs contain no excluded or capped windows.

All conclusions retain key `Zombies`, CFB8, the tested orientations and nibble phases, and preservation of numeric positions. The skipped combinations concern the 24- and 32-byte Rijndael block variants. Base64 means precisely its specified standard character set plus `=` and CR/LF; other encodings or spacing conventions are outside that class. These exclusions do not apply to an independently unknown modern key, other modes, altered numeric positions or additional layers.

One minor conservative detail: the `all=true` control path can summarize a trial as capped when another selected window already proves exclusion. Production scans use `all=false` and return immediately on an exhausted excluded window, so this does not weaken or overstate the reported production exclusions.

No root-owned source or result file was changed, and no new puzzle plaintext is asserted by this review.
