import pandas as pd
MAX_ROWS = 10
pd.set_option('display.max_rows', MAX_ROWS)
pd.set_option('display.max_columns', 20)
pd.set_option('display.max_colwidth', 200)
pd.set_option('display.width', 1000)
import psycopg2 # PostgreSQL database connector



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
rows = cursor.fetchall()
column_names = [desc[0] for desc in cursor.description]
df = pd.DataFrame(rows, columns=column_names)
print("\n\nList All Table(s):")
print(df)

# Insert Data into the Table
cursor.execute(f"""
    INSERT INTO {table_name} (name, age)
    VALUES ('Alice', 30), ('Bob', 25), ('Will', 35);
""")
conn.commit()
print(f'\n\nInserted data into table: "{table_name}"')

# # Read Data from the Table
# # Method 1: Using cursor (manual approach)
# cursor.execute(f"SELECT * FROM {table_name};")
# rows = cursor.fetchall()
# column_names = [desc[0] for desc in cursor.description]
# df = pd.DataFrame(rows, columns=column_names)
# Method 2: Direct pandas approach (alternative)
df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
print(f'\n\nRead (aka SELECT) data from table: "{table_name}"')
print(df)

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


