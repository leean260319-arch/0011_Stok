"""T010 encryption 유틸리티 테스트
파일 I/O는 tempfile.TemporaryDirectory 사용
"""
import os
import tempfile

import pytest

from src.security.encryption import (
    decrypt,
    decrypt_file,
    encrypt,
    encrypt_file,
    generate_key,
    load_key,
    save_key,
)


@pytest.fixture()
def key():
    return generate_key()


@pytest.fixture()
def tmpdir():
    with tempfile.TemporaryDirectory() as d:
        yield d


class TestGenerateKey:
    def test_returns_bytes(self, key):
        assert isinstance(key, bytes)

    def test_key_is_44_chars_base64(self, key):
        # Fernet 키는 URL-safe base64로 44바이트
        assert len(key) == 44

    def test_each_call_different(self):
        k1 = generate_key()
        k2 = generate_key()
        assert k1 != k2


class TestEncryptDecrypt:
    def test_encrypt_returns_string(self, key):
        result = encrypt("hello", key)
        assert isinstance(result, str)

    def test_decrypt_returns_original(self, key):
        original = "hello world"
        token = encrypt(original, key)
        assert decrypt(token, key) == original

    def test_encrypted_differs_from_original(self, key):
        original = "secret"
        assert encrypt(original, key) != original

    def test_roundtrip_unicode(self, key):
        original = "한국어 테스트 \u00e9\u00e0"
        assert decrypt(encrypt(original, key), key) == original

    def test_wrong_key_raises(self, key):
        token = encrypt("data", key)
        wrong_key = generate_key()
        with pytest.raises(Exception):
            decrypt(token, wrong_key)


class TestSaveLoadKey:
    def test_save_then_load_returns_same_key(self, key, tmpdir):
        path = os.path.join(tmpdir, "test.key")
        save_key(key, path)
        loaded = load_key(path)
        assert loaded == key

    def test_saved_file_exists(self, key, tmpdir):
        path = os.path.join(tmpdir, "my.key")
        save_key(key, path)
        assert os.path.isfile(path)


class TestEncryptDecryptFile:
    def test_encrypt_file_creates_dst(self, key, tmpdir):
        src = os.path.join(tmpdir, "src.txt")
        dst = os.path.join(tmpdir, "dst.enc")
        with open(src, "w", encoding="utf-8") as f:
            f.write("file contents")
        encrypt_file(src, dst, key)
        assert os.path.isfile(dst)

    def test_encrypt_file_differs_from_src(self, key, tmpdir):
        src = os.path.join(tmpdir, "src.txt")
        dst = os.path.join(tmpdir, "dst.enc")
        with open(src, "wb") as f:
            f.write(b"plaintext data")
        encrypt_file(src, dst, key)
        with open(src, "rb") as f:
            plain = f.read()
        with open(dst, "rb") as f:
            cipher = f.read()
        assert plain != cipher

    def test_decrypt_file_restores_original(self, key, tmpdir):
        src = os.path.join(tmpdir, "src.txt")
        enc = os.path.join(tmpdir, "enc.bin")
        dec = os.path.join(tmpdir, "dec.txt")
        original = b"binary \x00\x01\x02 data"
        with open(src, "wb") as f:
            f.write(original)
        encrypt_file(src, enc, key)
        decrypt_file(enc, dec, key)
        with open(dec, "rb") as f:
            result = f.read()
        assert result == original
