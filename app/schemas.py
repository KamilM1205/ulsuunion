from __future__ import annotations

from typing import Optional, List

from pydantic import BaseModel

import datetime as dt


class ArticleBase(BaseModel):
    title: str
    description: str
    content: str


class ArticleGet(ArticleBase):
    author: 'UserBase'


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(ArticleCreate):
    pass


class Article(ArticleBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: str
    name: str
    surname: str
    born_at: dt.date


class UserGet(UserBase):
    owned_articles: List['ArticleBase'] = []


class UserCreate(UserBase):
    password: str


class UserUpdate(UserCreate):
    id: int


class User(UserBase):
    id: int
    owned_articles: List[Article] = []

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
