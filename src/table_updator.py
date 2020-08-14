from regression_tester import *


''' TO DO:
        put all the neccessary Constants at the top of this file
        make script pull excel file from microsoft online
        read through update_table_column_from_excel_file()
            and do any neccessary refactoring
        comment out the part that actually updates aurora and test it

    '''




''' init_log()

    Description:
        Set the LOG_FILEPATH to a global variable within this file for the pprint() function to use.
        Optionally set OUTPUT_TO_CONSOLE and OUTPUT_TO_LOGFILE differently than how they're set in constants.py

    Arguments:
        log_filepath ... string ... complete path to the log file

    Returns:
        Nothing

    '''
def init_log(
    log_filepath,
    output_to_console=OUTPUT_TO_CONSOLE,
    output_to_logfile=OUTPUT_TO_LOGFILE,
    clear_old_log=False):

    global LOGFILE_PATH
    LOGFILE_PATH = log_filepath

    global OUTPUT_TO_CONSOLE
    OUTPUT_TO_CONSOLE = output_to_console

    global OUTPUT_TO_LOGFILE
    OUTPUT_TO_LOGFILE = output_to_logfile

    if clear_old_log:
        open(log_filepath, 'w').close() # clear log

''' pprint()

    Description:
        Log 'string' argument to logfile and/or console.
        Set how indented the line should be with 'num_indents' int argument.
            ^^^ very useful for organizing log ^^^

    Arguments:
        string .... string ........... what will be printed
        string .... indent ........... what an indent looks like
        int ....... num_indents ...... number of indents to put in front of the string
        boolean ... new_line_start ... print a new line in before the string
        boolean ... new_line_end ..... print a new line in after the string
        boolean ... draw_line ........ draw a line on the blank line before or after the string

    Returns:
        Nothing

    '''
def pprint(
    string='',
    num_indents=0,
    new_line_start=False,
    new_line_end=False,
    draw_line=DRAW_LINE):

    def output(out_loc):
        indent = len(INDENT)*' ' if out_loc != sys.stdout else INDENT
        total_indent0 = ''.join([indent] * num_indents)
        total_indent1 = ''.join([indent] * (num_indents + 1))
        if new_line_start:
            print(total_indent1 if draw_line else total_indent0, file=out_loc)
        for s in string.split('\n'):
            print(total_indent0 + s, file=out_loc)
        if new_line_end:
            print(total_indent1 if draw_line else total_indent0, file=out_loc)

    if OUTPUT_TO_CONSOLE:
        output(sys.stdout)
    if OUTPUT_TO_LOGFILE:
        logfile = open(LOGFILE_PATH, 'a')
        output(logfile)
        logfile.close()




''' init_session()

    Description:
        Create a boto3 AWS session object.

    Arguments:
        profile_name ..... string ................. AWS IAM or service account name
        verbose .......... boolean ................ log more details of this functions execution
        num_indents ...... int .................... base the number of indents for all logging in this function
        new_line_start ... boolean ................ print a new line before the the first log from this function

    Returns:
        session .......... boto3 session object ... session object if successful, else None

    '''
def init_session(
    profile_name=None,
    verbose=False,
    num_indents=0,
    new_line_start=False):

    pprint('Initializing AWS session ...', num_indents=num_indents, new_line_start=new_line_start)
    try:
        session = boto3.session.Session(profile_name=profile_name)
        if verbose:
            pprint('Session Details:', num_indents=num_indents+1)
            pprint('aws_session_token = %s' % session.aws_session_token, num_indents=num_indents+2)
            pprint('profile_name      = %s' % session.profile_name,      num_indents=num_indents+2)
            pprint('region_name       = %s' % session.region_name,       num_indents=num_indents+2)
        pprint('Successfully initialized AWS session.', num_indents=num_indents)
    except Exception as e:
        session = None
        pprint('Exception:', num_indents=num_indents+1)
        pprint('%s' % e, num_indents=num_indents+2)
        pprint('Failed to initialize AWS session.', num_indents=num_indents)
    return session

''' get_secret()

    Description:
        Get AWS secret with 'secret_name'.

    Arguments:
        secret_name ...... string ....... dictionary with credentials to aurora database
        region_name ...... string ....... aws region name of where aurora database is hosted
        verbose .......... boolean ...... log more details of this functions execution
        num_indents ...... int .......... base the number of indents for all logging in this function
        new_line_start ... boolean ...... print a new line before the the first log from this function

    Returns:
        tuple ...
            secret_dct ... dictionary ... dictionary of the AWS secret credentials
                                              key ..... string ... AWS secret key
                                              value ... string ... AWS secret value
            successful ... boolean ...... flag if the function executed successfully without any errors

    '''
