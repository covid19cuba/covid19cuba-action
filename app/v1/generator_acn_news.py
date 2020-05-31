#http://www.acn.cu/busqueda?searchword=covid&ordering=newest&searchphrase=all&limit=0&areas[0]=categories&areas[1]=content&areas[2]=tags

from json import dump
import requests
from bs4 import BeautifulSoup
from os import path
from feedparser import parse

URL_ACN = 'http://www.acn.cu/busqueda?searchword=covid&ordering=newest&searchphrase=all&limit=0&areas[0]=categories&areas[1]=content&areas[2]=tags'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}

payload = {
    'query':'test'
}


def Extract_href(element):
    index = element.find('href="')
    element = element[index+len('href="'):]
    element = element[:element.find('">')]    
    return element

def remove_junk(string):
    new_str = ''
    flag = False
    for i in string:
        if i == '<':
            flag = True
        if not flag:
            new_str = new_str+i
        if i == '>':
            flag = False
    new_str = new_str.split('\t')
    string = ''
    for i in new_str:
        string=string+i
    new_str = string.split('\n')
    string = ''
    for i in new_str:
        string=string+i
    new_str = string.split('\t')
    string = ''
    for i in new_str:
        string=string+i
    return string 

def clean_date(string):
    string = string[string.find('content="')+len('content="'):]
    return string[:string.find('"')]

def generate(debug=False):
    news = []
    r = requests.get(URL_ACN,data = payload ,headers = headers)

    soup = BeautifulSoup(r.text,'lxml')
    titles = soup.findAll('dt', {'class':'result-title'})
    abstracts = soup.findAll('dd', {'class':'result-text'})
    news_links = [Extract_href(str(i)) for i in titles]
    
    for i,item in enumerate(news_links):
        
        link ='http://www.acn.cu'+item
        r = requests.get(link,data = payload ,headers = headers)
        
        soup = BeautifulSoup(r.text,'lxml')
        title = str(soup.find('h1', {'class':'article-title'}))
        author = str(soup.find('dd', {'class':'createdby hasTooltip'}))
        created = str(soup.find('meta', {'itemprop':'datePublished'}))
        updated = str(soup.find('meta', {'itemprop':'dateModified'}))
        abstract = str(abstracts[i])
        summary = str(soup.find('section', {'class':'article-content'}))
        news.append({
            'id': link,
            'link': link,
            'title': remove_junk(title),
            'author': remove_junk(author),
            'published': clean_date(created),
            'updated': clean_date(updated),
            'summary': remove_junk(summary),
            'abstract':remove_junk(abstract),
        })
    
    result = {
        'news': news,
    }

    dump(result,
        open(f'api/v1/acn_news.json', mode='w', encoding='utf-8'),
        # open(f'acn_news.json', mode='w', encoding='utf-8'),
        
        ensure_ascii=False,
        indent=2 if debug else None,
        separators=(',', ': ') if debug else (',', ':'))



def findnth(haystack, needle, n):
    parts= haystack.split(needle, n+1)
    if len(parts)<=n+1:
        return -1
    return len(haystack) - len(parts[-1]) - len(needle)
