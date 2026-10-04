"""Password hashing and fixed-algorithm JWT primitives."""

import base64
import hashlib
import hmac
import secrets
import time

import jwt

TOKEN_LIFETIME_SECONDS = 900


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(password.encode(), salt=salt, n=16384, r=8, p=1, dklen=64)
    return 'scrypt$' + base64.b64encode(salt).decode() + '$' + base64.b64encode(digest).decode()


def parse_password_hash(encoded: str) -> tuple[bytes, bytes]:
    algorithm, salt_text, digest_text = encoded.split('$')
    salt = base64.b64decode(salt_text, validate=True)
    digest = base64.b64decode(digest_text, validate=True)
    if algorithm != 'scrypt' or len(salt) != 16 or len(digest) != 64:
        raise ValueError('Invalid password hash format')
    return salt, digest


def verify_password(password: str, encoded: str) -> bool:
    salt, expected = parse_password_hash(encoded)
    actual = hashlib.scrypt(password.encode(), salt=salt, n=16384, r=8, p=1, dklen=64)
    return hmac.compare_digest(actual, expected)


# Unknown usernames still perform the same password derivation as known users.
DUMMY_PASSWORD_HASH = hash_password(secrets.token_urlsafe(32))


def issue_token(user_id: str, role: str, secret: str) -> str:
    now = int(time.time())
    return jwt.encode({'sub': user_id, 'role': role, 'iat': now,
                       'exp': now + TOKEN_LIFETIME_SECONDS}, secret, algorithm='HS256')


def decode_token(token: str, secret: str) -> dict:
    return jwt.decode(token, secret, algorithms=['HS256'],
                      options={'require': ['sub', 'role', 'iat', 'exp']})
