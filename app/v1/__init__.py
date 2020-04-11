from .checker import check
from .generator import generate
from .generator_provinces import generate as generate_provinces
from ..send_message import send


def run(debug=False):
    try:
        check()
        generate(debug)
        generate_provinces(debug)
        send_msg('GitHub Action run successfully.', debug)
    except Exception as e:
        send_msg(e, debug)


def send_msg(message, debug):
    message = str(message)
    if debug:
        print(message)
    else:
        send(message)
