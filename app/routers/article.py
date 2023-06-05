from typing import Annotated
from fastapi import Request, Depends, Query
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import HTTPException
from sqlalchemy.orm import Session


from app.dependencies import get_db
from app import crud, dependencies, schemas

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


@router.post("/acticles/", response_model=schemas.Article)
async def create_article(
        article: schemas.ArticleCreate,
        db: Annotated[Session, Depends(get_db)],
        user: Annotated[schemas.User, Depends(dependencies.get_current_user)]):
    user_id = user.id
    db_article = crud.create_article(db, article, user_id)
    return db_article
