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


def send_msg(messages, debug):
    group_messages = []
    for i in range(0, len(messages), 5):
        segment = messages[i : i + 5]
        if segment:
            group_messages.append(segment)
    messages = []
    for group in group_messages:
        message = ''
        for item in group:
            message += item
        messages.append(message)
    for message in messages:
        if debug:
            print(message)
        else:
            send(message)


class ExceptionGroup(Exception):
    def __init__(self, messages, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.messages = messages
