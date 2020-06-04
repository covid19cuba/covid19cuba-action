import json
from json import dump
import datetime 
import requests
from datetime import date, timedelta
import parsel
from parsel import Selector
import os
from typing import List


def get_other_pages(html: Selector) -> List[str]:
    
    return html.css('.page::attr(href)').getall()


def get_news_page(html: Selector):
    for div in html.css('#archive > div.generic'):
        a = div.css('.title > a')

        yield {
            'tags': [tag for tag in div.attrib['class'].split(' ') if tag and tag != 'generic' ],
            'title': a.css('::text').get(),
            'link': a.css('::attr(href)').get()   
        }


def get_news_info(html: Selector):
    summary = ''.join(html.css('div.entry > div.note_content > p::text').getall()).strip()
    updated = ''
    author = '' 
    
    return {
        'summary' : summary,
        'abstract': ' '.join(summary.split(' ')[:min(120,len(summary.split(' ')))]),
        'updated' : '',
        'author' : author
    }
 
BASE_URL = 'http://www.cubadebate.cu'


def generate_urls(from_date: date, to_date: date):

    current_date = from_date

    while not current_date > to_date:

        yield {'link': f'{BASE_URL}/{current_date.year}/{current_date.month}/{current_date.day}', 'date': current_date}

        current_date += timedelta(days=1)


def proccess_links(links, recursive: bool = False):

    for link in links:
        date = str(link['date'])
        link = link['link']
        id = link

        response = requests.get(link)

        html = Selector(response.text)
        for page in get_news_page(html):
            page['published'] = date
            yield page

        if recursive:
            for other in get_other_pages(html):
                for page in proccess_links(other):
                    yield page

def process_new(news):

    for new in news:
        response = requests.get(new['link'])
        html = Selector(response.text)

        data = get_news_info(html)
        new.update(data)

        yield new


def get_news(from_date: date, to_date: date, folder='artícles') -> dict:
    return process_new(proccess_links(generate_urls(from_date, to_date)))


def find_match(new,keywords:str='covid'):
    for i in new['tags']:
        if type(i) == str and not i.lower().find(keywords) == -1:
            return True
    if not new['title'].lower().find(keywords) == -1 or not new['summary'].lower().find(keywords) == -1:
        return True
    return False

def generate(debug=False):
    

    json_file = []
    for new in get_news(datetime.datetime.now() - datetime.timedelta(5), datetime.datetime.now()):
        if find_match(new):
            new['id'] = new['link']
            json_file.append(new)
    
    result = {
        'news':json_file
    }
    dump(result,
        open(f'api/v2/cubadebate_news.json', mode='w', encoding='utf-8'),
        #open(f'cubadebate_news.json', mode='w', encoding='utf-8'), 
        ensure_ascii=False,
        indent=2 if debug else None,
        separators=(',', ': ') if debug else (',', ':'))
