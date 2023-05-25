# Movies

Make MoviesAPI your working directory :
```bash
cd ./MoviesAPI
```

#Create and setup an python env

how to create the virtual environment: 

Unix/Mac : 

```bash
python3 -m pip install --user virtualenv
python3 -m venv env
source env/bin/activate
```

Windows : 

```powershell
py -m pip install --user virtualenv
py -m venv env
.\env\Scripts\activate
```

When env activated, install requirement.txt :
```powershell
pip install -r requirements.txt
```

Install MoviesAPI
```bash
pip install -e .
```

# Create the database 

Fill the MoviesAPI/config.

```bash
flask --app movies_package init-db        
```
Run the API
```bash
flask --app movies_package run --debug    
```

# http://127.0.0.1:5000/movies/?genre=Comedy&after=2000-01-01&vote_average=6
#http PUT localhost:5000/movies/movie_id *args=values
#http PUT localhost:5000/movies/862 title='new title'
http DELETE localhost:5000/movies/862


Run the test : 

```bash
flask --app movies_package init-db
pytest
```
