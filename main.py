from json import dump, load
from os import makedirs


def main():
    makedirs('data/mini', exist_ok=True)
    data = load(open('data/covid19-cuba.json'))
    dump(data, open('data/mini/covid19-cuba.json', 'w'))


if __name__ == "__main__":
    main()
