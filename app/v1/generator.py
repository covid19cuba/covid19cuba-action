import itertools
from collections import defaultdict

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
    pass


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
    counter=defaultdict(lambda : {'total':0, 'name': '', 'gtotal': 0})
    gtotal=0
    data=map(lambda y: y['diagnosticados'] ,filter(lambda x: 'diagnosticados' in x ,data['casos']['dias'].values()))
    # in order to avoid double for we use itertools.chain with expanded data (*data)
    data = itertools.chain(*data)
    for i in data:
        counter[i['dpacode_provincia_deteccion']]['total']+=1
        # take province name from data, assumen that checker fix previosly
        counter[i['dpacode_provincia_deteccion']]['name']=i['provincia_detección']
        gtotal+=1
    res = []
    for i in itertools.islice(sorted(counter.values(), key=lambda x: x['total'], reverse=True), 10):
        i['gtotal']=gtotal
        res.append(i)
    return res


def top_10_affected_municipalities(data):
    counter=defaultdict(lambda : {'total':0, 'name': '', 'gtotal': 0, 'province_belong': ''})
    gtotal=0
    data=map(lambda y: y['diagnosticados'] ,filter(lambda x: 'diagnosticados' in x ,data['casos']['dias'].values()))
    # in order to avoid double for we use itertools.chain with expanded data (*data)
    data = itertools.chain(*data)
    for i in data:
        counter[i['dpacode_municipio_deteccion']]['total']+=1
        # take municipality name from data, assumen that checker fix previosly
        counter[i['dpacode_municipio_deteccion']]['name']=i['municipio_detección']
        # take province name from data, assumen that checker fix previosly
        counter[i['dpacode_municipio_deteccion']]['province_belong']=i['provincia_detección']
        gtotal+=1
    res = []
    for i in itertools.islice(sorted(counter.values(), key=lambda x: x['total'], reverse=True), 10):
        i['gtotal']=gtotal
        res.append(i)
    return res


def comparison_of_accumulated_cases(data):
    pass