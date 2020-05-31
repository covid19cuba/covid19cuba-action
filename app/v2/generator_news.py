from json import dump
from functools import cmp_to_key
from hashlib import sha1
from .generator_acn_news import generate as generate_acn_news
from .generator_gob_news import generate as generate_gob_news
from .generator_jt_news import generate as generate_jt_news
from ..utils import dump_util


def generate(debug=False):
    acn_news = generate_acn_news(debug)
    gob_news = generate_gob_news(debug)
    jt_news = generate_jt_news(debug)
    news = acn_news + gob_news + jt_news
    news.sort(key=cmp_to_key(comparator), reverse=True)
    result = {
        'news': news,
    }
    dump(result,
        open(f'api/v2/news.json', mode='w', encoding='utf-8'),
        ensure_ascii=False,
        indent=2 if debug else None,
        separators=(',', ': ') if debug else (',', ':'))
    build_news_state(debug)


def build_news_state(debug):
    dump_util('api/v2', news_state, debug=debug)


def news_state(data):
    result = {
        'cache': None,
    }
    with open('api/v2/news.json', encoding='utf-8') as file:
        text = file.read()
        cache = sha1(text.encode())
        result['cache'] = cache.hexdigest()
    return result


def comparator(a, b):
    for i in range(min(len(a['updated']), len(b['updated']))):
        if a['updated'][i] == b['updated'][i]:
            continue
        return a['updated'][i] - b['updated'][i]
    return 0
