import datetime
from pydantic import BaseModel
from typing import List


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    owner_id: int
    date_created: datetime.datetime
    date_updated: datetime.datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    posts: List[Post] = []

    class Config:
        orm_mode = True

# {
#   "email": "abc@gmail.com",
#   "id": 1,
#   "is_active": true,select * from user;
#   "posts": []
# }
