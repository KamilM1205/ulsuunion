from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.utils.article_generator import get_list

from app.routers import article


app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(article.router)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    articles = get_list()
    return templates.TemplateResponse("index.html", {"request": request, "articles": articles})