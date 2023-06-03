from datetime import datetime, timedelta
from typing import Optional, Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt


from sqlalchemy.orm import Session
from .database import SessionLocal

from passlib.context import CryptContext


##########
# Database
##########


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
