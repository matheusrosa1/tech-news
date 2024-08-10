# Requisito 7
from datetime import datetime
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
    try:
        iso_date = datetime.strptime(date, "%Y-%m-%d")
        formatted_date = iso_date.strftime("%d/%m/%Y")
    except ValueError:
        raise ValueError("Data inválida")
    return [
        (notice["title"], notice["url"])
        for notice in search_news({"timestamp": formatted_date})
    ]


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
    raise NotImplementedError
