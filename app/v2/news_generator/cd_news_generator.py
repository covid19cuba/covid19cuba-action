from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from json import dump
from datetime import datetime
from hashlib import sha1
from ...utils import dump_util

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
}


def get_page(url):
    page = Request(url=url, headers=HEADERS)
    html = urlopen(page)
    bs = BeautifulSoup(html.read(), 'html.parser')
    return bs


def get_datetime(arg):
    try:
        _datetime = datetime.strptime(arg, '%Y-%m-%d %H:%M:%S')
        return [
            _datetime.year,
            _datetime.month,
            _datetime.day,
            _datetime.hour,
            _datetime.minute,
            _datetime.second
        ]
    except:
        pass
    return None


def get_info(article):
    abstract = article.find('div', {'class': 'excerpt'}).p.text
    link = article.find('a').attrs['href']
    page = get_page(link)
    title = page.find('h2', {'class': 'title'}).text
    author = page.find('div', {'id': 'taxonomies'}).find('a').text
    published = get_datetime(page.find('time').attrs['datetime'])
    summary = page.find('div', {'class': 'note_content'})
    return {
        'id': str(link),
        'link': str(link),
        'title': str(title),
        'author': str(author),
        'published': published,
        'updated': published,
        'summary': str(summary),
        'abstract': str(abstract),
        'source': 'Cubadebate',
    }


def generate(debug=False):
    url = 'http://www.cubadebate.cu/etiqueta/covid-19/'
    page = get_page(url)
    articles_list = page.find_all('div', {'class': 'spoiler'})
    news = []
    for article in articles_list:
        info = get_info(article)
        news.append(info)
    result = {
        'news': news,
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
