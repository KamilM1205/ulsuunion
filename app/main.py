from typing import Annotated

from app.routers import article, login, registration
from app.utils.article_generator import get_list
from fastapi import FastAPI, Request, HTTPException, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from . import schemas, crud, models
from .database import engine

from .dependencies import get_db

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(article.router)
app.include_router(login.router)
app.include_router(registration.router)


@app.post("/user/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user_email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username already registered")
    user = crud.create_user(db, user)
    return user


@app.delete("/user/", response_model=schemas.User)
async def remove_user(user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user.id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User does not exists")
    return crud.delete_user(db, db_user)


@app.put("/user/", response_model=schemas.User)
async def edit_user(user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user.id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User does not exists")
    user = crud.update_user(db, user, db_user.id)
    return user


@app.get("/users/", response_model=list[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/", response_class=HTMLResponse)
async def root(request: Request, db: Session = Depends(get_db)):
    articles = get_list()
    return templates.TemplateResponse("index.html", {"request": request, "articles": articles})
