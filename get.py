from json import dump
from os import makedirs
from requests import get

data_cuba_url = 'https://covid19cubadata.github.io/data/covid19-cuba.json'
data_cuba = get(data_cuba_url)

data_deaths_url = 'https://covid19cubadata.github.io/data/covid19-fallecidos.json'
data_deaths = get(data_deaths_url)

data_world_url = 'https://covid19cubadata.github.io/data/paises-info-dias.json'
data_world = get(data_world_url)

data_oxford_url = 'https://covid19cubadata.github.io/data/oxford-indexes.json'
data_oxford = get(data_oxford_url)

data_protocols_url = 'https://covid19cubadata.github.io/data/protocols.json'
data_protocols = get(data_protocols_url)

makedirs('data', exist_ok=True)

with open('data/covid19-cuba.json', mode='w', encoding='utf-8') as file:
    file.write(data_cuba.text)

with open('data/covid19-fallecidos.json', mode='w', encoding='utf-8') as file:
    file.write(data_deaths.text)

with open('data/paises-info-dias.json', mode='w', encoding='utf-8') as file:
    file.write(data_world.text)

with open('data/oxford-indexes.json', mode='w', encoding='utf-8') as file:
    file.write(data_oxford.text)

with open('data/protocols.json', mode='w', encoding='utf-8') as file:
    file.write(data_protocols.text)
