import os

from flask import Flask

import json

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, template_folder='C:/Users/clair/Projets/ICM/flask_app/flaskr/templates')
    app.json.sort_keys = False
    app.config.from_file("../config.json", load=json.load)
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    from . import db
    db.init_app(app)
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/movies/<int:movie_id>', 'show_OR_delete_OR_update_movie', methods=["GET", "DELETE", "PUT"])
    app.add_url_rule('/movies', 'create', methods=['GET', 'POST'])
    app.add_url_rule('/movies/<string:search_term>', 'get_all_movies_with_word', methods=['GET'])
    app.add_url_rule('/movies/', 'api_filter', methods=['GET'])

    return app