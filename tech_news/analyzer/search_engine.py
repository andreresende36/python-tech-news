from tech_news.database import find_news
import re
from datetime import datetime


# Requisito 7
def search_by_title(title: str):
    result = []
    news = find_news()
    for new in news:
        if title.lower() in new["title"].lower():
            result.append((new["title"], new["url"]))
    return result


# Requisito 8
def search_by_date(date):
    result = []
    news = find_news()
    try:
        search_date_obj = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Data inválida")
    for new in news:
        new_date_obj = datetime.strptime(new["timestamp"], "%d/%m/%Y")
        if new_date_obj == search_date_obj:
            result.append((new["title"], new["url"]))
    return result


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
    raise NotImplementedError
