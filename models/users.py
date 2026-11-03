from pydantic import BaseModel
from typing import List


class User(BaseModel):
    id: int
    name: str
    is_active: bool = True  # default value, field becomes optional


# Body del PUT: sin id, porque el id se toma de la URL
class UpdateUserRequest(BaseModel):
    name: str
    is_active: bool = True


class GetUsersResponse(BaseModel):
    users: List[User]


class CreateUserResponse(BaseModel):
    message: str


class DeleteUserResponse(BaseModel):
    message: str


class UpdateUserResponse(BaseModel):
    message: str
