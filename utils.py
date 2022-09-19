from flask import json
import sqlite3

def get_data_by_sql(sql):
    with sqlite3.connect('netflix.db') as connection:
        connection.row_factory = sqlite3.Row

        result = connection.execute(sql).fetchall()

    return result

def step_5(name1='Rose McIver', name2='Ben Lamb'):
    names_dict = {}

    for item in get_data_by_sql(sql=f'''
                        SELECT *
                        FROM netflix
                        WHERE `cast` like '%{name1}%' and `cast` like '%{name2}%'
                        '''):
        result = dict(item)

        names = set(result.get('cast').split(", ")) - {name1, name2}

        for name in names:
            names_dict[name.strip()] = names_dict.get(name.strip(), 0) + 1

    print(names_dict)

    for key, value in names_dict.items():
        if value > 2:
            print(key)


def step_6(type, year, genre):
    result = []
    for item in get_data_by_sql(sql=f'''
                        SELECT *
                        FROM netflix
                        WHERE type = '{type.title()}' and release_year = '{year}' and listed_in like '%{str(genre).title()}%'
                        '''):
        result.append(dict(item))

    return json.dumps(result, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    print(step_6('movie', 2019, 'dramas'))