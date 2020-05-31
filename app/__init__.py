from .v1 import run as v1run
from .v2 import run as v2run
from .utils import send_msg


def run(debug=False):
    ok = v1run(debug)
    ok = ok and v2run(debug)
    if ok:
        send_msg('GitHub Action run successfully.', debug)
