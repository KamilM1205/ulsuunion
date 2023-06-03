from fastapi import Request
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/articles/{id}", response_class=HTMLResponse)
async def get_article(request: Request):
    return templates.TemplateResponse("article.html", {
            "request": request, 
            "title": title,
            "content": content,
            "author": author,
            "email": email,
            "phone": phone,
        })