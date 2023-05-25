import os
import json
from flask import abort
import datetime
from flask import Blueprint, g, redirect, render_template, request, jsonify, Response

# CONFIG_FILE_PATH = ''
# Load the config
with open(os.path.join("movies_package", "config.json"), "r") as config_file:
    config_data = json.load(config_file)

# Set environment variable from the dict config_data['DATABASE']
for GLOB_VAR in config_data["DATABASE"].keys():
    exec(f"{GLOB_VAR}=config_data['DATABASE']['{GLOB_VAR}']")


def from_db_row_to_dict(db_row, ID=ID, COLUMNS_DATABASE=COLUMNS_DATABASE):
    """
    Get a single row of the database as a tuple and return a dict mapping database columns names
    to their corresponding values for this database row.

    Args:
        db_row (tuple): Single database row
        ID (str, optional): Single database column name used as index. Defaults to ID.
        COLUMNS_DATABASE (dict, optional):  Dictionnary mapping the database columns names to the corresponding
                                            types , except the index columns). Defaults to COLUMNS_DATABASE.

    Returns:
        dict : dict mapping database columns names to the corresponding values in the the database row
    """
    res = dict(zip([ID] + list(COLUMNS_DATABASE.keys()), db_row))
    res["genres"] = res["genres"].split(", ")
    return res


"""def get_movie_from_id_as_dict(movie_id, conn, ID=ID, COLUMNS_DATABASE=COLUMNS_DATABASE):
    c = conn.cursor()
    sql_request = f"SELECT {', '.join([ID]+list(COLUMNS_DATABASE.keys()))} FROM movies WHERE {ID}==?"
    #'SELECT '+', '.join([ID]+list(COLUMNS_DATABASE.keys())) +' FROM movies WHERE '+ID+'==?'
    res = c.execute(sql_request, (movie_id,)).fetchall()

    if len(res) != 1:
        abort(404)
    else:
        movie_dict = from_db_row_to_dict(res[0])
    return movie_dict"""


def from_db_row_to_dict(
    db_row, ID=ID, ID_type=ID_type, COLUMNS_DATABASE=COLUMNS_DATABASE
):
    """
    Get a single row of the database as a tuple and return a dict mapping database columns names
    to their corresponding values for this database row.

    Args:
        db_row (tuple): Single database row
        ID (str, optional): Single database column name used as index. Defaults to ID.
        ID_type (str, optional): Index type. Defaults to ID_type.
        COLUMNS_DATABASE (dict, optional):  Dictionnary mapping the database columns names to the corresponding
                                            types , except the index columns). Defaults to COLUMNS_DATABASE.

    Returns:
        dict : dict mapping database columns names to the corresponding values in the the database row
    """
    res = dict(zip([ID] + list(COLUMNS_DATABASE.keys()), db_row))
    return correct_type(res, correct_genres=True)


def correct_type(
    movie,
    ID=ID,
    ID_type=ID_type,
    COLUMNS_DATABASE=COLUMNS_DATABASE,
    correct_genres=True,
):
    """
    Correct field type of the dict movie, if not possible the field is replace by 'TypeError'

    Args:
        movie (dict): dict mapping database columns names to the corresponding values for the movie
        ID (str, optional): Single database column name used as index. Defaults to ID.
        ID_type (str, optional): Index type. Defaults to ID_type.
        COLUMNS_DATABASE (dict, optional):  Dictionnary mapping the database columns names to the corresponding
                                            types , except the index columns). Defaults to COLUMNS_DATABASE. Defaults
                                            to COLUMNS_DATABASE.

    Returns:
        dict: dict mapping database columns names to the corresponding values for the movie, with correct type
    """
    keep_keys = list(COLUMNS_DATABASE.keys())
    keep_keys.remove("genres")
    for k in keep_keys:
        try:
            exec(f"movie['{k}']={COLUMNS_DATABASE[k]}(movie['{k}'])")
        except:
            movie[k] = "TypeError"

    exec(f"movie['{ID}']={ID_type}(movie['{ID}'])")

    if correct_genres:
        movie["genres"] = movie["genres"].split(", ")

    return movie


def get_movie_from_id(movie_id, conn, ID=ID, COLUMNS_DATABASE=COLUMNS_DATABASE):
    """
    Get a single movie id and return a dict mapping database columns names
    to their corresponding values for this movie.

    Args:
        movie_id (int): movie id
        conn (sqlite3.Connection): sqlite3.Connection of the database
        ID (str, optional): Single database column name used as index. Defaults to ID.
        COLUMNS_DATABASE (dict, optional):  Dictionnary mapping the database columns names to the corresponding
                                            types , except the index columns). Defaults to COLUMNS_DATABASE.

    Returns:
        json : json mapping database columns names to the corresponding values in the movie if possible else
        HTTPException: 404

    """
    c = conn.cursor()
    sql_request = f"SELECT {', '.join([ID]+list(COLUMNS_DATABASE.keys()))} FROM movies WHERE {ID}==?"
    #'SELECT '+', '.join([ID]+list(COLUMNS_DATABASE.keys())) +' FROM movies WHERE '+ID+'==?'
    res = c.execute(sql_request, (movie_id,)).fetchall()

    if len(res) != 1:
        abort(404)
    else:
        movie_dict = from_db_row_to_dict(res[0])
    return jsonify(movie_dict)


