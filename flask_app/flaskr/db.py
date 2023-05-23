import sqlite3
import pandas as pd
import os
import ast
import click
from flask import current_app, g
import json 

#CONFIG_FILE_PATH = ''
#Load the config 
with open(os.path.join('flaskr','config.json'), 'r') as config_file:
    config_data = json.load(config_file)
#Set environment variable from the dict config_data['DATABASE']
for GLOB_VAR in config_data['DATABASE'].keys():
    exec(f"{GLOB_VAR}=config_data['DATABASE']['{GLOB_VAR}']")

def get_db(DB_PATH=DB_PATH, DB_NAME=DB_NAME):
    if 'db' not in g:
        g.db = sqlite3.connect(
            os.path.join(DB_PATH, f"{DB_NAME}.db")
        )
        
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
        
def init_db(
    DB_NAME=DB_NAME, DB_PATH=DB_PATH, 
    CSV_NAME=CSV_NAME, COLUMNS_DATABASE=COLUMNS_DATABASE_SQLITE, 
    COLUMNS_CSV_type=COLUMNS_CSV_type, COLUMNS_CSV=COLUMNS_CSV, 
    ID=ID
    ):
    """
    Create the database sqlite3 from the csv file, keep desired columns, set desired types, delete Nan index

    Args:
        DB_NAME (str, optional): Database desired name. Defaults to DB_NAME.
        DB_PATH (str, optional): Path to the CSV file used to build the database. Defaults to DB_PATH.
        CSV_NAME (str, optional): Name of the CSV file used to build the database. Defaults to CSV_NAME.
        COLUMNS_DATABASE (dict, optional):  Dictionnary mapping columns name in the sqlite database to the 
                                            corresponding SQLITE type. Defaults to COLUMNS_DATABASE_SQLITE.
        COLUMNS_CSV_type (dict, optional):   Dictionnary mapping columns name in the CSV to the 
                                        corresponding python type. Defaults to COLUMNS_CSV.
        COLUMNS_CSV (dict, optional):   Dictionnary mapping columns name in the CSV to the 
                                        corresponding columns name in the SQLITE database. Defaults to COLUMNS_CSV.
        ID (str, optional): CSV column used as index of the database . Defaults to ID.
    """
    # Read the CSV datas and keep only the columns for sqlite db
    CSV_DATA = pd.read_csv(
        os.path.join(DB_PATH,CSV_NAME)
        )[
            COLUMNS_CSV.keys()
        ].rename(
            columns=COLUMNS_CSV
        )
    print(
        os.path.join(DB_PATH,CSV_NAME),
        ' is loaded')

    # Modify the genres column to be a list of the genres for each row
    try:
        CSV_DATA['genres'] = CSV_DATA[
            'genres'
        ].apply(
            lambda x : ', '.join(
                [x_['name'] for x_ in ast.literal_eval(x)]
                )
            )
        print('"gender" is changed to a string that is a list of genders')
    except:
        print('"gender" is not changed')
    
    #modify types errors are deleted
    for col in COLUMNS_CSV_type.keys():
        if COLUMNS_CSV_type[col]!='str':
            CSV_DATA[col] = pd.to_numeric(CSV_DATA[col], downcast = COLUMNS_CSV_type[col], errors='coerce')
            print(col, 
                ' type is set to ', 
                COLUMNS_CSV_type[col], 
                ' or value is set to Na '
            )
        else:
            CSV_DATA[col] = CSV_DATA[col].astype(str)
            print(col, 
                ' type is set to str'
            )
    
    init_row = CSV_DATA.shape[0]
    CSV_DATA = CSV_DATA.dropna(subset=ID)
    print(init_row-CSV_DATA.shape[0], ' rows are deleted because ID is NaN')
    init_row = CSV_DATA.shape[0]
    CSV_DATA = CSV_DATA.drop_duplicates()
    print(init_row-CSV_DATA.shape[0], ' rows are deleted because duplicates')

    # Create a database connection and cursor to execute queries
    conn = get_db()
    c = conn.cursor()
    print(os.path.join(DB_PATH, f"{DB_NAME}.db"), 'is created')

    # create a movies table
    c.execute(
        'CREATE TABLE IF NOT EXISTS movies ('+', '.join([k+' '+COLUMNS_DATABASE[k] for k in COLUMNS_DATABASE.keys()])+')'
        )

    # Load CSV into sqlite table
    CSV_DATA.to_sql('movies', conn, if_exists='append', index = False)
    c.execute('''SELECT * FROM movies''').fetchall()

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
