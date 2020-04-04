from json import load, dump
from os import makedirs
from .checker import check
from .generator import resume, cases_by_sex, cases_by_mode_of_contagion, \
    evolution_of_cases_by_days, distribution_by_age_ranges, \
    cases_by_nationality, distribution_by_nationality_of_foreign_cases, \
    list_of_tests_performed, tests_for_days, top_10_affected_provinces, \
    top_10_affected_municipalities, comparison_of_accumulated_cases


def run():
    if not check():
        return
    makedirs('api/v1', exist_ok=True)
    data = load(open('data/covid19-cuba.json', encoding='utf-8'))
    function_list = [
        resume,
        cases_by_sex,
        cases_by_mode_of_contagion,
        evolution_of_cases_by_days,
        distribution_by_age_ranges,
        cases_by_nationality,
        distribution_by_nationality_of_foreign_cases,
        list_of_tests_performed,
        tests_for_days,
        top_10_affected_provinces,
        top_10_affected_municipalities,
        comparison_of_accumulated_cases
    ]
    dump({f.__name__: dump_util(f, data) for f in function_list},
         open(f'api/v1/data.json', mode='w', encoding='utf-8'),
         ensure_ascii=False)


def dump_util(func, data):
    result = func(data)
    dump(result,
         open(f'api/v1/{func.__name__}.json', mode='w', encoding='utf-8'),
         ensure_ascii=False)
    return result
