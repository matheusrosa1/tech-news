from datetime import datetime
from tech_news.database import search_news


def search_by_title(title):
    search_news_by_title = search_news(
        {"title": {"$regex": title, "$options": "i"}}
    )

    return [
        (notice["title"], notice["url"]) for notice in search_news_by_title
    ]


def search_by_date(date):
    try:
        iso_date = datetime.strptime(date, "%Y-%m-%d")
        formatted_date = iso_date.strftime("%d/%m/%Y")
    except ValueError:
        raise ValueError("Data inválida")

    search_news_by_date = search_news({"timestamp": formatted_date})

    if not search_news_by_date:
        return []

    return [(notice["title"], notice["url"]) for notice in search_news_by_date]


def search_by_category(category):
    search_news_by_category = search_news(
        {"category": {"$regex": category, "$options": "i"}}
    )

    if not search_news_by_category:
        return []

    return [
        (notice["title"], notice["url"]) for notice in search_news_by_category
    ]
