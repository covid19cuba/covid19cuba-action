from json import dump, load, loads
from hashlib import sha1
from os import listdir, makedirs, path
from .checker import check
from .generator import generate
from .generator_municipalities import generate as generate_municipalities
from .generator_news import generate as generate_news
from .generator_provinces import generate as generate_provinces
from ..static.about_us import about_us as data_about_us
from ..static.app_version import APP_VERSION_CODE
from ..static.changelog import changelog as data_changelog
from ..static.tips import tips as data_tips
from ..utils import dump_util, send_msg


def run(debug=False):
    try:
        makedirs('api/v2', exist_ok=True)
        ok = check(debug)
        # generate(debug)
        # generate_provinces(debug)
        # generate_municipalities(debug)
        generate_news(debug)
        build_about_us(debug)
        build_changelog(debug)
        build_tips(debug)
        # build_full('api/v2', debug)
        # build_state(debug)
        if ok:
            return True
    except Exception as e:
        send_msg(e, debug)
        if debug:
            raise e
    return False


def build_state(debug):
    dump_util('api/v2', state, debug=debug)


def state(data):
    result = {
        'version': APP_VERSION_CODE,
        'cache': None,
        'days': 0
    }
    with open('api/v2/full.json', encoding='utf-8') as file:
        text = file.read()
        cache = sha1(text.encode())
        data = loads(text)
        days = len(data['all']['evolution_of_cases_by_days']['accumulated']['values'])
        result['cache'] = cache.hexdigest()
        result['days'] = days
    return result


def build_about_us(debug):
    dump_util('api/v2', about_us, debug=debug)


def about_us(_):
    return data_about_us


def build_changelog(debug):
    dump_util('api/v2', changelog, debug=debug)


def changelog(_):
    return data_changelog


def build_tips(debug):
    dump_util('api/v2', tips, debug= debug)


def tips(_):
    return data_tips


def build_full(base_path, debug):
    subdirs = [ name for name in listdir(base_path) if path.isdir(path.join(base_path, name)) ]
    all_data = None
    try:
        with open(path.join(base_path, 'all.json'), encoding='utf-8') as file:
            all_data = load(file)
    except FileNotFoundError:
        pass
    full_data = dict()
    for subdir in subdirs:
        subdir_full_data = build_full(path.join(base_path, subdir), debug)
        if len(list(subdir_full_data.keys())):
            full_data[subdir] = subdir_full_data
    if all_data:
        full_data['all'] = all_data
        if len(subdirs):
            with open(path.join(base_path, 'full.json'), mode='w', encoding='utf-8') as file:
                dump(full_data, file,
                    ensure_ascii=False,
                    indent=2 if debug else None,
                    separators=(',', ': ') if debug else (',', ':'))
    return full_data
