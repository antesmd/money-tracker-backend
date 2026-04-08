from __future__ import annotations

import bcrypt


def hash_with_bcrypt(plain_text: str) -> str:
    return bcrypt.hashpw(
        plain_text.encode("utf-8"),
        bcrypt.gensalt(),
    ).decode("utf-8")


def verify_bcrypt_hash(
    plain_text: str,
    hashed_text: str,
) -> bool:
    return bcrypt.checkpw(
        plain_text.encode("utf-8"),
        hashed_text.encode("utf-8"),
    )