def get_secret(
    session,
    secret_name,
    region_name,
    verbose=False,
    num_indents=0,
    new_line_start=False):

    pprint('Getting AWS secret: %s' % secret_name, num_indents=num_indents, new_line_start=new_line_start)
    try:
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name)
        secrets_dct = json.loads(
            client.get_secret_value(
                SecretId=secret_name)['SecretString'])

        # log a successful collection of the credentials, and return them
        if verbose: pprint(json.dumps(secrets_dct, indent=4), num_indents=num_indents+1)
        pprint('Successfully retrieved secret.', num_indents=num_indents)
        successful = True

    except Exception as e:
        secrets_dct = None
        pprint('Exception:', num_indents=num_indents+1)
        pprint('%s' % e, num_indents=num_indents+2)
        pprint('Failed to retrieve secret.', num_indents=num_indents)
        successful = False

    return secrets_dct, successful

''' connect_to_aurora()

    Description:
        Connect to AWS Aurora database.

    Arguments:
        secret_dct ....... string ................... dictionary with credentials to aurora database
        ar_host .......... string ................... key to aurora host name in secret_dct
        ar_user .......... string ................... key to aurora user name in secret_dct
        ar_pswd .......... string ................... key to aurora password in secret_dct
        ar_dtbs .......... string ................... key to aurora database name in secret_dct
        verbose .......... boolean .................. log more details of this functions execution
        num_indents ...... int ...................... base the number of indents for all logging in this function
        new_line_start ... boolean .................. print a new line before the the first log from this function

    Returns:
        tuple ...
            aurora_db .... mysql.connector object ... Connector to aurora database
            successful ... boolean .................. flag if the function executed successfully without any errors

    '''
def connect_to_aurora(
    secrets_dct,
    ar_host=AURORA_HOST,
    ar_user=AURORA_USER,
    ar_pswd=AURORA_PSWD,
    ar_dtbs=AURORA_DTBS,
    verbose=False,
    num_indents=0,
    new_line_start=False):

    pprint('Connecting to Aurora DB ...', num_indents=num_indents, new_line_start=new_line_start)
    try:
        aurora_db = mysql.connector.connect(
            host=secrets_dct[ar_host],
            user=secrets_dct[ar_user],
            passwd=secrets_dct[ar_pswd],
            database=secrets_dct[ar_dtbs])
        if verbose:
            pprint('Aurora Database:', num_indents=num_indents+1)
            pprint('host:     %s' % secrets_dct[ar_host],     num_indents=num_indents+2)
            pprint('user:     %s' % secrets_dct[ar_user],     num_indents=num_indents+2)
            pprint('database: %s' % secrets_dct[ar_database], num_indents=num_indents+2)
        pprint('Successfully connected to Aurora database.', num_indents=num_indents)
        successful = True
    except Exception as e:
        aurora_db = None
        pprint('Exception:', num_indents=num_indents+1)
        pprint('%s' % e, num_indents=num_indents+2)
        pprint('Failed to connect to Aurora database.', num_indents=num_indents)
        successful = False
    return aurora_db, successful

''' select_query_aurora()

    Description:
        Run a select query on aurora database.

    Arguments:
        aurora_db ........ mysql.connector object ... Connector to aurora database
        select_query ..... string ................... SQL select query to run on aurora database
        verbose .......... boolean .................. log more details of this functions execution
        num_indents ...... int ...................... base the number of indents for all logging in this function
        new_line_start ... boolean .................. print a new line before the the first log from this function

    Returns:
        tuple ...
            response ..... list of dictionaries ..... each dict is a row in the query response
                                                          key ..... string ... column_name
                                                          value ... string ... cell value at given row and column
            successful ... boolean .................. flag if the function executed successfully without any errors

    '''
