from json import load
from jsonschema import Draft7Validator
from .schema import schema
from .municipality_codes import municipality_codes
from .province_codes import province_codes
from .utils import send_msg


def check(debug=False):
    data = load(open('data/covid19-cuba.json', encoding='utf-8'))
    validator = Draft7Validator(schema)
    index_error = 1
    index_warning = 1
    message_error = '\n'
    message_warning = '\n'
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
        message_error += f'Error {index_error}:\n'
        message_error += f'Cause: {error.message}\n'
        message_error += f'Location: {location}{end}\n'
        message_error += '============================================\n'
        index_error += 1
    for message, path in check_errors(data):
        message_error += '============================================\n'
        message_error += f'Error {index_error}:\n'
        message_error += f'Cause: {message}\n'
        message_error += f'Location: {path}\n'
        message_error += '============================================\n'
        index_error += 1
    for message, path in check_warnings(data):
        message_warning += '============================================\n'
        message_warning += f'Warning {index_warning}:\n'
        message_warning += f'Cause: {message}\n'
        message_warning += f'Location: {path}\n'
        message_warning += '============================================\n'
        index_warning += 1
    if index_warning > 1:
        send_msg(message_warning, debug)
    if index_error > 1:
        raise Exception(message_error)
    return index_error == 1 and index_warning == 1


def check_errors(data):
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
                check_province = _check_province_match(i, value, day)
                if check_province:
                    yield check_province

                check_municipality = _check_municipality_match(i, value, day)
                if check_municipality:
                    yield check_municipality

                check_municipality_province_codes = _check_municipality_province_codes_match(i, value, day)
                if check_municipality_province_codes:
                    yield check_municipality_province_codes


def check_warnings(data):
    for day in data['casos']['dias']:
        x = data['casos']['dias'][day]
        if 'diagnosticados' in x:
            diagnosed = x['diagnosticados']
            for i, value in enumerate(diagnosed):
                check_sex = _check_sex_match(i, value, day)
                if check_sex:
                    yield check_sex


def _check_sex_match(i, value, day):
    sex = value['sexo']
    if not value.get('info'):
        return
    expected_sex = value['info'].strip().split(' ')[0].lower()
    if expected_sex == 'ciudadano':
        expected_sex = 'hombre'
    elif expected_sex == 'ciudadana':
        expected_sex = 'mujer'
    else:
        return
    if sex != expected_sex:
        message = f'Invalid "sex". ' + \
                  f'Expected: {expected_sex}, Found: {sex}.'
        path = f'Id: {value["id"]}, {["casos", "dias", day, "diagnosticados", i, value["id"]]}'
        return message, path


def _check_province_match(i, value, day):
    province_code = value['dpacode_provincia_deteccion']
    province = value['provincia_detección']
    expected_province_code = province_codes.get(province_code)
    if province != expected_province_code and \
            (province or expected_province_code != 'Desconocida'):
        message = f'Invalid "provincia_detección" by ' + \
                  f'"dpacode_provincia_deteccion". ' + \
                  f'Expected: {expected_province_code}, Found: {province}.'
        path = f'Id: {value["id"]}, {["casos", "dias", day, "diagnosticados", i, value["id"]]}'
        return message, path


def _check_municipality_match(i, value, day):
    municipality_code = value['dpacode_municipio_deteccion']
    municipality = value['municipio_detección']
    expected_municipality_code = municipality_codes.get(municipality_code)
    if municipality != expected_municipality_code and \
            (municipality or expected_municipality_code != 'Desconocido'):
        message = f'Invalid "municipio_detección" by ' + \
                  f'"dpacode_municipio_deteccion". ' + \
                  f'Expected: {expected_municipality_code}, Found: {municipality}.'
        path = f'Id: {value["id"]}, {["casos", "dias", day, "diagnosticados", i, value["id"]]}'
        return message, path


def _check_municipality_province_codes_match(i, value, day):
    province_code = value['dpacode_provincia_deteccion']
    municipality_code = value['dpacode_municipio_deteccion']
    match = True
    if municipality_code:
        if province_code != municipality_code.split('.')[0] and \
            (municipality_code and province_code != '40.01'):
            match = False
    elif province_codes == '40.01':
        match = False
    if not match:
        message = f'Province and municipality codes mismatch. ' + \
                  f'Expected: {province_code} == {municipality_code.split(".")[0]}.'
        path = f'Id: {value["id"]}, {["casos", "dias", day, "diagnosticados", i, value["id"]]}'
        return message, path
