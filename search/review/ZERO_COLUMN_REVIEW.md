# Independent review of zero-column CFB8 recovery

**No false-negative bug found in the completed, stated scope.** Reviewed `continuation_zero_column/recover.cpp` at SHA-256 `c3fd5d13fbdc2777d97e69a0e3170ee589ca38b0cee55c81f3452bda588e74e9`. The tested negative is conditional on key `Zombies`, the listed algorithms/IV fills, the generated missing-position patterns, and the entire plaintext belonging to the selected language class.

## Recurrence and search

`streambyte(pos)` encrypts exactly the previous ciphertext block, left-padded with the IV while `pos < block_size`, then uses its first byte. `cipher_byte XOR stream_byte` is the CFB8 plaintext byte. Each candidate ciphertext byte must match the fixed nibble mask. The DFS advances the UTF-8 automaton with that plaintext byte and accepts only a complete message ending in state zero. This correctly reconstructs arbitrary missing bytes within the generated masks.

The failed-state key contains the position, UTF-8 automaton state and preceding ciphertext block. Those determine every future constraint for a fixed task, algorithm, key, IV and language. The failed set is cleared per case. No terminal language score, count quota or prefix-dependent acceptance condition is omitted: expected-plaintext comparison is diagnostic only. States are cached only after all children fail without a node cap. This avoids the earlier unrelated memo bug involving a whole-message printable-run acceptance criterion.

Positions use two bytes in the memo key. This is safe for these 585–631-byte inputs. If this helper is reused for messages of 65,536 bytes or more, its position field should be widened; that is not a limitation encountered in the current search.

## Known-region pruning

A plaintext byte is marked definite only when its own ciphertext byte and every preceding ciphertext byte in the feedback block are fully known. Therefore zero placeholders never participate in a definite byte's dependency set. The separately computed definite plaintext agrees with actual encrypted fixtures.

Every unsafe gap resets the automaton to a superset of possible states at the next safe byte. This includes continuation states for the permitted two-/three-byte UTF-8 sequences and the BOM-specific states at positions 1/2. At the end of the message, a definite terminal region must admit ground state. These are necessary conditions, so their failure safely excludes every completion in the chosen language class. Starting a safe region in the middle of a UTF-8 punctuation sequence does not cause a false rejection.

The class called `language=1` is **not arbitrary UTF-8**. It accepts printable ASCII plus tab/CR/LF, NBSP, the explicitly listed U+2013/U+2014/U+2018–U+201F/U+2022/U+2026/U+202F characters, and one initial UTF-8 BOM. Other valid UTF-8 characters, such as an accented letter, are outside scope. NUL bytes and binary padding are also outside both language classes. Full-message text constraints are stronger than the selected-window gates used in earlier scans.

After known-region pruning, a surviving run of more than four partially or fully unknown bytes is marked incomplete rather than enumerated. A node cap is also incomplete. Neither status may be counted as an exhausted exclusion. Neither occurred in the focused encode search. In the focused decode CFB8 search, all cases were already rejected by definite plaintext before that guard.

## Independent controls added

| Check | Cases | Result |
|---|---:|---|
| UTF-8 automaton against a Python codec/character-set oracle | 66,844 | Exact agreement, including every two-byte string, punctuation and BOM boundaries |
| Actual-cipher recurrence and known-region pruning | 760 | Exact plaintext recurrence for all 19 primitives and both IV fills; expected acceptance/rejection in every case |
| Memo and nonmemo search against exhaustive identity-block oracle | 102 | Exact completion counts, no caps or long-erasure skips |

The recurrence fixtures deliberately put the first definite byte at the second/third byte of allowed UTF-8 punctuation after an erased ciphertext byte. They also include malformed UTF-8, truncated sequences and misplaced BOMs, so the tests check both rejection and preservation.

The memo unit test uses a bijective one-byte identity block permutation solely to make the state graph exhaustively checkable. Its infeasible case exercises 97 cached failures: 198 nodes with memoization versus 295 without, both zero completions. Its feasible counterpart preserves all 98 completions in both versions. The 100 further planted/mutated patterns match independent exhaustive enumeration. These artificial controls are not cipher hypotheses or candidate puzzle messages.

The harness copies the reviewed functions, changes only the include path and adds an optional memo disable switch. Original agent files were not edited. The raw fixtures, outputs, oracle and counters are adjacent to this note; `RESULTS.json` preserves the reviewed source hash.

## Result interpretation

The reviewed focused encode log records 54,720 cases, 609,352 nodes, zero candidates, 43,378 definite-region rejections and no incomplete cases. The focused decode CFB8 log records 109,440 cases, all rejected by definite regions, zero DFS nodes and no incomplete cases.

The separate zero-filled multi-mode diagnostic log's 4,380 `HIT` lines are **not recovered plaintext**. In CFB8, a sufficiently long artificial all-zero ciphertext segment makes the feedback register constant; its decrypted byte can then repeat a printable value throughout the missing segment. Such runs can be entirely dependent on placeholders. They do not contradict either CFB8 exclusion above. Other-mode conclusions should come from the new dependency-mask analysis being developed by the owning agent, not from this diagnostic.

The existing 152 planted full chains recovered every exact ciphertext/plaintext, and every emitted completion was checked by modern re-encryption and the forward projection. Their separate original-PHP verification reports 152 exact matches. This audit did not rerun or claim authorship of those prior controls.

```sh
clang++ -O3 -std=c++17 -I mcrypt/include continuation_audit/zero_column_review/harness.cpp -L mcrypt/lib -lmcrypt -o continuation_audit/zero_column_review/harness
python3 -B continuation_audit/zero_column_review/checks.py
```