def select_query_aurora(
    aurora_db,
    select_query,
    verbose=False,
    num_indents=0,
    new_line_start=False):

    pprint('Running Select Query on Aurora DB ...', num_indents=num_indents, new_line_start=new_line_start)
    if verbose:
        pprint('Query:', num_indents=num_indents+1)
        pprint('%s' % select_query, num_indents=num_indents+2)
    try:
        cursor = aurora_db.cursor()
        cursor.execute(select_query)
        response = cursor.fetchall()
        column_names = list(map(lambda d : d[0], cursor.description))
        response = [dict(zip(column_names, r)) for r in response] # convert list of tuples to list of dicts
        pprint('Successfully queried Aurora DB.', num_indents=num_indents)
        successful = True
    except Exception as e:
        response = []
        pprint('Exception:', num_indents=num_indents+1)
        pprint('%s' % e, num_indents=num_indents+2)
        pprint('Failed to query Aurora DB.', num_indents=num_indents)
        successful = False
    return response, successful

''' update_query_aurora()

    Description:
        Run an update query on aurora db.

    Arguments:
        aurora_db ........ mysql.connector object ... Connector to aurora database
        update_query ..... string ................... SQL update query to run on aurora database
        verbose .......... boolean .................. log more details of this functions execution
        num_indents ...... int ...................... base the number of indents for all logging in this function
        new_line_start ... boolean .................. print a new line before the the first log from this function

    Returns:
        successful ....... boolean .................. flag if the function executed successfully without any errors

    '''
def update_query_aurora(
    aurora_db,
    update_query,
    verbose=False,
    num_indents=0,
    new_line_start=False):

    pprint('Running Update Query on Aurora DB ...', num_indents=num_indents, new_line_start=new_line_start)
    if verbose:
        pprint('Query:', num_indents=num_indents+1)
        pprint('%s' % update_query, num_indents=num_indents+2)
    try:
        cursor = aurora_db.cursor()
        cursor.execute(update_query)
        aurora_db.commit()
        pprint('Successfully updated Aurora DB.', num_indents=num_indents)
        successful = True
    except Exception as e:
        pprint('Exception:', num_indents=num_indents+1)
        pprint('%s' % e, num_indents=num_indents+2)
        pprint('Failed to update Aurora DB.', num_indents=num_indents)
        successful = False
    return successful




def update_table_column_of_json_strings(
    aurora_db,
    table_name,
    id_col_name,
    column_name,
    key_list,
    new_data,
    key_or_value='value',
    rows_to_change='all_rows', # if not 'all_rows': list of IDs
    verbose=False,
    num_indents=0):

    pprint('Updating table column of json strings ...', num_indents=num_indents, new_line_start=True)

    try:
        cursor = aurora_db.cursor()
        pprint('Created mysql.connector.cursor() ...', num_indents=num_indents+1)
    except Exception as e:
        pprint('Failed to create mysql.connector.cursor().\nException:\n%s' % e, num_indents=num_indents+1)
        return False

    # get a list of the current column values
    try:
        columns = id_col_name+', '+column_name
        pprint('\nQuery:%s' % GET_TABLE_COLUMNS.format(
                columns=columns,
                table=table_name), num_indents=num_indents)
        cursor.execute(
            GET_TABLE_COLUMNS.format(
                columns=columns,
                table=table_name))
        ret = cursor.fetchall()
        if verbose:
            pprint('Successfully aquired list of %d column values:' % len(ret), num_indents=num_indents)
    except Exception as e:
        pprint('Failed to run mysql.connector.cursor.execute().\nException:\n%s' % e, num_indents=num_indents)
        return False

    num_rows_updated = 0
    for j, row in enumerate(ret):
        testcase_id, json_str = row[0], row[1]

        if rows_to_change != 'all_rows' and testcase_id not in rows_to_change:
            continue

        # get json dictionary
        original_json_dct = json.loads(json_str)
        if verbose:
            pprint('\nColumn Value %d of %d: testcase_id = %s' % (
                j+1,
                len(ret),
                testcase_id), num_indents=num_indents+1)
            pprint('original_json_dct:', num_indents=num_indents+2)
            pprint('%s' % json.dumps(original_json_dct, indent=4), num_indents=num_indents+3)

        # set dct[key_list] to new_value
        def recursive_dict_setter(
            dct, key_list, data, key_or_value):

            # handle invalid input
            if key_list == []:
                return Exception('Exception: key_list must have at least 1 key.')
            if key_list[0] not in dct.keys():
                return Exception('Exception: key %s not in dct' % key_list[0])

            # base case
            if len(key_list) == 1:
                if key_or_value == 'value':
                    dct[key_list[0]] = data
                    return dct
                elif key_or_value == 'key':
                    dct[data] = dct[key_list[0]]
                    del dct[key_list[0]]
                    return dct

            # general case
            dct[key_list[0]] = recursive_dict_setter(
                                    dct[key_list[0]],
                                    key_list[1:],
                                    data,
                                    key_or_value)
            return dct
        try:
            new_json_dct = recursive_dict_setter(
                                original_json_dct,
                                key_list,
                                new_data,
                                key_or_value)
            if verbose:
                pprint('new_json_dct:', num_indents=num_indents+2)
                pprint('%s' % (json.dumps(new_json_dct, indent=4)), num_indents=num_indents+3)

        except Exception as e:
            pprint('Failed to set new_value in column.\nException:\n%s' % e, num_indents=num_indents)
            continue

        new_json_str = '\''+json.dumps(new_json_dct)+'\''

        # update it in aurora
        try:
            if verbose:
                pprint('\nUpdating aurora ...', num_indents=num_indents+2)
                pprint('\nUPDATE_TABLE_CELL query:', num_indents=num_indents+3)
                pprint('%s' % UPDATE_TABLE_CELL.format(
                        table=table_name,
                        column=column_name,
                        new_value=new_json_str,
                        table_id_name=id_col_name,
                        table_id_value=testcase_id),
                    num_indents=num_indents+4)
            cursor.execute(
                UPDATE_TABLE_CELL.format(
                    table=table_name,
                    column=column_name,
                    new_value=new_json_str,
                    table_id_name=id_col_name,
                    table_id_value=testcase_id))
            aurora_db.commit()
            if verbose: pprint('\nSuccessfully ran UPDATE_TABLE_CELL.',
                num_indents=num_indents+3)
            num_rows_updated += 1
        except Exception as e:
            pprint('\nException:', num_indents=num_indents+4)
            pprint('%s' % e, num_indents=num_indents+5)
            pprint('Failed to run query.', num_indents=num_indents+3)
            return False

    if verbose: pprint('', num_indents=num_indents, draw_line=True)
    pprint('Updated %d out of %d of the rows in the column' % (
        num_rows_updated,
        len(ret) if rows_to_change == 'all_rows' else len(rows_to_change)),
        num_indents=num_indents)

    return True

