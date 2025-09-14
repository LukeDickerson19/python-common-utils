
# LIBRARIES

# import standard libraries
import os
import sys
import time
import pathlib
from datetime import datetime, timezone, timedelta

# import non-standard libraries
# None

# import common utils
COMMON_UTILS_REPO_PATH = str(pathlib.Path(__file__).resolve().parent.parent.parent.parent.parent)
LOG_UTIL_PATH          = os.path.join(COMMON_UTILS_REPO_PATH, 'utils', 'logging', 'src')
POSTGRESQL_UTIL_PATH   = os.path.join(COMMON_UTILS_REPO_PATH, 'utils', 'sql', 'src')
sys.path.append(LOG_UTIL_PATH)
sys.path.append(POSTGRESQL_UTIL_PATH)
# print('COMMON_UTILS_REPO_PATH\t', COMMON_UTILS_REPO_PATH)
# print('LOG_UTIL_PATH\t\t', LOG_UTIL_PATH)
# print('POSTGRESQL_UTIL_PATH\t\t', POSTGRESQL_UTIL_PATH)
# sys.exit()
import logging_utils
import postgresql_utils




# CONSTANTS

LOG_FILENAME = 'log.txt'
LOG_FILEPATH = os.path.join(COMMON_UTILS_REPO_PATH, 'utils', 'sql', 'log', LOG_FILENAME)
DATA_PATH    = os.path.join(COMMON_UTILS_REPO_PATH, 'utils', 'sql', 'data')
# print('LOG_FILEPATH\t', LOG_FILEPATH)
# print('DATA_PATH\t', DATA_PATH)
# sys.exit()

TEST_VERBOSE = False

# PostgreSQL database credentials
TEST_HOSTNAME = ''
TEST_PORT     = ''
TEST_USERNAME = ''
TEST_PASSWORD = ''
TEST_DATABASE = ''




TEST_SELECT_QUERY = '''
select
	material_id,
	title_asset_id,
	title
from bbv_title
where material_id like 'B00114370%'
'''



def test_connect_to_postgresql_db(
	log,
	verbose=False,
	num_indents=0,
	new_line_start=False):

	if verbose:
		log.print('test_connect_to_postgresql_db',
			num_indents=num_indents, new_line_start=new_line_start)
	postgresql_db = postgresql_utils.PostgreSQL_Database(
		TEST_HOSTNAME,
		TEST_PORT,
		TEST_USERNAME,
		TEST_PASSWORD,
		TEST_DATABASE,
		log,
		verbose=TEST_VERBOSE,
		num_indents=num_indents+1,
		new_line_start=False)
	test_result = 'SUCCEEDED' if postgresql_db.successful else 'FAILED'
	log.print('Test Function: connect_to_postgresql_db ....................... %s' % test_result,
		num_indents=num_indents, new_line_start=False)
	if test_result == 'FAILED':
		sys.exit()
	return postgresql_db

def test_postgresql_select_query(
	postgresql_db,
	verbose=False,
	num_indents=0,
	new_line_start=False):

	if verbose:
		postgresql_db.log.print('test_postgresql_select_query',
			num_indents=num_indents, new_line_start=new_line_start)

	# test pandas dataframe return type
	response1 = \
		postgresql_db.postgresql_select_query(
			TEST_SELECT_QUERY,
			return_type='pandas dataframe',
			verbose=TEST_VERBOSE,
			print_query_results=True,
			num_indents=num_indents+1,
			new_line_start=False)

	# test list of dictionaries return type
	response2 = \
		postgresql_db.postgresql_select_query(
			TEST_SELECT_QUERY,
			return_type='list of dictionaries',
			verbose=TEST_VERBOSE,
			print_query_results=True,
			num_indents=num_indents+1,
			new_line_start=False)

	test_result = 'SUCCEEDED' if response1 != None and response2 != None else 'FAILED'
	postgresql_db.log.print('Test Function: postgresql_select_query ........................ %s' % test_result,
		num_indents=num_indents, new_line_start=False)

def test_postgresql_close_db_connection(
	postgresql_db,
	verbose=False,
	num_indents=0,
	new_line_start=False):

	if verbose:
		postgresql_db.log.print('test_postgresql_close_db_connection',
			num_indents=num_indents, new_line_start=new_line_start)
	successful = postgresql_db.close_db_connection(
		verbose=TEST_VERBOSE,
		num_indents=num_indents+1,
		new_line_start=False)
	test_result = 'SUCCEEDED' if successful else 'FAILED'
	postgresql_db.log.print('Test Function: close_db_connection ............................ %s' % test_result,
		num_indents=num_indents, new_line_start=False)
	if test_result == 'FAILED':
		sys.exit()



if __name__ == '__main__':

	log = logging_utils.Log(LOG_FILEPATH)
	log.print('Running Postgre SQL Utils Tests:',
		num_indents=0,
		new_line_start=True)

	postgresql_db = test_connect_to_postgresql_db(
		log,
		verbose=TEST_VERBOSE,
		num_indents=1,
		new_line_start=True)

	test_postgresql_select_query(
		postgresql_db,
		verbose=TEST_VERBOSE,
		num_indents=1,
		new_line_start=True)

	test_postgresql_close_db_connection(
		postgresql_db,
		verbose=TEST_VERBOSE,
		num_indents=1,
		new_line_start=True)



