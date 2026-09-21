# Original PHP execution confirms the AMSCO projections

The unchanged historical `class.amsco.php` executed successfully in **PHP 8.4.25**, using the official WordPress PHP-WASM packages. All **1,180 comparisons passed with zero mismatches**, confirming both zero-column encode and malformed-key decode projections.

| Case category | Encode/decode comparisons |
|---|---:|
| Historical default `135624` fixture | 2 |
| Valid numeric permutations of widths 2–9 | 192 |
| Forty nonleading-zero permutations of `0..9` | 960 |
| Other malformed keys | 24 |
| Uppercasing and PHP whitespace trimming | 2 |
| Total | 1,180 |

The zero-containing tests include lengths 1,2,3,14,15,16,36,1092,1170,1260,1262,1263. The four named keys are `1234567890`, `1357924680`, `1023456789` and `1203456789`; another 36 deterministic random keys begin with `1`. All keys fit signed 32-bit integers, although the executed runtime uses 64-bit integers.

The original class was loaded as unmodified binary bytes from the [official 2016 CrypTool snapshot](https://github.com/cryptool-org/cto/blob/887e095c586f7dbae805ae40a29e82ce0d565a6f/_ctoLegacy/tools/amsco/class.amsco.php). Its SHA-256 is `132d61ff8b794ab9717a0ce284d7bf21f82c8dbfe39bf9f1a3b5f7aa7eb91e4f`, and PHP's hash of its in-memory file matched the host file exactly. This preserves the legacy file's original encoding.

The harness defines `_JEXEC`, supplies a minimal `JURI::base()` stub and the plugin-name variable, then calls the class's original `setKey`, `setText`, `encode`/`decode`, and `getText` methods. It reproduces the wrapper's numeric-to-integer key conversion. The full Joomla page wrapper was not executed. Expected results remain in Node/Python and are not supplied to PHP. The original five-character grouping is recorded, then spaces are removed for comparison with the projections.

PHP emitted undefined-array and null-argument warnings/deprecations. A collecting error handler recorded their counts while preserving PHP's continuation behavior; it did not modify the source or replace any algorithm operation. The runtime completed normally. There were 50,537 diagnostics in total, stored as aggregated counts with 15 examples rather than a large repetitive log.

This directly confirms the critical malformed-key behaviors:

- Encode with a nonleading-zero permutation of `0..9` omits the column labeled `0` because output iterates labels 1 through 10. Depending on the zero-column parity, input length 1,170 or 1,260 can produce 1,092 characters.
- Decode cannot find numeric label `10` among the key's individual digit characters. `getPos(10)` returns null; adding one selects column 1 and overwrites its earlier contents. Input lengths 1,260 and 1,262 can both produce 1,092 characters.

These are verified implementation behaviors, not evidence that Rev-7 was produced with a malformed key. Tests used PHP 8.4, not an identified 2016 production runtime. Restricting keys to the signed 32-bit range avoids one platform-dependent integer-casting question; historical deployment remains unestablished.

The isolated dependency setup follows [WordPress's documented single-version loader](https://wordpress.github.io/wordpress-playground/developers/architecture/php-wasm-packages/). `@php-wasm/universal` and `@php-wasm/node-8-4` are pinned to version `3.1.53`; installation used `--ignore-scripts --no-audit --no-fund` and a task-specific `/tmp/rev7-php-npm-cache`. No global installation, filesystem mount into PHP, network proxy, or external code posting was used. Installed dependencies occupy approximately 66 MiB.

Reproduce from this directory:

```sh
npm ci --ignore-scripts --no-audit --no-fund --cache /tmp/rev7-php-npm-cache
python3 -B build_cases.py > cases_summary.json
node run.mjs > runtime.log
```

Evidence: `RESULTS.json`, `actual_outputs.json`, `cases.json`, `cases_summary.json`, `package-lock.json`, `run.mjs`, and `build_cases.py`. The source models being checked are in `../continuation_numeric_amsco/zero_projection.py`, `zero_decode_projection.py`, and the corrected `../continuation_historical_tools/literal_models.py`.
