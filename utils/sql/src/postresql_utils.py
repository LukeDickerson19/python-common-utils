# LIBRARIES

# import standard libraries
import os
import sys
import pathlib

# import non-standard libraries
import numpy as np
import pandas as pd
MAX_ROWS = 10
pd.set_option('display.max_rows', MAX_ROWS)
pd.set_option('display.max_columns', 20)
pd.set_option('display.max_colwidth', 200)
pd.set_option('display.width', 1000)
import psycopg2 # PostgreSQL database connector
from datetime import datetime

# import common utils
COMMON_UTILS_REPO_PATH = str(pathlib.Path(__file__).resolve().parent.parent.parent.parent)
LOG_UTIL_PATH          = os.path.join(COMMON_UTILS_REPO_PATH, 'utils', 'logging', 'src')
sys.path.append(LOG_UTIL_PATH)
import logging_utils
# print('COMMON_UTILS_REPO_PATH\t', COMMON_UTILS_REPO_PATH)
# print('LOG_UTIL_PATH\t\t', LOG_UTIL_PATH)
# sys.exit()



# CONSTANTS

# Connect to PostgreSQL
# default database is 'postgres'
# 
HOSTNAME = 'localhost'
PORT     = '5432'
USERNAME = 'admin'
PASSWORD = 'password'
DATABASE = 'postgres'
# conn = psycopg2.connect(
#     dbname=DATABASE,
#     user=USERNAME,
#     password=PASSWORD,
#     host=HOSTNAME,
#     port=PORT,
# )
CONNECTION_STRING = f"postgresql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}"
conn = psycopg2.connect(CONNECTION_STRING)
conn.autocommit = True  # Required for database creation
cursor = conn.cursor()
print(f'\n\nConnected to database "{DATABASE}"')
print(type(conn))
print(conn)

# Create a new database
dbname = 'my_database'
cursor.execute(f"DROP DATABASE IF EXISTS {dbname};")
cursor.execute(f"CREATE DATABASE {dbname};")
print(f'\n\nCreated database "{dbname}"')

# List all databases
cursor.execute("SELECT datname FROM pg_database;")
databases = cursor.fetchall()
print("\n\nList All Database(s):")
print(databases)

# Connect to newly created database: dbname
cursor.close()
conn.close()
CONNECTION_STRING = f"postgresql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{dbname}"
conn = psycopg2.connect(CONNECTION_STRING)
conn.autocommit = True
cursor = conn.cursor()
print(f'\n\nConnected to database "{dbname}"')
print(type(conn))
print(conn)

# Create a Table
table_name = 'my_table'
cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
cursor.execute(f"""
    CREATE TABLE {table_name} (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        age INT
    );
""")
conn.commit()
print(f'\n\nCreated table: "{table_name}"')

# List All Tables
cursor.execute("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public';
""")
tables = cursor.fetchall()
print("\n\nList All Table(s):")
print(tables)

# Insert Data into the Table
cursor.execute(f"""
    INSERT INTO {table_name} (name, age)
    VALUES ('Alice', 30), ('Bob', 25), ('Will', 35);
""")
conn.commit()
print(f'\n\nInserted data into table: "{table_name}"')

# Read Data from the Table
cursor.execute(f"SELECT * FROM {table_name};")
rows = cursor.fetchall()
print(f'\n\nRead (aka SELECT) data from table: "{table_name}"')
for row in rows:
    print(row)

# Delete the Table
cursor.execute(f"DROP TABLE {table_name};")
conn.commit()
print(f'\n\nDeleted table: "{table_name}"')

# Delete the Database
cursor.close()
conn.close()
conn = psycopg2.connect(
    dbname=DATABASE,
    user=USERNAME,
    password=PASSWORD,
    host=HOSTNAME
)
conn.autocommit = True
cursor = conn.cursor()
print(f'\n\nConnected to database "{DATABASE}"')
print(type(conn))
print(conn)
cursor.execute(f"DROP DATABASE {dbname};")
print(f'\n\nDeleted database: "{dbname}"\n\n')

# Final Disconnect
cursor.close()
conn.close()


