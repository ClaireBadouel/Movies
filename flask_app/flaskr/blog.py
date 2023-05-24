from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
    jsonify,
)
from werkzeug.exceptions import abort
from flaskr.db import get_db
from flaskr.utils import *
import datetime

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


@bp.route("/movies/<int:movie_id>", methods=("GET", "DELETE", "PUT"))
def show_OR_delete_OR_update_movie(movie_id):
    if request.method == "GET":
        """
            Get a movie id (int) and return a corresponding JSON response object
        Args:
            movie_id (int): Id of a movie in the database

        Returns:
            JSON response object: corresponding json mapping database columns names
            to the corresponding values in the movie
        """
        with get_db() as conn:
            res = get_movie_from_id_as_dict(movie_id, conn)
            return jsonify(res)

    if request.method == "DELETE":
        """
            Delete the movie corresponding to movie id in the database
        Args:
            movie_id (int): Id of a movie in the database

        Returns:
            HTTPException: 404 or 202 if the deletion fails
        """
        with get_db() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
            conn.commit()
            if c.rowcount == 1:
                return "", 204
            else:
                abort(404)

    if request.method == "PUT":
        with get_db() as conn:
            c = conn.cursor()
            if request.method == "PUT":
                res = c.execute(
                    "SELECT EXISTS(SELECT * FROM movies WHERE id==?)", (movie_id,)
                ).fetchall()
                if res[0][0] != 1:
                    abort(404)
                else:
                    if all([key in COLUMNS_DATABASE for key in request.json.keys()]):
                        # all the keys of the json should be columns name of the database /!\ except id /!\
                        if "vote_average" in request.json:
                            try:
                                _ = float(request.json.get("vote_average"))
                            except:
                                return abort(404)
                        if "vote_count" in request.json:
                            try:
                                _ = int(request.json.get("vote_count"))
                            except:
                                return abort(404)
                        # sql_request = 'UPDATE movies SET ' + ' = ? ,'.join(request.json.keys())+' = ? WHERE id = ?'
                        sql_request = f"UPDATE movies SET {' = ? ,'.join(request.json.keys())} = ? WHERE id = ?"
                        # return([sql_request, tuple(list(request.json.values())+[str(movie_id)])])
                        values_request = tuple(list(request.json.values()) + [movie_id])
                        c.execute(sql_request, values_request)
                        conn.commit()
                        return redirect(f"/movies/{movie_id}")
                    else:
                        return abort(404)


@bp.route("/movies", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        # get value from post
        title = request.form["title"]
        description = request.form["description"]
        genres = request.form.getlist("genres")
        release_date = request.form["release_date"]
        vote_average = request.form["vote_average"]
        vote_count = request.form["vote_count"]

        # check values
        title_check = type(title) == str
        description_check = type(description) == str
        genres_check = check_genres_exist(genres)
        try:
            _ = datetime.date.fromisoformat(release_date)
            date_check = True
        except:
            date_check = False
        try:
            vote_average_check = (
                float(vote_average) >= 0.0 and float(vote_average) <= 10.0
            )
        except:
            vote_average_check = False
        try:
            vote_count_check = int(vote_count) > 0
        except:
            vote_count_check = False

        if (
            title_check
            and description_check
            and genres_check
            and date_check
            and vote_average_check
            and vote_count_check
        ):
            genres = ", ".join(genres)

            if (
                not title
                or not description
                or not genres
                or not release_date
                or not vote_average
                or not vote_count
            ):
                abort(404)
            else:
                with get_db() as conn:
                    c = conn.cursor()
                    ids = [
                        elt[0] for elt in c.execute("SELECT id FROM movies").fetchall()
                    ]
                    # new_id = max([elt for elt in ids if type(elt)==int ])+1
                    new_id = max(ids) + 1
                    sql = """INSERT INTO movies 
                    (id, title, description, genres, release_date, vote_average, vote_count) 
                    VALUES(?, ?, ?, ?, ?, ?, ?)"""
                    print(new_id)
                    c.execute(
                        sql,
                        (
                            new_id,
                            title,
                            description,
                            genres,
                            release_date,
                            vote_average,
                            vote_count,
                        ),
                    )
                    conn.commit()
                    # return(redirect('/movies/'+str(new_id)))
                    return redirect(f"/movies/{new_id}")
        else:
            return [
                title_check,
                description_check,
                genres_check,
                date_check,
                vote_average_check,
                vote_count_check,
                vote_average,
                vote_count,
            ]
            abort(404)
    return render_template("blog/create_movie.html")


@bp.get("/movies/<string:search_term>")
def get_all_movies_with_word(search_term, COLUMNS_SEARCHED=["title", "description"]):
    with get_db() as conn:
        c = conn.cursor()
        # "SELECT "+", ".join([ID]+list(COLUMNS_DATABASE.keys())) +" FROM movies WHERE title like '%"+search_term+"%' AND description like '%"+search_term+"%';"
        sql_request = f"SELECT {', '.join([ID]+list(COLUMNS_DATABASE.keys())) } FROM movies WHERE title like '%{search_term}%' OR description like '%{search_term}%';"
        res = c.execute(sql_request).fetchall()
    all_movies = from_multiple_db_rows_to_dict(res)
    return jsonify(all_movies)


# http://127.0.0.1:5000/movies/?genre=Comedy&after=2000-01-01&vote_average=6
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
            sql_request = f"""SELECT {
                                        ', '.join([ID]+list(COLUMNS_DATABASE.keys())) 
                                    } FROM movies WHERE {
                                        ' AND '.join(like_request)
                                    };"""
            res = c.execute(sql_request).fetchall()
        all_movies = from_multiple_db_rows_to_dict(res)
        return jsonify(all_movies)
        return sql_request
    else:
        abort(404)
