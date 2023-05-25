import os
import datetime
import json


# CONFIG_FILE_PATH = ''
# Load the config
with open(os.path.join("tests", "configtest.json"), "r") as config_file:
    config_data = json.load(config_file)

# Set environment variable from the dict config_data['DATABASE']
for GLOB_VAR in config_data["TEST_INPUT"].keys():
    exec(f"{GLOB_VAR}=config_data['TEST_INPUT']['{GLOB_VAR}']")

list_formdata_incorrect = [formdata_incorrect[key] for key in formdata_incorrect.keys()]


def test_GET_existing_movie(client, JSON_INPUT=JSON_INPUT):
    ID = JSON_INPUT["id"]
    response = client.get(f"/movies/{ID}")
    # the endpoint returns the expected response :
    # movie 11860 correspond to the one in the database
    assert json.loads(response.data) == JSON_INPUT

    # the endpoint returns the expected status code :
    # movie 11860 exists - expected status 200
    assert response.status_code == 200


def test_GET_non_existing_movie(client):
    # the endpoint returns the expected response when the requested resource is not found
    # movie 0 doesn't exists - expected status 404
    response = client.get("/movies/0")
    assert response.status_code == 404


def test_POST_correct_format_movies(client, formdata_correct=formdata_correct):
    # the endpoint returns the expected response
    # a movie is created and then the user is redirected to the corresponding path

    rand_number = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    formdata_correct_randomized = formdata_correct.copy()
    formdata_correct_randomized[
        "title"
    ] = f"{formdata_correct_randomized['title']} - {rand_number}"
    response = client.post(
        "/movies", data=formdata_correct_randomized, follow_redirects=True
    )
    response.request.path
    redirection = response.request.path
    redirection_response = json.loads(client.get(redirection).data)
    del redirection_response["id"]
    assert redirection_response == formdata_correct_randomized

    # the endpoint returns the expected status code :
    # movie created - expected status 200 and redirection
    assert response.status_code == 200


def test_multiple_POST_incorrect_format_movies(
    client, list_formdata_incorrect=list_formdata_incorrect
):
    for one_formdata_incorrect in list_formdata_incorrect:
        print(one_formdata_incorrect)
        response = client.post("/movies", data=one_formdata_incorrect)
        print(response.status_code)
        assert response.status_code == 400
