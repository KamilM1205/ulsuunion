import json

from app.constants import APP_DOMAIN

def get_list():
    articles = []

    for i in range(5):
        article = {
                "title": "Заголовок",
                "author": f"Я {i}",
                "description": "Некое короткое описание статьи",
                "link": f"/articles/{i}"
            }
        articles.append(article)

    return articles