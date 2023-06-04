from typing import Annotated
from fastapi import Request, Depends, Form
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import HTTPException
from sqlalchemy.orm import Session


from app.dependencies import get_db
import app.crud as crud
import app.schemas as schemas

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/articles/{id}", response_class=HTMLResponse)
async def get_article(request: Request, id: int, db: Session = Depends(get_db)):
    db_article = crud.get_article_by_id(db, id)

    if not db_article:
        raise HTTPException(status_code=404)
    article = schemas.Article.from_orm(db_article)

    return templates.TemplateResponse("article.html", {
        "request": request,
        **article.dict()
    })


@router.get("/edit_article", response_class=HTMLResponse)
async def get_article_editor(request: Request):
    return templates.TemplateResponse("article_editor.html", {
        "request": request,
    })


@router.post("/acticles/", response_model=schemas.Article)
async def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    # get user by id
    # CHECK IF ITS EXISTS
    user_id = 1
    db_article = crud.create_article(db, article, user_id)
    return db_article
