# SQL Utilities


<details open>
<summary>Description</summary>

example usage of the following python SQL libraries:
 - mysql-connector-python
 - cx-Oracle
 - psycopg2

shows how to:
 - connect/disconnect to a SQL database
 - run arbitrary SQL queries/commands

to run the test you must:
 - set up a sql db, give it a table called eam_assets with columns:
    - asset_id, provider_id, description
 - in the tests/libraries_and_constants.py file, enter the:
    - TEST_HOSTNAME, TEST_PORT, TEST_USERNAME, TEST_PASSWORD, TEST_DATABASE
    - tested with Python version 3.13.5 and library versions in requirements.txt

</details>

<details>
<summary> Linux Postgresql Setup </summary>
    ```
    
    sudo pacman -S postgresql # install postgresql
    sudo systemctl start postgresql
    sudo systemctl status postgresql

    # create example 'admin' superuser w/ password 'password'
    sudo -u postgres psql
        CREATE ROLE admin WITH LOGIN PASSWORD 'password';
        ALTER ROLE admin CREATEDB;
        ALTER ROLE admin WITH SUPERUSER;

    # update config file to require password from databases at localhost
    # by changing "trust" to "md5" in METHOD column
    sudo nano /var/lib/postgresql/17/main/pg_hba.conf
    ```
</details>

<details>
<summary>Sources</summary>

MySQL Connector/Python Docs
https://github.com/mysql/mysql-connector-python

Oracle Database Connection in Python
 - cx_Oracle lib requires Oracle Client libraries
    - download the Basic one
       - https://www.oracle.com/database/technologies/instant-client.html
 - and add it to your path:
    - C:\oracle\instantclient_19_10
 - https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html
https://www.geeksforgeeks.org/oracle-database-connection-in-python/

PostgreSQL Connector
https://pypi.org/project/psycopg2/

</details>

#### TO DO
```
	
	create optional argument in select query function to save
	the results to a file, and another argument to read from
	a file if it exists
		this will be helpful in only running long lasting queries once

	create function to run update queries, and test it
		function created, it just needs to be tested and documented

```
