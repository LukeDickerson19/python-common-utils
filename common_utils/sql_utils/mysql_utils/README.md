# MySQL Utilities
easy to use wrapper for the mysql.connector python library with logging utils integrated


#### DESCRIPTION
```
	easy to use wrapper for the mysql.connector python library with logging utils integrated
	so far it can only be used to connect/disconnect to a mysql database and run select
	queries on that database

	to run the test you must:
		set up a mysql db, give it a table called eam_assets with columns:
			asset_id, provider_id, description
		in the tests/libraries_and_constants.py file, enter the:
			TEST_HOSTNAME, TEST_PORT, TEST_USERNAME, TEST_PASSWORD, TEST_DATABASE

```

#### TO DO
```
	create function to run update queries, and test it

```

#### SOURCES
```

	MySQL Connector/Python Docs
	https://github.com/mysql/mysql-connector-python

```


