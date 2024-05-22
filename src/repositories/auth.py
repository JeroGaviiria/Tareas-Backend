from fastapi import HTTPException, status
from src.repositories.user import UserRepository
from src.config.database import SessionLocal
from src.auth import auth_handler
from src.schemas.user import UserLogin as UserLoginSchema
from src.schemas.user import UserCreate as UserCreateSchema


class AuthRepository:
    def __init__(self) -> None:
        pass

    def register_user(self, user: UserCreateSchema) -> dict:
        db = SessionLocal()
        if UserRepository(db).get_user(email=user.email) is not None:
            raise Exception("Account already exists")
        hashed_password = auth_handler.hash_password(password=user.password)
        new_user: UserCreateSchema = UserCreateSchema(
            name=user.name, email=user.email, password=hashed_password, is_active=True
        )
        return UserRepository(db).create_user(new_user)

    def login_user(self, user: UserLoginSchema) -> dict:
        db = SessionLocal()
        check_user = UserRepository(db).get_user(email=user.email)
        if check_user is None:
            print("aqui fallo 1")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials (1)",
            )
        if not check_user.is_active:
            print("aqui fallo 2")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="The user is not allowed to log in",
            )
        if not auth_handler.verify_password(user.password, check_user.password):
            print("aqui fallo 3")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials (2)",
            )
        access_token = auth_handler.encode_token(check_user)
        refresh_token = auth_handler.encode_refresh_token(check_user)

        return access_token, refresh_token
