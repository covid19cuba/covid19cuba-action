from json import dump
from os import makedirs
from .send_message import send


def dump_util(path, func, **data):
    makedirs(path, exist_ok=True)
    result = func(data)
    dump(result,
         open(f'{path}/{func.__name__}.json', mode='w', encoding='utf-8'),
         ensure_ascii=False,
         indent=2 if data.get('debug') else None,
         separators=(',', ': ') if data.get('debug') else (',', ':'))
    return result


def send_msg(message, debug):
    message = str(message)
    if debug:
        print(message)
    else:
        send(message)
