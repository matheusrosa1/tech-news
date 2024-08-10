import time
from bs4 import BeautifulSoup
import requests


headers = {"user-agent": "Fake user-agent"}


# Requisito 1
def fetch(url):
    try:
        time.sleep(1)
        response = requests.get(url, headers=headers, timeout=3)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.Timeout:
        return None


# Requisito 2
def scrape_updates(html_content):
    bs = BeautifulSoup(html_content, "html.parser")

    articles = bs.find_all("article", {"class": "entry-preview"})

    news_links = []

    for article in articles:
        link_tag = article.find("a", {"class": "cs-overlay-link"})
        if link_tag:
            news_links.append(link_tag["href"])

    return news_links


# Requisito 3
def scrape_next_page_link(html_content):
    bs = BeautifulSoup(html_content, "html.parser")
    next_page = bs.find("a", {"class": "next"})

    if next_page:
        return next_page["href"]
    return None


# Requisito 4
def scrape_news(html_content):
    bs = BeautifulSoup(html_content, "html.parser")

    url = bs.find("link", {"rel": "canonical"})["href"]

    title = bs.find("h1", {"class": "entry-title"}).get_text().strip()

    timestamp = bs.find("li", {"class": "meta-date"}).get_text().strip()

    writer = bs.find("span", {"class": "author"}).get_text().strip()

    reading_time_str = bs.find("li", {"class": "meta-reading-time"}).get_text()

    if reading_time_str:
        reading_time = int("".join(filter(str.isdigit, reading_time_str)))
    else:
        reading_time = None  # Ou um valor padrão, como 0, dependendo do caso

    summary_tag = bs.find("div", {"class": "entry-content"})
    if summary_tag:
        summary_paragraph = summary_tag.find("p")
        summary = (
            summary_paragraph.get_text().strip() if summary_paragraph else ""
        )
    else:
        summary = ""

    category = bs.find("span", {"class": "label"}).get_text().strip()

    new_data = {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "reading_time": reading_time,
        "summary": summary,
        "category": category,
    }

    return new_data


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
    raise NotImplementedError
