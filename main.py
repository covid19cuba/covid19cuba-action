from json import dump, load
from os import makedirs
from jsonschema import validate


def check():
    data = load(open('data/covid19-cuba.json', encoding="utf-8"))
    schema = load(open('schema.json', encoding="utf-8"))
    validate(data, schema)
    return True


def mimificate():
    makedirs('data/mini', exist_ok=True)
    data = load(open('data/covid19-cuba.json', encoding='utf-8'))
    dump(data, open('data/mini/covid19-cuba.json', mode='w', encoding='utf-8'))


if __name__ == "__main__":
    if check():
        mimificate()
