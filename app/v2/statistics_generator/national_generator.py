from json import load, dump
from math import log10
from ...static.countries import countries, countries_codes, trans_countries, countries_iso3Code
from ...static.cuba_population import CUBA_POPULATION
from ...static.moments import moments
from ...static.provinces_population import provinces_population
from ...utils import dump_util


def generate(debug=False):
    data_cuba = load(open('data/covid19-cuba.json', encoding='utf-8'))
    data_deaths = load(open('data/covid19-fallecidos.json', encoding='utf-8'))
    data_world = load(open('data/paises-info-dias.json', encoding='utf-8'))
    data_oxford = load(open('data/oxford-indexes.json', encoding='utf-8'))
    function_list = [
        updated,
        # National
        resume,
        note,
        map_data,
        events,
        cases_by_sex,
        cases_by_mode_of_contagion,
        evolution_of_cases_by_days,
        evolution_of_recovered_by_days,
        evolution_of_deaths_by_days,
        distribution_of_cases,
        evolution_of_cases_and_recovered_by_days,
        evolution_of_active_and_recovered_accumulated,
        distribution_by_age_ranges,
        cases_by_nationality,
        distribution_by_nationality_of_foreign_cases,
        relation_of_tests_performed,
        tests_by_days,
        percent_positive_tests,
        critics_serious_evolution,
        percent_critics_serious_to_actives,
        effective_reproductive_number,
        stringency_index_cuba,
        affected_provinces,
        affected_municipalities,
        # World
        multiple_comparison_of_cuba_with_radar,
        curves_comparison,
        test_behavior_comparison,
        curves_evolution,
        world_countries,
        # Extra
        pesquisador,
    ]
    dump({
        f.__name__: dump_util('api/v2', f,
                              data_cuba=data_cuba,
                              data_deaths=data_deaths,
                              data_world=data_world,
                              data_oxford=data_oxford,
                              debug=debug)
        for f in function_list},
        open(f'api/v2/all.json', mode='w', encoding='utf-8'),
        ensure_ascii=False,
        indent=2 if debug else None,
        separators=(',', ': ') if debug else (',', ':'))


