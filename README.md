# python-common-utils


#### DESCRIPTION
```
Utility functions for common backend processes:
	logging_utils
	aws_utils
	snowflake_utils
	mysql_utils
	oracle_sql_utils
	emails_utils
	general_utils

Visit each util subfolder in the common_utils folder for
usage and details on the functions each util provides.
```

#### TO DO
```
restructure each *_util.py file in the src folder to be like the util folders in the common_utils folder

	what i've fixed up so far is
		common_utils/logging_utils
		common_utils/email_utils/outlook_utils

	for each one you need to see what constants it uses in src/constants.py
		and replicate the exact structure of the:
			<util_folders>/<util>/src/libraries_and_constants.py

		maybe put it all in a cicd (or deploy) folder
			\deploy\
				parse_NOTES_to_README.py

fix up general utils
	required for aws_utils to work

fix up aws utils

clean up the notes above each function
	or maybe make a docs page in markdown

make common_components a python lib
	see this link too
	https://medium.com/analytics-vidhya/how-to-create-a-python-library-7d5aea80cc3f
https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56
```