def from_multiple_db_rows_to_dict(multiple_db_rows, ID=ID):
    """_summary_
        Get a multiple rows of the database as a list of tuple and return a corresponding dict object
    Args:
        multiple_db_rows (list of tuple): Get a multiple rows of the database as a list of tuple

    Returns:
        dict:
            'count': Total number of rows (int)
            'movies': dictionnary mapping id (int) to the corresponding movies
    """
    all_movies = dict()
    all_movies["count"] = 0
    movies_list = [from_db_row_to_dict(movie) for movie in multiple_db_rows]
    all_movies["movies"] = dict(zip([movie[ID] for movie in movies_list], movies_list))
    all_movies["count"] = len(all_movies["movies"])
    return all_movies


def check_genres_exist(genres, genres_all=genres_all):
    return all([g in genres_all for g in genres])


def get_fields_from_form(form):
    title = form["title"]
    description = form["description"]
    genres = form.getlist("genres")
    release_date = form["release_date"]
    vote_average = form["vote_average"]
    vote_count = form["vote_count"]
    return (title, description, genres, release_date, vote_average, vote_count)


def check_fields(fields):
    title, description, genres, release_date, vote_average, vote_count = fields
    title_check = type(title) == str
    description_check = type(description) == str
    genres_check = check_genres_exist(genres)
    try:
        _ = datetime.date.fromisoformat(release_date)
        date_check = True
    except:
        date_check = False
    try:
        vote_average_check = float(vote_average) >= 0.0 and float(vote_average) <= 10.0
    except:
        vote_average_check = False
    try:
        vote_count_check = int(vote_count) > 0
    except:
        vote_count_check = False
    return (
        title_check
        and description_check
        and genres_check
        and date_check
        and vote_average_check
        and vote_count_check
    )


def modify_gender_from_fields(fields):
    title, description, genres, release_date, vote_average, vote_count = fields
    genres = ", ".join(genres)
    return (title, description, genres, release_date, vote_average, vote_count)


def add_new_id_to_field(fields, new_id):
    title, description, genres, release_date, vote_average, vote_count = fields
    return (
        new_id,
        title,
        description,
        genres,
        release_date,
        vote_average,
        vote_count,
    )


def generate_new_id(conn):
    c = conn.cursor()
    ids = [elt[0] for elt in c.execute("SELECT id FROM movies").fetchall()]
    # new_id = max([elt for elt in ids if type(elt)==int ])+1
    new_id = int(max(ids) + 1)
    return new_id


def delete_movie_from_id(movie_id, conn):
    """
        Delete the movie corresponding to movie id in the database
        conn (sqlite3.Connection): sqlite3.Connection of the database
    Args:
        movie_id (int): Id of a movie in the database

    Returns:
        HTTPException: 404 or 202 if the deletion fails
    """
    c = conn.cursor()
    c.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
    conn.commit()
    print(c.rowcount)
    if c.rowcount == 1:
        return Response("", status=204)
    else:
        abort(404)


def is_movie_not_existing(conn, movie_id):
    c = conn.cursor()
    res = c.execute(
        "SELECT EXISTS(SELECT * FROM movies WHERE id==?)", (movie_id,)
    ).fetchall()
    return res[0][0] != 1


def is_all_keys_in_json(request):
    return all([key in COLUMNS_DATABASE for key in request.keys()])


def check_request_type(updated_movie):
    if "vote_average" in updated_movie:
        try:
            type(updated_movie["vote_average"]) == float
        except:
            return {}
    if "vote_count" in updated_movie:
        try:
            type(updated_movie["vote_count"]) == int
        except:
            return {}
    if "genres" in updated_movie:
        try:
            updated_movie["genres"] = ", ".join(updated_movie["genres"])
        except:
            return {}
    return updated_movie


def send_put_request(conn, updated_movie, movie_id):
    sql_request = (
        f"UPDATE movies SET {' = ? ,'.join(updated_movie.keys())} = ? WHERE id = ?"
    )
    values_request = tuple(list(updated_movie.values()) + [movie_id])
    c = conn.cursor()
    c.execute(
        sql_request,
        values_request,
    )
    conn.commit()
