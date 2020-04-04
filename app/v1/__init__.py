from .checker import check
from .mimificator import mimificate


def run():
    if check():
        mimificate()
