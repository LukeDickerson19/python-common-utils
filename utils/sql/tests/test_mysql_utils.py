
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
MYSQL_UTIL_PATH        = os.path.join(COMMON_UTILS_REPO_PATH, 'utils', 'sql', 'mysql', 'src')
sys.path.append(LOG_UTIL_PATH)
sys.path.append(MYSQL_UTIL_PATH)
# print('COMMON_UTILS_REPO_PATH\t', COMMON_UTILS_REPO_PATH)
# print('LOG_UTIL_PATH\t\t', LOG_UTIL_PATH)
# print('MYSQL_UTIL_PATH\t\t', MYSQL_UTIL_PATH)
# sys.exit()
import logging_utils
import mysql_utils




# CONSTANTS

LOG_FILENAME = 'log.txt'
LOG_FILEPATH = os.path.join(COMMON_UTILS_REPO_PATH, 'utils', 'sql', 'mysql', 'log', LOG_FILENAME)
DATA_PATH    = os.path.join(COMMON_UTILS_REPO_PATH, 'utils', 'sql', 'mysql', 'data')
# print('LOG_FILEPATH\t', LOG_FILEPATH)
# print('DATA_PATH\t', DATA_PATH)
# sys.exit()

TEST_VERBOSE = False

# MySQL database credentials
TEST_HOSTNAME = ''
TEST_PORT     = ''
TEST_USERNAME = ''
TEST_PASSWORD = ''
TEST_DATABASE = ''


TEST_SELECT_QUERY = '''
select
	asset_id,
	provider_id,
	description
from eam_asset
limit 10
'''



def test_connect_to_mysql_db(
	log,
	verbose=False,
	num_indents=0,
	new_line_start=False):

	if verbose:
		log.print('test_connect_to_mysql_db',
			num_indents=num_indents, new_line_start=new_line_start)
	mysql_db = mysql_utils.MySQL_Database(
		TEST_HOSTNAME,
		TEST_PORT,
		TEST_USERNAME,
		TEST_PASSWORD,
		TEST_DATABASE,
		log,
		verbose=TEST_VERBOSE,
		num_indents=num_indents+1,
		new_line_start=False)
	test_result = 'SUCCEEDED' if mysql_db.successful else 'FAILED'
	log.print('Test Function: connect_to_mysql_db ............................ %s' % test_result,
		num_indents=num_indents, new_line_start=False)
	if test_result == 'FAILED':
		sys.exit()
	return mysql_db

def test_mysql_select_query(
	mysql_db,
	verbose=False,
	num_indents=0,
	new_line_start=False):

	if verbose:
		mysql_db.log.print('test_mysql_select_query',
			num_indents=num_indents, new_line_start=new_line_start)

	# test pandas dataframe return type
	response1 = \
		mysql_db.mysql_select_query(
			TEST_SELECT_QUERY,
			return_type='pandas dataframe',
			verbose=TEST_VERBOSE,
			print_query_results=True,
			num_indents=num_indents+1,
			new_line_start=False)

	# test list of dictionaries return type
	response2 = \
		mysql_db.mysql_select_query(
			TEST_SELECT_QUERY,
			return_type='list of dictionaries',
			verbose=TEST_VERBOSE,
			print_query_results=True,
			num_indents=num_indents+1,
			new_line_start=False)

	test_result = 'SUCCEEDED' if response1 != None and response2 != None else 'FAILED'
	mysql_db.log.print('Test Function: test_get_all_messages_in_inbox ................. %s' % test_result,
		num_indents=num_indents, new_line_start=False)

def test_mysql_close_db_connection(
	mysql_db,
	verbose=False,
	num_indents=0,
	new_line_start=False):

	if verbose:
		mysql_db.log.print('test_mysql_close_db_connection',
			num_indents=num_indents, new_line_start=new_line_start)
	successful = mysql_db.close_db_connection(
		verbose=TEST_VERBOSE,
		num_indents=num_indents+1,
		new_line_start=False)
	test_result = 'SUCCEEDED' if successful else 'FAILED'
	mysql_db.log.print('Test Function: close_db_connection ............................ %s' % test_result,
		num_indents=num_indents, new_line_start=False)
	if test_result == 'FAILED':
		sys.exit()

		

if __name__ == '__main__':

	log = logging_utils.Log(LOG_FILEPATH)
	log.print('Running MySQL Utils Tests:',
		num_indents=0,
		new_line_start=True)

	mysql_db = test_connect_to_mysql_db(
		log,
		verbose=TEST_VERBOSE,
		num_indents=1,
		new_line_start=True)

	test_mysql_select_query(
		mysql_db,
		verbose=TEST_VERBOSE,
		num_indents=1,
		new_line_start=True)

	test_mysql_close_db_connection(
		mysql_db,
		verbose=TEST_VERBOSE,
		num_indents=1,
		new_line_start=True)


