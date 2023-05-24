import os
import json
from flask import abort

# CONFIG_FILE_PATH = ''
# Load the config
with open(os.path.join("flaskr", "config.json"), "r") as config_file:
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


def get_movie_from_id_as_dict(movie_id, conn, ID=ID, COLUMNS_DATABASE=COLUMNS_DATABASE):
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
        dict : dict mapping database columns names to the corresponding values in the movie
    """
    c = conn.cursor()
    sql_request = f"SELECT {', '.join([ID]+list(COLUMNS_DATABASE.keys()))} FROM movies WHERE {ID}==?"
    #'SELECT '+', '.join([ID]+list(COLUMNS_DATABASE.keys())) +' FROM movies WHERE '+ID+'==?'
    res = c.execute(sql_request, (movie_id,)).fetchall()

    if len(res) != 1:
        abort(404)
    else:
        movie_dict = from_db_row_to_dict(res[0])
    return movie_dict


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


def get_movie_from_id_as_dict(movie_id, conn, ID=ID, COLUMNS_DATABASE=COLUMNS_DATABASE):
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
        dict : dict mapping database columns names to the corresponding values in the movie
    """
    c = conn.cursor()
    sql_request = f"SELECT {', '.join([ID]+list(COLUMNS_DATABASE.keys()))} FROM movies WHERE {ID}==?"
    #'SELECT '+', '.join([ID]+list(COLUMNS_DATABASE.keys())) +' FROM movies WHERE '+ID+'==?'
    res = c.execute(sql_request, (movie_id,)).fetchall()

    if len(res) != 1:
        abort(404)
    else:
        movie_dict = from_db_row_to_dict(res[0])
    return movie_dict


def from_multiple_db_rows_to_dict(multiple_db_rows):
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
    all_movies["count"] = len(multiple_db_rows)
    ids = [movie[0] for movie in multiple_db_rows]
    all_movies["movies"] = dict(
        zip(ids, [from_db_row_to_dict(movie) for movie in multiple_db_rows])
    )
    return all_movies


def check_genres_exist(genres, genres_all=genres_all):
    return all([g in genres_all for g in genres])
