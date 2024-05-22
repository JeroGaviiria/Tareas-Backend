from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class User(BaseModel):
    id: Optional[int] = Field(default=None, title="Id of the user")
    name: str = Field(min_length=4, max_length=60, title="Name of the user")
    email: EmailStr = Field(min_length=6, max_length=64, title="Email of theuser")
    password: str = Field(max_length=64, title="Password of the user")
    is_active: bool = Field(default=True, title="Status of the user")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "email": "pepe@base.net",
                "name": "Pepe Pimentón",
                "password": "xxx",
                "is_active": True,
            }
        }


class UserCreate(BaseModel):
    name: str = Field(min_length=4, max_length=60, title="Name of the user")
    email: EmailStr = Field(min_length=6, max_length=64, title="Email of the user")
    password: str = Field(max_length=64, title="Password of the user")


class UserLogin(BaseModel):
    email: EmailStr = Field(
        min_length=6, max_length=64, alias="username", title="Email of the user"
    )
    password: str = Field(min_length=4, title="Password of the user")
