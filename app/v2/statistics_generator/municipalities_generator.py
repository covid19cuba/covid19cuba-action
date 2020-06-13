from json import load, dump
from math import log10
from ...static.countries import countries
from ...static.province_codes import province_abbrs, province_codes
from ...static.municipality_codes import municipality_codes
from ...utils import *


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


def filter_by_municipalities(data, item):
    return item.get('provincia_detección') != data['province'] or item.get('municipio_detección') != data['municipality']


def dpa_municipality_code(data):
    return f"{data['mun_code']}"


def updated(data, json_file='data_cuba'):
    return updated_util(data, json_file)


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
        diagnosed = len(list(filter(\
            lambda a: a.get('provincia_detección') == data['province'] and
            a.get('municipio_detección') == data['municipality'], \
            days[i]['diagnosticados']))) \
            if 'diagnosticados' in days[i] else 0
        if diagnosed:
            break
        days_since_last_diagnosed += 1
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
    return result


def cases_by_sex(data, json_file='data_cuba', case_type='diagnosticados'):
    return cases_by_sex_util(data, json_file, case_type, filter_by_municipalities)


def cases_by_mode_of_contagion(data, json_file='data_cuba', case_type='diagnosticados'):
    return cases_by_mode_of_contagion_util(data, json_file, case_type, filter_by_municipalities)


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
                lambda a: a.get('provincia_detección') == data['province'] and
                a.get('municipio_detección') == data['municipality'],
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
    return distribution_by_age_ranges_util(data, json_file, case_type, filter_by_municipalities)


def cases_by_nationality(data, json_file='data_cuba', case_type='diagnosticados'):
    return cases_by_nationality_util(data, json_file, case_type, filter_by_municipalities)


def distribution_by_nationality_of_foreign_cases(data, json_file='data_cuba', case_type='diagnosticados'):
    return distribution_by_nationality_of_foreign_cases_util(data, json_file, case_type, filter_by_municipalities)

#Deceases section

def deceases_updated(data):
    return updated(data, json_file='data_deaths')


def deceases_evolution_by_days(data):
    return evolution_of_deaths_by_days_util(data, json_file='data_deaths', case_type='fallecidos', filter_func=filter_by_municipalities)


def deceases_by_sex(data):
    return cases_by_sex(data, json_file='data_deaths', case_type='fallecidos')


def deceases_distribution_by_age_ranges(data):
    return distribution_by_age_ranges(data, json_file='data_deaths', case_type='fallecidos')


def deceases_by_nationality(data):
    return cases_by_nationality(data, json_file='data_deaths', case_type='fallecidos')


def deceases_distribution_amount_disease_history(data):
    return deceases_distribution_amount_disease_history_util(data, filter_func=filter_by_municipalities)


def deceases_common_previous_diseases(data):
    return deceases_common_previous_diseases_util(data, filter_func=filter_by_municipalities)


