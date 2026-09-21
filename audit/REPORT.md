# Legacy AMSCO deployment and fix audit — September 13, 2026

**Finding:** the unchanged data-loss implementation survives in 11 public repository copies examined. No code push since September 7 was found among the 26 forks in the two identified repository families. No recent fix PR or issue was found in either upstream. The current and legacy official app catalogs do not list AMSCO; the tested AMSCO routes return 404. This supports treating it as a surviving legacy-source defect with no confirmed active official deployment.

## Repositories and code

- `cryptool-org/cto`: prior direct API checks found the historical AMSCO directory was removed in commit `3220945062fedebbe56db59e44b0d659732d9cf9` on October 27, 2020. Latest default-branch commit is July 25, 2023. No PR/issue activity since September 7, 2026 was found.
- Its 18 public forks: none has a `pushed_at` date on or after September 7, 2026. Three default branches retain the old file: `SmashITs/cto`, `simlei/cto`, and `s-rech/cto`. Fifteen tested default-branch paths return 404.
- Older upstream `fschell/cryptool-online`: its current default branch retains the identical old implementation. Its latest reported push was September 1, 2020. All five PRs were inspected; none concerns AMSCO. Its issues endpoint returned no items updated since September 7, 2026.
- Its eight public forks: none reports a push since September 7, 2026. Seven retain the identical file. The tested path in `npmcdn-to-unpkg-bot/cryptool-online` returns 404.
- Each of the 11 retained files has exact raw-byte SHA-256 `132d61ff8b794ab9717a0ce284d7bf21f82c8dbfe39bf9f1a3b5f7aa7eb91e4f`, matching the historical source. The original PHP comments use a legacy encoding; raw bytes were preserved and hashed rather than UTF-8 replacement text.

Examples: [older upstream file](https://github.com/fschell/cryptool-online/blob/master/_ctoLegacy/tools/amsco/class.amsco.php), [surviving newer-family fork](https://github.com/simlei/cto/blob/master/_ctoLegacy/tools/amsco/class.amsco.php), [2020 upstream removal](https://github.com/cryptool-org/cto/commit/3220945062fedebbe56db59e44b0d659732d9cf9).

## Official sites and successor interface

- [Current app catalog](https://www.cryptool.org/en/cto/): HTTP 200; no AMSCO entry or AMSCO occurrence in the fetched HTML. It lists Simple Columnar Transposition separately.
- [Legacy app catalog](https://legacy.cryptool.org/en/cto/): HTTP 200; its full 26-cipher list does not include AMSCO.
- `https://www.cryptool.org/en/cto/amsco/`, `https://legacy.cryptool.org/en/cto/amsco`, and the latter with `.html`: HTTP 404.
- `http://www.cryptool-online.org/` redirects to the current official app catalog. An exploratory old-style query URL redirected to the current site and returned 404. These query parameters were not authenticated as the historical AMSCO menu identifier and are not treated as proof that every historical endpoint is gone.
- Direct HTTPS requests to the former `cryptool-online.org` hostname failed certificate hostname verification. Verification was not disabled; that failure is not evidence of a patch.
- The current [Simple Columnar Transposition page](https://www.cryptool.org/en/cto/transposition/) identifies a React `TranspositionComponent.jsx`. Its page metadata does not identify it as AMSCO. No claim is made that every behavior of that distinct app has been audited.
- The official [source-code page](https://www.cryptool.org/en/cto/source-code/) says source publication is forthcoming while infrastructure changes. Consequently, the old GitHub repository cannot establish the contents of private current server deployments.

## Fresh minimal reproduction

The original unchanged class was executed again in isolated PHP 8.4.25:

```text
Input:   0123456789ABCDE
Key:     1947038265
Output:  01B83 4ECD5 9A2
Compact: 01B834ECD59A2
Lengths: 15 input characters -> 13 output characters
Lost:    67, the fifth input column labeled 0
```

Thus this is a reproducible silent-data-loss defect in the retained source. It does not establish an active vulnerability in modern encryption libraries or current production deployments. A supported implementation should either reject keys outside its defined label convention or preserve all columns consistently; the maintainer should choose the intended convention.

## Remaining uncertainty and next step

Public-source and public-route inspection cannot prove the absence of private copies, unlisted endpoints, detached repositories, or deployments modified without a public commit. The concrete unresolved question is whether CrypTool maintains or deploys this legacy class anywhere today. A [maintainer message](MAINTAINER_REPORT.md) is prepared for that question; it has not been submitted. The official route is the [CrypTool-Online feedback form](https://www.cryptool.org/en/feedback/?section=cto).

Evidence: `results.json`, `old_family_results.json`, both complete fork metadata snapshots, `github_activity.json`, saved public HTML, and the fetched source files. Fetch scripts are `../deployment_audit_20260913.py` and `old_family.py`.
