# Conditional local-window CFB8 bounds

**No Rev-7 solution was recovered.** This search excludes a relaxed family for selected clean plaintext windows; feasible witnesses are deliberately underconstrained and are not proposed plaintexts.

The tested family keeps every decimal digit nibble fixed and allows every observed A–F nibble independently to become any A–F value. This contains every A–F-only transposition, substitution, or composition that preserves the digit positions. We use the known candidate key `Zombies` with the existing 19 libmcrypt-compatible block primitives in CFB8.

The search selects a window of 16, 24, or 32 plaintext bytes whose preceding feedback block contains at most seven unknown A–F nibbles. Candidate windows are ranked by `(unknown_context + unknown_window) * ln(6) + length * ln(alphabet_size / 256)`. That expression is a heuristic for selecting a tractable window; **the exclusion itself comes from exhaustive enumeration**, not from a probability estimate.

For each initial feedback assignment, a depth-first search requires every decoded window byte to belong to the selected alphabet. It stops at the first feasible assignment. A failed-state cache uses only the current position and complete feedback block: those determine every possible future continuation because there are no global histogram or repeated-symbol constraints. Only completely searched failed states are cached. The terminal condition accepts a completed window immediately, with no extra minimum-run or whole-message gate.

The initial feedback block is taken directly from the selected preceding ciphertext positions. Consequently the search requires no IV and makes no assumption that the earlier plaintext is readable. It does require the selected window itself to be free of damage or nonalphabet content.

## Results with context limit seven and node cap 500,000

| Next-layer alphabet | Cases with an excluded window | Cases with all three selected windows feasible | Capped cases | Skipped cases |
|---|---:|---:|---:|---:|
| Base64 letters/digits, `+/=`, CR/LF | 136 | 0 | 0 | 16 |
| Printable ASCII, tab, CR/LF | 86 | 50 | 0 | 16 |

There are 19 algorithms × four orientations × two nibble phases = 152 cases per alphabet. The 16 skipped cases are Rijndael-192 and Rijndael-256, whose best available feedback contexts exceed the seven-nibble limit. The base64 pass examined 136 windows, totaling 5,641,445 DFS nodes, with a maximum of 159,368 nodes in one window. It completed in approximately 3.6 seconds. The printable pass examined 237 windows, totaling 1,836,734 nodes.

Each excluded case proves only this conditional statement: **under that exact algorithm, key, orientation and nibble phase, no assignment of A–F values preserving the digit positions can make the recorded local window entirely belong to the named alphabet.** It does not exclude an error within that window, another key, a digit-changing outer transform, or binary/compressed/non-ASCII intermediate data. It does not establish any layer of Rev-7.

## Limited Rijndael-192 extension

Increasing the feedback-context limit to eight and the node cap to five million produced no further exclusions. For base64, five orientation/phase cases had feasible assignments for all three selected windows and three remained capped. For printable ASCII, all eight cases had feasible assignments. These are underconstrained witnesses, not solutions. Rijndael-256 was not extended: its smallest contexts need roughly twelve unknown nibbles (over two billion raw feedback assignments).

## Independent controls

`validate.py` generates ciphertext with the separate libmcrypt wrapper, using arbitrary IVs, then reverses the entire A–F subsequence while retaining digits. Fourteen registered algorithms are checked for each alphabet. All 28 ciphertext controls remain feasible; none is falsely excluded. Each of the **84 emitted local-window witnesses** is independently decrypted with libmcrypt using its enumerated feedback block as the IV, and checked against both its alphabet and every observed digit/A–F constraint.

The three separately loaded extra primitives use the same generic CFB8 logic and pass their primitive self-tests, but are not included in those independent library-mode controls. A separate audit completed without finding a demonstrated false-negative bug; see `../continuation_historical_tools/WINDOW_REVIEW.md`. It confirms that the local terminal condition makes the memo key safe and that local feasibility does not establish global compatibility.

Files: `window.cpp`, `validate.py`, `validation_results.json`, `base64.log`, `print.log`; extension logs `base64_rijndael192_ctx8.log` and `print_rijndael192_ctx8.log`. Log witnesses are bounded to short local windows and at most 60 examples per process.

From the parent `revelations_rev7` directory:

```sh
clang++ -O3 -std=c++17 -I mcrypt/include continuation_window_bounds/window.cpp -L mcrypt/lib -lmcrypt -Wl,-rpath,$PWD/mcrypt/lib -o continuation_window_bounds/window
python3 -B continuation_window_bounds/validate.py
continuation_window_bounds/window scan base64 500000
continuation_window_bounds/window scan print 500000
MAX_CONTEXT=8 ONLY_ALG=rijndael-192 continuation_window_bounds/window scan base64 5000000
```
