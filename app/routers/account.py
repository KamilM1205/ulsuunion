from typing import Annotated
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session

from datetime import date
from app import crud, dependencies, schemas

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def age_calc(birthdate):
    today = date.today()
    age = today.year - birthdate.year - \
        ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age


@router.get("/account", response_class=HTMLResponse)
def get_account(request: Request, db: Annotated[Session, Depends(dependencies.get_db)]):

    user = schemas.User.from_orm(crud.get_user_by_id(db, 2))
    articles = [schemas.Article.from_orm(article)
                for article in user.owned_articles]
    print(articles)
    age = age_calc(user.born_at)
    return templates.TemplateResponse("account.html", {
        "request": request,
        "articles": articles,
        "age": age,
        **user.dict()
    })
