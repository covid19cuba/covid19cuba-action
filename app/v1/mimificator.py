from json import dump, load
from os import makedirs


def mimificate():
    makedirs('api/v1', exist_ok=True)
    data = load(open('data/covid19-cuba.json', encoding='utf-8'))
    dump(data, open('api/v1/covid19-cuba.json', mode='w', encoding='utf-8'))
