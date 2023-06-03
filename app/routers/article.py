from fastapi import Depends, Request
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session

from app.crud import get_article_by_id, get_articles
from app.dependencies import get_db


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/articles/{id}", response_class=HTMLResponse)
async def get_article(request: Request, id: int, db: Session = Depends(get_db)):
    article = get_article_by_id(db, id)
    return templates.TemplateResponse("article.html", {
            "request": request, 
            "title": article.title,
            "content": article.content,
            "author": article.author,
            "email": article.email,
            "phone": article.phone,
        })