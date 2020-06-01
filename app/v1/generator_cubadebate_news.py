from json import dump
import datetime 
from download_comments import get_news


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
        # open(f'api/v1/cubadebate_news.json', mode='w', encoding='utf-8'),
        open(f'cubadebate_news.json', mode='w', encoding='utf-8'), 
        ensure_ascii=False,
        indent=2 if debug else None,
        separators=(',', ': ') if debug else (',', ':'))
    
generate()