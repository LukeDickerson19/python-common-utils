from mysql_utils_libraries_and_constants import *



class MySQL_Database:

    ''' __init__()

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

        '''
    def __init__(
        self,
        hostname,
        port,
        username,
        password,
        database,
        log,
        verbose=False,
        num_indents=0,
        new_line_start=False):

        self.log = log

        if verbose:
            self.log.print('Connecting to MySQL database ...', num_indents=num_indents, new_line_start=new_line_start)
        try:
            self.mysql_db = mysql.connector.connect(
                host=hostname,
                port=port,
                user=username,
                passwd=password,
                database=database)
            if verbose:
                self.log.print('Connection Details:', num_indents=num_indents+1)
                self.log.print('hostname = %s' % hostname, num_indents=num_indents+2)
                self.log.print('port     = %s' % port,   num_indents=num_indents+2)
                self.log.print('database = %s' % database, num_indents=num_indents+2)
                self.log.print('Successfully connected to MySQL database.', num_indents=num_indents)
            self.successful = True
        except Exception as e:
            self.log.print('Exception:', num_indents=num_indents+1)
            self.log.print('%s' % e, num_indents=num_indents+2)
            self.log.print('Failed to connect to MySQL database.', num_indents=num_indents)
            self.mysql_db = None
            self.successful = False

    ''' mysql_select_query()

        Description:
            Run a select query on MySQL database.

        Arguments:
            select_query .......... string ................... SQL select query to run on MySQL database
            return_type ........... string ................... data type of query results, valid values: 'pandas dataframe', 'list of dictionaries'
            verbose ............... boolean .................. log more details of this functions execution
            print_query_results ... boolean .................. flag if you want to log the query results
            num_indents ........... int ...................... base the number of indents for all logging in this function
            new_line_start ........ boolean .................. print a new line before the the first log from this function

        Returns:
            tuple ...
                response ..... pandas dataframe ......... query results
                         OR
                         ..... list of dictionaries ..... each dict is a row in the query response
                                                              key ..... string ... column_name
                                                              value ... string ... cell value at given row and column
                         if successful, else it returns None

        '''
    def mysql_select_query(
        self,
        select_query,
        return_type='pandas dataframe',
        verbose=False,
        print_query_results=False,
        num_indents=0,
        new_line_start=False):

        if self.mysql_db == None:
            if verbose:
                self.log.print('Unable to query database. Not Connected.',
                    num_indents=num_indents, new_line_start=new_line_start)
            return None

        if return_type == 'pandas dataframe':
            return self.mysql_select_query_dataframe(
                select_query,
                verbose=verbose,
                print_query_results=print_query_results,
                num_indents=num_indents,
                new_line_start=new_line_start)

        elif return_type == 'list of dictionaries':
            return self.mysql_select_query_dictionary(
                select_query,
                verbose=verbose,
                print_query_results=print_query_results,
                num_indents=num_indents,
                new_line_start=new_line_start)

        else:
            self.log.print('Invalid return_type \'%s\', valid values: \'pandas dataframe\', \'list of dictionaries\' ' % return_type)
            return None
    def mysql_select_query_dictionary(
        self,
        select_query,
        verbose=False,
        print_query_results=False,
        num_indents=0,
        new_line_start=False):

        if verbose:
            self.log.print('Running Select Query on MySQL DB ...', num_indents=num_indents, new_line_start=new_line_start)
            self.log.print('Query:', num_indents=num_indents+1)
            self.log.print('%s' % select_query, num_indents=num_indents+2)
        try:
            cursor = self.mysql_db.cursor()
            cursor.execute(select_query)
            response = cursor.fetchall()
            column_names = list(map(lambda d : d[0], cursor.description))
            response = [dict(zip(column_names, r)) for r in response] # convert list of tuples to list of dicts
            if verbose:
                if print_query_results:
                    self.log.print('Results:', num_indents=num_indents+1)
                    response_str = '[\n\t' + ',\n\t'.join(map(lambda x : str(x), response)) + '\n]'
                    self.log.print(response_str, num_indents=num_indents+2)
                self.log.print('Successfully queried MySQL DB.', num_indents=num_indents)
        except Exception as e:
            self.log.print('Exception:', num_indents=num_indents+1)
            self.log.print('%s' % e, num_indents=num_indents+2)
            self.log.print('Failed to query MySQL DB.', num_indents=num_indents)
            response = None
        return response
    def mysql_select_query_dataframe(
        self,
        select_query,
        verbose=False,
        print_query_results=False,
        num_indents=0,
        new_line_start=False):

        if verbose:
            self.log.print('Running Select Query on MySQL DB ...', num_indents=num_indents, new_line_start=new_line_start)
            self.log.print('Query:', num_indents=num_indents+1)
            self.log.print('%s' % select_query, num_indents=num_indents+2)
        try:
            response = pd.read_sql(select_query, con=self.mysql_db)
            if verbose:
                if print_query_results:
                    self.log.print('Results:', num_indents=num_indents+1)
                    response_str = response.to_string(max_rows=MAX_ROWS)
                    self.log.print(response_str, num_indents=num_indents+2)
                self.log.print('Successfully queried MySQL DB.', num_indents=num_indents)
        except Exception as e:
            response = None
            self.log.print('Exception:', num_indents=num_indents+1)
            self.log.print('%s' % e, num_indents=num_indents+2)
            self.log.print('Failed to query MySQL DB.', num_indents=num_indents)
        return response

    ''' mysql_update_query()
    
        '''
    def mysql_update_query(
        self,
        update_query,
        verbose=False,
        num_indents=0,
        new_line_start=False):

        if verbose:
            self.log.print('Running Update Query on MySQL DB ...',
                num_indents=num_indents, new_line_start=new_line_start)
            self.log.print('Query:', num_indents=num_indents+1)
            self.log.print('%s' % update_query, num_indents=num_indents+2)
        try:
            cursor = self.mysql_db.cursor()
            cursor.execute(update_query)
            self.mysql_db.commit()
            if verbose:
                self.log.print('Successfully updated MySQL DB.', num_indents=num_indents)
        except Exception as e:
            self.log.print('Exception:', num_indents=num_indents+1)
            self.log.print('%s' % e, num_indents=num_indents+2)
            self.log.print('Failed to update MySQL DB.', num_indents=num_indents)

    ''' close_db_connection()

        Description:
            close the database and return boolean flagging if your were successful

        Arguments:
            verbose ............... boolean .................. log more details of this functions execution
            num_indents ........... int ...................... base the number of indents for all logging in this function
            new_line_start ........ boolean .................. print a new line before the the first log from this function

        Returns:
            successful ... boolean .................. flag if the function executed successfully without any errors

        '''
    def close_db_connection(
        self,
        verbose=False,
        num_indents=0,
        new_line_start=False):

        if verbose:
            self.log.print('Closing MySQL Database Connection',
                num_indents=num_indents, new_line_start=new_line_start)
        try:
            self.mysql_db.close()
            if verbose:
                self.log.print('Successfully closed MySQL Database Connection',
                    num_indents=num_indents)
            successful = True
        except Exception as e:
            self.log.print('Exception:', num_indents=num_indents+1)
            self.log.print('%s' % e, num_indents=num_indents+2)
            self.log.print('Failed to query MySQL DB.', num_indents=num_indents)
            successful = False
        return successful


