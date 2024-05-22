import bcrypt
import jwt
from fastapi import HTTPException
from datetime import (
    datetime,
    timezone,
    timedelta,
)
from src.repositories.user import UserRepository
from fastapi.security import HTTPAuthorizationCredentials


class JWTHandler:
    def __init__(self, secret, algorithm) -> None:
        self.secret = secret
        self.algorithm = algorithm

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password=password.encode("utf-8"), salt=bcrypt.gensalt())

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            password=password.encode("utf-8"),
            hashed_password=hashed_password.encode("utf-8"),
        )

    def encode_token(self, user):
        payload = {
            # exp (expiration time): Time after which the JWT expires
            "exp": datetime.now(tz=timezone.utc) + timedelta(hours=1),
            # iat (issued at time): Time at which the JWT was issued
            "iat": datetime.now(tz=timezone.utc),
            # sub (subject): Subject of the JWT (the user)
            "sub": user.email,
            # Custom Issues
            "scope": "access_token",
            "user.name": user.name,
            "user.id": user.id,
        }
        jwt_token = None
        try:
            jwt_token = jwt.encode(payload, self.secret, algorithm=self.algorithm)
        except Exception as e:
            print("Error:", e)

        return jwt_token

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            if payload["scope"] == "access_token":
                return payload
            raise HTTPException(
                status_code=401, detail="Scope for the token is invalid"
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def encode_refresh_token(self, user):
        payload = {
            "exp": datetime.now(tz=timezone.utc) + timedelta(hours=10),
            "iat": datetime.now(tz=timezone.utc),
            "scope": "refresh_token",
            "sub": user.email,
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def refresh_token(self, refresh_token):
        try:
            payload = jwt.decode(
                refresh_token, self.secret, algorithms=[self.algorithm]
            )
            if payload and payload["scope"] == "refresh_token":
                user = UserRepository.get_user(payload["sub"])
                new_token = self.encode_token(user)
                return new_token
            raise HTTPException(status_code=401, detail="Invalid scope for token")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Refresh token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

    def verify_jwt(self, credentials: HTTPAuthorizationCredentials) -> bool:
        isTokenValid: bool = False
        try:
            token = credentials.credentials
            payload = self.decode_token(token=token)
        except jwt.PyJWKError:
            payload = None
        if payload:
            isTokenValid = True

        return isTokenValid
