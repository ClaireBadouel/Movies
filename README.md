# Movies

Make flask_app your working directory :

cd my_path_to_flask_app\flask_app\

#Create and setup an python env

how to create the virtual environment: 

Unix/Mac : 

python3 -m pip install --user virtualenv

python3 -m venv env

source env/bin/activate

Windows : 

py -m pip install --user virtualenv

py -m venv env

.\env\Scripts\activate

When env activated, install requirement.txt :
pip install -r requirements.txt

# Create the database 
Fill the flask_app/config.json
flask --app flaskr init-db        
