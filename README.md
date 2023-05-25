# Movies

Make flask_app your working directory :
```bash
cd ./flask_app
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
http PUT localhost:5000/movies/862 title='new title'

# Create the database 

Fill the flask_app/config.

```bash
flask --app flaskr init-db        
```
Run the API
```bash
flask --app flaskr run --debug    
```

# http://127.0.0.1:5000/movies/?genre=Comedy&after=2000-01-01&vote_average=6
#http PUT localhost:5000/movies/movie_id *args=values
#http PUT localhost:5000/movies/862 title='new title'