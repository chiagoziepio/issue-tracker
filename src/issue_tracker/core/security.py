from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

from issue_tracker.core.config import get_config
from issue_tracker.types import (
    ACCESS_TOKEN_COOKIE_DATA_TYPE,
    REFRESH_TOKEN_COOKIE_DATA_TYPE,
)


class Security:
    def __init__(self):
        self.password_hash = PasswordHash.recommended()

    def hash_password(self, password: str) -> str:
        """Hash the provided password using a secure hashing algorithm."""
        return self.password_hash.hash(password)

    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify if the provided password matches the hashed password."""
        return self.password_hash.verify(password, password_hash)

    def generate_access_token(self, user_id: str) -> str:
        """Generate a new access token for the provided user."""
        now = datetime.now(UTC)
        expires = now + timedelta(minutes=get_config().JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "user_id": user_id,
            "exp": expires,
            "iat": now,
            "iss": get_config().JWT_ISSUER,
            "type": "access",
            "aud": get_config().AUDIENCE,
        }

        token = jwt.encode(
            payload, get_config().JWT_SECRET_KEY, algorithm=get_config().JWT_ALGORITHM
        )
        return token

    def verify_access_token(self, token: str) -> ACCESS_TOKEN_COOKIE_DATA_TYPE:
        """Verify the provided access token and return the decoded payload."""
        payload = jwt.decode(
            token,
            get_config().JWT_SECRET_KEY,
            algorithms=[get_config().JWT_ALGORITHM],
            options={
                "require": [
                    "user_id",
                    "exp",
                    "iat",
                    "iss",
                    "type",
                ]
            },
            audience=get_config().AUDIENCE,
            issuer=get_config().JWT_ISSUER,
        )
        if payload.get("type") != "access":
            raise jwt.InvalidTokenError("Invalid token type. Expected 'access'.")
        return {"user_id": payload["user_id"], "type": payload["type"]}

    def generate_fresh_token(self, user_id: str) -> str:
        """Generate a new access token for the provided user."""
        now = datetime.now(UTC)
        expires = now + timedelta(minutes=get_config().JWT_FRESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "user_id": user_id,
            "exp": expires,
            "iat": now,
            "iss": get_config().JWT_ISSUER,
            "type": "refresh",
            "aud": get_config().AUDIENCE,
        }

        token = jwt.encode(
            payload, get_config().JWT_SECRET_KEY, algorithm=get_config().JWT_ALGORITHM
        )
        return token

    def verify_fresh_token(self, token: str) -> REFRESH_TOKEN_COOKIE_DATA_TYPE:
        """Verify the provided refresh token and return the decoded payload."""
        payload = jwt.decode(
            token,
            get_config().JWT_SECRET_KEY,
            algorithms=[get_config().JWT_ALGORITHM],
            options={
                "require": [
                    "user_id",
                    "exp",
                    "iat",
                    "iss",
                    "type",
                ]
            },
            audience=get_config().AUDIENCE,
            issuer=get_config().JWT_ISSUER,
        )
        if payload.get("type") != "refresh":
            raise jwt.InvalidTokenError("Invalid token type. Expected 'refresh'.")
        return {"user_id": payload["user_id"], "type": payload["type"]}
