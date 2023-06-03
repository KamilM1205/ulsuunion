from fastapi import Request, Depends
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas import Article

from app.dependencies import get_db
from app.crud import get_article_by_id

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/articles/{id}", response_class=HTMLResponse)
async def get_article(request: Request, id: int, db: Session = Depends(get_db)):
    db_article = get_article_by_id(db, id)

    if not db_article:
        raise HTTPException(status_code=404)
    article = Article.from_orm(db_article)

    return templates.TemplateResponse("article.html", {
        "request": request,
        **article.dict()
    })
