from flask import Flask
from . import blog
from . import db


def create_app(test_config=None):
    app = Flask(__name__, template_folder="templates")
    app.json.sort_keys = False

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    db.init_app(app)
    app.register_blueprint(blog.bp)
    app.add_url_rule(
        "/movies/<int:movie_id>",
        "handle_movie",
        methods=["GET", "DELETE", "PUT"],
    )
    app.add_url_rule("/movies", "create", methods=["GET", "POST"])
    app.add_url_rule(
        "/movies/<string:search_term>", "get_all_movies_with_word", methods=["GET"]
    )
    app.add_url_rule("/movies/", "api_filter", methods=["GET"])

    return app
