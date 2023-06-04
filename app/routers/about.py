from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/about", response_class=HTMLResponse)
def get_about(request: Request):
    return templates.TemplateResponse("about.html", {
        "request": request,
    })