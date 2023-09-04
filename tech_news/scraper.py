import requests
from time import sleep
from parsel import Selector
from bs4 import BeautifulSoup
import re


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


# headers = {
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,
# image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)
# AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
# }
# text = requests.get(
#     "https://blog.betrybe.com/tecnologia/jogos-iniciantes-aprender-programar/",
#     headers=headers,
# ).text
# with open("text.html", "w") as file:
#     file.write(text)


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


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
    raise NotImplementedError
