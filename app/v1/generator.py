def resume(data):
    pass


def cases_by_sex(data):
    result = {'hombre': 0, 'mujer': 0, 'no reportado': 0}
    days = list(data['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    for diagnosed in (x['diagnosticados'] for x in days if x.get('diagnosticados')):
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
    result_list = [(pretty[key] if key in pretty else key.title(), result[key]) for key in result]
    return result_list


def cases_by_mode_of_contagion(data):
    result = {'importado': 0, 'introducido': 0, 'autoctono': 0, 'desconocido': 0}
    days = list(data['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    for diagnosed in (x['diagnosticados'] for x in days if x.get('diagnosticados')):
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
    result_list = [(pretty[key] if key in pretty else key.title(), result[key]) for key in result]
    return result_list


def evolution_of_cases_by_days(data):
    result = [0]
    days = list(data['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    for x in days:
        result.append(result[-1])
        if x.get('diagnosticados'):
            result[-1] += len(x['diagnosticados'])
    
    return result[1:]


def distribution_by_age_ranges(data):
    pass


def cases_by_nationality(data):
    pass


def distribution_by_nationality_of_foreign_cases(data):
    pass


def list_of_tests_performed(data):
    pass


def tests_for_days(data):
    pass


def top_10_affected_provinces(data):
    pass


def top_10_affected_municipalities(data):
    pass


def comparison_of_accumulated_cases(data):
    pass
