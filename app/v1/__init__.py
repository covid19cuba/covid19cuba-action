from hashlib import sha1
from .checker import check
from .generator import generate
from .generator_provinces import generate as generate_provinces
from .generator_municipality import generate as generate_municipality
from .utils import dump_util
from ..send_message import send

APP_VERSION_CODE = 6


def run(debug=False):
    try:
        check()
        generate(debug)
        generate_provinces(debug)
        generate_municipality(debug)
        build_state(debug)    
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


def send_msg(message, debug):
    message = str(message)
    if debug:
        print(message)
    else:
        send(message)
