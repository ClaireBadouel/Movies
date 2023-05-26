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
# Run the API
```bash
flask --app movies_package run --debug    
```

# Run the test : 
```bash
flask --app movies_package init-db
pytest
```
