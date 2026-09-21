# Building the native search tools

**You do not need any of this to verify the solve.** The portable verifier in
`solution/verify_portable.py` is stdlib-only Python and reproduces the whole
chain on its own. These notes are for re-running the actual constraint search
(`search/zero_full/targeted_reproduce.py`), which uses a native binary linked
against libmcrypt.

libmcrypt is **not vendored** here. It is a 9.4 MB autotools source tree and a
build product, neither of which belongs in this repository. Build it yourself
with the exact version and flags below.

## 1. libmcrypt 2.5.8

Upstream tarball: `libmcrypt-2.5.8.tar.gz` (Sourceforge, `mcrypt` project).

    tar xzf libmcrypt-2.5.8.tar.gz
    cd libmcrypt-2.5.8
    ./configure --prefix="$PWD/../mcrypt" \
        --disable-dependency-tracking \
        --build=arm-apple-darwin \
        CFLAGS="-O3 -Wno-implicit-function-declaration -Wno-int-conversion"
    make && make install
    cd ..

That is the exact invocation used for the solve, on Apple Silicon macOS.
Drop `--build=arm-apple-darwin` on other platforms. The warning suppressions
are required: the 2003-era C in this tree does not compile clean under modern
clang. Dynamic module loading ends up disabled, which is why the three extra
algorithms below are built separately.

Result: `mcrypt/include/mcrypt.h` and `mcrypt/lib/libmcrypt.dylib`, both
referenced by the commands below. Keep the `mcrypt/` prefix directory at the
root of this repository; `.gitignore` already excludes it.

## 2. extras.dylib — Threeway, SAFER-SK64, SAFER-SK128

The old libmcrypt build registers 16 block algorithms. Three more compile fine
but are omitted by its registration step, so the scanner `dlopen`s them
separately. `lib/search.cpp` loads `./extras.dylib` **relative to the working
directory**, and only when `EXTRA_ONLY` is set, which `recover.cpp` does on its
second `init()` call. Build it from the unmodified libmcrypt module sources:

    cd libmcrypt-2.5.8/modules/algorithms
    cc -DHAVE_CONFIG_H -I. -I../.. -I../../lib -O3 \
       -Wno-implicit-function-declaration -Wno-int-conversion -Wno-implicit-int \
       -dynamiclib 3-way.c safer64.c safer128.c -o ../../../extras.dylib
    cd ../../..

`extras.dylib` must sit at the repository root, because that is the working
directory the search runs from. It should be 36,736 bytes and export 33
`*_LTX__mcrypt_*` symbols:

    nm -gU extras.dylib | grep -c LTX     # 33

## 3. The recovery binary

    clang++ -O3 -std=c++17 -I mcrypt/include \
        search/zero_column/recover.cpp \
        -L mcrypt/lib -lmcrypt -Wl,-rpath,"$PWD/mcrypt/lib" \
        -o search/zero_column/recover

One `-Wunqualified-std-cast-call` warning is expected and harmless.

## 4. Re-run the search

    python3 -B search/zero_full/targeted_reproduce.py

Runs in well under a second. It reads `cipher.txt`, projects it back through
the AMSCO layout with the zero column masked, hands the masked pattern to
`recover` with **no plaintext crib**, and asserts that exactly 64 candidates
come back — all of them `blowfish-compat` / IV fill `0x30` / language class 1.
It then cross-checks them against the recorded
`search/zero_full/candidates_decoded.json` and writes
`targeted_results.json`.

Selecting candidate 18 happens *after* enumeration and is a reading judgment,
not a solver output. See the caveats in the top-level README.

## Other binaries

Same pattern, from the repository root:

    clang++ -O3 -std=c++17 -I mcrypt/include search/zero_full/benchmark.cpp \
        -L mcrypt/lib -lmcrypt -o search/zero_full/benchmark
    clang++ -O3 -std=c++17 -I mcrypt/include search/review/harness.cpp \
        -L mcrypt/lib -lmcrypt -o search/review/harness

## Files here

| File | Role |
|---|---|
| `search.cpp` | Shared scanner: algorithm registry, CFB8/ECB/CBC probes, printable-text gate. Included directly by `recover.cpp` and `support.inc`. |
| `crypto.py` | Python-side libmcrypt bindings and chain helpers used by the control scripts. |
| `zero_projection.py` | Forward/inverse AMSCO projection for non-leading-zero 10-digit keys, including the dropped column. `python3 -I lib/zero_projection.py` runs its 200-case self-test against `literal_models.py`. |
| `literal_models.py` | Literal Python translation of the 2016 PHP AMSCO class, used only to check the projection. The authoritative check is the unmodified PHP itself, under `historical_source/php_runtime/`. |
