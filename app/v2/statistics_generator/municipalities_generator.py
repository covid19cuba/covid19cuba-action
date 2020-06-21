from json import load, dump
from math import log10
from ...static.countries import countries
from ...static.province_codes import province_abbrs, province_codes
from ...static.municipality_codes import municipality_codes
from ...utils import dump_util


def generate(debug=False):
    data_cuba = load(open('data/covid19-cuba.json', encoding='utf-8'))
    data_deaths = load(open('data/covid19-fallecidos.json', encoding='utf-8'))
    function_list = [
        dpa_municipality_code,
        updated,
        resume,
        cases_by_sex,
        cases_by_mode_of_contagion,
        evolution_of_cases_by_days,
        distribution_by_age_ranges,
        cases_by_nationality,
        distribution_by_nationality_of_foreign_cases,
        # Deceases section
        deceases_updated,
        deceases_resume,
        deceases_evolution_by_days,
        deceases_by_sex,
        deceases_distribution_by_age_ranges,
        deceases_by_nationality,
        deceases_distribution_amount_disease_history,
        deceases_common_previous_diseases,
    ]
    province_codes_r = {j: i for i, j in province_codes.items()}
    for key in province_abbrs:
        value = province_abbrs[key]
        dpa_code = province_codes_r[value]
        municipalities = [(key, key.split('.')[1])
                          for key in municipality_codes if key.startswith(dpa_code)]
        for full_code, mun_code in municipalities:
            mun_value = municipality_codes[full_code]
            dump({f.__name__: dump_util(f'api/v2/provinces/{key}/municipalities/{full_code}', f,
                                        data_cuba=data_cuba,
                                        data_deaths=data_deaths,
                                        province=value,
                                        municipality=mun_value,
                                        dpa_code=dpa_code,
                                        mun_code=mun_code,
                                        debug=debug)
                  for f in function_list},
                 open(f'api/v2/provinces/{key}/municipalities/{full_code}/all.json',
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
    days_since_last_diagnosed = 0
    for i in range(len(days) - 1, -1, -1):
        temp = len(list(filter(
            lambda a: a.get('provincia_detección') == data['province'] and
            a.get('municipio_detección') == data['municipality'],
            days[i]['diagnosticados']))) \
            if 'diagnosticados' in days[i] else 0
        if temp:
            break
        days_since_last_diagnosed += 1
    days = list(data['data_deaths']['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    days_since_last_deceased = 0
    for i in range(len(days) - 1, -1, -1):
        deaths = len(list(filter(
            lambda a: a.get('provincia_detección') == data['province'] and
            a.get('municipio_detección') == data['municipality'],
            days[i]['fallecidos']))) \
            if 'fallecidos' in days[i] else 0
        if deaths:
            break
        days_since_last_deceased += 1
    result = [
        {'name': 'Diagnosticados', 'value': diagnosed}
    ]
    if diagnosed:
        result.append({
            'name': 'Diagnosticados Nuevos',
            'value': new_diagnosed,
        })
        result.append({
            'name': 'Días Desde El Último Diagnosticado',
            'value': days_since_last_diagnosed,
        })
        result.append({
            'name': 'Días Desde El Último Fallecido',
            'value': days_since_last_deceased,
        })
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
        'no reportado': 'No Reportados',
    }
    hard = {
        'hombre': 'men',
        'mujer': 'women',
        'no reportado': 'unknown',
    }
    return {
        hard[key] if key in hard else key: {
            'name': pretty[key] if key in pretty else key.title(),
            'value': result[key],
        }
        for key in result
    }


def cases_by_mode_of_contagion(data):
    result = {
        'importado': 0,
        'introducido': 0,
        'autoctono': 0,
        'desconocido': 0,
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
        'desconocido': 'Desconocidos',
    }
    hard = {
        'importado': 'imported',
        'introducido': 'inserted',
        'autoctono': 'autochthonous',
        'desconocido': 'unknown',
    }
    return {
        hard[key] if key in hard else key: {
            'name': pretty[key] if key in pretty else key.title(),
            'value': result[key],
        }
        for key in result
    }


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
            'values': accumulated[1:],
        },
        'daily': {
            'name': 'Casos en el día',
            'values': daily[1:],
        },
        'date': {
            'name': 'Fecha',
            'values': date,
        },
    }


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
            else:
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


def cases_by_nationality(data):
    pretty = {
        'foreign': 'Extranjeros',
        'cubans': 'Cubanos',
        'unknown': 'No reportados',
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
            'value': result[key],
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
            'value': result[key],
        }
        for key in result
    ]

# Deceases section


