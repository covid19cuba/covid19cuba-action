from ...static.about_us import about_us as data_about_us
from ...static.changelog import changelog as data_changelog
from ...static.tips import tips as data_tips
from ...utils import dump_util


def generate(debug=False):
    build_about_us(debug)
    build_changelog(debug)
    build_tips(debug)


def build_about_us(debug):
    dump_util('api/v2', about_us, debug=debug)


def about_us(_):
    return data_about_us


def build_changelog(debug):
    dump_util('api/v2', changelog, debug=debug)


def changelog(_):
    return data_changelog


def build_tips(debug):
    dump_util('api/v2', tips, debug=debug)


def tips(_):
    return data_tips
