def find_contract_from_invoice(ocr_str, dico_contracts):
    dict_count_contracts = dict.fromkeys(list(dico_contracts.keys()))
    for k, v in dico_contracts.items():
        dict_count_contracts[k] = 0
        for el in v:
            dict_count_contracts[k] += ocr_str.count(el)

    dict_count_contracts_sum = {
        "Electricity": dict_count_contracts["Electricity_+"]
        - dict_count_contracts["Electricity_-"],
        "Gas": dict_count_contracts["Gas_+"] - dict_count_contracts["Gas_-"],
        "Heat": dict_count_contracts["Heat_+"] - dict_count_contracts["Heat_-"],
    }

    if dict_count_contracts_sum["Heat"] > 2:
        return "Heat", "To be checked"
    else:
        if dict_count_contracts_sum["Electricity"] > dict_count_contracts_sum["Gas"]:
            if (
                dict_count_contracts_sum["Electricity"] > 7
                and dict_count_contracts_sum["Electricity"]
                - dict_count_contracts_sum["Gas"]
                > 5
            ):
                return "Electricity", "Certain"
            else:
                return "Electricity", "To be checked"
        elif dict_count_contracts_sum["Electricity"] < dict_count_contracts_sum["Gas"]:
            if (
                dict_count_contracts_sum["Gas"] > 7
                and dict_count_contracts_sum["Gas"]
                - dict_count_contracts_sum["Electricity"]
                > 5
            ):
                return "Gas", "Certain"
            else:
                return "Electricity", "To be checked"
        else:
            return "Unknown", "To be checked"


def find_provider_from_invoice(ocr_str, dico_provider):
    dict_count_providers = dict.fromkeys(list(dico_provider.keys()))
    for k, v in dico_provider.items():
        dict_count_providers[k] = 0
        for el in v:
            dict_count_providers[k] += ocr_str.count(el)
    prov = max(dict_count_providers, key=dict_count_providers.get)
    prov_val = dict_count_providers[prov]
    if prov_val > 0:
        prov_others = dict_count_providers.copy()
        del prov_others[prov]
        if prov_val > prov_others[max(prov_others, key=prov_others.get)]:
            return prov
    return "Unknown"
