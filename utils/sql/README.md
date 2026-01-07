# SQL Utils


<details open>
<summary><h2>Description</h2></summary>

    example usage of the following python SQL libraries:
        mysql-connector-python (MySQL)
        cx-Oracle (Oracle SQL)
        psycopg2 (PostgreSQL)

    shows how to:
        connect/disconnect to a SQL database
        run arbitrary SQL queries/commands

    to run the test you must:
        set up a sql db, give it a table called eam_assets with columns:
            asset_id, provider_id, description
        in the tests/libraries_and_constants.py file, enter the:
            TEST_HOSTNAME, TEST_PORT, TEST_USERNAME, TEST_PASSWORD, TEST_DATABASE
            tested with Python version 3.13.5 and library versions in requirements.txt

</details>

<details>
<summary><h2>Linux Postgresql Setup</h2></summary>
    
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

    # update tmp dir to be recreated automatically on boot
    sudo nano /etc/tmpfiles.d/postgresql.conf # create file
    copy/paste, and save this file content:
        D /run/postgresql 0755 postgres postgres -
    sudo systemd-tmpfiles --create # apply this configuration

    # i didn't setup postgres to autostart when booting up the compter, so run this each time:
    sudo systemctl start postgresql
    # to setup autostart, run: sudo systemctl enable postgresql

    postgres db stored at:
        /var/lib/postgresql/17/main
        found with:
            psql -U admin -d postgres -c "SHOW data_directory;"
                see file: postgresql_credentials.json for password

</details>

<details>
<summary><h2>Linux Postgresql Usage</h2></summary>

    sudo systemctl status postgresql # chech if postgres is running
    sudo systemctl start postgresql # start it if it isn't

    # list all databases (as admin user)
    psql -U admin -l

    # enter postgres terminal shell as admin user
    psql -U admin -d mydatabase

    # see file src/postgresql_utils.py for example SQL commands to run

    # from within psql shell run
    \? # for help menu
    exit # to exit the shell

</details>

<details>
<summary><h2>Sources</h2></summary>

    MySQL Connector/Python Docs
        https://github.com/mysql/mysql-connector-python

    Oracle Database Connection in Python
        https://www.geeksforgeeks.org/oracle-database-connection-in-python/
    
        cx_Oracle lib requires Oracle Client libraries
            download the Basic one
            https://www.oracle.com/database/technologies/instant-client.html
        and add it to your path:
            C:\oracle\instantclient_19_10
        https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html

    PostgreSQL Connector
        https://pypi.org/project/psycopg2/
        https://www.psycopg.org/docs/

</details>


<details>
<summary><h2>TODO:</h2></summary>

    update mysql_utils.py and oracle_sql_utils.py to not be a class,
    and just use similar file content to postgreql_utils.py
	
</details>

