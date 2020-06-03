from hashlib import sha1
from ...static.about_us import about_us as data_about_us
from ...static.changelog import changelog as data_changelog
from ...static.faqs import faqs as data_faqs
from ...static.tips import tips as data_tips
from ...utils import dump_util


def generate(debug=False):
    build_about_us(debug)
    build_changelog(debug)
    build_faqs(debug)
    build_tips(debug)


def build_about_us(debug):
    dump_util('api/v2', about_us, debug=debug)
    build_about_us_state(debug)


def about_us(_):
    return data_about_us


def build_about_us_state(debug):
    dump_util('api/v2', about_us_state, debug=debug)


def about_us_state(data):
    result = {
        'cache': None,
    }
    with open('api/v2/about_us.json', encoding='utf-8') as file:
        text = file.read()
        cache = sha1(text.encode())
        result['cache'] = cache.hexdigest()
    return result


def build_changelog(debug):
    dump_util('api/v2', changelog, debug=debug)
    build_changelog_state(debug)


def changelog(_):
    return data_changelog


def build_changelog_state(debug):
    dump_util('api/v2', changelog_state, debug=debug)


def changelog_state(data):
    result = {
        'cache': None,
    }
    with open('api/v2/changelog.json', encoding='utf-8') as file:
        text = file.read()
        cache = sha1(text.encode())
        result['cache'] = cache.hexdigest()
    return result


def build_faqs(debug):
    dump_util('api/v2', faqs, debug=debug)
    build_faqs_state(debug)


def faqs(_):
    return data_faqs


def build_faqs_state(debug):
    dump_util('api/v2', faqs_state, debug=debug)


def faqs_state(data):
    result = {
        'cache': None,
    }
    with open('api/v2/faqs.json', encoding='utf-8') as file:
        text = file.read()
        cache = sha1(text.encode())
        result['cache'] = cache.hexdigest()
    return result


def build_tips(debug):
    dump_util('api/v2', tips, debug=debug)
    build_tips_state(debug)


def tips(_):
    return data_tips


def build_tips_state(debug):
    dump_util('api/v2', tips_state, debug=debug)


def tips_state(data):
    result = {
        'cache': None,
    }
    with open('api/v2/tips.json', encoding='utf-8') as file:
        text = file.read()
        cache = sha1(text.encode())
        result['cache'] = cache.hexdigest()
    return result
