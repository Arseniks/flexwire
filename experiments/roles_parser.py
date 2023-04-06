import json
import re

import pandas as pd


def is_string_clean(text):
    clean_text = re.sub(r'[^\w\s]', '', text)
    clean_text = re.sub(r'\s+', ' ', clean_text)
    if (
        clean_text != text
        or len(re.findall(r'\w+', text)) > 5
        or re.search(r'\d', text)
    ):
        return False
    return True


def normalize_roles(roles):
    result_array = []
    for role in roles:
        role = role.lower()
        if is_string_clean(role):
            result_array.append(role)
    return result_array


def remove_similar_strings(roles):
    spam_words = {
        'engineer',
        'developer',
        'programmer',
        'lead',
        'junior',
        'senior',
        'analyse',
        'analytic',
    }
    result_roles_without_repeating = []
    for string1 in roles:
        words1 = re.findall(r'\w+', string1)
        is_similar = False
        for string2 in roles:
            if string1 != string2:
                words2 = re.findall(r'\w+', string2)
                count = 0
                for word1 in words1:
                    for word2 in words2:
                        if word1 == word2 and word1 not in spam_words:
                            count += 1
                        if count == 2:
                            is_similar = True
                            break
                    if is_similar:
                        break
                if is_similar:
                    break
        if not is_similar or not result_roles_without_repeating:
            result_roles_without_repeating.append(string1)
    return result_roles_without_repeating


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
    normalized_roles = normalize_roles(all_roles)
    normalized_roles_without_repeating = remove_similar_strings(
        normalized_roles
    )

    result = roles_list_to_fixture_json(normalized_roles_without_repeating)
    result_json = json.dumps(result)

    with open('data.json', 'w') as outfile:
        json.dump(result_json, outfile)
