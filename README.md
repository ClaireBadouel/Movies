# MoviesAPI

# Overview
The goal of this project is to create a REST API to manage movies. The API must be built with Python, and
(recommended) any framework of your choice. The project must include a database to store the movies and
reviews. The API must be able to:
• Create, update, delete, and get movies
• Get a list of movies
• Search for movies by keywords in the title or description
• For the list and search endpoints: filter by genre, date, and rating.
# Guidelines for implementation
• Language: Flask
• Database: SQLite.
• Environment: requirements.txt file listing the required packages. The project is runnable in a virtual environment. The project is in development mode.
• Documentation: The API is documented using Swagger documentation format. The project include a README file that explains how to run the project.
• Tests: The project include unit tests. The tests are runnable with a single command

# Install the API

## Creation of virtual environments

- **Installation for Windows** 

Make MoviesAPI your working directory :
```
cd ./MoviesAPI
```
Create the virtual environment: 

```bash
py -m pip install --user virtualenv
py -m venv env
.\env\Scripts\activate
```


 - **Installation for Unix/Mac**

Make MoviesAPI your working directory :
```bash
cd ./MoviesAPI
```
Create the virtual environment: 

```bash
python3 -m pip install --user virtualenv
python3 -m venv env
source env/bin/activate
```


## Set up your virtual environments

Install requirement.txt :
```bash
pip install -r requirements.txt
```

Install MoviesAPI
```bash
pip install -e .
```

## Create the database 

Fill the `MoviesAPI/config`


```bash
flask --app movies_package init-db        
```
**This command reset completely the database if existing**

# Run the API
```bash
flask --app movies_package run --debug    
```

# Run the test : 
```bash
flask --app movies_package init-db
pytest
```
# MovieAPI Endpoints
## Return the Swagger Docs

Return the movie with the given id or a 404 error if not found.
### Request
```GET /```

```
http GET http://localhost:5000/
```

Response

```
HTTP/1.1 200 OK
Connection: close
Content-Length: 2239
Content-Type: application/json
Date: Fri, 26 May 2023 10:10:03 GMT
Server: Werkzeug/2.3.4 Python/3.11.3

doc
```
## Return the form to POST a movie

Return the form to POST a movie.
### Request
```GET /movies```

```
http GET http://localhost:5000/movies
```

Response

```
HTTP/1.1 200 OK
Connection: close
Content-Length: 2955
Content-Type: text/html; charset=utf-8
Date: Fri, 26 May 2023 10:12:28 GMT
Server: Werkzeug/2.3.4 Python/3.11.3
       
    <h1> Add a New Movie </h1>
    <form method="post">
        <label for="title">Title</label>
        <br>
        <input type="text" name="title"
               placeholder="Please enter here the title"
               value=""></input>
        <br>

        <label for="description">Post description</label>
        <br>
        <textarea name="description"
                  placeholder="Please enter here the description"
                  rows="5"
                  cols="200"
                  ></textarea>
        <br>

        <label for="genres">Genres</label>
        <br>
            <input type="checkbox" name="genres" value="Action">Action<br>
            <input type="checkbox" name="genres" value="Adventure">Adventure<br>
            <input type="checkbox" name="genres" value="Animation">Animation<br>
            <input type="checkbox" name="genres" value="Comedy">Comedy<br>
            <input type="checkbox" name="genres" value="Crime">Crime<br>
            <input type="checkbox" name="genres" value="Documentary">Documentary<br>
            <input type="checkbox" name="genres" value="Drama">Drama<br>
            <input type="checkbox" name="genres" value="Family">Family<br>
            <input type="checkbox" name="genres" value="Fantasy">Fantasy<br>
            <input type="checkbox" name="genres" value="Foreign">Foreign<br>
            <input type="checkbox" name="genres" value="History">History<br>
            <input type="checkbox" name="genres" value="Music">Music<br>
            <input type="checkbox" name="genres" value="Mystery">Mystery<br>
            <input type="checkbox" name="genres" value="Romance">Romance<br>
            <input type="checkbox" name="genres" value="Science Fiction">Science Fiction<br>
            <input type="checkbox" name="genres" value="TV Movie">TV Movie<br>
            <input type="checkbox" name="genres" value="Thriller">Thriller<br>
            <input type="checkbox" name="genres" value="War">War<br>
            <input type="checkbox" name="genres" value="Western">Western<br>
        <br>

        <label for="release_date">release_date</label>
        <br>
        <input type="date" name="release_date"
               placeholder="Post release_date"
               value=""></input>
        <br>

        <label for="vote_average">Vote Average</label>
        <br>
        <input type="number" name="vote_average" min=0 max=10 step=0.1
               placeholder="Please enter here the vote average"
               value=""></input>
        <br>

        <label for="vote_count">Number of vote</label>
        <br>
        <input type="number" name="vote_count" step=1
               placeholder="Please enter here the number of vote"
               value=""></input>
        <br>

        <button type="submit">Submit</button>
    </form>
```

