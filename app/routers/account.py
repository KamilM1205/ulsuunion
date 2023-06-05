from typing import Annotated
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session

from datetime import date
from app import dependencies, schemas

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def age_calc(birthdate):
    today = date.today()
    age = today.year - birthdate.year - \
        ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

@router.get("/account", response_class=HTMLResponse)
def get_account(request: Request):
    return templates.TemplateResponse("account.html", {
        "request": request,
    })