def update_table_column_from_excel_file(
    aurora_db,
    table_name,
    aurora_id_col_name,
    aurora_column_name,
    excel_id_col_name,
    excel_column_name,
    excel_filepath,
    table_sheetname,
    excel_row_range,
    rows_to_change='all_rows', # if not 'all_rows': list of IDs
    verbose=False,
    num_indents=0):

    pprint('Updating table column from excel file ...', num_indents=num_indents, new_line_start=True)

    if verbose:
        pprint('aurora_id_col_name = %s'   % aurora_id_col_name, num_indents=num_indents+1)
        pprint('aurora_column_name = %s'   % aurora_id_col_name, num_indents=num_indents+1)
        pprint('excel_id_col_name  = %s'   % excel_id_col_name,  num_indents=num_indents+1)
        pprint('excel_column_name  = %s\n' % excel_column_name,  num_indents=num_indents+1)

    try:
        cursor = aurora_db.cursor()
        pprint('Created mysql.connector.cursor() ...', num_indents=num_indents+1)
    except Exception as e:
        pprint('\nException:', num_indents=num_indents+2)
        pprint('%s' % e, num_indents=num_indents+3)
        pprint('Failed to create mysql.connector.cursor().', num_indents=num_indents+1)
        return False

    try:
        df = pd.read_excel(excel_filepath, sheet_name=table_sheetname)
        pprint('\nOpened excel file: %s' % excel_filepath, num_indents=num_indents+1)
    except Exception as e:
        pprint('\nException:', num_indents=num_indents+2)
        pprint('%s' % e, num_indents=num_indents+3)
        pprint('Failed to open excel file: %s' % excel_filepath, num_indents=num_indents+1)
        return False

    pprint('Iterating over excel rows ...',
        num_indents=num_indents+1,
        new_line_start=True)
    num_rows_updated = 0
    for index, line in df.iterrows():

        if index < excel_row_range[0] or index > excel_row_range[1]:
            continue

        row_id = line[excel_id_col_name]
        if rows_to_change != 'all_rows':
            print('a')
            if row_id not in rows_to_change:
                print('b')
                continue

        # new_value = json.dumps(
        #     json.loads(line[excel_column_name].replace('\n', '')),
        #     indent=4).replace('"', '\"')
        new_value = line[excel_column_name].replace('\n', '')

        # update it in aurora
        try:
            if verbose:
                pprint('\nUpdating aurora, %s = %s ...' % (
                    aurora_id_col_name, row_id),
                    num_indents=num_indents+2)
                pprint('\nUPDATE_TABLE_CELL query:', num_indents=num_indents+3)
                pprint('%s' % UPDATE_TABLE_CELL.format(
                        table=table_name,
                        column=aurora_column_name,
                        new_value='\''+new_value+'\'',
                        table_id_name=aurora_id_col_name,
                        table_id_value=row_id),
                    num_indents=num_indents+4)
            cursor.execute(
                UPDATE_TABLE_CELL.format(
                        table=table_name,
                        column=aurora_column_name,
                        new_value='\''+new_value+'\'',
                        table_id_name=aurora_id_col_name,
                        table_id_value=row_id))
            aurora_db.commit()
            if verbose: pprint('\nSuccessfully ran UPDATE_TABLE_CELL.',
                num_indents=num_indents+3)
            num_rows_updated += 1
        except Exception as e:
            pprint('\nException:', num_indents=num_indents+4)
            pprint('%s' % e, num_indents=num_indents+5)
            pprint('Failed to run query.', num_indents=num_indents+3)
            return False

    if verbose: pprint('', num_indents=num_indents, draw_line=True)
    total_num_excel_rows = excel_row_range[1] - excel_row_range[0]
    pprint('Updated %d out of %d of the rows in the column\n' % (
        num_rows_updated,
        total_num_excel_rows if rows_to_change == 'all_rows' else len(rows_to_change)),
        num_indents=num_indents)




