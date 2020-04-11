def cases_by_sex(data, province_code, province_name):
    result = {'hombre': 0, 'mujer': 0, 'no reportado': 0}
    days = list(data['data_cuba']['casos']['dias'].values())
    days.sort(key=lambda x: x['fecha'])
    for diagnosed in (x['diagnosticados'] for x in days if 'diagnosticados' in x):
        for item in diagnosed:
            if item.get('provincia_detección') != province_name:
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
