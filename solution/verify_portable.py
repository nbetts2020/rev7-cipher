#!/usr/bin/env python3
"""Verify the recovered Rev-7 message using Python 3's standard library only.

Run: python3 verify_portable.py
Keep this script, blowfish_constants.json, plaintext.txt,
recovered_cipher.hex and observed_cipher.txt in the same directory.

Blowfish constants/key expansion and little-endian compatibility behavior
follow libmcrypt 2.5.8's blowfish-compat.c. See BLOWFISH_SOURCE_NOTICE.txt
and COPYING.LIB for attribution and the GNU Lesser General Public License.
This verifier checks a supplied recovered message; it does not redo the
search for erased ciphertext bytes or claim uniqueness of a lossy cipher.
"""
from pathlib import Path
import hashlib
import json
import struct
import sys

MASK32 = (1 << 32) - 1
HERE = Path(__file__).resolve().parent


class BlowfishCompat:
    """libmcrypt blowfish-compat: standard rounds, little-endian block words."""

    def __init__(self, key, constants_path=HERE / "blowfish_constants.json"):
        if not isinstance(key, bytes) or not 1 <= len(key) <= 56:
            raise ValueError("Blowfish key must contain 1 to 56 bytes")
        initial = json.loads(Path(constants_path).read_text(encoding="utf-8"))
        self.p = [int(word, 16) for word in initial["P"]]
        self.s = [[int(word, 16) for word in box] for box in initial["S"]]
        if len(self.p) != 18 or len(self.s) != 4 or any(len(box) != 256 for box in self.s):
            raise ValueError("Invalid Blowfish constants")
        if any(not 0 <= x <= MASK32 for x in self.p + sum(self.s, [])):
            raise ValueError("Constant outside the 32-bit range")
        # Key bytes form big-endian 32-bit words; only external block IO is LE.
        cursor = 0
        for i in range(18):
            word = 0
            for _ in range(4):
                word = (word << 8) | key[cursor]
                cursor = (cursor + 1) % len(key)
            self.p[i] ^= word
        left = right = 0
        for i in range(0, 18, 2):
            left, right = self._encrypt_words(left, right)
            self.p[i], self.p[i + 1] = left, right
        for box in self.s:
            for i in range(0, 256, 2):
                left, right = self._encrypt_words(left, right)
                box[i], box[i + 1] = left, right

    def _f(self, value):
        a = self.s[0][value >> 24]
        b = self.s[1][(value >> 16) & 255]
        c = self.s[2][(value >> 8) & 255]
        d = self.s[3][value & 255]
        return ((((a + b) & MASK32) ^ c) + d) & MASK32

    def _encrypt_words(self, left, right):
        for i in range(16):
            left ^= self.p[i]
            right ^= self._f(left)
            left, right = right, left
        left, right = right, left
        right ^= self.p[16]
        left ^= self.p[17]
        return left, right

    def encrypt_block(self, block):
        if len(block) != 8:
            raise ValueError("A Blowfish block contains exactly eight bytes")
        return struct.pack("<II", *self._encrypt_words(*struct.unpack("<II", block)))

    def decrypt_block(self, block):
        if len(block) != 8:
            raise ValueError("A Blowfish block contains exactly eight bytes")
        left, right = struct.unpack("<II", block)
        for i in range(17, 1, -1):
            left ^= self.p[i]
            right ^= self._f(left)
            left, right = right, left
        left, right = right, left
        right ^= self.p[1]
        left ^= self.p[0]
        return struct.pack("<II", left, right)

    def cfb8(self, data, iv=b"00000000", decrypt=False):
        if len(iv) != 8:
            raise ValueError("The IV contains exactly eight bytes")
        register = bytes(iv)
        output = bytearray()
        for byte in data:
            transformed = byte ^ self.encrypt_block(register)[0]
            output.append(transformed)
            feedback = byte if decrypt else transformed
            register = register[1:] + bytes([feedback])
        return bytes(output)


