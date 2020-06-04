from datetime import datetime, timedelta
from json import dump
from parsel import Selector
from requests import get
from hashlib import sha1
from ...utils import dump_util

BASE_URL = 'http://www.cubadebate.cu'


def get_other_pages(html):
    return html.css('.page::attr(href)').getall()


def get_news_page(html):
    for div in html.css('#archive > div.generic'):
        a = div.css('.title > a')
        yield {
            'tags': [
                tag for tag in div.attrib['class'].split(' ')
                if tag and tag != 'generic'
            ],
            'title': a.css('::text').get(),
            'link': a.css('::attr(href)').get(),
            'id': a.css('::attr(href)').get(),
        }


def get_news_info(html):
    summary = ''.join(
        html.css('div.entry > div.note_content > p').getall()).strip()
    index_abstract = findnth(summary, '</p>', 2)
    abstract = summary[:index_abstract + 4]
    author = None
    return {
        'summary': summary,
        'abstract': abstract,
        'author': author,
    }


def generate_urls(from_date, to_date):
    current = from_date
    while current <= to_date:
        yield {
            'link': f'{BASE_URL}/{current.year}/{current.month}/{current.day}',
            'date': current,
        }
        current += timedelta(days=1)


def proccess_links(links):
    for link in links:
        published = str(link['date'])
        published = datetime.strptime(published, '%Y-%m-%d %H:%M:%S.%f')
        published = [
            published.year,
            published.month,
            published.day,
            published.hour,
            published.minute,
            published.second
        ]
        link = link['link']
        response = get(link)
        html = Selector(response.text)
        for page in get_news_page(html):
            page['published'] = published
            page['updated'] = published
            yield page


def process_new(news):
    for new in news:
        response = get(new['link'])
        html = Selector(response.text)
        data = get_news_info(html)
        new.update(data)
        yield new


def get_news(from_date, to_date, folder='artícles') -> dict:
    return process_new(proccess_links(generate_urls(from_date, to_date)))


def find_match(new, keywords: str = 'covid'):
    for i in new['tags']:
        if type(i) == str and not i.lower().find(keywords) == -1:
            return True
    if not new['title'].lower().find(keywords) == -1 or not new['summary'].lower().find(keywords) == -1:
        return True
    return False


def generate(debug=False):
    news = []
    for new in get_news(datetime.now() - timedelta(5), datetime.now()):
        if find_match(new):
            del new['tags']
            new['source'] = 'Cubadebate'
            news.append(new)
    result = {
        'news': news
    }
    dump(result,
         open(f'api/v2/cd_news.json', mode='w', encoding='utf-8'),
         ensure_ascii=False,
         indent=2 if debug else None,
         separators=(',', ': ') if debug else (',', ':'))
    build_cd_news_state(debug)
    return news


def build_cd_news_state(debug):
    dump_util('api/v2', cd_news_state, debug=debug)


def cd_news_state(data):
    result = {
        'cache': None,
    }
    with open('api/v2/cd_news.json', encoding='utf-8') as file:
        text = file.read()
        cache = sha1(text.encode())
        result['cache'] = cache.hexdigest()
    return result


def findnth(haystack, needle, n):
    parts = haystack.split(needle, n+1)
    if len(parts) <= n+1:
        return -1
    return len(haystack) - len(parts[-1]) - len(needle)
