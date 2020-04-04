from json import dump, load
from jsonschema import validate


def check():
    data = load(open('data/covid19-cuba.json', encoding='utf-8'))
    schema = load(open('app/v1/schema.json', encoding='utf-8'))
    validate(data, schema)
    return True
