import json

import pandas as pd


def roles_list_to_fixture_json(roles):
    list_dicts = list()

    for num, role_name in enumerate(roles, 1):
        one_role_object = dict()
        one_role_object['model'] = 'teams.role'
        one_role_object['pk'] = num
        one_role_object['fields'] = {'name': role_name}
        list_dicts.append(one_role_object)
    return list_dicts


if __name__ == '__main__':
    df = pd.read_csv('naukri_data_science_jobs_india.csv')

    all_roles = list(set(df['Job_Role']))

    result = roles_list_to_fixture_json(all_roles)
    print(result)

    json.dump(result, fp=open('data.json', 'w'))
