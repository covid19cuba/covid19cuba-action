import requests
from datetime import date, timedelta
from parsers import get_news_page, get_other_pages, get_comments, get_news_info
from parsel import Selector
import logging
import json
import os

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



def get_comments_links(html: Selector, recursive: bool = False):

    last = html.css('a.last::attr(href)').get()

    ans = get_comments(html)

    if last and recursive:
        num = int(last.split('#')[0].split('-')[-1])
        partial = '-'.join(last.split('#')[0].split('-')[:-1])
        links = [f'{partial}{i}' for i in range(1, num+1)]

        for link in links:
            response = requests.get(link)
            html = Selector(response.text)
            comments = get_comments(html)

            ans.extend(comments)

    return ans


def process_new(news):

    for new in news:
        response = requests.get(new['link'])
        html = Selector(response.text)

        data = get_news_info(html)
        new.update(data)

        yield new


def get_news(from_date: date, to_date: date, folder='artícles') -> dict:
    return process_new(proccess_links(generate_urls(from_date, to_date)))

