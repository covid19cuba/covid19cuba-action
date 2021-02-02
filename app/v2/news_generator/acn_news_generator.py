from datetime import datetime
from hashlib import sha1
from json import dump
from typing import Dict, Optional

from bs4 import BeautifulSoup
from requests import get

from ...utils import dump_util

URL_ACN = (
    "http://www.acn.cu/busqueda?searchword=covid&ordering=newest"
    "&searchphrase=all&limit=0&areas[0]=categories"
    "&areas[1]=content&areas[2]=tags"
)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) "
    "Gecko/20100101 Firefox/40.1"
}

payload = {"query": "test"}


def remove_html_tags(string):
    new_str = ""
    flag = False
    if string is None:
        return string
    for i in string:
        if i == "<":
            flag = True
        if not flag:
            new_str = new_str + i
        if i == ">":
            flag = False
    new_str = new_str.split("\t")
    string = ""
    for i in new_str:
        string = string + i
    new_str = string.split("\n")
    string = ""
    for i in new_str:
        string = string + i
    new_str = string.split("\t")
    string = ""
    for i in new_str:
        string = string + i
    return string


def get_datetime(arg):
    return datetime.strptime(arg, "%Y-%m-%dT%H:%M:%S-04:00")


def clean_date(string):
    if string is None:
        return string
    string = string[string.find('content="') + len('content="') :]
    _datetime = get_datetime(string[: string.find('"')])
    return [
        _datetime.year,
        _datetime.month,
        _datetime.day,
        _datetime.hour,
        _datetime.minute,
        _datetime.second,
    ]


def extract_href(element):
    index = element.find('href="')
    element = element[index + len('href="') :]
    element = element[: element.find('">')]
    return element


def verify_none(element):
    if element == "None":
        return None
    return element


def generate(debug=False):
    limit = 10
    news = []
    r = get(URL_ACN, data=payload, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    titles = soup.findAll("dt", {"class": "result-title"})
    abstracts = soup.findAll("dd", {"class": "result-text"})
    news_links = [extract_href(str(i)) for i in titles]
    for i, item in enumerate(news_links):
        if i > limit:
            break
        link = "http://www.acn.cu" + item
        r = get(link, data=payload, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        author = verify_none(str(soup.find("dd", {"class": "createdby hasTooltip"})))
        created = verify_none(str(soup.find("meta", {"itemprop": "datePublished"})))
        updated = verify_none(str(soup.find("meta", {"itemprop": "dateModified"})))

        title = str(soup.find("h1", {"class": "article-title"}))
        abstract = str(abstracts[i])
        summary = str(soup.find("section", {"class": "article-content"}))

        if (
            title == "None" or abstract == "None" or summary == "None"
        ):  # verify required non None fields on the news
            continue

        news.append(
            {
                "id": link,
                "link": link,
                "title": remove_html_tags(title),
                "author": remove_html_tags(author),
                "published": clean_date(created),
                "updated": clean_date(updated),
                "summary": summary,
                "abstract": abstract,
            }
        )
    result = {
        "news": news,
    }
    dump(
        result,
        open("api/v2/acn_news.json", mode="w", encoding="utf-8"),
        ensure_ascii=False,
        indent=2 if debug else None,
        separators=(",", ": ") if debug else (",", ":"),
    )
    build_acn_news_state(debug)
    return news


def build_acn_news_state(debug):
    dump_util("api/v2", acn_news_state, debug=debug)


def acn_news_state(data):
    result: Dict[str, Optional[str]] = {
        "cache": None,
    }
    with open("api/v2/acn_news.json", encoding="utf-8") as file:
        text = file.read()
        cache = sha1(text.encode())
        result["cache"] = cache.hexdigest()
    return result
