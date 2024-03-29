from datetime import datetime
from hashlib import sha1
from json import dump
from typing import Dict, Optional
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

from ...utils import dump_util

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) "
    "Gecko/20100101 Firefox/40.1"
}


def get_page(url, headers):
    page = Request(url=url, headers=headers)
    html = urlopen(page)
    bs = BeautifulSoup(html.read(), "html.parser")
    return bs


def get_author_and_summary(url, headers):
    bs = get_page(url, headers)
    summary = bs.find("article")
    text = summary.find("div", {"class": "text-justify"})  # type: ignore
    author = summary.ul.find("span").text  # type: ignore
    summary = str(text)
    return str(author), str(summary)


def get_datetime(arg):
    try:
        _datetime = datetime.strptime(arg, "%Y-%m-%d %H:%M:%S")
        return [
            _datetime.year,
            _datetime.month,
            _datetime.day,
            _datetime.hour,
            _datetime.minute,
            _datetime.second,
        ]
    finally:
        return None


def generate(debug=False):
    base_url = "https://www.presidencia.gob.cu"
    url = "https://www.presidencia.gob.cu/es/cuba/covid-19/"
    page = get_page(url, HEADERS)
    article_list = page.find_all("article", {"class": "grid-item"})
    news = []
    for article in article_list:
        link = base_url + article.a.attrs["href"]  # type: ignore
        title = article.find("div", {"class": "p-20"}).h5.text  # type: ignore
        author, summary = get_author_and_summary(link, HEADERS)
        summary = " ".join(summary.split())
        published = get_datetime(article.find("time").attrs["datetime"])  # type: ignore
        updated = published
        index_abstract = findnth(summary, "</p>", 2)
        abstract = summary[: index_abstract + 4]
        news.append(
            {
                "id": link,
                "link": link,
                "title": title,
                "author": author,
                "published": published,
                "updated": updated,
                "summary": summary,
                "abstract": abstract,
                "abstract_str": BeautifulSoup(abstract, "html.parser").text,
                "source": "Presidencia Cuba",
            }
        )
    result = {
        "news": news,
    }
    dump(
        result,
        open("api/v2/gob_news.json", mode="w", encoding="utf-8"),
        ensure_ascii=False,
        indent=2 if debug else None,
        separators=(",", ": ") if debug else (",", ":"),
    )
    build_gob_news_state(debug)
    return news


def build_gob_news_state(debug):
    dump_util("api/v2", gob_news_state, debug=debug)


def gob_news_state(data):
    result: Dict[str, Optional[str]] = {
        "cache": None,
    }
    with open("api/v2/gob_news.json", encoding="utf-8") as file:
        text = file.read()
        cache = sha1(text.encode())
        result["cache"] = cache.hexdigest()
    return result


def findnth(haystack, needle, n):
    parts = haystack.split(needle, n + 1)
    if len(parts) <= n + 1:
        return -1
    return len(haystack) - len(parts[-1]) - len(needle)