''' !!!!!!!!!!!!!!!! WARNING !!!!!!!!!!!!!!!!

    If you ever use this script again you have to read through it and reconnect portions here and there.
    It was removed from its original configuration and placed here.

    '''
if __name__ == '__main__':

    # create connection to Aurora database (read/write privaleges)
    profile_name = 'ndicke'
    secret_name = 'bdd-ccpa-test-validator'
    session = init_boto3_session(profile_name, num_indents=0, new_line_start=True)
    secret_dct, successful = get_secret(secret_name, num_indents=0, new_line_start=True)
    if not successful: sys.exit()
    aurora_db, successful = connect_to_aurora(secret_dct, num_indents=0, new_line_start=True)
    if not successful: sys.exit()

    # mv ~/Downloads/Firebug\ Scripts\ and\ Data.xlsx testcase_summary_excel.xlsx
    table_name = 'testcase_summary'
    aurora_id_col_name = 'testcase_id'
    aurora_column_name = 'expected_test_output' # 'testcase_description'
    excel_id_col_name = 'testcase_id'
    excel_column_name = 'expected_test_output (json)' # 'test_description'
    excel_filepath = 'testcase_summary_excel.xlsx'
    table_sheetname = 'Functional Tests'
    excel_start_row = 0
    excel_end_row   = 37 # WARNING: testcases 4004 and 4005 were removed in aurora but not excel
    rows_to_change = 'all_rows' # if not 'all_rows': list of IDs

    reg_tester.update_table_column_from_excel_file(
        aurora_db,
        table_name,
        aurora_id_col_name,
        aurora_column_name,
        excel_id_col_name,
        excel_column_name,
        excel_filepath,
        table_sheetname,
        (excel_start_row, excel_end_row),
        rows_to_change=rows_to_change,
        verbose=True,
        num_indents=0)



    # make updates
    # # testcase_ids_to_change = [5,    10,   15,   20,   25,   30,   33  ]
    # testcase_ids_to_change = [1005, 1010, 2005, 2010, 3005, 3010, 4003]
    # # testcase_ids_to_change = 'all_rows'
    # reg_tester.update_table_column_of_json_strings(
    #     aurora_db,
    #     'testcase_summary',
    #     'testcase_id',
    #     'expected_test_output',
    #     [
    #         'request_intake',
    #         'request_summary',
    #         'request_compliance_type'
    #     ],
    #     'test_ccpa',
    #     key_or_value='value',
    #     rows_to_change=testcase_ids_to_change,
    #     verbose=True,
    #     num_indents=0)


