"""StokAI 암호화 유틸리티 모듈
버전: 1.0.0
Fernet 대칭키 암호화/복호화, 키 생성/관리, 파일 암호화/복호화
"""
from cryptography.fernet import Fernet

from src.utils.logger import get_logger

logger = get_logger("security.encryption")


def generate_key() -> bytes:
    """새 Fernet 키를 생성하여 반환."""
    key = Fernet.generate_key()
    logger.debug("새 암호화 키 생성")
    return key


def encrypt(data: str, key: bytes) -> str:
    """문자열을 Fernet으로 암호화하여 base64 문자열 반환."""
    f = Fernet(key)
    token = f.encrypt(data.encode("utf-8"))
    return token.decode("utf-8")


def decrypt(encrypted: str, key: bytes) -> str:
    """암호화된 base64 문자열을 복호화하여 원본 문자열 반환."""
    f = Fernet(key)
    plain = f.decrypt(encrypted.encode("utf-8"))
    return plain.decode("utf-8")


def save_key(key: bytes, path: str) -> None:
    """암호화 키를 파일로 저장."""
    with open(path, "wb") as f:
        f.write(key)
    logger.debug("키 저장: %s", path)


def load_key(path: str) -> bytes:
    """파일에서 암호화 키를 로드."""
    with open(path, "rb") as f:
        return f.read()


def encrypt_file(src: str, dst: str, key: bytes) -> None:
    """파일 전체를 Fernet으로 암호화하여 저장."""
    f = Fernet(key)
    with open(src, "rb") as fin:
        data = fin.read()
    token = f.encrypt(data)
    with open(dst, "wb") as fout:
        fout.write(token)
    logger.debug("파일 암호화: %s -> %s", src, dst)


def decrypt_file(src: str, dst: str, key: bytes) -> None:
    """암호화된 파일을 복호화하여 저장."""
    f = Fernet(key)
    with open(src, "rb") as fin:
        token = fin.read()
    data = f.decrypt(token)
    with open(dst, "wb") as fout:
        fout.write(data)
    logger.debug("파일 복호화: %s -> %s", src, dst)
