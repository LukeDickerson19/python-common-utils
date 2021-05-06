from libraries_and_constants import *



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
	response, successful1 = \
		mysql_db.mysql_select_query(
			TEST_SELECT_QUERY,
			return_type='pandas dataframe',
			verbose=TEST_VERBOSE,
			print_query_results=True,
			num_indents=num_indents+1,
			new_line_start=False)

	# test list of dictionaries return type
	response, successful2 = \
		mysql_db.mysql_select_query(
			TEST_SELECT_QUERY,
			return_type='list of dictionaries',
			verbose=TEST_VERBOSE,
			print_query_results=True,
			num_indents=num_indents+1,
			new_line_start=False)

	test_result = 'SUCCEEDED' if successful1 and successful2 else 'FAILED'
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


