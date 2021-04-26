import sys
import json
from logging_utils import *
import mysql.connector
from constants import *



''' connect_to_mysql_db()

    Description:
        Connect to MySQL database.
        Don't forget to close the database connection when you're done using it.
            mysql_db.close()

    Arguments:

        hostname ......... string ................. ip address of server hosting the database
        port ............. string ................. port to connect to
        username ......... string ................. username to access database
        password ......... string ................. password to access database
        database ......... string ................. name of database on server
        log .............. logging_util object .... object used to print to log
        verbose .......... boolean ................ log more details of this functions execution
        num_indents ...... int .................... base the number of indents for all logging in this function
        new_line_start ... boolean ................ print a new line before the the first log from this function

    Returns:
        mysql_db ....... mysql.connector object ... mysql connector to database if successful, else None

    '''
def connect_to_mysql_db(
    hostname,
    port,
    username,
    password,
    database,
    log,
    verbose=False,
    num_indents=0,
    new_line_start=False):

    log.print('Connecting to MySQL database ...', num_indents=num_indents, new_line_start=new_line_start)
    try:
        mysql_db = mysql.connector.connect(
            host=hostname,
            port=port,
            user=username,
            passwd=password,
            database=database)
        if verbose:
            log.print('Connection Details:', num_indents=num_indents+1)
            log.print('hostname = %s' % hostname, num_indents=num_indents+2)
            log.print('port     = %s' % port,     num_indents=num_indents+2)
            log.print('database = %s' % database, num_indents=num_indents+2)
        log.print('Successfully connected to MySQL database.', num_indents=num_indents)
    except Exception as e:
        mysql_db = None
        log.print('Exception:', num_indents=num_indents+1)
        log.print('%s' % e, num_indents=num_indents+2)
        log.print('Failed to connect to MySQL database.', num_indents=num_indents)
    return mysql_db



''' mysql_select_query()

    Description:
        Run a select query on MySQL database.

    Arguments:
        mysql_db ......... mysql.connector object ... mysql connector to database
        select_query ..... string ................... SQL select query to run on MySQL database
        log .............. logging_util object ...... object used to print to log
        verbose .......... boolean .................. log more details of this functions execution
        num_indents ...... int ...................... base the number of indents for all logging in this function
        new_line_start ... boolean .................. print a new line before the the first log from this function
        return_type ...... string ................... data type of query results, valid values: 'pandas dataframe', 'list of dictionaries'

    Returns:
        tuple ...
            response ..... pandas dataframe ......... query results
                     OR
                     ..... list of dictionaries ..... each dict is a row in the query response
                                                          key ..... string ... column_name
                                                          value ... string ... cell value at given row and column
            successful ... boolean .................. flag if the function executed successfully without any errors

    '''
def mysql_select_query(
    mysql_db,
    select_query,
    log,
    verbose=False,
    num_indents=0,
    new_line_start=False,
    return_type='pandas dataframe'):

    if return_type == 'pandas dataframe':
        return mysql_select_query_dataframe(
            mysql_db,
            select_query,
            log,
            verbose=verbose,
            num_indents=num_indents,
            new_line_start=new_line_start)

    elif return_type == 'list of dictionaries':
        return mysql_select_query_dictionary(
            mysql_db,
            select_query,
            log,
            verbose=verbose,
            num_indents=num_indents,
            new_line_start=new_line_start)

    else:
        log.print('Invalid return_type \'%s\', valid values: \'pandas dataframe\', \'list of dictionaries\' ' % return_type)
        return None, False
def mysql_select_query_dictionary(
    mysql_db,
    select_query,
    log,
    verbose=False,
    num_indents=0,
    new_line_start=False):

    log.print('Running Select Query on MySQL DB ...', num_indents=num_indents, new_line_start=new_line_start)
    if verbose:
        log.print('Query:', num_indents=num_indents+1)
        log.print('%s' % select_query, num_indents=num_indents+2)
    try:
        cursor = mysql_db.cursor()
        cursor.execute(select_query)
        response = cursor.fetchall()
        column_names = list(map(lambda d : d[0], cursor.description))
        response = [dict(zip(column_names, r)) for r in response] # convert list of tuples to list of dicts
        log.print('Successfully queried MySQL DB.', num_indents=num_indents)
        successful = True
    except Exception as e:
        response = []
        pprint('Exception:', num_indents=num_indents+1)
        pprint('%s' % e, num_indents=num_indents+2)
        pprint('Failed to query MySQL DB.', num_indents=num_indents)
        successful = False
    return response, successful
def mysql_select_query_dataframe(
    mysql_db,
    select_query,
    log,
    verbose=False,
    num_indents=0,
    new_line_start=False):

    log.print('Running Select Query on MySQL DB ...', num_indents=num_indents, new_line_start=new_line_start)
    if verbose:
        log.print('Query:', num_indents=num_indents+1)
        log.print('%s' % select_query, num_indents=num_indents+2)
    try:
        response = pd.read_sql(select_query, con=mysql_db)
        log.print('Successfully queried MySQL DB.', num_indents=num_indents)
        successful = True
    except Exception as e:
        response = pd.DataFrame()
        pprint('Exception:', num_indents=num_indents+1)
        pprint('%s' % e, num_indents=num_indents+2)
        pprint('Failed to query MySQL DB.', num_indents=num_indents)
        successful = False
    return response, successful


