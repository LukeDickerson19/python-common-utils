from libraries_and_constants import *



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



