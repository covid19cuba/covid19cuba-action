from hashlib import sha1
from .checker import check
from .generator import generate
from .generator_provinces import generate as generate_provinces
from .generator_municipality import generate as generate_municipality
from .utils import dump_util
from ..send_message import send
from .changelog import changelog as data_changelog

APP_VERSION_CODE = 8
 

def run(debug=False):
    try:
        check()
        generate(debug)
        generate_provinces(debug)
        generate_municipality(debug)
        build_state(debug)
        build_changelog(debug)
        send_msg('GitHub Action run successfully.', debug)
    except Exception as e:
        send_msg(e, debug)


def build_state(debug):
    dump_util('api/v1', state, debug=debug)


def state(data):
    result = {
        'version': APP_VERSION_CODE,
        'cache': None
    }
    with open('api/v1/all.json', encoding='utf-8') as file:
        text = file.read()
        cache = sha1(text.encode())
        result['cache'] = cache.hexdigest()
    return result


def build_changelog(debug):
    dump_util('api/v1', changelog, debug=debug)


def changelog(data):
    result = data_changelog
    return result


def send_msg(message, debug):
    message = str(message)
    if debug:
        print(message)
    else:
        send(message)