def legacy_amsco_encode(text, key="1947038265"):
    """Forward legacy numeric-column AMSCO, including its dropped zero column.

    This implements the relevant nonnegative numeric-key/hexadecimal-input
    behavior. It is not a general replacement for the historical PHP UI.
    """
    key = str(int(key))  # Historical controller's numeric-to-integer conversion.
    if not key.isascii() or not key.isdigit() or not key:
        raise ValueError("Expected a nonnegative numeric key")
    text = text.upper()
    if any(c not in "0123456789ABCDEF" for c in text):
        raise ValueError("This verifier expects compact hexadecimal input")
    rows = []
    cursor = cell = 0
    while cursor < len(text):
        row = {}
        for digit in key:
            if cursor >= len(text):
                break
            take = 2 if cell % 2 == 0 else 1
            row[int(digit)] = text[cursor:cursor + take]
            cursor += take
            cell += 1
        rows.append(row)
    # Label zero is never emitted. Missing label ten contributes no characters.
    return "".join(row.get(label, "") for label in range(1, len(key) + 1) for row in rows)


def read_hex(path):
    text = "".join(Path(path).read_text(encoding="utf-8").split()).upper()
    if any(c not in "0123456789ABCDEF" for c in text) or len(text) % 2:
        raise ValueError("Invalid even-length hexadecimal file: " + str(path))
    return text


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    # Exact known-answer self-test from the original compatibility source.
    test_key = bytes((i * 2 + 10) % 256 for i in range(56))
    test_cipher = BlowfishCompat(test_key)
    vector = bytes.fromhex("de8e9a3a9cd44280")
    require(test_cipher.encrypt_block(bytes(range(8))) == vector, "Original Blowfish compatibility self-test failed")
    require(test_cipher.decrypt_block(vector) == bytes(range(8)), "Blowfish inverse self-test failed")

    plaintext = (HERE / "plaintext.txt").read_bytes()
    recovered_hex = read_hex(HERE / "recovered_cipher.hex")
    observed_hex = read_hex(HERE / "observed_cipher.txt")
    recovered = bytes.fromhex(recovered_hex)
    cipher = BlowfishCompat(b"Zombies")
    require(cipher.cfb8(recovered, decrypt=True) == plaintext, "Recovered ciphertext does not decrypt to the supplied plaintext")
    require(cipher.cfb8(plaintext) == recovered, "Plaintext does not reproduce the recovered ciphertext")
    amsco_output = legacy_amsco_encode(recovered_hex)
    regenerated = amsco_output[::-1]
    require(regenerated == observed_hex, "AMSCO/drop-zero/reversal does not match the observed cipher")
    reversed_groups = " ".join(amsco_output[i:i + 5] for i in range(0, len(amsco_output), 5))[::-1].split()
    observed_groups = (HERE / "observed_cipher.txt").read_text(encoding="utf-8").split()
    require(reversed_groups == observed_groups, "Reversed five-character grouping does not match the paper")
    require((len(plaintext), len(recovered_hex), len(observed_hex)) == (630, 1260, 1092), "Unexpected solution artifact lengths")
    print("PASS original Blowfish compatibility known-answer test")
    print("PASS exact CFB8 decryption and re-encryption of all 630 bytes")
    print("PASS legacy AMSCO key 1947038265, dropped column 0, and character reversal")
    print("PASS all 1,092 observed hexadecimal characters match")
    print("PASS all 219 printed groups match, including the initial 83")
    print("Plaintext SHA-256:", hashlib.sha256(plaintext).hexdigest())
    print("Observed hex SHA-256:", hashlib.sha256(observed_hex.encode("ascii")).hexdigest())
    print("The original transform loses 168 hex characters; this verifies the supplied recovery, not mathematical uniqueness.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print("FAIL:", exc, file=sys.stderr)
        sys.exit(1)
