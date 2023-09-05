import requests
from time import sleep
from parsel import Selector
from bs4 import BeautifulSoup
import re
from tech_news.database import create_news
from typing import Any


# Requisito 1
def fetch(url: str):
    headers = {"user-agent": "Fake user-agent"}
    try:
        response = requests.get(url, timeout=3, headers=headers)
        sleep(1)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.exceptions.Timeout:
        return None


# Requisito 2
def scrape_updates(html_content):
    selector = Selector(html_content)
    return selector.css(".cs-overlay-link::attr(href)").getall()


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(html_content)
    return selector.css(".next::attr(href)").get()


# Requisito 4
def scrape_news(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    url_element = soup.find(rel="canonical")
    url = url_element["href"] if url_element else None  # type: ignore
    title_element = soup.find("h1")
    title = title_element.text.replace("\xa0", "") if title_element else None
    timestamp_element = soup.find("li", {"class": "meta-date"})
    timestamp = timestamp_element.text if timestamp_element else None
    writer_parent = soup.find("span", {"class": "author"})
    writer = writer_parent.a.text if writer_parent else None  # type: ignore
    reading_time_element = soup.find("li", {"class": "meta-reading-time"})
    reading_time = (
        int(re.findall(r"\d+", reading_time_element.text)[0])
        if reading_time_element
        else None
    )
    summary_parent = soup.find("div", {"class": "entry-content"})
    summary = (
        summary_parent.p.text.replace("\xa0", "").removesuffix(  # type: ignore
            " "
        )
        if summary_parent
        else None
    )
    category_element = soup.find("span", {"class": "label"})
    category = category_element.text if category_element else None

    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "reading_time": reading_time,
        "summary": summary,
        "category": category,
    }


def fill_news_list(
    news_urls: list[str], amount: int, news: list[dict[str, Any]]
):
    for new in news_urls:
        if len(news) < amount:
            news.append(scrape_news(fetch(new)))
    return news


# Requisito 5
def get_tech_news(amount):
    BASE_URL = "https://blog.betrybe.com"
    news = []

    while len(news) < amount:
        response_HTML = fetch(BASE_URL)
        news_urls = scrape_updates(response_HTML)
        news = fill_news_list(news_urls, amount, news)
        next_page_url = scrape_next_page_link(response_HTML)
        if not next_page_url:
            break
        BASE_URL = next_page_url
    create_news(news)
    return news


get_tech_news(30)
