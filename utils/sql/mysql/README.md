# MySQL Utilities



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
	
	create optional argument in select query function to save
	the results to a file, and another argument to wread from
	a file if it exists
		this will be helpful in only running long lasting queries once

	create function to run update queries, and test it
		function created, it just needs to be tested and documented

```

#### SOURCES
```

	MySQL Connector/Python Docs
	https://github.com/mysql/mysql-connector-python

```


