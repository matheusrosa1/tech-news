# Requisito 7
from tech_news.database import search_news


def search_by_title(title):
    return [
        (notice["title"], notice["url"])
        for notice in search_news(
            {"title": {"$regex": title, "$options": "i"}}
        )
    ]


# Requisito 8
def search_by_date(date):
    """Seu código deve vir aqui"""
    raise NotImplementedError


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
    raise NotImplementedError
