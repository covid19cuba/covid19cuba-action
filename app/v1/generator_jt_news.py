from json import dump
from feedparser import parse

URL_JT_MEDIUM_FEED = 'https://medium.com/feed/juventud-t%C3%A9cnica/tagged/covid19'


def generate(debug=False):
    feed = parse(URL_JT_MEDIUM_FEED)
    news = []
    for entry in feed.entries:
        news.append({
            'id': entry['id'],
            'link': entry['link'],
            'title': entry['title'],
            'author': entry['author'],
            'published': entry['published_parsed'],
            'updated': entry['updated_parsed'],
            'summary': entry['summary'],
        })
    result = {
        'news': news,
    }
    dump(result,
        open(f'api/v1/jt_news.json', mode='w', encoding='utf-8'),
        ensure_ascii=False,
        indent=2 if debug else None,
        separators=(',', ': ') if debug else (',', ':'))
