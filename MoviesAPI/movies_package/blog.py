from flask import (
    Blueprint,
    g,
    redirect,
    render_template,
    request,
    jsonify,
)
from werkzeug.exceptions import abort
from movies_package.db import get_db
import movies_package.utils as utils
import datetime
import json
import os

bp = Blueprint("blog", __name__)


# class MovieRepository:
#     def __init__(self, conn):
#         self.conn = conn

#     def findMovieById(self, movie_id: int):
#         return get_movie_from_id_as_dict(movie_id, self.conn)


# class FakeMovieRepository:
#     def __init__(self, conn):
#         pass

#     def findMovieById(self, movie_id: int):
#         return {"id": 123}

# Load the config
with open(os.path.join("movies_package", "config.json"), "r") as config_file:
    config_data = json.load(config_file)

# Set environment variable from the dict config_data['DATABASE']
for GLOB_VAR in config_data["DATABASE"].keys():
    exec(f"{GLOB_VAR}=config_data['DATABASE']['{GLOB_VAR}']")


@bp.route("/movies/<int:movie_id>", methods=("GET", "DELETE", "PUT"))
def handle_movie(movie_id):
    if request.method == "GET":
        with get_db() as conn:
            # res = get_movie_from_id(movie_id, conn)
            return utils.get_movie_from_id(movie_id, conn)
        # jsonify(res)

    if request.method == "DELETE":
        with get_db() as conn:
            return utils.delete_movie_from_id(movie_id, conn)

    if request.method == "PUT":
        with get_db() as conn:
            if utils.is_movie_not_existing(conn, movie_id):
                abort(404)
            else:
                if utils.is_all_keys_in_json(request.json):
                    # all the keys of the json should be columns name of the database /!\ except id /!\
                    updated_movie = utils.check_request_type(request.json.copy())
                    if updated_movie == {}:
                        return abort(400, "Request body is invalid")
                    else:
                        utils.send_put_request(conn, updated_movie, movie_id)
                        return redirect(f"/movies/{movie_id}")
                else:
                    return abort(400, "Request body is invalid")


@bp.route("/movies", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        # get value from post
        fields = utils.get_fields_from_form(request.form)

        if utils.check_fields(fields):
            fields = utils.modify_gender_from_fields(fields)

            with get_db() as conn:
                c = conn.cursor()

                new_id = utils.generate_new_id(conn)

                fields = utils.add_new_id_to_field(fields, new_id)

                sql = """INSERT INTO movies 
                (id, title, description, genres, release_date, vote_average, vote_count) 
                VALUES(?, ?, ?, ?, ?, ?, ?)"""

                c.execute(
                    sql,
                    fields,
                )

                conn.commit()

                # return(redirect('/movies/'+str(new_id)))
                return redirect(f"/movies/{new_id}")
        else:
            abort(400, "Field(s) type incorrect")
    return render_template("blog/create_movie.html")


@bp.get("/movies/<string:search_term>")
def get_all_movies_with_word(search_term, COLUMNS_SEARCHED=["title", "description"]):
    with get_db() as conn:
        c = conn.cursor()
        # "SELECT "+", ".join([ID]+list(COLUMNS_DATABASE.keys())) +" FROM movies WHERE title like '%"+search_term+"%' AND description like '%"+search_term+"%';"
        sql_request = f"SELECT {', '.join([ID]+list(COLUMNS_DATABASE.keys())) } FROM movies WHERE title like '%{search_term}%' OR description like '%{search_term}%';"
        res = c.execute(sql_request).fetchall()
    all_movies = utils.from_multiple_db_rows_to_dict(res)
    return jsonify(all_movies)


@bp.get("/movies/")
def api_filter():
    query_parameters = request.args
    like_request = []
    if all(
        [
            key in ["genre", "before", "after", "vote_average"]
            for key in query_parameters.keys()
        ]
    ):
        if "genre" in query_parameters.keys():
            genres = query_parameters.get("genre")
            like_request.append(f"genres like '%{genres}%'")

        if "before" in query_parameters.keys():
            before = query_parameters.get("before")
            try:
                _ = datetime.date.fromisoformat(before)
            except:
                abort(404)
            like_request.append(f"release_date <= date('{before}')")

        if "after" in query_parameters.keys():
            after = query_parameters.get("after")
            try:
                _ = datetime.date.fromisoformat(after)
            except:
                abort(404)
            like_request.append(f"release_date >= date('{after}')")

        if "vote_average" in query_parameters.keys():
            vote_average = float(query_parameters.get("vote_average"))
            if vote_average >= 0 and vote_average <= 10:
                like_request.append(f"vote_average >= {vote_average}")
            else:
                abort(404)

        with get_db() as conn:
            c = conn.cursor()
            # "SELECT "+", ".join([ID]+list(COLUMNS_DATABASE.keys())) +" FROM movies WHERE title like '%"+search_term+"%' AND description like '%"+search_term+"%';"
            if len(like_request) > 0:
                sql_request = f"""SELECT {
                                            ', '.join([ID]+list(COLUMNS_DATABASE.keys())) 
                                        } FROM movies WHERE {
                                            ' AND '.join(like_request)
                                        };"""
            else:
                sql_request = f"""SELECT {
                            ', '.join([ID]+list(COLUMNS_DATABASE.keys())) 
                        } FROM movies ;"""

            res = c.execute(sql_request).fetchall()
        all_movies = utils.from_multiple_db_rows_to_dict(res)
        return jsonify(all_movies)
        return sql_request
    else:
        abort(404)
