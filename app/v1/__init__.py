from json import load, dump
from os import makedirs
from .checker import check
from .generator import resume, cases_by_sex, cases_by_mode_of_contagion, \
    evolution_of_cases_by_days, distribution_by_age_ranges, \
    cases_by_nationality, distribution_by_nationality_of_foreign_cases, \
    list_of_tests_performed, tests_by_days, affected_provinces, \
    affected_municipalities, comparison_of_accumulated_cases, map_data


def run(debug=False):
    if not check():
        return
    makedirs('api/v1', exist_ok=True)
    data_cuba = load(open('data/covid19-cuba.json', encoding='utf-8'))
    data_world = load(open('data/paises-info-dias.json', encoding='utf-8'))
    function_list = [
        resume,
        cases_by_sex,
        cases_by_mode_of_contagion,
        evolution_of_cases_by_days,
        distribution_by_age_ranges,
        cases_by_nationality,
        distribution_by_nationality_of_foreign_cases,
        list_of_tests_performed,
        tests_by_days,
        affected_provinces,
        affected_municipalities,
        comparison_of_accumulated_cases,
        map_data
    ]
    dump({
        f.__name__: dump_util(f,
                              data_cuba=data_cuba,
                              data_world=data_world,
                              debug=debug)
        for f in function_list},
        open(f'api/v1/all', mode='w', encoding='utf-8'),
        ensure_ascii=False,
        indent=2 if debug else None,
        separators=(',', ': ') if debug else (',', ':'))


def dump_util(func, **data):
    result = func(data)
    dump(result,
         open(f'api/v1/{func.__name__}', mode='w', encoding='utf-8'),
         ensure_ascii=False,
         indent=2 if data['debug'] else None,
         separators=(',', ': ') if data['debug'] else (',', ':'))
    return result
