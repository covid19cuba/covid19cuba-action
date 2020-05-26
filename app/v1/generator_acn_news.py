#http://www.acn.cu/busqueda?searchword=covid&ordering=newest&searchphrase=all&limit=0&areas[0]=categories&areas[1]=content&areas[2]=tags

from json import dump
# from feedparser import parse
import requests
from bs4 import BeautifulSoup
from os import path

URL_ACN = 'http://www.acn.cu/busqueda?searchword=covid&ordering=newest&searchphrase=all&limit=0&areas[0]=categories&areas[1]=content&areas[2]=tags'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}

payload = {
    'query':'test'
}


def Extract_href(elements):
    new_list = []
    for item in elements:
        temp_list = str(item).split(" ")
        for i in temp_list:
            if i[:4] == 'href':
                new_list.append(i[6:-1])
    return new_list

def generate(debug=False):
    feed = parse(URL_ACN)
    news = []
    r = requests.get(URL_ACN,data = payload ,headers = headers)
    
    soup = BeautifulSoup(r.text,'lxml')
    title = soup.findAll('dt', {'class':'result-title'})
    category = soup.findAll('dd', {'class':'result-category'})
    created = soup.findAll('dd', {'class':'result-created'})
    summary = soup.findAll('dd', {'class':'result-text'})
    
    links = []
    # print(items)
    print(summary)
    for i in range(len(title)):
        news.append({
            'title':str(title[i]),
            #'link':links[i],
            'abstract':str(category[i]), # not shure
            'published':str(created[i]),
            'summary':str(summary[i])
            #falta id, author y updated
            })

    result = {
        'news': news,
    }
    
    dump(result,
        open(f'acn_news.json', mode='w', encoding='utf-8'),
        ensure_ascii=False,
        indent=2 if debug else None,
        separators=(',', ': ') if debug else (',', ':'))

    
    # dump(result,
    #     open(f'api/v1/acn_news.json', mode='w', encoding='utf-8'),
    #     ensure_ascii=False,
    #     indent=2 if debug else None,
    #     separators=(',', ': ') if debug else (',', ':'))


def findnth(haystack, needle, n):
    parts= haystack.split(needle, n+1)
    if len(parts)<=n+1:
        return -1
    return len(haystack) - len(parts[-1]) - len(needle)

generate()