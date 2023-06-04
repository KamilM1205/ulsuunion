from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/account", response_class=HTMLResponse)
def get_account(request: Request):
    return templates.TemplateResponse("account.html", {
        "request": request,
    })