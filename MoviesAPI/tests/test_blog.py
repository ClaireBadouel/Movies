import pytest
from movies_package.db import get_db
import json
from html.parser import HTMLParser
import datetime
import os
from helpers.test_utils import *

# CONFIG_FILE_PATH = ''
# Load the config
with open(os.path.join("tests", "configtest.json"), "r") as config_file:
    config_data = json.load(config_file)

# Set environment variable from the dict config_data['DATABASE']
for GLOB_VAR in config_data["TEST_INPUT"].keys():
    exec(f"{GLOB_VAR}=config_data['TEST_INPUT']['{GLOB_VAR}']")

# the endpoint returns the expected response
# the endpoint returns the expected status code
# the endpoint returns the expected response when the request is invalid
# the endpoint returns the expected response when the requested resource is not found


def test_GET_movies_ID(client, JSON_INPUT=JSON_INPUT):
    ######################## Expected behavior ########################
    # Return the movie with the given id or a 404 error if not found
    ###################################################################
    # the endpoint returns the expected response :
    # movie 11860 correspond to the one in the database
    # and
    # the endpoint returns the expected status code
    # movie 11860 exists - expected status 200
    test_GET_existing_movie(client)

    # the endpoint returns the expected response when the requested resource is not found
    # movie 0 doesn't exists - expected status 404
    test_GET_non_existing_movie(client)


def test_POST_movies(client):
    ######################## Expected behavior ########################
    # Create a new movie. The body of the request must be a JSON object
    # representing the movie to create. The id field must not be set in
    # the request body. Return the created movie with its id, or a 400
    # error with an explicit error message if the request body is invalid.
    ###################################################################

    # the endpoint returns the expected response
    # a movie is created and then the user is redirected to the corresponding path
    # and
    # the endpoint returns the expected status code :
    # movie created - expected status 200 and redirection
    test_POST_correct_format_movies(client)

    # the endpoint returns the expected response when the request is invalid
    # invalid form - expected status 404
    test_multiple_POST_incorrect_format_movies(client)
