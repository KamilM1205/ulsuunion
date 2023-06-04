from datetime import datetime, timedelta
from typing import Optional, Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext


from .database import SessionLocal
from . import crud, schemas


##########
# Database
##########


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


##########
# Security
##########


# Security constants
SECRET_CODE = "7b50be3cf0eacad427db4e8baee7193ed1a571af224ff36fdc26a943b53ec680"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def verify_password(plain_pwd, hashed_pwd):
    return pwd_context.verify(plain_pwd, hashed_pwd)


def get_password_hash(pwd):
    return pwd_context.hash(pwd)


def get_user(db: Session, username: str):
    db_user = crud.get_user_by_username(db, username)
    if not db_user:
        return None
    return schemas.UserInDB.from_orm(db_user)


def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_CODE, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(db: Annotated[Session, Depends(get_db)], token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not authorise credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_CODE, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)  # type: ignore
    if user is None:
        raise credentials_exception
    return user