def deceases_updated(data):
    days = list(data['data_deaths']['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    return days[-1]['fecha']


def deceases_resume(data):
    days = list(data['data_deaths']['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    new_deaths = len(list(filter(
        lambda a: a.get('provincia_detección') == data['province']
        and a.get('municipio_detección') == data['municipality'],
        days[-1]['fallecidos']))) if 'fallecidos' in days[-1] else 0
    deaths = sum((
        len(list(filter(
            lambda a: a.get('provincia_detección') == data['province'] and
            a.get('municipio_detección') == data['municipality'],
            x['fallecidos'])))
        for x in days
        if 'fallecidos' in x
    ))
    days_since_last_deceased = 0
    for i in range(len(days) - 1, -1, -1):
        temp = len(list(filter(
            lambda a: a.get('provincia_detección') == data['province'] and
            a.get('municipio_detección') == data['municipality'],
            days[i]['fallecidos']))) \
            if 'fallecidos' in days[i] else 0
        if temp:
            break
        days_since_last_deceased += 1
    result = [
        {'name': 'Fallecidos', 'value': deaths}
    ]
    if deaths:
        result.append({
            'name': 'Fallecidos Nuevos',
            'value': new_deaths,
        })
        result.append({
            'name': 'Días Desde El Último Fallecido',
            'value': days_since_last_deceased,
        })
    return result


def deceases_evolution_by_days(data):
    accumulated = [0]
    daily = [0]
    date = []
    days = list(data['data_deaths']['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    for x in days:
        accumulated.append(accumulated[-1])
        daily.append(0)
        if x.get('fallecidos'):
            temp = len(list(filter(
                lambda a: a.get('provincia_detección') == data['province'] and
                a.get('municipio_detección') == data['municipality'],
                x['fallecidos'])))
            accumulated[-1] += temp
            daily[-1] += temp

        date.append(x['fecha'])

    return {
        'accumulated': {
            'name': 'Fallecidos acumulados',
            'values': accumulated[1:],
        },
        'daily': {
            'name': 'Fallecidos en el día',
            'values': daily[1:],
        },
        'date': {
            'name': 'Fecha',
            'values': date,
        },
    }


def deceases_by_sex(data):
    result = {'hombre': 0, 'mujer': 0, 'no reportado': 0}
    days = list(data['data_deaths']['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    for diagnosed in (x['fallecidos'] for x in days if 'fallecidos' in x):
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
        'no reportado': 'No Reportados',
    }
    hard = {
        'hombre': 'men',
        'mujer': 'women',
        'no reportado': 'unknown',
    }
    return {
        hard[key] if key in hard else key: {
            'name': pretty[key] if key in pretty else key.title(),
            'value': result[key],
        }
        for key in result
    }


def deceases_distribution_by_age_ranges(data):
    keys = ['0-19', '20-39', '40-59', '60-79', '>=80', '--']
    hard = ['0-19', '20-39', '40-59', '60-79', '>=80', 'unknown']
    intervals = [[0, 19], [20, 39], [40, 59], [60, 79], [80, 2**10]]
    result = [0] * (len(intervals) + 1)
    men = [0] * (len(intervals) + 1)
    women = [0] * (len(intervals) + 1)
    unknown = [0] * (len(intervals) + 1)
    days = list(data['data_deaths']['casos']['dias'].values())
    for deaths in (x['fallecidos'] for x in days if 'fallecidos' in x):
        for item in deaths:
            if item.get('provincia_detección') != data['province'] or item.get('municipio_detección') != data['municipality']:
                continue
            age = item.get('edad')
            sex = item.get('sexo')
            sex_list = men if sex == 'hombre' else women if sex == 'mujer' else unknown
            if age is None:
                result[-1] += 1
                sex_list[-1] += 1
            else:
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


def deceases_by_nationality(data):
    pretty = {
        'foreign': 'Extranjeros',
        'cubans': 'Cubanos',
        'unknown': 'No reportados',
    }
    result = {'foreign': 0, 'cubans': 0, 'unknown': 0}
    days = list(data['data_deaths']['casos']['dias'].values())
    for deaths in (x['fallecidos'] for x in days if 'fallecidos' in x):
        for item in deaths:
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
            'value': result[key],
        }
        for key in result
    }


def deceases_distribution_amount_disease_history(data):
    result = {}
    days = list(data['data_deaths']['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    for deaths in (x['fallecidos'] for x in days if 'fallecidos' in x):
        for item in deaths:
            if item.get('provincia_detección') != data['province'] or item.get('municipio_detección') != data['municipality']:
                continue
            temp = item['enfermedades'] if 'enfermedades' in item else []
            try:
                result[len(temp)] += 1
            except KeyError:
                result[len(temp)] = 1
    return {
        str(key): {
            'name': 'Ninguna'
            if key == 0 else f'{key} Enfermedad'
                    if key == 1 else f'{key} Enfermedades',
            'value': result[key]
        }
        for key in result
    }


def deceases_common_previous_diseases(data):
    result = {}
    days = list(data['data_deaths']['casos']['dias'].values())
    for deaths in (x['fallecidos'] for x in days if 'fallecidos' in x):
        for item in deaths:
            for disease in item['enfermedades']:
                if item.get('provincia_detección') != data['province'] or item.get('municipio_detección') != data['municipality']:
                    continue
                try:
                    result[disease]['value'] += 1
                except KeyError:
                    result[disease] = {
                        'value': 1,
                        'code': disease,
                        'name': data['data_deaths']['enfermedades'][disease].title(),
                    }
    result_list = list(result.values())
    result_list.sort(key=lambda x: x['value'], reverse=True)
    return result_list[:8]
