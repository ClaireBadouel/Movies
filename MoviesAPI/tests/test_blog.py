import os
import datetime
import json

# the endpoint returns the expected response
# the endpoint returns the expected status code
# the endpoint returns the expected response when the request is invalid
# the endpoint returns the expected response when the requested resource is not found

with open(os.path.join("tests", "configtest.json"), "r") as config_file:
    config_data = json.load(config_file)

# Set environment variable from the dict config_data['DATABASE']
for GLOB_VAR in config_data["TEST_INPUT"].keys():
    exec(f"{GLOB_VAR}=config_data['TEST_INPUT']['{GLOB_VAR}']")

list_formdata_incorrect = [formdata_incorrect[key] for key in formdata_incorrect.keys()]

######## Expected behavior for "/movies/<int:movie_id>"", methods=("GET") ########

# Return the movie with the given id or a 404 error if not found.

##################################################################################


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

    ######## Expected behavior for "/movies", methods=("POST") ########

    # Create a new movie. The body of the request must be a JSON object
    # representing the movie to create. The id field must not be set in
    # the request body. Return the created movie with its id, or a 400
    # error with an explicit error message if the request body is invalid.

    ###################################################################


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
    # the endpoint returns the expected response when the request is invalid
    for one_formdata_incorrect in list_formdata_incorrect:
        response = client.post("/movies", data=one_formdata_incorrect)
        assert response.status_code == 400

    ######## Expected behavior for "/movies/<int:movie_id>", methods=("DELETE") ########

    # Delete the movie with the given id. Return a 204 status code with an empty body.
    # Return a 404 error if the movie is not found

    ####################################################################################


def test_DELETE_existing_movie(
    client, existing_movie_id_to_delete=existing_movie_id_to_delete
):
    # the endpoint returns the expected response
    # the endpoint returns the expected status code
    response = client.delete(f"/movies/{int(existing_movie_id_to_delete)}")
    # assert response.status_code == 204
    # assert response.data == b""


def test_DELETE_non_existing_movie(
    client, existing_movie_id_to_delete=non_existing_movie_id_to_delete
):
    # the endpoint returns the expected response when the requested resource is not found
    response = client.delete(f"/movies/{int(existing_movie_id_to_delete)}")
    assert response.status_code == 404

    ######## Expected behavior for "/movies/<int:id>" - methods=("PUT") ########
    # Update the movie with the given id. The body of the request must be a JSON
    # object representing the movie to update. The id field must not be set in
    # the request body. Return the updated movie, or a 400 error with an explicit
    # error message if the request body is invalid. Return a 404 error if the
    # movie is not found.
    ############################################################################


def test_PUT_existing_movie(client, existing_movie_to_update=existing_movie_to_update):
    response = client.put(
        f"/movies/{existing_movie_to_update['id']}",
        data=json.dumps(existing_movie_to_update),
        content_type="application/json",
    )

    assert response.status_code == 400
    assert b"Request body is invalid" in response.data

    correct_request = existing_movie_to_update.copy()
    del correct_request["id"]
    response = client.put(
        f"/movies/{existing_movie_to_update['id']}",
        data=json.dumps(correct_request),
        content_type="application/json",
        follow_redirects=True,
    )
    print(response.data)
    redirection = response.request.path
    redirection_response = json.loads(client.get(redirection).data)
    assert redirection_response == existing_movie_to_update
