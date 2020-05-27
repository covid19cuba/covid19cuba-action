from json import dump
from feedparser import parse

URL_JT_MEDIUM_FEED = 'https://medium.com/feed/juventud-t%C3%A9cnica/tagged/covid19'


def generate(debug=False):
    feed = parse(URL_JT_MEDIUM_FEED)
    news = []
    for entry in feed.entries:
        summary = str(entry['summary'])
        index_summary = summary.rindex('<hr>')
        summary = summary[:index_summary]
        index_abstract = findnth(summary, '</p>', 2)
        abstract = summary[:index_abstract + 4]
        news.append({
            'id': entry['id'],
            'link': entry['link'],
            'title': entry['title'],
            'author': entry['author'],
            'published': entry['published_parsed'],
            'updated': entry['updated_parsed'],
            'summary': summary,
            'abstract': abstract,
        })
    result = {
        'news': news,
    }
    dump(result,
        open(f'api/v1/jt_news.json', mode='w', encoding='utf-8'),
        ensure_ascii=False,
        indent=2 if debug else None,
        separators=(',', ': ') if debug else (',', ':'))


def findnth(haystack, needle, n):
    parts= haystack.split(needle, n+1)
    if len(parts)<=n+1:
        return -1
    return len(haystack) - len(parts[-1]) - len(needle)
