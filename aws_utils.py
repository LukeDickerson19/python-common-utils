import sys
import json
from logging_utils import pprint
import boto3
import mysql.connector
from constants import *



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

''' s3_file_upload()

    Description:
        Upload a local file to a specific AWS S3 path.

    Arguments:
        local_filepath ... string .... local path to the file to upload to s3
        s3_bucket ........ string .... s3 bucket to upload the file to
        s3_filepath ...... string .... s3 key (filepath excluding bucket) to upload the file to
        verbose .......... boolean ... log more details of this functions execution
        num_indents ...... int ....... base the number of indents for all logging in this function
        new_line_start ... boolean ... print a new line before the the first log from this function

    Returns:
        successful ....... boolean ... flag if the function executed successfully without any errors

    '''
def s3_file_upload(
    session,
    region_name,
    local_filepath,
    s3_bucket,
    s3_key_filepath,
    verbose=False,
    num_indents=0,
    new_line_start=False):

    if verbose:
        pprint('Uploading file to s3 ...',
            num_indents=num_indents,
            new_line_start=new_line_start)
        pprint('local_filepath:  %s' % local_filepath,  num_indents=num_indents+1)
        pprint('s3_bucket:       %s' % s3_bucket,       num_indents=num_indents+1)
        pprint('s3_key_filepath: %s' % s3_key_filepath, num_indents=num_indents+1)

    client = session.client(
        service_name='s3',
        region_name=region_name)
    try:
        client = session.client(
            service_name='s3',
            region_name=region_name)
        response = client.put_object(
            Bucket=s3_bucket,
            Key=s3_key_filepath,
            Body=open(local_filepath, 'rb'))
        if verbose: pprint('Successfully uploaded file to s3.', num_indents=num_indents)
        successful = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except Exception as e:
        if verbose:
            pprint('Exception:', num_indents=num_indents+1)
            pprint('%s' % e, num_indents=num_indents+2)
            pprint('Failed to upload file to s3.', num_indents=num_indents)
        successful = False
    return successful


