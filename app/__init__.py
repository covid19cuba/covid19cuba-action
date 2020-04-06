from os import makedirs
from .v1 import run as v1run

APP_VERSION_CODE = 6


def run(debug=False):
    main_run()
    v1run(debug)


def main_run():
    makedirs('api', exist_ok=True)
    with open('api/app_version_code.json', mode='w') as file:
        file.write(str(APP_VERSION_CODE))
