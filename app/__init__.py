from .v1 import run as v1run
from .utils import send_msg


def run(debug=False):
    ok = v1run(debug)
    if ok:
        send_msg('GitHub Action run successfully.', debug)
