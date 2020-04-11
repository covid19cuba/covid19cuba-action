from json import dump, load
from jsonschema import Draft7Validator
from .schema import schema
from .municipality_codes import municipality_codes
from .province_codes import province_codes


def check():
    data = load(open('data/covid19-cuba.json', encoding='utf-8'))
    validator = Draft7Validator(schema)
    index = 1
    message_error = '\n'
    for error in sorted(validator.iter_errors(data), key=str):
        location = error.path
        try:
            keys = []
            loc = 0
            for i, value in enumerate(list(error.path)):
                keys.append(value)
                if value == 'diagnosticados':
                    loc = i + 1
                    break
            if loc < len(list(error.path)):
                loc = list(error.path)[loc]
            value = data
            for key in keys:
                value = value[key]
            location = f'Id: {value[loc]["id"]}'
        except:
            pass
        end = f', {error.path}' if location != error.path else ''
        message_error += '============================================\n'
        message_error += f'Error {index}:\n'
        message_error += f'Cause: {error.message}\n'
        message_error += f'Location: {location}{end}\n'
        message_error += '============================================\n'
        index += 1
    for message, path in check_provinces_and_municipalities(data):
        message_error += '============================================\n'
        message_error += f'Error {index}:\n'
        message_error += f'Cause: {message}\n'
        message_error += f'Location: {path}\n'
        message_error += '============================================\n'
        index += 1
    if index > 1:
        raise Exception(message_error)


def check_provinces_and_municipalities(data):
    for key in data['centros_aislamiento']:
        value = data['centros_aislamiento'][key]
        code = value['dpacode_provincia']
        actual = value['provincia']
        expected = province_codes.get(code)
        if actual != expected:
            message = f'Invalid "provincia" by "dpacode_provincia". ' + \
                f'Expected: {expected}, Found: {actual}.'
            path = f'Id: {key}, {["centros_aislamiento", key]}'
            yield message, path
    for key in data['centros_diagnostico']:
        value = data['centros_diagnostico'][key]
        code = value['dpacode_provincia']
        actual = value['provincia']
        expected = province_codes.get(code)
        if actual != expected:
            message = f'Invalid "provincia" by "dpacode_provincia". ' + \
                f'Expected: {expected}, Found: {actual}.'
            path = f'Id: {key}, {["centros_diagnostico", key]}'
            yield message, path
    for day in data['casos']['dias']:
        x = data['casos']['dias'][day]
        if 'diagnosticados' in x:
            diagnosed = x['diagnosticados']
            for i, value in enumerate(diagnosed):
                code = value['dpacode_provincia_deteccion']
                actual = value['provincia_detección']
                expected = province_codes.get(code)
                if actual != expected and \
                        (actual or expected != 'Desconocida'):
                    message = f'Invalid "provincia_detección" by ' + \
                        f'"dpacode_provincia_deteccion". ' + \
                        f'Expected: {expected}, Found: {actual}.'
                    path = f'Id: {value["id"]}, {["casos", "dias", day, "diagnosticados", i, value["id"]]}'
                    yield message, path
                code = value['dpacode_municipio_deteccion']
                actual = value['municipio_detección']
                expected = municipality_codes.get(code)
                if actual != expected and \
                        (actual or expected != 'Desconocido'):
                    message = f'Invalid "municipio_detección" by ' + \
                        f'"dpacode_municipio_deteccion". ' + \
                        f'Expected: {expected}, Found: {actual}.'
                    path = f'Id: {value["id"]}, {["casos", "dias", day, "diagnosticados", i, value["id"]]}'
                    yield message, path
