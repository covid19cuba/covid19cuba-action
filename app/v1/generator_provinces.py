from json import load, dump
from math import log10
from .countries import countries
from .province_codes import province_abbrs
from .utils import dump_util


def generate(debug=False):
    data_cuba = load(open('data/covid19-cuba.json', encoding='utf-8'))
    function_list = [
        cases_by_sex
    ]
    for key in province_abbrs:
        value = province_abbrs[key]
        dump({f.__name__: dump_util(f'api/v1/provinces/{key}', f,
                                    data_cuba=data_cuba, province=value,
                                    debug=debug)
              for f in function_list},
             open(f'api/v1/provinces/{key}/all.json',
                  mode='w', encoding='utf-8'),
             ensure_ascii=False,
             indent=2 if debug else None,
             separators=(',', ': ') if debug else (',', ':'))


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
