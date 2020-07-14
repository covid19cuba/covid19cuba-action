from json import dump
from feedparser import parse
from hashlib import sha1
from bs4 import BeautifulSoup
from ...utils import dump_util

URL_JT_MEDIUM_FEED = 'https://medium.com/feed/juventud-t%C3%A9cnica/tagged/covid19'


def generate(debug=False):
    feed = parse(URL_JT_MEDIUM_FEED)
    news = []
    for entry in feed.entries:
        summary = str(entry['summary'])
        index_summary = summary.rindex('<hr>')
        summary = summary[:index_summary]
        summary = " ".join(summary.split())
        index_abstract = findnth(summary, '</p>', 2)
        abstract = summary[:index_abstract + 4]
        news.append({
            'id': entry['id'],
            'link': entry['link'],
            'title': entry['title'],
            'author': entry['author'],
            'published': entry['published_parsed'][:-3],
            'updated': entry['updated_parsed'][:-3],
            'summary': summary,
            'abstract': abstract,
            'abstract_str': BeautifulSoup(abstract, 'html.parser').text,
            'source': 'Juventud Técnica',
        })
    result = {
        'news': news,
    }
    dump(result,
         open(f'api/v2/jt_news.json', mode='w', encoding='utf-8'),
         ensure_ascii=False,
         indent=2 if debug else None,
         separators=(',', ': ') if debug else (',', ':'))
    build_jt_news_state(debug)
    return news


def build_jt_news_state(debug):
    dump_util('api/v2', jt_news_state, debug=debug)


def jt_news_state(data):
    result = {
        'cache': None,
    }
    with open('api/v2/jt_news.json', encoding='utf-8') as file:
        text = file.read()
        cache = sha1(text.encode())
        result['cache'] = cache.hexdigest()
    return result


def findnth(haystack, needle, n):
    parts = haystack.split(needle, n+1)
    if len(parts) <= n+1:
        return -1
    return len(haystack) - len(parts[-1]) - len(needle)
