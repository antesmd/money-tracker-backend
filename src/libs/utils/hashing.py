from __future__ import annotations

import bcrypt


def hash_with_bcrypt(plain_text: str) -> str:
    return bcrypt.hashpw(
        plain_text.encode("utf-8"),
        bcrypt.gensalt(),
    ).decode("utf-8")
