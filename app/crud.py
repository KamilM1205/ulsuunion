from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import update

from . import models, schemas


############
# Users CRUD
############


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, user_email: str):
    return db.query(models.User).filter(models.User.email == user_email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_pword = user.password + "_not_really_hashed"
    db_user = models.User(
        **user.dict(exclude={"password"}), hashed_password=fake_hashed_pword)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user: models.User):
    db.delete(user)
    db.commit()
    return user


def update_user(db: Session, user_new_data: schemas.UserUpdate, user_id):
    hashed_password = user_new_data.password + "_not_really_hashed"
    user = user_new_data.dict(exclude={"password"})
    user["hashed_password"] = hashed_password
    user["id"] = user_id
    db.execute(update(models.User), [user])
    db.commit()
    db.refresh(user)


###############
# Articles CRUD
###############


def get_article_by_id(db: Session, article_id: int):
    return db.query(models.Article).filter(models.Article.id == article_id).first()


def get_articles(db: Session, skip: int, limit: int = 100):
    return db.query(models.Article).offset(skip).limit(limit).all()


def create_article(db: Session, article: schemas.ArticleCreate, user_id: int):
    db_article = models.Article(**article.dict(), author_id=user_id)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def update_article(db: Session, updated_article: schemas.ArticleUpdate, article_id: int):
    article = update_article.dict()
    article["id"] = article_id
    db.execute(update(models.Article), [article])


def delete_article(db: Session, article: models.Article):
    db.delete(article)
    db.commit()
    return article
