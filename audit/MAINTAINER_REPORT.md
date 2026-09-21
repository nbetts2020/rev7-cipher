Subject: Historical AMSCO silently discards column 0 — is any supported deployment affected?

While investigating historical cipher-tool behavior, I reproduced silent data loss in the legacy AMSCO class:

https://github.com/fschell/cryptool-online/blob/master/_ctoLegacy/tools/amsco/class.amsco.php

The same source exists in the pre-release 2016 history of `cryptool-org/cto`. Exact source SHA-256: `132d61ff8b794ab9717a0ce284d7bf21f82c8dbfe39bf9f1a3b5f7aa7eb91e4f`.

Minimal reproduction, using the unchanged class in PHP 8.4.25:

```text
Plaintext: 0123456789ABCDE
Key:       1947038265
Encoded:   01B83 4ECD5 9A2
```

The input has 15 characters, but the compact output has 13. `sortArray()` assigns cells to the numeric labels taken from the key. The output loop enumerates labels 1 through the key length, so label 0 is never emitted. Here it contains `67`.

I found that the directory was removed from `cryptool-org/cto` in October 2020, but the identical file remains in the older upstream and several forks. Neither the current nor the legacy official catalog lists AMSCO, and the AMSCO routes I checked return 404. Your current source-code page says source publication is undergoing infrastructure changes.

Could you confirm whether this class is still used by any maintained deployment or distributed tool? If it is, which repository should receive a patch? A narrow fix could reject keys outside the intended label convention before encoding, with regression tests for length preservation and round trips; alternatively, zero-based keys could be supported consistently if that is the intended interface.

I am reporting verified behavior in the historical implementation, not asserting that the current website is affected. I can provide the preserved source and reproduction details.
