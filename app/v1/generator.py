from .utils import countries


def resume(data):
    days = list(data['casos']['dias'].values())
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
    return [
        {'name': 'Diagnosticados', 'value': diagnosed},
        {'name': 'Activos', 'value': active},
        {'name': 'Recuperados', 'value': recovered},
        {'name': 'Evacuados', 'value': evacuees},
        {'name': 'Muertos', 'value': deaths}
    ]


def cases_by_sex(data):
    result = {'hombre': 0, 'mujer': 0, 'no reportado': 0}
    days = list(data['casos']['dias'].values())
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
    days = list(data['casos']['dias'].values())
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


def evolution_of_cases_by_days(data):
    accumulated = [0]
    daily = [0]
    days = list(data['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    for x in days:
        accumulated.append(accumulated[-1])
        daily.append(0)
        if x.get('diagnosticados'):
            accumulated[-1] += len(x['diagnosticados'])
            daily[-1] += len(x['diagnosticados'])
    return {
        'accumulated': {
            'name': 'Casos acumulados',
            'values': accumulated[1:]
        },
        'daily': {
            'name': 'Casos en el día',
            'values': daily[1:]
        }
    }


def distribution_by_age_ranges(data):
    result = [0] * 5
    keys = ['0-18', '19-40', '41-60', '>=61', 'Desconocido']
    hard = ['0-18', '19-40', '41-60', '>=61', 'unknown']
    days = list(data['casos']['dias'].values())
    for diagnosed in (x['diagnosticados'] for x in days if 'diagnosticados' in x):
        for item in diagnosed:
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


def cases_by_nationality(data):
    pretty = {
        'foreign': 'Extranjeros',
        'cubans': 'Cubanos',
        'unknown': 'No reportados'
    }
    result = {'foreign': 0, 'cubans': 0, 'unknown': 0}
    days = list(data['casos']['dias'].values())
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
    days = list(data['casos']['dias'].values())
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
            'value': result[key]
        }
        for key in result
    ]


def list_of_tests_performed(data):
    total = 0
    positive = 0
    days = list(data['casos']['dias'].values())
    for day in (x for x in days if 'diagnosticados' in x):
        positive += len(day['diagnosticados'])
        if 'tests_total' in day:
            total = max(total, day['tests_total'])
    return {
        'positive': {
            'name': 'Tests Positivos',
            'value': positive
        },
        'negative': {
            'name': 'Tests Negativos',
            'value': total - positive
        },
        'total': {
            'name': 'Total de Tests',
            'value': total
        }
    }


def tests_for_days(data):
    ntest_days = []
    ntest_negative = []
    ntest_positive = []
    ntest_cases = []
    prev_test_cases = 0
    prev_test_negative = 0
    prev_test_positive = 0
    total = 0
    days = list(data['casos']['dias'].values())
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
            ntest_days.append(day['fecha'].replace('2020/', ''))
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
            'values': ntest_days[1:]
        },
        'negative': {
            'name': 'Tests Negativos',
            'values': ntest_negative[1:]
        },
        'positive': {
            'name': 'Tests Positivos',
            'values': ntest_positive[1:]
        },
        'total': {
            'name': 'Total de Tests',
            'values': ntest_cases[1:]
        }
    }


def top_10_affected_provinces(data):
    counter = {}
    total = 0
    days = list(data['casos']['dias'].values())
    diagnosed = [x['diagnosticados'] for x in days if 'diagnosticados' in x]
    for patients in diagnosed:
        for p in patients:
            dpacode = 'dpacode_provincia_deteccion'
            try:
                counter[p[dpacode]]['value'] += 1
                counter[p[dpacode]]['name'] = p['provincia_detección']
            except KeyError:
                counter[p[dpacode]] = {
                    'value': 1,
                    'name': p['provincia_detección']
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


def top_10_affected_municipalities(data):
    counter = {}
    total = 0
    days = list(data['casos']['dias'].values())
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
                    'province': p['provincia_detección']
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


def comparison_of_accumulated_cases(data):
    pass
