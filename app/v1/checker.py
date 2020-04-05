from json import dump, load
from jsonschema import validate
from .schema import schema
from .municipality_codes import municipality_codes
from .province_codes import province_codes


def check():
    data = load(open('data/covid19-cuba.json', encoding='utf-8'))
    validate(data, schema)
    check_provinces_and_municipalities(data)
    return True


def check_provinces_and_municipalities(data):
    for key in data['centros_aislamiento']:
        value = data['centros_aislamiento'][key]
        code = value['dpacode_provincia']
        actual = value['provincia']
        expected = province_codes.get(code)
        if actual != expected:
            message = f'Expected: {expected}, Found: {actual}.'
            message = f'Invalid "provincia" by "dpacode_provincia". {message}'
            message = f'{message} Id: {key}'
            raise Exception(message)
    for key in data['centros_diagnostico']:
        value = data['centros_diagnostico'][key]
        code = value['dpacode_provincia']
        actual = value['provincia']
        expected = province_codes.get(code)
        if actual != expected:
            message = f'Invalid "provincia" by "dpacode_provincia". ' + \
                f'Expected: {expected}, Found: {actual}. ' + \
                f'Id: {key}'
            raise Exception(message)
    days = list(data['casos']['dias'].values())
    for diagnosed in (x['diagnosticados'] for x in days if 'diagnosticados' in x):
        for value in diagnosed:
            code = value['dpacode_provincia_deteccion']
            actual = value['provincia_detección']
            expected = province_codes.get(code)
            if actual != expected and \
                    (actual or expected != 'Desconocida'):
                message = f'Invalid "provincia_detección" by' + \
                    f'"dpacode_provincia_deteccion". ' + \
                    f'Expected: {expected}, Found: {actual}. ' + \
                    f'Id: {value["id"]}'
                raise Exception(message)
            code = value['dpacode_municipio_deteccion']
            actual = value['municipio_detección']
            expected = municipality_codes.get(code)
            if actual != expected and \
                    (actual or expected != 'Desconocido'):
                message = f'Invalid "municipio_detección" by ' + \
                    f'"dpacode_municipio_deteccion". ' + \
                    f'Expected: {expected}, Found: {actual}. ' + \
                    f'Id: {value["id"]}'
                raise Exception(message)