## POST a movie
In a navigator, go to : 
(http://localhost:5000/movies)

Fill the form and submit

## Return the movie with the given id

Return the movie with the given id or a 404 error if not found.
### Request
```GET /movies/862```

```
http GET http://localhost:5000/movies/862
```

Response

```
HTTP/1.1 200 OK
Connection: close
Content-Length: 518
Content-Type: application/json
Date: Fri, 26 May 2023 09:54:54 GMT
Server: Werkzeug/2.3.4 Python/3.11.3

{
    "description": "Led by Woody, Andy's toys live happily in his room until Andy's birthday brings Buzz Lightyear onto the scene. Afraid of losing his place in Andy's heart, Woody plots against Buzz. But when circumstances separate Buzz and Woody from their owner, the duo eventually learns to put aside their differences.",
    "genres": [
        "Animation",
        "Comedy",
        "Family"
    ],
    "id": 862,
    "release_date": "1995-10-30",
    "title": "Toy Story",
    "vote_average": 7.699999809265137,
    "vote_count": 5415
}
```

## Delete the movie with the given id

  Delete the movie with the given id. Return a 204 status code with an empty body.
  Return a 404 error if the movie is not found.

### Request
```DELETE /movies/862```

```
http DELETE http://localhost:5000/movies/862
```

Response

```
HTTP/1.1 204 NO CONTENT
Connection: close
Content-Type: text/html; charset=utf-8
Date: Fri, 26 May 2023 09:58:20 GMT
Server: Werkzeug/2.3.4 Python/3.11.3
```

## Update the movie with the given id
Update the movie with the given id. The body of the request must be a JSON object
representing the movie to update. The id field must not be set in the request body. Return the
updated movie, or a 400 error with an explicit error message if the request body is invalid.
- Return a 404 error if the movie is not found.
- Delete the movie with the given id. Return a 204 status code with an empty body.
- Return a 404 error if the movie is not found.

### Request
```PUT /movies/863```

```
http PUT http://localhost:5000/movies/863 title="Toy Story PUT" description=""
```

Response

```
HTTP/1.1 302 FOUND
Connection: close
Content-Length: 209
Content-Type: text/html; charset=utf-8
Date: Fri, 26 May 2023 10:07:56 GMT
Location: /movies/863
Server: Werkzeug/2.3.4 Python/3.11.3

<!doctype html>
<html lang=en>
<title>Redirecting...</title>
<h1>Redirecting...</h1>
<p>You should be redirected automatically to the target URL: <a href="/movies/863">/movies/863</a>. If not, click the link.
```

## Return a list of movies
Return a list of movies. The response must be a JSON object with the following fields:
  * `count`: the total number of movies returned from the request
  * `movies`: an array of movies (see the movie object above)
  If no filter is provided (see below), the endpoint must return all the movies in the
database.

### Request
```GET /movies/```

```
http GET http://localhost:5000/movies/
```

Response
```
HTTP/1.1 200 OK
Connection: close
Content-Length: 26343651
Content-Type: application/json
Date: Fri, 26 May 2023 10:29:58 GMT
Server: Werkzeug/2.3.4 Python/3.11.3

list of all movies
```

## Return a list of movies
Return a list of movies. The response must be a JSON object with the following fields:
  * `count`: the total number of movies returned from the request
  * `movies`: an array of movies (see the movie object above)
  If no filter is provided (see below), the endpoint must return all the movies in the
database.

### Request
```GET /movies/```

```
http GET http://localhost:5000/movies/
```

Response
```
HTTP/1.1 200 OK
Connection: close
Content-Length: 26343651
Content-Type: application/json
Date: Fri, 26 May 2023 10:29:58 GMT
Server: Werkzeug/2.3.4 Python/3.11.3

list of all movies
```


## Return a list of movies matching the given search term

Return a list of movies matching the given search term. The response must be a JSON object
with the following fields:
  * `count`: the total number of movies returned from the request
  * `movies`: an array of movies (see the movie object above)
  You're expected to implement the search against a single word in the title or description of the movie (so `term` is a single word, not a sentence). The search must be case-insensitive and must match the exact search term, found in the title or description of the movie.
  * `count`: the total number of movies returned from the request
  * `movies`: an array of movies (see the movie object above)
  If no filter is provided (see below), the endpoint must return all the movies in the database.

### Request
```GET /movies/search/<term>```

or

```GET /movies/search/<term>```

```
http GET http://localhost:5000/movies/Nordham
```

Response
```
HTTP/1.1 200 OK
Connection: close
Content-Length: 675
Content-Type: application/json
Date: Fri, 26 May 2023 10:39:10 GMT
Server: Werkzeug/2.3.4 Python/3.11.3

{
    "count": 1,
    "movies": {
        "39929": {
            "description": "When Hamilton High's Prom Queen of 1957, Mary Lou Maloney is killed by her jilted boyfriend, she comes back for revenge 30 years later. Bill Nordham is now the principle of Hamilton High and his son is about to attend the prom with Vicki Carpenter. However, she is possessed by Mary Lou Maloney after opening a trunk in the school's basement. Now Bill must face the horror he left behind in 1957.",   
            "genres": [
                "Horror"
            ],
            "id": 39929,
            "release_date": "1987-11-13",
            "title": "Hello Mary Lou: Prom Night II",
            "vote_average": 6.0,
            "vote_count": 35
        }
    }
}
```