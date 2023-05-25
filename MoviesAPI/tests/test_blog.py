import pytest
from flaskr.db import get_db
import json
from html.parser import HTMLParser
import datetime

JSON_11860 = {
    "id": 11860,
    "title": "Sabrina",
    "description": "An ugly duckling having undergone a remarkable change, still harbors feelings for her crush: a carefree playboy, but not before his business-focused brother has something to say about it.",
    "genres": ["Comedy", "Romance"],
    "release_date": "1995-12-15",
    "vote_average": 6.199999809265137,
    "vote_count": 141,
}

formdata_correct = {
    "title": "Pytest title",
    "description": "description",
    "genres": ["Comedy"],
    "release_date": "2023-04-01",
    "vote_average": 0.0,
    "vote_count": 9,
}

formdata_incorrect_title = {
    "title": "Pytest title",
    "description": "description",
    "genres": ["Comedy"],
    "release_date": "2023-04-01",
    "vote_average": 0.0,
    "vote_count": 9,
}

formdata_incorrect_title = {
    "title": 9,
    "description": "description",
    "genres": ["Comedy"],
    "release_date": "2023-04-01",
    "vote_average": 0.0,
    "vote_count": 9,
}


def test_movies_idx_get(client):
    response = client.get("/movies/11860")
    # the endpoint returns the expected response :
    # movie 11860 correspond to the one in the database
    assert json.loads(response.data) == JSON_11860

    # the endpoint returns the expected status code :
    # movie 11860 exists - expected status 200
    assert response.status_code == 200

    # the endpoint returns the expected response when the request is invalid
    # None

    # the endpoint returns the expected response when the requested resource is not found
    # movie 0 doesn't exist - expected status 404
    response = client.get("/movies/0")
    assert response.status_code == 404


def test_movies_idx_post(
    client,
    formdata_correct=formdata_correct,
    formdata_incorrect_title=formdata_incorrect_title,
):
    # the endpoint returns the expected response :
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
    assert response.status_code == 200

    # the endpoint returns the expected response when the request is invalid
    # This is already assured by the form
    rand_number = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    formdata_incorrect_title_randomized = formdata_incorrect_title.copy()
    formdata_incorrect_title_randomized[
        "title"
    ] = f"{formdata_incorrect_title_randomized['title']} - {rand_number}"
    response = client.post(
        "/movies", data=formdata_incorrect_title_randomized, follow_redirects=True
    )
    print(response.status_code)

    # the endpoint returns the expected response when the requested resource is not found
    # movie 0 doesn't exist - expected status 404
    # None
