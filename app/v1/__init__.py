from .checker import check
from .generator import generate
from ..send_message import send


def run(debug=False):
    try:
        check()
        generate(debug)
        send_msg('GitHub Action run successfully.', debug)
    except Exception as e:
        send_msg(e, debug)


def send_msg(message, debug):
    message = str(message)
    if debug:
        print(message)
    else:
        send(message)
