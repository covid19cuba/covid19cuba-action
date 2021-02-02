from json import load


def generate(debug=False):
    data = load(open("data/protocols.json", encoding="utf-8"))
    medicines = data["medicamentos"]
    scenarios = data["escenarios"]
    protocols = list(data["protocolos"].values())
    protocols.sort(key=lambda x: x["version"])
    result = []
    for protocol in protocols:
        item = {
            "id": protocol["id"],
            "link": f'https://covid19cubadata.github.io/protocolos/{protocol["file"]}',
            "name": protocol["nombre"],
            "date": protocol["fecha"],
            "version": protocol["version"],
            "indications": [],
        }
        indications = protocol["indicaciones"]["general"]
        for indication_key, indication_value in indications.items():
            indication = {
                "id": indication_key,
                "name": medicines[indication_key]["nombre"],
                "abbreviation": medicines[indication_key]["nombre-corto"],
                "category": medicines[indication_key]["categoría"],
                "description": medicines[indication_key]["descripción"],
                "update": item["version"] > 1
                and indication_key
                not in data["protocolos"][str(item["version"] - 1)]["indicaciones"][
                    "general"
                ],
                "scenarios": [],
            }
            indication_scenarios = indication_value["escenarios"]
            for indication_scenario_key in indication_scenarios:
                indication_scenario_value = scenarios[indication_scenario_key]
                scenario = {
                    "id": indication_scenario_key,
                    "name": indication_scenario_value["nombre"],
                    "shortname": indication_scenario_value["nombre-corto"],
                    "category": indication_scenario_value["categoria"],
                    "abbreviation": indication_scenario_value["abreviatura"],
                    "order": indication_scenario_value["orden"],
                    "update": item["version"] > 1
                    and (
                        indication["update"]
                        or indication_scenario_key
                        not in data["protocolos"][str(item["version"] - 1)][
                            "indicaciones"
                        ]["general"][indication_key]["escenarios"]
                    ),
                    "details": indication_scenarios[indication_scenario_key],
                }
                indication["scenarios"].append(scenario)
            indication["scenarios"].sort(key=lambda x: x["order"], reverse=True)
            item["indications"].append(indication)
        result.append(item)
    return {
        "protocols": result,
    }
