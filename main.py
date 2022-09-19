from flask import Flask
import json
from utils import *


app = Flask('__name__')


# create view for title searching
@app.route('/movie/<title>/')
def page_by_title(title):
    result = {}
    for item in get_data_by_sql(sql=f'''
                    SELECT title, country, release_year, listed_in, description
                    FROM netflix
                    WHERE title = '{title}'
                    ORDER BY release_year DESC
                    LIMIT 1
                    '''):
        result = dict(item)

    return app.response_class(
        json.dumps(result, ensure_ascii=False, indent=4),
        status=200
    )

# create view for year filter
@app.route('/movie/<year1>/to/<year2>/')
def page_by_year(year1, year2):
    result = []
    for item in get_data_by_sql(sql=f'''select * from netflix
                    where release_year >= {year1}
                    AND release_year <= {year2}
                    limit 100
                    '''):
        result.append(dict(item))

    return app.response_class(
        json.dumps(result, ensure_ascii=False, indent=4),
        status=200
    )

# create view for rating
@app.route('/rating/<rating>/')
def page_by_rating(rating):
    result = []
    my_rating = {
        "children":("G", "G"),
        "family":("G", "PG", "PG-13"),
        "adult":("R", "NC-17")
    }
    for item in get_data_by_sql(sql=f'''
                    SELECT *
                    FROM netflix
                    WHERE rating in {my_rating.get(rating)}
                    '''):
        result.append(dict(item))

    return app.response_class(
        json.dumps(result, ensure_ascii=False, indent=4),
        status=200
    )

# create view for genre
@app.route('/genre/<genre>/')
def page_by_genre(genre):
    result = []
    for item in get_data_by_sql(sql=f'''
                    SELECT show_id, type
                    FROM netflix
                    WHERE listed_in like '%{str(genre).title()}%'
                    '''):
        result.append(dict(item))

    return app.response_class(
        json.dumps(result, ensure_ascii=False, indent=4),
        status=200
    )


if __name__ == '__main__':
    app.run(host="localhost", port=5035, debug=True)



