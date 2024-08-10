from collections import Counter
from tech_news.database import search_news


def top_5_categories():
    all_news = search_news({})

    categories = [news["category"] for news in all_news if "category" in news]

    category_counts = Counter(categories)

    sorted_categories = sorted(
        category_counts.items(), key=lambda item: (-item[1], item[0])
    )

    top_categories = [category for category, count in sorted_categories]

    return top_categories[:5]
