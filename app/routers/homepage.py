from fastapi import APIRouter, Request, Depends

from app import crud, dependencies, schemas

from sqlalchemy.orm import Session

from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def homepage(request: Request, db: Session = Depends(dependencies.get_db)):
    db_articles = crud.get_articles(db)
    articles = [schemas.Article.from_orm(article)
                for article in db_articles]
    return templates.TemplateResponse("index.html", {
        "request": request,
        "articles": db_articles,
    })
