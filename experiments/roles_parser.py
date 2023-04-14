from ast import literal_eval
import json

import pandas as pd


def data_list_to_fixture_json(data, model, field_name):
    list_dicts = list()

    for num, object_name in enumerate(data, 1):
        one_role_object = dict()
        one_role_object['model'] = model
        one_role_object['pk'] = num
        one_role_object['fields'] = {field_name: object_name}
        list_dicts.append(one_role_object)
    return list_dicts


if __name__ == '__main__':
    roles_dataframe = pd.read_csv('naukri_data_science_jobs_india.csv')
    all_roles = list(set(roles_dataframe['Job_Role']))
    roles_fixture = data_list_to_fixture_json(all_roles, 'teams.role', 'name')
    json.dump(roles_fixture, open('roles_data.json', 'w'))

    languages_dataframe = pd.read_csv('top_100_languages.csv')
    all_languages = list(set(languages_dataframe['Language']))
    languages_fixture = data_list_to_fixture_json(
        all_languages, 'users.language', 'language'
    )
    json.dump(languages_fixture, open('languages_data.json', 'w'))

    technologies_dataframe = pd.read_csv('it_vacancies_full.csv')
    all_technologies = list(technologies_dataframe['Keys'])
    cleared_technologies = set()
    for technologies_list in all_technologies:
        for technologies in literal_eval(technologies_list):
            cleared_technologies.add(technologies)
    technologies_fixture = data_list_to_fixture_json(
        list(cleared_technologies), 'users.language', 'language'
    )
    json.dump(technologies_fixture, open('technologies_data.json', 'w'))
