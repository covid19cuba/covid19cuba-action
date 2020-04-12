from json import load, dump
from math import log10
from .countries import countries
from .province_codes import province_abbrs, province_codes
from .utils import dump_util


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
        affected_municipalities,
        dpa_province_code
    ]
    province_codes_r = {j:i for i,j in province_codes.items()}
    for key in province_abbrs:
        value = province_abbrs[key]
        dpa_code = province_codes_r[value]
        dump({f.__name__: dump_util(f'api/v1/provinces/{key}', f,
                                    data_cuba=data_cuba, province=value,
                                    debug=debug, dpa_code=dpa_code)
              for f in function_list},
             open(f'api/v1/provinces/{key}/all.json',
                  mode='w', encoding='utf-8'),
             ensure_ascii=False,
             indent=2 if debug else None,
             separators=(',', ': ') if debug else (',', ':'))

def dpa_province_code(data):
    return data['dpa_code']

def updated(data):
    days = list(data['data_cuba']['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    return days[-1]['fecha']


def resume(data):
    days = list(data['data_cuba']['casos']['dias'].values())
    diagnosed = sum((
        len(list(filter(
            lambda a: a.get('provincia_detección') == data['province'],
            x['diagnosticados'])))
        for x in days
        if 'diagnosticados' in x
    ))
    return [
        {'name': 'Diagnosticados', 'value': diagnosed},
    ]


def cases_by_sex(data):
    result = {'hombre': 0, 'mujer': 0, 'no reportado': 0}
    days = list(data['data_cuba']['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    for diagnosed in (x['diagnosticados'] for x in days if 'diagnosticados' in x):
        for item in diagnosed:
            if item.get('provincia_detección') != data['province']:
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
            if item.get('provincia_detección') != data['province']:
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
            if item.get('provincia_detección') != data['province']:
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
            if item.get('provincia_detección') != data['province']:
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
    result = [0] * 5
    keys = ['0-18', '19-40', '41-60', '>=61', 'Desconocido']
    hard = ['0-18', '19-40', '41-60', '>=61', 'unknown']
    days = list(data['data_cuba']['casos']['dias'].values())
    for diagnosed in (x['diagnosticados'] for x in days if 'diagnosticados' in x):
        for item in diagnosed:
            if item.get('provincia_detección') != data['province']:
                continue
            age = item.get('edad')
            if age is None:
                result[4] += 1
            elif 0 <= age <= 18:
                result[0] += 1
            elif 18 < age <= 40:
                result[1] += 1
            elif 40 < age <= 60:
                result[2] += 1
            else:
                result[3] += 1
    return [
        {'code': item[0], 'name': item[1][0], 'value': item[1][1]}
        for item in zip(hard, zip(keys, result))
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
                lambda a: a.get('provincia_detección') == data['province'],
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


def affected_municipalities(data):
    counter = {}
    total = 0
    days = list(data['data_cuba']['casos']['dias'].values())
    diagnosed = [x['diagnosticados'] for x in days if 'diagnosticados' in x]
    for patients in diagnosed:
        for p in patients:
            if p.get('provincia_detección') != data['province']:
                continue
            dpacode = 'dpacode_municipio_deteccion'
            try:
                counter[p[dpacode]]['value'] += 1
                counter[p[dpacode]]['name'] = p['municipio_detección']
            except KeyError:
                counter[p[dpacode]] = {
                    'value': 1,
                    'name': p['municipio_detección']
                }
            total += 1
    result = []
    result_list = list(counter.values())
    result_list.sort(key=lambda x: x['value'], reverse=True)
    for item in result_list:
        item['total'] = total
        result.append(item)
    return result
