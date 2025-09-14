
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
ORACLE_SQL_UTIL_PATH   = os.path.join(COMMON_UTILS_REPO_PATH, 'utils', 'sql', 'oracle_sql', 'src')
sys.path.append(LOG_UTIL_PATH)
sys.path.append(ORACLE_SQL_UTIL_PATH)
# print('COMMON_UTILS_REPO_PATH\t', COMMON_UTILS_REPO_PATH)
# print('LOG_UTIL_PATH\t\t', LOG_UTIL_PATH)
# print('ORACLE_SQL_UTIL_PATH\t\t', ORACLE_SQL_UTIL_PATH)
# sys.exit()
import logging_utils
import oracle_sql_utils




# CONSTANTS

LOG_FILENAME = 'log.txt'
LOG_FILEPATH = os.path.join(COMMON_UTILS_REPO_PATH, 'utils', 'sql', 'oracle_sql', 'log', LOG_FILENAME)
DATA_PATH    = os.path.join(COMMON_UTILS_REPO_PATH, 'utils', 'sql', 'oracle_sql', 'data')
# print('LOG_FILEPATH\t', LOG_FILEPATH)
# print('DATA_PATH\t', DATA_PATH)
# sys.exit()

TEST_VERBOSE = False

# Oracle SQL database credentials
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



def test_connect_to_oracle_sql_db(
	log,
	verbose=False,
	num_indents=0,
	new_line_start=False):

	if verbose:
		log.print('test_connect_to_oracle_sql_db',
			num_indents=num_indents, new_line_start=new_line_start)
	oracle_sql_db = oracle_sql_utils.Oracle_SQL_Database(
		TEST_HOSTNAME,
		TEST_PORT,
		TEST_USERNAME,
		TEST_PASSWORD,
		TEST_DATABASE,
		log,
		verbose=TEST_VERBOSE,
		num_indents=num_indents+1,
		new_line_start=False)
	test_result = 'SUCCEEDED' if oracle_sql_db.successful else 'FAILED'
	log.print('Test Function: connect_to_oracle_sql_db ....................... %s' % test_result,
		num_indents=num_indents, new_line_start=False)
	if test_result == 'FAILED':
		sys.exit()
	return oracle_sql_db

def test_oracle_sql_select_query(
	oracle_sql_db,
	verbose=False,
	num_indents=0,
	new_line_start=False):

	if verbose:
		oracle_sql_db.log.print('test_oracle_sql_select_query',
			num_indents=num_indents, new_line_start=new_line_start)

	# test pandas dataframe return type
	response1 = \
		oracle_sql_db.oracle_sql_select_query(
			TEST_SELECT_QUERY,
			return_type='pandas dataframe',
			verbose=TEST_VERBOSE,
			print_query_results=True,
			num_indents=num_indents+1,
			new_line_start=False)

	# test list of dictionaries return type
	response2 = \
		oracle_sql_db.oracle_sql_select_query(
			TEST_SELECT_QUERY,
			return_type='list of dictionaries',
			verbose=TEST_VERBOSE,
			print_query_results=True,
			num_indents=num_indents+1,
			new_line_start=False)

	test_result = 'SUCCEEDED' if response1 != None and response2 != None else 'FAILED'
	oracle_sql_db.log.print('Test Function: oracle_sql_select_query ........................ %s' % test_result,
		num_indents=num_indents, new_line_start=False)

def test_oracle_sql_close_db_connection(
	oracle_sql_db,
	verbose=False,
	num_indents=0,
	new_line_start=False):

	if verbose:
		oracle_sql_db.log.print('test_oracle_sql_close_db_connection',
			num_indents=num_indents, new_line_start=new_line_start)
	successful = oracle_sql_db.close_db_connection(
		verbose=TEST_VERBOSE,
		num_indents=num_indents+1,
		new_line_start=False)
	test_result = 'SUCCEEDED' if successful else 'FAILED'
	oracle_sql_db.log.print('Test Function: close_db_connection ............................ %s' % test_result,
		num_indents=num_indents, new_line_start=False)
	if test_result == 'FAILED':
		sys.exit()



if __name__ == '__main__':

	log = logging_utils.Log(LOG_FILEPATH)
	log.print('Running Oracle SQL Utils Tests:',
		num_indents=0,
		new_line_start=True)

	oracle_sql_db = test_connect_to_oracle_sql_db(
		log,
		verbose=TEST_VERBOSE,
		num_indents=1,
		new_line_start=True)

	test_oracle_sql_select_query(
		oracle_sql_db,
		verbose=TEST_VERBOSE,
		num_indents=1,
		new_line_start=True)

	test_oracle_sql_close_db_connection(
		oracle_sql_db,
		verbose=TEST_VERBOSE,
		num_indents=1,
		new_line_start=True)



