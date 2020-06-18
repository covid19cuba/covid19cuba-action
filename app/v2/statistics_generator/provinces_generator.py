from json import load, dump
from math import log10
from ...static.countries import countries
from ...static.province_codes import province_abbrs, province_codes
from ...static.provinces_population import provinces_population
from ...utils import *


def generate(debug=False):
    data_cuba = load(open('data/covid19-cuba.json', encoding='utf-8'))
    data_deaths = load(open('data/covid19-fallecidos.json', encoding='utf-8'))
    function_list = [
        dpa_province_code,
        updated,
        resume,
        map_data,
        cases_by_sex,
        cases_by_mode_of_contagion,
        evolution_of_cases_by_days,
        distribution_by_age_ranges,
        cases_by_nationality,
        distribution_by_nationality_of_foreign_cases,
        effective_reproductive_number,
        affected_municipalities,
        # Deceases section
        deceases_updated,
        deceases_map_data,
        deceases_evolution_by_days,
        deceases_by_sex,
        deceases_distribution_by_age_ranges,
        deceases_by_nationality,
        deceases_distribution_amount_disease_history,
        deceases_common_previous_diseases,
        deceases_affected_municipalities,
    ]
    province_codes_r = {j: i for i, j in province_codes.items()}
    for key in province_abbrs:
        value = province_abbrs[key]
        dpa_code = province_codes_r[value]
        dump({f.__name__: dump_util(f'api/v2/provinces/{key}', f,
                                    data_cuba=data_cuba,
                                    data_deaths=data_deaths,
                                    province=value,
                                    dpa_code=dpa_code,
                                    debug=debug)
              for f in function_list},
             open(f'api/v2/provinces/{key}/all.json',
                  mode='w', encoding='utf-8'),
             ensure_ascii=False,
             indent=2 if debug else None,
             separators=(',', ': ') if debug else (',', ':'))


def filter_by_provinces(data, item):
    return item.get('provincia_detección') != data['province']


def dpa_province_code(data):
    return data['dpa_code']


def updated(data, json_file='data_cuba'):
    return updated_util(data, json_file)


def resume(data):
    days = list(data['data_cuba']['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    new_diagnosed = len(list(filter(
        lambda a: a.get('provincia_detección') == data['province'],
        days[-1]['diagnosticados']))) if 'diagnosticados' in days[-1] else 0
    diagnosed = sum((
        len(list(filter(
            lambda a: a.get('provincia_detección') == data['province'],
            x['diagnosticados'])))
        for x in days
        if 'diagnosticados' in x
    ))
    last15days = 0
    for i in range(len(days) - 1, max(len(days) - 16, -1), -1):
        diagnosed = len(list(filter(\
            lambda a: a.get('provincia_detección') == data['province'], \
            days[i]['diagnosticados']))) \
            if 'diagnosticados' in days[i] else 0
        last15days += diagnosed
    last15days = last15days * 10**5 / provinces_population[data['dpa_code']] \
        if data['dpa_code'] in provinces_population else 0
    days_since_last_diagnosed = 0
    for i in range(len(days) - 1, -1, -1):
        diagnosed = len(list(filter(\
            lambda a: a.get('provincia_detección') == data['province'], \
            days[i]['diagnosticados']))) \
            if 'diagnosticados' in days[i] else 0
        if diagnosed:
            break
        days_since_last_diagnosed += 1
    return [
        {
            'name': 'Diagnosticados',
            'value': diagnosed,
        },
        {
            'name': 'Diagnosticados Nuevos',
            'value': new_diagnosed,
        },
        {
            'name': 'Tasa (por 100 mil) Últimos 15 Días',
            'value': last15days,
        },
        {
            'name': 'Días Desde El Último Diagnosticado',
            'value': days_since_last_diagnosed,
        },
    ]


def map_data(data, json_file='data_cuba', case_type='diagnosticados'):
    muns = {}
    p_code = data['dpa_code']
    days = list(data[json_file]['casos']['dias'].values())
    cases = [x[case_type] for x in days if case_type in x]
    for patients in cases:
        for p in filter(lambda x: x['dpacode_provincia_deteccion'] == p_code, patients):
            try:
                muns[p['dpacode_municipio_deteccion']] += 1
            except KeyError:
                muns[p['dpacode_municipio_deteccion']] = 1
    total = 0
    max_muns = 0
    for key in muns:
        if key and muns[key] > max_muns:
            max_muns = muns[key]
        if key:
            total += muns[key]
    return {
        'muns': muns,
        'genInfo': {
            'max_muns': max_muns,
            'total': total,
        },
    }


def cases_by_sex(data, json_file='data_cuba', case_type='diagnosticados'):
    cases_by_sex_util(data, json_file, case_type, filter_by_provinces)


def cases_by_mode_of_contagion(data, json_file='data_cuba', case_type='diagnosticados'):
    return cases_by_mode_of_contagion_util(data, json_file, case_type, filter_by_provinces)


def evolution_of_cases_by_days(data, json_file='data_cuba', case_type='diagnosticados'):
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
                lambda a: a.get('provincia_detección') == data['province'],
                x[case_type])))
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


def distribution_by_age_ranges(data, json_file='data_cuba', case_type='diagnosticados'):
    return distribution_by_age_ranges_util(data, json_file, case_type, filter_by_provinces)


def cases_by_nationality(data, json_file='data_cuba', case_type='diagnosticados'):
    return cases_by_nationality_util(data, json_file, case_type, filter_by_provinces)


def distribution_by_nationality_of_foreign_cases(data, json_file='data_cuba', case_type='diagnosticados'):
    return distribution_by_nationality_of_foreign_cases_util(data, json_file, case_type, filter_by_provinces)


def effective_reproductive_number(data):
    if not data['dpa_code'] in data['data_cuba']['numero-reproductivo']:
        return None
    data_prov = data['data_cuba']['numero-reproductivo'][data['dpa_code']]
    return effective_reproductive_number_util(data=data_prov)


def affected_municipalities(data, json_file='data_cuba', case_type='diagnosticados'):
    return affected_municipalities_util(data, json_file, case_type, filter_by_provinces)

#Deceases section

def deceases_updated(data):
    return updated(data, json_file='data_deaths')


def deceases_map_data(data):
    return map_data(data, json_file='data_deaths', case_type='fallecidos')


def deceases_evolution_by_days(data):
    return evolution_of_deaths_by_days_util(data, json_file='data_deaths', case_type='fallecidos', filter_func=filter_by_provinces)


def deceases_by_sex(data):
    return cases_by_sex(data, json_file='data_deaths')


def deceases_distribution_by_age_ranges(data):
    return distribution_by_age_ranges(data, json_file='data_deaths', case_type='fallecidos')


def deceases_by_nationality(data):
    return cases_by_nationality(data, json_file='data_deaths', case_type='fallecidos')


def deceases_distribution_amount_disease_history(data):
    return deceases_distribution_amount_disease_history_util(data, filter_func=filter_by_provinces)


def deceases_common_previous_diseases(data):
    return deceases_common_previous_diseases_util(data, filter_func=filter_by_provinces)


def deceases_affected_municipalities(data):
    return affected_municipalities(data, json_file='data_deaths', case_type='fallecidos')