def updated(data):
    days = list(data['data_cuba']['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    return days[-1]['fecha']

# National

def resume(data):
    days = list(data['data_cuba']['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    diagnosed = sum((
        len(x['diagnosticados'])
        for x in days
        if 'diagnosticados' in x
    ))
    deaths = sum((
        x['muertes_numero']
        for x in days
        if 'muertes_numero' in x
    ))
    evacuees = sum((
        x['evacuados_numero']
        for x in days
        if 'evacuados_numero' in x
    ))
    recovered = sum((
        x['recuperados_numero']
        for x in days
        if 'recuperados_numero' in x
    ))
    active = diagnosed - deaths - evacuees - recovered
    new_diagnosed = len(days[-1]['diagnosticados']) \
        if 'diagnosticados' in days[-1] else 0
    new_recovered = days[-1]['recuperados_numero'] \
        if 'recuperados_numero' in days[-1] else 0
    new_deaths = days[-1]['muertes_numero'] \
        if 'muertes_numero' in days[-1] else 0
    new_evacuees = days[-1]['evacuados_numero'] \
        if 'evacuados_numero' in days[-1] else 0
    last15days = 0
    for i in range(len(days) - 1, max(len(days) - 16, -1), -1):
        diagnosed = len(days[i]['diagnosticados']) \
            if 'diagnosticados' in days[i] else 0
        last15days += diagnosed
    last15days = last15days * 10**5 / CUBA_POPULATION
    days_since_last_diagnosed = 0
    for i in range(len(days) - 1, -1, -1):
        if 'diagnosticados' in days[i] and len(days[i]['diagnosticados']) != 0:
            break
        days_since_last_diagnosed += 1
    days_since_last_deceased = 0
    for i in range(len(days) - 1, -1, -1):
        if 'muertes_numero' in days[i] and days[i]['muertes_numero'] != 0:
            break
        days_since_last_deceased += 1
    result = [
        {
            'name': 'Diagnosticados',
            'value': diagnosed,
        },
        {
            'name': 'Activos',
            'value': active,
        },
        {
            'name': 'Recuperados',
            'value': recovered,
        },
        {
            'name': 'Evacuados',
            'value': evacuees,
        },
        {
            'name': 'Fallecidos',
            'value': deaths,
        },
        {
            'name': 'Diagnosticados Nuevos',
            'value': new_diagnosed,
        },
        {
            'name': 'Recuperados Nuevos',
            'value': new_recovered,
        },
        {
            'name': 'Fallecidos Nuevos',
            'value': new_deaths,
        },
        {
            'name': 'Tasa (por 100 mil) Últimos 15 Días',
            'value': last15days,
        },
        {
            'name': 'Días Desde El Último Diagnosticado',
            'value': days_since_last_diagnosed,
        },
        {
            'name': 'Días Desde El Último Fallecido',
            'value': days_since_last_deceased,
        },
    ]
    if new_evacuees:
        result.append({'name': 'Evacuados Nuevos', 'value': new_evacuees})
    return result


def note(data):
    return data['data_cuba']['note-text'] if 'note-text' in data['data_cuba'] else ''


def map_data(data):
    muns = {}
    pros = {}
    days = list(data['data_cuba']['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    diagnosed = [x['diagnosticados'] for x in days if 'diagnosticados' in x]
    for patients in diagnosed:
        for p in patients:
            try:
                muns[p['dpacode_municipio_deteccion']] += 1
            except KeyError:
                muns[p['dpacode_municipio_deteccion']] = 1
            try:
                pros[p['dpacode_provincia_deteccion']] += 1
            except KeyError:
                pros[p['dpacode_provincia_deteccion']] = 1
    total = 0
    max_muns = 0
    max_pros = 0
    for key in muns:
        if key and muns[key] > max_muns:
            max_muns = muns[key]
    for key in pros:
        if key and pros[key] > max_muns:
            max_pros = pros[key]
        if key:
            total += pros[key]
    return {
        'muns': muns,
        'pros': pros,
        'genInfo': {
            'max_muns': max_muns,
            'max_pros': max_pros,
            'total': total,
        }
    }


def events(data):
    return data['data_cuba']['eventos']


def cases_by_sex(data):
    result = {'hombre': 0, 'mujer': 0, 'no reportado': 0}
    days = list(data['data_cuba']['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    for diagnosed in (x['diagnosticados'] for x in days if 'diagnosticados' in x):
        for item in diagnosed:
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
            'value': result[key]
        }
        for key in result
    }


def evolution_of_cases_by_days(data):
    accumulated = [0]
    daily = [0]
    date = []
    actives = []
    total = 0
    deaths = 0
    recover = 0
    evacuees = 0
    days = list(data['data_cuba']['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    for x in days:
        accumulated.append(accumulated[-1])
        daily.append(0)
        if x.get('diagnosticados'):
            accumulated[-1] += len(x['diagnosticados'])
            daily[-1] += len(x['diagnosticados'])
        total += len(x['diagnosticados']) if 'diagnosticados' in x else 0
        deaths += x['muertes_numero'] if 'muertes_numero' in x else 0
        recover += x['recuperados_numero'] if 'recuperados_numero' in x else 0
        evacuees += x['evacuados_numero'] if 'evacuados_numero' in x else 0
        actives.append(total - deaths - recover - evacuees)
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
        'active': {
            'name': 'Casos activos',
            'values': actives,
        },
        'date': {
            'name': 'Fecha',
            'values': date,
        }
    }


def evolution_of_recovered_by_days(data):
    accumulated = [0]
    daily = [0]
    date = []
    days = list(data['data_cuba']['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    for x in days:
        accumulated.append(accumulated[-1])
        daily.append(0)
        if x.get('recuperados_numero'):
            accumulated[-1] += x['recuperados_numero']
            daily[-1] += x['recuperados_numero']
        date.append(x['fecha'])
    return {
        'accumulated': {
            'name': 'Altas acumuladas',
            'values': accumulated[1:],
        },
        'daily': {
            'name': 'Altas en el día',
            'values': daily[1:],
        },
        'date': {
            'name': 'Fecha',
            'values': date,
        }
    }


def evolution_of_deaths_by_days(data):
    accumulated = [0]
    daily = [0]
    date = []
    days = list(data['data_cuba']['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    for x in days:
        accumulated.append(accumulated[-1])
        daily.append(0)
        if x.get('muertes_numero'):
            accumulated[-1] += x['muertes_numero']
            daily[-1] += x['muertes_numero']
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


def distribution_of_cases(data):
    days = list(data['data_cuba']['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    cases = sum((
        len(x['diagnosticados'])
        for x in days
        if 'diagnosticados' in x
    ))
    deaths = sum((
        x['muertes_numero']
        for x in days
        if 'muertes_numero' in x
    ))
    evacuees = sum((
        x['evacuados_numero']
        for x in days
        if 'evacuados_numero' in x
    ))
    recovered = sum((
        x['recuperados_numero']
        for x in days
        if 'recuperados_numero' in x
    ))
    active = cases - deaths - evacuees - recovered
    return {
        'recovered': {
            'name': 'Recuperados',
            'value': recovered,
        },
        'active': {
            'name': 'Activos',
            'value': active,
        },
        'evacuees': {
            'name': 'Evacuados',
            'value': evacuees,
        },
        'deaths': {
            'name': 'Fallecidos',
            'value': deaths,
        },
        'cases': {
            'name': 'Casos',
            'value': cases,
        }
    }


def evolution_of_cases_and_recovered_by_days(data):
    diagnosed = []
    recovered = []
    date = []
    days = list(data['data_cuba']['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    for x in days:
        diagnosed.append(0)
        recovered.append(0)
        if x.get('diagnosticados'):
            diagnosed[-1] += len(x['diagnosticados'])
        if x.get('recuperados_numero'):
            recovered[-1] += x['recuperados_numero']
        date.append(x['fecha'])
    return {
        'diagnosed': {
            'name': 'Casos en el día',
            'values': diagnosed,
        },
        'recovered': {
            'name': 'Altas en el día',
            'values': recovered,
        },
        'date': {
            'name': 'Fecha',
            'values': date,
        }
    }


def evolution_of_active_and_recovered_accumulated(data):
    date = []
    actives = []
    recovered = [0]
    total = 0
    deaths = 0
    recover = 0
    evacuees = 0
    days = list(data['data_cuba']['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    for x in days:
        recovered.append(recovered[-1])
        if x.get('recuperados_numero'):
            recovered[-1] += x['recuperados_numero']
        total += len(x['diagnosticados']) if 'diagnosticados' in x else 0
        deaths += x['muertes_numero'] if 'muertes_numero' in x else 0
        recover += x['recuperados_numero'] if 'recuperados_numero' in x else 0
        evacuees += x['evacuados_numero'] if 'evacuados_numero' in x else 0
        actives.append(total - deaths - recover - evacuees)
        date.append(x['fecha'])
    return {
        'active': {
            'name': 'Casos activos',
            'values': actives,
        },
        'recovered': {
            'name': 'Altas acumuladas',
            'values': recovered[1:],
        },
        'date': {
            'name': 'Fecha',
            'values': date,
        }
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
    days.sort(key=lambda x: x['fecha'])
    for diagnosed in (x['diagnosticados'] for x in days if 'diagnosticados' in x):
        for item in diagnosed:
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
    days.sort(key=lambda x: x['fecha'])
    for diagnosed in (x['diagnosticados'] for x in days if 'diagnosticados' in x):
        for item in diagnosed:
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
    days.sort(key=lambda x: x['fecha'])
    for diagnosed in (x['diagnosticados'] for x in days if 'diagnosticados' in x):
        for item in diagnosed:
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


def relation_of_tests_performed(data):
    total = 0
    positive = 0
    days = list(data['data_cuba']['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    for day in (x for x in days if 'diagnosticados' in x):
        positive += len(day['diagnosticados'])
        if 'tests_total' in day:
            total = max(total, day['tests_total'])
    return {
        'positive': {
            'name': 'Tests Positivos',
            'value': positive,
        },
        'negative': {
            'name': 'Tests Negativos',
            'value': total - positive,
        },
        'total': {
            'name': 'Total de Tests',
            'value': total,
        }
    }


def tests_by_days(data):
    ntest_days = []
    ntest_negative = []
    ntest_positive = []
    ntest_cases = []
    prev_test_cases = 0
    prev_test_negative = 0
    prev_test_positive = 0
    total = 0
    days = list(data['data_cuba']['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    for day in (x for x in days if 'diagnosticados' in x):
        total += len(day['diagnosticados'])
        if 'tests_total' in day:
            prev_test_cases = day['tests_total']
            test_negative = day['tests_total'] - total
            prev_test_negative = test_negative
            prev_test_positive = total
            break
    for day in (x for x in days if 'diagnosticados' in x):
        total += len(day['diagnosticados'])
        if 'tests_total' in day:
            ntest_days.append(day['fecha'])
            ntest_cases.append(day['tests_total'] - prev_test_cases)
            prev_test_cases = day['tests_total']
            test_negative = day['tests_total'] - total
            ntest_negative.append(test_negative - prev_test_negative)
            prev_test_negative = test_negative
            ntest_positive.append(total - prev_test_positive)
            prev_test_positive = total
    return {
        'date': {
            'name': 'Fecha',
            'values': ntest_days[1:],
        },
        'negative': {
            'name': 'Tests Negativos',
            'values': ntest_negative[1:],
        },
        'positive': {
            'name': 'Tests Positivos',
            'values': ntest_positive[1:],
        },
        'total': {
            'name': 'Total de Tests',
            'values': ntest_cases[1:],
        }
    }


def percent_positive_tests(data):
    _data = tests_by_days(data)
    date = _data['date']
    daily_positive = _data['positive']['values']
    daily_total = _data['total']['values']
    accum_positive = []
    accum_total = []
    total = 0
    positive = 0
    days = list(data['data_cuba']['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    for day in (x for x in days if 'diagnosticados' in x):
        positive += len(day['diagnosticados'])
        if 'tests_total' in day:
            total = max(total, day['tests_total'])
            accum_positive.append(positive)
            accum_total.append(total)
    daily = [float('%.2f' % (i * 100 / j))
             for i, j in zip(daily_positive, daily_total)]
    accum = [float('%.2f' % (i * 100 / j))
             for i, j in zip(accum_positive[1:], accum_total[1:])]
    return {
        'date': date,
        'daily': {
            'name': '% de Tests Positivos en el Día',
            'values': daily,
        },
        'accumulated': {
            'name': '% de Tests Positivos Acumulados',
            'values': accum,
        },
    }


def critics_serious_evolution(data):
    days = list(data['data_cuba']['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    date = [day['fecha'] for day in days]
    critics = [day['criticos_numero'] if 'criticos_numero' in day else 0 for day in days]
    serious = [day['graves_numero'] if 'graves_numero' in day else 0 for day in days]
    return {
        'date': {
            'name': 'Fecha',
            'values': date,
        },
        'critics': {
            'name': 'Críticos',
            'values': critics,
        },
        'serious': {
            'name': 'Graves',
            'values': serious,
        },
    }


def percent_critics_serious_to_actives(data):
    days = list(data['data_cuba']['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    date = [day['fecha'] for day in days]
    critics = [day['criticos_numero'] if 'criticos_numero' in day else 0 for day in days]
    serious = [day['graves_numero'] if 'graves_numero' in day else 0 for day in days]
    critics_serious = [x[0] + x[1] for x in zip(critics, serious)]
    total = 0
    deaths = 0
    recover = 0
    evacuees = 0
    actives = []
    for x in days:
        total += len(x['diagnosticados']) if 'diagnosticados' in x else 0
        deaths += x['muertes_numero'] if 'muertes_numero' in x else 0
        recover += x['recuperados_numero'] if 'recuperados_numero' in x else 0
        evacuees += x['evacuados_numero'] if 'evacuados_numero' in x else 0
        actives.append(total - deaths - recover - evacuees)
    result = [x[0] * 100 / x[1] for x in zip(critics_serious, actives)]
    return {
        'percents': {
            'name': 'Por ciento de casos graves y críticos',
            'values': result,
        },
        'date': {
            'name': 'Fecha',
            'values': date,
        },
    }


def effective_reproductive_number(data):
    data_cu = data['data_cuba']['numero-reproductivo']['cu']
    dates = []
    for item in data_cu['dates']:
        dates.append(f'2020/{item}')
    data_cu['dates'] = dates
    return {
        'upper': {
            'name': 'Margen Superior',
            'values': data_cu['upper'],
        },
        'value': {
            'name': 'Número Reproductivo Efectivo',
            'values': data_cu['value'],
        },
        'lower': {
            'name': 'Margen Inferior',
            'values': data_cu['lower'],
        },
        'date': {
            'name': 'Fecha',
            'values': data_cu['dates'],
        },
    }


def stringency_index_cuba(data):
    data_oxford = data['data_oxford']['data']
    index_days = []
    for i in data_oxford:
        index_days.append(i.replace('-', '/'))
    index_days = sorted(index_days)
    index_values_cuba_all = []
    index_values_cuba_legacy_all = []
    index_last_value = 0
    index_last_value_legacy = 0
    for i in index_days:
        day = data_oxford[i.replace('/', '-')]
        if 'CUB' in day:
            val = day['CUB']['stringency']
            index_values_cuba_all.append(val)
            index_last_value = max(index_last_value, val)
            val = day['CUB']['stringency_legacy_disp']
            index_values_cuba_legacy_all.append(val)
            index_last_value_legacy = max(index_last_value_legacy, val)
        else:
            index_values_cuba_all.append(None)
            index_values_cuba_legacy_all.append(None)
    cuba_length = len(list(data['data_cuba']['casos']['dias'].values()))
    index_slice = len(index_days) - cuba_length - 1
    index_slice = max(index_slice, 0)
    index_days = index_days[index_slice:]
    index_values_cuba_all = index_values_cuba_all[index_slice:]
    index_values_cuba_legacy_all = index_values_cuba_legacy_all[index_slice:]
    return {
        'days': index_days,
        'data': index_values_cuba_all,
        'data-legacy': index_values_cuba_legacy_all,
        'moments': moments,
    }


def affected_provinces(data):
    counter = {}
    total = 0
    days = list(data['data_cuba']['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    diagnosed = [x['diagnosticados'] for x in days if 'diagnosticados' in x]
    for patients in diagnosed:
        for p in patients:
            dpacode = 'dpacode_provincia_deteccion'
            try:
                counter[p[dpacode]]['value'] += 1
                counter[p[dpacode]]['name'] = p['provincia_detección']
                counter[p[dpacode]]['code'] = p[dpacode]
            except KeyError:
                counter[p[dpacode]] = {
                    'code': p[dpacode],
                    'value': 1,
                    'name': p['provincia_detección'],
                }
            total += 1
    result = []
    result_list = list(counter.values())
    result_list.sort(key=lambda x: x['value'], reverse=True)
    for item in result_list:
        item['total'] = total
        item['population'] = provinces_population[item['code']]
        del item['code']
        result.append(item)
    return result


def affected_municipalities(data):
    counter = {}
    total = 0
    days = list(data['data_cuba']['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    diagnosed = [x['diagnosticados'] for x in days if 'diagnosticados' in x]
    for patients in diagnosed:
        for p in patients:
            dpacode = 'dpacode_municipio_deteccion'
            try:
                counter[p[dpacode]]['value'] += 1
                counter[p[dpacode]]['name'] = p['municipio_detección']
                counter[p[dpacode]]['province'] = p['provincia_detección']
            except KeyError:
                counter[p[dpacode]] = {
                    'value': 1,
                    'name': p['municipio_detección'],
                    'province': p['provincia_detección'],
                }
            total += 1
    result = []
    result_list = list(counter.values())
    result_list.sort(key=lambda x: x['value'], reverse=True)
    result_list = result_list[:10]
    for item in result_list:
        item['total'] = total
        result.append(item)
    return result

# World

def multiple_comparison_of_cuba_with_radar(data):
    def get_last(array):
        res = array[-1]
        for i in array[::-1]:
            if i is not None:
                res = i
                break
        return res
    dataw = data['data_world']
    world_data = curves_comparison(data)
    iso3Code_countries = {j: i for i, j in countries_iso3Code.items()}
    radar = {}
    cuba_pop = 11209628
    dataw['tests']['CUB']['population'] = cuba_pop
    cuba_test = dataw['tests']['CUB']['total_tests_per_million']
    cuba_confirmed = int(world_data['data']['CUB']
                         ['confirmed'][-1]/cuba_pop*10**6)
    for j, i in world_data['data'].items():
        if len(i['stringency']) == 0 or j not in dataw['tests']:
            continue
        radar[i['name']] = {
            'name': i['name'],
            'confirmed_per_million': i['confirmed'][-1],
            'deaths_p': i['deaths'][-1]/i['confirmed'][-1]*100,
            'recovered_p': i['recovered'][-1]/i['confirmed'][-1]*100,
            'stringency': get_last(i['stringency']),
        }
    for key, dat in dataw['tests'].items():
        if key not in countries_codes:
            continue
        name = trans_countries[iso3Code_countries[key]]
        if name not in radar:
            continue
        radar[name]['test_per_million'] = dat['total_tests_per_million']
        radar[name]['test_p'] = dat['test_efectivity']
        radar[name]['confirmed_per_million'] = int(
            radar[name]['confirmed_per_million']/dat['population']*10**6)
        radar[name]['confirmed_per_million_bound'] = int(
            1.1*max(radar[name]['confirmed_per_million'], cuba_confirmed))
        radar[name]['test_per_million_bound'] = int(
            1.1*max(int(dat['total_tests_per_million']), cuba_test))
    return {
        'data': radar,
        'bounds': {
            'stringency': 100,
            'deaths_p': 15,
            'recovered_p': 100,
            'test_p': 40,
        },
    }


def curves_comparison(data):
    world = data['data_world']
    confirmed = [0]
    daily = [0]
    recovered = [0]
    deaths = [0]
    actives = []
    _total = 0
    _deaths = 0
    _recover = 0
    _evacuees = 0
    days = list(data['data_cuba']['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    for day in days:
        confirmed.append(confirmed[-1])
        recovered.append(recovered[-1])
        deaths.append(deaths[-1])
        daily.append(0)
        if day.get('diagnosticados'):
            confirmed[-1] += len(day['diagnosticados'])
            daily[-1] += len(day['diagnosticados'])
        if day.get('recuperados_numero'):
            recovered[-1] += day['recuperados_numero']
        if day.get('muertes_numero'):
            deaths[-1] += day['muertes_numero']
        _total += len(day['diagnosticados']) if 'diagnosticados' in day else 0
        _deaths += day['muertes_numero'] if 'muertes_numero' in day else 0
        _recover += day['recuperados_numero'] if 'recuperados_numero' in day else 0
        _evacuees += day['evacuados_numero'] if 'evacuados_numero' in day else 0
        actives.append(_total - _deaths - _recover - _evacuees)
    for key in world['paises_info']:
        _value = world['paises_info'][key]
        _confirmed = _value['confirmed']
        _recovered = _value['recovered']
        _deaths = _value['deaths']
        _daily = [confirmed[0]]
        _active = []
        for i in range(1, len(_confirmed)):
            _daily.append(_confirmed[i] - _confirmed[i - 1])
        for i in range(len(_confirmed)):
            _active.append(_confirmed[i] - _deaths[i] - _recovered[i])
        _value['daily'] = _daily
        _value['active'] = _active
    world['paises_info']['Cuba']['confirmed'] = confirmed[1:]
    world['paises_info']['Cuba']['recovered'] = recovered[1:]
    world['paises_info']['Cuba']['deaths'] = deaths[1:]
    world['paises_info']['Cuba']['daily'] = daily[1:]
    world['paises_info']['Cuba']['active'] = actives
    dataw = data['data_world']
    curves_stringency = {}
    stringency_countries = []
    for i in dataw['indexes']['countries']:
        if i in countries_codes:
            stringency_countries.append(i)
    for i in trans_countries.keys():
        curves_stringency[i] = []
    for i in sorted(dataw['indexes']['data'].keys()):
        day = dataw['indexes']['data'][i]
        for j in stringency_countries:
            if j in day:
                curves_stringency[countries_codes[j]].append(
                    day[j]['stringency'])
            else:
                curves_stringency[countries_codes[j]].append(None)
    for i in curves_stringency.keys():
        if len(curves_stringency[i]) > 0:
            curves_stringency[i] = curves_stringency[i][:-1]
    for key in curves_stringency:
        world['paises_info'][key]['stringency'] = curves_stringency[key][
            max(len(curves_stringency[key]) -
                len(world['paises_info'][key]['confirmed']), 0):
        ]
    _data = {}
    for key in world['paises_info']:
        if key not in trans_countries:
            continue
        _data[countries_iso3Code[key]] = world['paises_info'][key]
        _data[countries_iso3Code[key]]['name'] = trans_countries[key]
    return {
        'data': _data,
        'updated': world['dia-actualizacion'],
    }


def test_behavior_comparison(data):
    result = data['data_world']['tests']
    for key in result:
        result[key]['name'] = trans_countries[countries_codes[key]
                                              ] if key in countries_codes else None
        result[key]['test_efectivity'] = float(result[key]['test_efectivity'])
        result[key]['total_tests_per_million'] = float(
            result[key]['total_tests_per_million'])
    cuba_population = 11209628
    cuba_total = 0
    cuba_positive = 0
    cuba_days = list(data['data_cuba']['casos']['dias'].values())
    cuba_days.sort(key=lambda x: x['fecha'])
    for cuba_day in (x for x in cuba_days if 'diagnosticados' in x):
        cuba_positive += len(cuba_day['diagnosticados'])
        if 'tests_total' in cuba_day:
            cuba_total = max(cuba_total, cuba_day['tests_total'])
    result['CUB']['name'] = trans_countries[countries_codes['CUB']]
    result['CUB']['test_efectivity'] = float(cuba_positive / cuba_total * 100)
    result['CUB']['total_tests_per_million'] = float(
        cuba_total / cuba_population * 10**6)
    curves = curves_evolution(data)
    tests = result
    result = {}
    for key in tests:
        if not tests[key]['name']:
            continue
        name = tests[key]['name']
        if not name in curves:
            continue
        result[key] = tests[key]
        result[key]['total'] = curves[name]['ctotal']
    return result


def curves_evolution(data):
    dataw = data['data_world']
    curves = {}
    def scaleX(x): return None if x < 0 else 0 if x == 0 else log10(x)
    def scaleY(y): return None if y < 0 else 0 if y == 0 else log10(y)
    for c, dat in dataw['paises'].items():
        weeksum = 0
        weeks = []
        accum = []
        prevweek = 0
        total = 0
        ctotal = 0
        for i, (day, day1) in enumerate(zip(dat[:-1], dat[1:])):
            ctotal = day1
            if (i + 1) % 7 == 0 and day > 30:
                total = day
                weeksum = total - prevweek
                weeks.append(scaleY(weeksum))
                weeksum = 0
                prevweek = total
                accum.append(scaleX(total))
        curves[c] = {
            'weeks': weeks,
            'cummulative_sum': accum,
            'total': total,
            'ctotal': ctotal
        }
    return {
        trans_countries[i]: j
        for i, j in (list(
            sorted(
                curves.items(),
                key=lambda x: x[0],
                reverse=False
            )
        )) if i in trans_countries
    }


def world_countries(data):
    countries_info = curves_comparison(data)['data']
    result = []
    for key in countries_info:
        value = countries_info[key]
        confirmed = value['confirmed'][-1]
        recovered = value['recovered'][-1]
        deaths = value['deaths'][-1]
        name = value['name']
        result.append((confirmed, recovered, deaths, name))
    result.sort(reverse=True)
    return list(map(lambda x: {
        'name': x[3],
        'value': x[0],
        'confirmed': x[0],
        'recovered': x[1],
        'deaths': x[2],
    }, result))

# Extra

def pesquisador(data):
    return {
        'url': 'http://autopesquisa.sld.cu/',
        'javascript': "document.querySelector('app-root').removeChild(document.querySelector('mat-toolbar'));",
        'contains': 'autopesquisa.sld.cu'
    }
