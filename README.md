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
# Create the database 

Fill the flask_app/config.

```bash
flask --app flaskr init-db        
```
