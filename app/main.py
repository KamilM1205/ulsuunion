from typing import Annotated

from app.routers import article, user, token_endpoint
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
app.include_router(token_endpoint.router)
app.include_router(user.router)
