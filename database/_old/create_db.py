import sqlite3
import pandas as pd
import os
import ast

DB_NAME = "movies.db"
DB_PATH = "database"
CSV_NAME = "movies_metadata.csv"

# Columns in the sqlite database and their corresponding types
COLUMNS_DATABASE = {
    'id':'int',
    'title':'text',
    'description':'text',
    'genres':'text',
    'release_date':'text',
    'vote_average':'real',
    'vote_count':'int',
    }

"""
Values of this dict are strings describing the type of the columns (name of the .db)
can be 'str' 
or 
Can be ‘integer’, ‘signed’, ‘unsigned’, or ‘float’ (downcast arg of pandas.to_numeric)
"""
COLUMNS_CSV_type = {
    'id':'integer',
    'title':'str',
    'description':'str',
    'genres':'str',
    'release_date':'str',
    'vote_average':'float',
    'vote_count':'integer',
    }

# ID used for the database
ID = 'id'

# columns in the CSV and their corresponding name in the sqlite database
COLUMNS_CSV = {
    'id':'id',
    'title':'title',
    'overview':'description',
    'genres':'genres',
    'release_date':'release_date',
    'vote_average':'vote_average',
    'vote_count':'vote_count',
    }

def create_base(DB_NAME=DB_NAME, DB_PATH=DB_PATH, CSV_NAME=CSV_NAME, COLUMNS_DATABASE=COLUMNS_DATABASE, COLUMNS_CSV=COLUMNS_CSV):
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
    conn = sqlite3.connect(os.path.join(DB_PATH, DB_NAME))
    c = conn.cursor()
    print(os.path.join(DB_PATH, DB_NAME), 'is created')

    # create a movies table
    c.execute(
        'CREATE TABLE IF NOT EXISTS movies ('+', '.join([k+' '+COLUMNS_DATABASE[k] for k in COLUMNS_DATABASE.keys()])+')'
        )

    # Load CSV into sqlite table
    CSV_DATA.to_sql('movies', conn, if_exists='append', index = False)
    c.execute('''SELECT * FROM movies''').fetchall()
    
if __name__ == '__main__':
    create_base()