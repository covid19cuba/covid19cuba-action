from bs4 import BeautifulSoup
from requests import get
from urllib import request


def bulletins(debug = False, base_url = 'https://covid19cubadata.github.io/'):
    result = []
    source = get(f'{base_url}boletines').text
    soup = BeautifulSoup(source, 'html.parser')
    for elem in soup.findAll('a'):
        description = elem.text
        link = elem.get('href')
        number = description[description.find('No.') + 4]
        size = int(request.urlopen(base_url + link).info()['Content-Length'])/10**6
        result.append({
            'id': number,
            'info': description,
            'url': link,
            'size': size})

    _bulletins.sort(key= lambda x : x['id'])

    data = { 
        'providers': 
        [ 
            {
                'name': 'CEDEM',
                'url': 'http://www.biblioteca.uh.cu/red-bibliotecas/centro-estudios-demograficos-cedem',
                'data_source': base_url,
                'bulletins': _bulletins 
            } 
        ]
    }

    return data
    
