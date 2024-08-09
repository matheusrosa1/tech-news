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
    """Seu código deve vir aqui"""
    raise NotImplementedError


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
    raise NotImplementedError
