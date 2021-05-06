# Oracle SQL Utilities



#### DESCRIPTION
```
	easy to use wrapper for the cx_Oracle python library with logging utils integrated
	so far it can only be used to connect/disconnect to a oracle database and run select
	queries on that database

	to run the test you must:
		set up a oracle sql db, give it a table called bbv_title with columns:
			material_id, title_asset_id, title
		in the tests/libraries_and_constants.py file, enter the:
			TEST_HOSTNAME, TEST_PORT, TEST_USERNAME, TEST_PASSWORD, TEST_DATABASE
```

#### TO DO
```
	create function to run update queries, and test it

```

#### SOURCES
```

	Oracle Database Connection in Python
		cx_Oracle lib requires Oracle Client libraries
			download the Basic one
				https://www.oracle.com/database/technologies/instant-client.html
			and add it to your path:
				C:\oracle\instantclient_19_10
		https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html
	https://www.geeksforgeeks.org/oracle-database-connection-in-python/

```


