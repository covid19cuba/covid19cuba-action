from json import load, dump
from math import log10
from ..static.countries import countries
from ..static.province_codes import province_abbrs, province_codes
from ..static.municipality_codes import municipality_codes
from ..utils import dump_util


def generate(debug=False):
    data_cuba = load(open('data/covid19-cuba.json', encoding='utf-8'))
    function_list = [
        updated,
        resume,
        cases_by_sex,
        cases_by_mode_of_contagion,
        cases_by_nationality,
        distribution_by_nationality_of_foreign_cases,
        distribution_by_age_ranges,
        evolution_of_cases_by_days,
        dpa_municipality_code,
    ]
    province_codes_r = {j: i for i, j in province_codes.items()}
    for key in province_abbrs:
        value = province_abbrs[key]
        dpa_code = province_codes_r[value]
        municipalities = [(key, key.split('.')[1])
                          for key in municipality_codes if key.startswith(dpa_code)]
        for full_code, mun_code in municipalities:
            mun_value = municipality_codes[full_code]
            dump({f.__name__: dump_util(f'api/v1/provinces/{key}/municipalities/{full_code}', f,
                                        data_cuba=data_cuba, province=value,
                                        debug=debug, dpa_code=dpa_code, mun_code=mun_code,
                                        municipality=mun_value)
                  for f in function_list},
                 open(f'api/v1/provinces/{key}/municipalities/{full_code}/all.json',
                      mode='w', encoding='utf-8'),
                 ensure_ascii=False,
                 indent=2 if debug else None,
                 separators=(',', ': ') if debug else (',', ':'))


def dpa_municipality_code(data):
    return f"{data['mun_code']}"


