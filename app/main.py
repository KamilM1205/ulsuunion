from app.routers import article, homepage, user, token_endpoint
from app.routers import about, article, account

from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(article.router)
app.include_router(token_endpoint.router)
app.include_router(user.router)
app.include_router(account.router)
app.include_router(about.router)
app.include_router(homepage.router)
