from typing import Annotated, List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends


from app import schemas,  dependencies, crud

router = APIRouter()


@router.post("/users/register", response_model=schemas.User)
async def create_user(
    user: schemas.UserCreate,
    db: Annotated[Session, Depends(dependencies.get_db)]
):
    user_in_db = crud.get_user_by_username(db, user.username)
    if user_in_db:
        raise
    user_in_db = crud.get_user_by_email(db, user.email)
    if user_in_db:
        raise
    new_user = crud.create_user(db, user)
    return new_user


@router.get("/users/me", response_model=schemas.User)
async def users_read_me(
    current_user: Annotated[schemas.User,
                            Depends(dependencies.get_current_user)]
):
    return current_user


@router.get("/users/me/items", response_model=List[schemas.Article])
async def users_own_items(
    current_user: Annotated[schemas.User,
                            Depends(dependencies.get_current_user)],
    db: Annotated[Session, Depends(dependencies.get_db)]
):
    return crud.get_user_articles(current_user.id, db)