def updated(data):
    days = list(data['data_cuba']['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    return days[-1]['fecha']


def resume(data):
    days = list(data['data_cuba']['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    new_diagnosed = len(list(filter(
        lambda a: a.get('provincia_detección') == data['province']
        and a.get('municipio_detección') == data['municipality'],
        days[-1]['diagnosticados']))) if 'diagnosticados' in days[-1] else 0
    diagnosed = sum((
        len(list(filter(
            lambda a: a.get('provincia_detección') == data['province'] and
            a.get('municipio_detección') == data['municipality'],
            x['diagnosticados'])))
        for x in days
        if 'diagnosticados' in x
    ))
    result = [
        {'name': 'Diagnosticados', 'value': diagnosed}
    ]
    if diagnosed:
        result.append({'name': 'Diagnosticados Nuevos', 'value': new_diagnosed})
    return result


def cases_by_sex(data):
    result = {'hombre': 0, 'mujer': 0, 'no reportado': 0}
    days = list(data['data_cuba']['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    for diagnosed in (x['diagnosticados'] for x in days if 'diagnosticados' in x):
        for item in diagnosed:
            if item.get('provincia_detección') != data['province'] or item.get('municipio_detección') != data['municipality']:
                continue
            if item.get('sexo') is None:
                result['no reportado'] += 1
            else:
                try:
                    result[item.get('sexo')] += 1
                except KeyError:
                    result[item.get('sexo')] = 1
    pretty = {
        'hombre': 'Hombres',
        'mujer': 'Mujeres',
        'no reportado': 'No Reportados'
    }
    hard = {
        'hombre': 'men',
        'mujer': 'women',
        'no reportado': 'unknown'
    }
    return {
        hard[key] if key in hard else key: {
            'name': pretty[key] if key in pretty else key.title(),
            'value': result[key]
        }
        for key in result
    }


def cases_by_mode_of_contagion(data):
    result = {
        'importado': 0,
        'introducido': 0,
        'autoctono': 0,
        'desconocido': 0
    }
    days = list(data['data_cuba']['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    for diagnosed in (x['diagnosticados'] for x in days if 'diagnosticados' in x):
        for item in diagnosed:
            if item.get('provincia_detección') != data['province'] or item.get('municipio_detección') != data['municipality']:
                continue
            if item.get('contagio') is None:
                result['desconocido'] += 1
            else:
                try:
                    result[item.get('contagio')] += 1
                except KeyError:
                    result[item.get('contagio')] = 1
    pretty = {
        'importado': 'Importados',
        'introducido': 'Introducidos',
        'autoctono': 'Autóctonos',
        'desconocido': 'Desconocidos'
    }
    hard = {
        'importado': 'imported',
        'introducido': 'inserted',
        'autoctono': 'autochthonous',
        'desconocido': 'unknown'
    }
    return {
        hard[key] if key in hard else key: {
            'name': pretty[key] if key in pretty else key.title(),
            'value': result[key]
        }
        for key in result
    }


def cases_by_nationality(data):
    pretty = {
        'foreign': 'Extranjeros',
        'cubans': 'Cubanos',
        'unknown': 'No reportados'
    }
    result = {'foreign': 0, 'cubans': 0, 'unknown': 0}
    days = list(data['data_cuba']['casos']['dias'].values())
    for diagnosed in (x['diagnosticados'] for x in days if 'diagnosticados' in x):
        for item in diagnosed:
            if item.get('provincia_detección') != data['province'] or item.get('municipio_detección') != data['municipality']:
                continue
            country = item.get('pais')
            if country is None:
                result['unknown'] += 1
            elif country == 'cu':
                result['cubans'] += 1
            else:
                result['foreign'] += 1
    return {
        key: {
            'name': pretty[key] if key in pretty else key.title(),
            'value': result[key]
        }
        for key in result
    }


def distribution_by_nationality_of_foreign_cases(data):
    result = {}
    days = list(data['data_cuba']['casos']['dias'].values())
    for diagnosed in (x['diagnosticados'] for x in days if 'diagnosticados' in x):
        for item in diagnosed:
            if item.get('provincia_detección') != data['province'] or item.get('municipio_detección') != data['municipality']:
                continue
            country = item['pais']
            if country == 'cu':
                continue
            try:
                result[country] += 1
            except KeyError:
                result[country] = 1
    return [
        {
            'code': key,
            'name': countries[key] if key in countries else key.title(),
            'value': result[key]
        }
        for key in result
    ]


def distribution_by_age_ranges(data):
    keys = ['0-19', '20-39', '40-59', '60-79', '>=80', '--']
    hard = ['0-19', '20-39', '40-59', '60-79', '>=80', 'unknown']
    intervals = [[0, 19], [20, 39], [40, 59], [60, 79], [80, 2**10]]
    result = [0] * (len(intervals) + 1)
    men = [0] * (len(intervals) + 1)
    women = [0] * (len(intervals) + 1)
    unknown = [0] * (len(intervals) + 1)
    days = list(data['data_cuba']['casos']['dias'].values())
    for diagnosed in (x['diagnosticados'] for x in days if 'diagnosticados' in x):
        for item in diagnosed:
            if item.get('provincia_detección') != data['province'] or item.get('municipio_detección') != data['municipality']:
                continue
            age = item.get('edad')
            sex = item.get('sexo')
            sex_list = men if sex == 'hombre' else women if sex == 'mujer' else unknown
            if age is None:
                result[-1] += 1
                sex_list[-1] += 1
            for index, (left, right) in enumerate(intervals):
                if left <= age <= right:
                    result[index] += 1
                    sex_list[index] += 1
                    break
    return [
        {
            'code': item[0],
            'name': item[1],
            'value': item[2],
            'men': item[3],
            'women': item[4],
            'unknown': item[5],
        }
        for item in zip(hard, keys, result, men, women, unknown)
    ]


def evolution_of_cases_by_days(data):
    accumulated = [0]
    daily = [0]
    date = []
    days = list(data['data_cuba']['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    for x in days:
        accumulated.append(accumulated[-1])
        daily.append(0)
        if x.get('diagnosticados'):
            temp = len(list(filter(
                lambda a: a.get('provincia_detección') == data['province'] and
                a.get('municipio_detección') == data['municipality'],
                x['diagnosticados'])))
            accumulated[-1] += temp
            daily[-1] += temp
        date.append(x['fecha'])
    return {
        'accumulated': {
            'name': 'Casos acumulados',
            'values': accumulated[1:]
        },
        'daily': {
            'name': 'Casos en el día',
            'values': daily[1:]
        },
        'date': {
            'name': 'Fecha',
            'values': date
        }
    }
