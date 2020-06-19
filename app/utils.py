from json import dump
from os import makedirs
from .send_message import send
from .static.countries import countries


def dump_util(path, func, **data):
    makedirs(path, exist_ok=True)
    result = func(data)
    dump(result,
         open(f'{path}/{func.__name__}.json', mode='w', encoding='utf-8'),
         ensure_ascii=False,
         indent=2 if data.get('debug') else None,
         separators=(',', ': ') if data.get('debug') else (',', ':'))
    return result


def updated_util(data, json_file: str):
    days = list(data[json_file]['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    return days[-1]['fecha']

def cases_by_sex_util(data, json_file: str, case_type: str, filter_func) -> dict:
    result = {'hombre': 0, 'mujer': 0, 'no reportado': 0}
    days = list(data[json_file]['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    for cases in (x[case_type] for x in days if case_type in x):
        for item in cases:
            if filter_func(data, item):
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


def cases_by_mode_of_contagion_util(data, json_file: str, case_type: str, filter_func) -> dict:
    result = {
        'importado': 0,
        'introducido': 0,
        'autoctono': 0,
        'desconocido': 0,
    }
    days = list(data[json_file]['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    for cases in (x[case_type] for x in days if case_type in x):
        for item in cases:
            if filter_func(data, item):
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


def evolution_of_deaths_by_days_util(data, json_file: str, case_type: str, filter_func) -> dict:
    accumulated = [0]
    daily = [0]
    date = []
    days = list(data[json_file]['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    for x in days:
        accumulated.append(accumulated[-1])
        daily.append(0)
        if x.get(case_type):
            temp = len(list(filter(
                lambda a: not filter_func(data, a),
                x[case_type])))
            accumulated[-1] += temp
            daily[-1] += temp
        date.append(x['fecha'])
    return {
        'accumulated': {
            'name': 'Fallecimientos acumulados',
            'values': accumulated[1:],
        },
        'daily': {
            'name': 'Fallecimientos en el día',
            'values': daily[1:],
        },
        'date': {
            'name': 'Fecha',
            'values': date,
        }
    }


def distribution_by_age_ranges_util(data, json_file: str, case_type: str, filter_func) -> list:
    keys = ['0-19', '20-39', '40-59', '60-79', '>=80', '--']
    hard = ['0-19', '20-39', '40-59', '60-79', '>=80', 'unknown']
    intervals = [[0, 19], [20, 39], [40, 59], [60, 79], [80, 2**10]]
    result = [0] * (len(intervals) + 1)
    men = [0] * (len(intervals) + 1)
    women = [0] * (len(intervals) + 1)
    unknown = [0] * (len(intervals) + 1)
    days = list(data[json_file]['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    for cases in (x[case_type] for x in days if case_type in x):
        for item in cases:
            if filter_func(data, item):
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


def cases_by_nationality_util(data, json_file: str, case_type: str, filter_func) -> dict:
    pretty = {
        'foreign': 'Extranjeros',
        'cubans': 'Cubanos',
        'unknown': 'No reportados',
    }
    result = {'foreign': 0, 'cubans': 0, 'unknown': 0}
    days = list(data[json_file]['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    for cases in (x[case_type] for x in days if case_type in x):
        for item in cases:
            if filter_func(data, item):
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

def distribution_by_nationality_of_foreign_cases_util(data, json_file: str, case_type: str, filter_func) -> list:
    result = {}
    days = list(data[json_file]['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    for cases in (x[case_type] for x in days if case_type in x):
        for item in cases:
            if filter_func(data, item):
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


def effective_reproductive_number_util(data) -> dict:
    dates = []
    for item in data['dates']:
        dates.append(f'2020/{item}')
    data['dates'] = dates
    return {
        'upper': {
            'name': 'Margen Superior',
            'values': data['upper'],
        },
        'value': {
            'name': 'Número Reproductivo Efectivo',
            'values': data['value'],
        },
        'lower': {
            'name': 'Margen Inferior',
            'values': data['lower'],
        },
        'date': {
            'name': 'Fecha',
            'values': data['dates'],
        },
    }


def affected_municipalities_util(data, json_file: str, case_type: str, filter_func, truncate=False) -> list:
    counter = {}
    total = 0
    days = list(data[json_file]['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    for cases in (x[case_type] for x in days if case_type in x):
        for item in cases:
            if filter_func(data, item):
                continue
            dpacode = 'dpacode_municipio_deteccion'
            try:
                counter[item[dpacode]]['value'] += 1
                counter[item[dpacode]]['name'] = item['municipio_detección']
                counter[item[dpacode]]['province'] = item['provincia_detección']
            except KeyError:
                counter[item[dpacode]] = {
                    'value': 1,
                    'name': item['municipio_detección'],
                    'province': item['provincia_detección'],
                }
            total += 1
    result = []
    result_list = list(counter.values())
    result_list.sort(key=lambda x: x['value'], reverse=True)
    if truncate:
        result_list = result_list[:10]
    for item in result_list:
        item['total'] = total
        result.append(item)
    return result


def deceases_distribution_amount_disease_history_util(data, filter_func) -> dict:
    result = {}
    days = list(data['data_deaths']['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    for cases in (x['fallecidos'] for x in days if 'fallecidos' in x):
        for item in cases:
            if filter_func(data, item):
                continue
            temp = item['enfermedades'] if 'enfermedades' in item else []
            try:
                result[len(temp)] += 1
            except KeyError:
                result[len(temp)] = 1

    return {
        str(key): {
            'name': 'Ninguna' \
                if key == 0 else f'{key} Enfermedad' \
                    if key == 1 else f'{key} Enfermedades',
            'value': result[key]
        }
        for key in result
    }


def deceases_common_previous_diseases_util(data, filter_func) -> list:
    result = {}
    days = list(data['data_deaths']['casos']['dias'].values())
    for cases in (x['fallecidos'] for x in days if 'fallecidos' in x):
        for item in cases:
            for disease in item['enfermedades']:
                if filter_func(data, disease):
                    continue
                try:
                    result[disease]['value'] += 1
                except KeyError:
                    result[disease] = {
                        'value': 1,
                        'name' : data['data_deaths']['enfermedades'][disease].title(),
                    }
    
    result_list = list(result.values())
    result_list.sort(key=lambda x: x['value'], reverse=True)
    return result_list


def send_msg(message, debug):
    message = str(message)
    if debug:
        print(message)
    else:
        send(message)
