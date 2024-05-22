from typing import List
from src.schemas.user import User as UserSchema
from src.schemas.user import UserCreate as UserCreateSchema
from src.models.user import User as UserModel


class UserRepository:
    def __init__(self, db) -> None:
        self.db = db

    def get_user(self, email: str) -> UserSchema:
        user = self.db.query(UserModel).filter(UserModel.email == email).first()
        return user

    def create_user(self, user: UserCreateSchema) -> dict:
        new_user = UserModel(**user.model_dump())
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
    def get_all_users(self) -> List[UserSchema]:
        users = self.db.query(UserModel).all()
        return users
