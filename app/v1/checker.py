from json import dump, load
from jsonschema import validate
from .schema import schema


def check():
    data = load(open('data/covid19-cuba.json', encoding='utf-8'))
    validate(data, schema)
    return True
