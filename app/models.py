from __future__ import annotations

from typing import List

from sqlalchemy import (
    ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

import datetime as dt

from .database import Base


class BaseModel(Base):

    __abstract__ = True

    id: Mapped[int] = mapped_column(unique=True, primary_key=True, index=True)
    created_at: Mapped[dt.datetime] = mapped_column(default=dt.datetime.now())
    updated_at: Mapped[dt.datetime] = mapped_column(
        default=dt.datetime.now(), onupdate=(dt.datetime.now()))


class User(BaseModel):
    __tablename__ = 'users'
    hashed_password: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)

    name: Mapped[str] = mapped_column()
    surname: Mapped[str] = mapped_column()
    born_at: Mapped[dt.date] = mapped_column()
    owned_articles: Mapped[List['Article']
                           ] = relationship(back_populates='author')


class Article(BaseModel):
    __tablename__ = 'articles'

    title: Mapped[str] = mapped_column()

    description: Mapped[str] = mapped_column()
    content: Mapped[str] = mapped_column()

    author: Mapped['User'] = relationship(back_populates="owned_articles")
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
