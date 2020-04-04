from json import load, dump
from .checker import check
from .generator import resume, cases_by_sex, cases_by_mode_of_contagion, \
    evolution_of_cases_by_days, distribution_by_age_ranges, \
    cases_by_nationality, distribution_by_nationality_of_foreign_cases, \
    list_of_tests_performed, tests_for_days, top_10_affected_provinces, \
    top_10_affected_municipalities, comparison_of_accumulated_cases


def run():
    if check():
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
        result_dict = {}
        for function in function_list:
            result = dump_util(function, data)
            result_dict[function.__name__] = result
        dump(result_dict, open(f'api/v1/data.json', mode='w', encoding='utf-8'), ensure_ascii=False)


def dump_util(function, data):
    result = function(data)
    dump(result, open(f'api/v1/{function.__name__}.json', mode='w', encoding='utf-8'), ensure_ascii=False)
    return result
