import time
from bs4 import BeautifulSoup
import requests

from tech_news.database import create_news


headers = {"user-agent": "Fake user-agent"}


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


def scrape_updates(html_content):
    bs = BeautifulSoup(html_content, "html.parser")

    articles = bs.find_all("article", {"class": "entry-preview"})

    news_links = []

    for article in articles:
        link_tag = article.find("a", {"class": "cs-overlay-link"})
        if link_tag:
            news_links.append(link_tag["href"])

    return news_links


def scrape_next_page_link(html_content):
    bs = BeautifulSoup(html_content, "html.parser")
    next_page = bs.find("a", {"class": "next"})

    if next_page:
        return next_page["href"]
    return None


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
        reading_time = None

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


def get_tech_news(amount):
    news_list = []
    url = "https://blog.betrybe.com/"
    while len(news_list) < amount:
        html_content = fetch(url)
        news_urls = scrape_updates(html_content)

        for news_url in news_urls:
            if len(news_list) < amount:
                news_html = fetch(news_url)
                news_data = scrape_news(news_html)
                news_list.append(news_data)
            else:
                break

        url = scrape_next_page_link(html_content)
        if not url:
            break

    create_news(news_list)
    return news_list
