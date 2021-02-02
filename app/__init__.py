from .utils import send_msg
from .v1 import run as v1run
from .v2 import run as v2run


def run(debug=False):
    print("Running generator v1 ...")
    ok = v1run(debug)
    print(f"Api v1 generated: {ok}")
    print("Running generator v2 ...")
    ok = v2run(debug) and ok
    print(f"Api v2 generated {ok}")
    if ok:
        send_msg(["GitHub Action run successfully."], debug)
