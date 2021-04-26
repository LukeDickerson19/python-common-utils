from logging_utils import pprint
from constants import *
import snowflake.connector



''' init_connection()

    Description:
        Create a snowflake connector object.

    Arguments:
        secret_dct ....... dictionary ................... dictionary with credentials to snowflake database
        sf_user .......... string ....................... key to snowflake user value in secret_dct
        sf_pswd .......... string ....................... key to snowflake password value in secret_dct
        sf_acct .......... string ....................... key to snowflake account value in secret_dct
        verbose .......... boolean ...................... log more details of this functions execution
        num_indents ...... int .......................... base the number of indents for all logging in this function
        new_line_start ... boolean ...................... print a new line before the the first log from this function

    Returns:
        conn ............. snowflake connector object ... snowflake connector object if successful, else None

    '''
def init_connection(
    secret_dct,
    sf_user=SNOWFLAKE_USER,
    sf_pswd=SNOWFLAKE_PSWD,
    sf_acct=SNOWFLAKE_ACCT,
    sf_dtbs=SNOWFLAKE_DTBS,
    verbose=False,
    num_indents=0,
    new_line_start=False):

    pprint('Initializing Snowflake connection ...',
        num_indents=num_indents,
        new_line_start=new_line_start)
    try:
        dtbs = secret_dct[sf_dtbs] if sf_dtbs != None else None
        conn = snowflake.connector.connect(
            user=secret_dct[sf_user],
            password=secret_dct[sf_pswd],
            account=secret_dct[sf_acct],
            database=dtbs)
        if verbose:
            pprint('Connection Details:', num_indents=num_indents+1)
            pprint('user     = %s' % secret_dct[sf_user], num_indents=num_indents+2)
            pprint('account  = %s' % secret_dct[sf_acct], num_indents=num_indents+2)
            pprint('database = %s' % dtbs,                num_indents=num_indents+2)
        pprint('Successfully initialized Snowflake connection.', num_indents=num_indents)
    except Exception as e:
        conn = None
        pprint('Exception:', num_indents=num_indents+1)
        pprint('%s' % e, num_indents=num_indents+2)
        pprint('Failed to initialize Snowflake connection.', num_indents=num_indents)
    return conn


''' select_query_snowflake()

    Description:
        Run a select query on snowflake database.

    Arguments:
        snowflake_conn ... snowflake.connector object ... Connector to snowflake database
        select_query ..... string ....................... SQL select query to run on snowflake database
        verbose .......... boolean ...................... log more details of this functions execution
        num_indents ...... int .......................... base the number of indents for all logging in this function
        new_line_start ... boolean ...................... print a new line before the the first log from this function

    Returns:
        tuple ...
            response ..... list of dictionaries ......... each dict is a row in the query response
                                                              key ..... string ... column_name
                                                              value ... string ... cell value at given row and column
            successful ... boolean ...................... flag if the function executed successfully without any errors

    '''
def select_query_snowflake(
    snowflake_conn,
    select_query,
    verbose=False,
    num_indents=0,
    new_line_start=False):

    pprint('Running Select Query on Snowflake DB ...', num_indents=num_indents, new_line_start=new_line_start)
    if verbose:
        pprint('Query:', num_indents=num_indents+1)
        pprint('%s' % select_query, num_indents=num_indents+2)
    try:
        cursor = snowflake_conn.cursor()
        cursor.execute(select_query)
        response = cursor.fetchall()
        column_names = list(map(lambda d : d[0], cursor.description))
        response = [dict(zip(column_names, r)) for r in response] # convert list of tuples to list of dicts
        pprint('Successfully queried Snowflake DB.', num_indents=num_indents)
        successful = True
    except Exception as e:
        response = []
        pprint('Exception:', num_indents=num_indents+1)
        pprint('%s' % e, num_indents=num_indents+2)
        pprint('Failed to query Snowflake DB.', num_indents=num_indents)
        successful = False
    return response, successful


