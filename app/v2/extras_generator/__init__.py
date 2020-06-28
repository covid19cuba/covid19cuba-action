from hashlib import sha1
from ...static.about_us import about_us as data_about_us
from ...static.downloads import downloads as data_downloads
from ...static.changelog import changelog as data_changelog
from ...static.faqs import faqs as data_faqs
from ...static.tips import tips as data_tips
from ...utils import dump_util
from .bulletins_generator import generate as generate_bulletins
from .protocols_generator import generate as generate_protocols


def generate(debug=False):
    build_about_us(debug)
    build_bulletins(debug)
    build_changelog(debug)
    build_downloads(debug)
    build_faqs(debug)
    build_protocols(debug)
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


def build_bulletins(debug):
    dump_util('api/v2', bulletins, debug=debug)
    build_bulletins_state(debug)


def bulletins(data):
    return generate_bulletins(debug=data['debug'])


def build_bulletins_state(debug):
    dump_util('api/v2', bulletins_state, debug=debug)


def bulletins_state(data):
    result = {
        'cache': None,
    }
    with open('api/v2/bulletins.json', encoding='utf-8') as file:
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


def build_downloads(debug):
    dump_util('api/v2', downloads, debug=debug)
    build_downloads_state(debug)


def downloads(_):
    return data_downloads


def build_downloads_state(debug):
    dump_util('api/v2', downloads_state, debug=debug)


def downloads_state(data):
    result = {
        'cache': None,
    }
    with open('api/v2/downloads.json', encoding='utf-8') as file:
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


def build_protocols(debug):
    dump_util('api/v2', protocols, debug=debug)
    build_protocols_state(debug)


def protocols(data):
    return generate_protocols(debug=data['debug'])


def build_protocols_state(debug):
    dump_util('api/v2', protocols_state, debug=debug)


def protocols_state(data):
    result = {
        'cache': None,
    }
    with open('api/v2/protocols.json', encoding='utf-8') as file:
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
