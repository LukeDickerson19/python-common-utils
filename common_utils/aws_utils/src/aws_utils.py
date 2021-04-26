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

''' s3_file_download()

    Description:
        Download a specified file on s3 to a specified local path.

    Arguments:
        session .......... boto3 session object ... AWS session object
        region_name ...... string ................. aws region name of where s3 database is hosted
        local_filepath ... string ................. local path to download the file to
        s3_bucket ........ string ................. s3 bucket to download the file from
        s3_filepath ...... string ................. s3 key (filepath excluding bucket) to to download the file from
        verbose .......... boolean ................ log more details of this functions execution
        num_indents ...... int .................... base the number of indents for all logging in this function
        new_line_start ... boolean ................ print a new line before the the first log from this function

    Returns:
        successful ....... boolean ................ flag if the function executed successfully without any errors

    '''
def s3_file_download(
    session,
    region_name,
    local_filepath,
    s3_bucket,
    s3_key_filepath,
    verbose=False,
    num_indents=0,
    new_line_start=False):

    log.print('Downloading file from s3 ...',
        num_indents=num_indents, new_line_start=new_line_start)
    if verbose:
        log.print('s3_bucket:       %s' % s3_bucket,       num_indents=num_indents+1)
        log.print('s3_key_filepath: %s' % s3_key_filepath, num_indents=num_indents+1)
        log.print('local_filepath:  %s' % local_filepath,  num_indents=num_indents+1)

    try:
        client = session.client(
            service_name='s3',
            region_name=region_name)
        response = client.dowload_file(
            s3_bucket, s3_key_filepath, local_filepath)
        if verbose:
            log.print('Successfully downloaded file from s3.', num_indents=num_indents)
        successful = True
    except Exception as e:
        log.print('Exception:', num_indents=num_indents+1)
        log.print('%s' % e, num_indents=num_indents+2)
        log.print('Failed to download file from s3', num_indents=num_indents)
        successful = False

    return successful

''' send_email()
    
    Description:
        Send an email using a specified AWS SNS Topic

    Arguments:
        session ......... boto3 session object ... AWS session object
        region_name ..... string ................. aws region name, ex: us-west-2
        sns_topic ....... string ................. ARN of sns topic, ex: arn:aws:sns:us-west-2:708352435812:bane-bdd-ccpa-alerts
        email_subject ... string .................
        email_body ...... string .................
        verbose ......... boolean ................ log more details of this functions execution
        num_indents ..... int .................... base the number of indents for all logging in this function
        new_line_start .. boolean ................ print a new line before the the first log from this function

    '''
def send_email(
    session,
    region_name,
    sns_topic,
    email_subject,
    email_body,
    verbose=False,
    num_indents=0,
    new_line_start=False):

    log.print('Sending email with AWS SNS topic ...',
        num_indents=num_indents, new_line_start=new_line_start)
    if verbose:
        log.print('SNS topic:       %s' % sns_topic,     num_indents=num_indents+1)
        log.print('Email Subject:   %s' % email_subject, num_indents=num_indents+1)
        log.print('Email Body:'                          num_indents=num_indents+1)
        log.print('%s\n' % email_body,                   num_indents=num_indents+2)

    try:
        aws_sns = session.client('sns', region_name=region_name)
        aws_sns.publish(
            TopicArn=sns_topic,
            Subject=email_subject,
            Message=email_body)
        log.print('Successfully sent email.', num_indents=num_indents)
        successful = True
    except Exception as e:
        log.print('Exception:', num_indents=num_indents+1)
        log.print('%s' % e, num_indents=num_indents+2)
        log.print('Failed to send email.', num_indents=num_indents)
        successful = False

    return successful

''' lambda_handler()

    Description:
        Copy this function into the AWS console to create a lambda function with the proper syntax.

    '''
def lambda_handler(event, context):

    ######## lambda logic goes here ###############

    return {
        'statusCode' : 200,
        'body' : json.dumps('Hello from Lambda')
    }




''' Spark Stuff

import sys
import findspark
findspark.init()

from pyspark.sql import SparkSession
from pyspark import SparkContext

sc = sparkContext()
spark = SparkSession(sc)

s3_path = ...
rdd = sc.wholeTextFiles(s3_path)
# wholeTextFiles gets all the filespaths (and none of the sub-directory paths) in s3_path
# and the contents of each file into an rdd (table)  where each file gets a row
# ex: [(u's3://cmdt-user/ndicke/test_json_with_pii.json', u'{"name":"Michael"}\n{"name":"Andy", "age":30}\n'), ...]
print('rdd rows:')
for row in rdd.collect():
    filename = str(row[0])
    file_content = str(row[1]).split('\n')
    print(filename)
    print(file_content)
    print()

sys.exit()

def func(f):
    path, content = f
    lines = content.split('\n')
    for line in lines:
        print(line)
    return []

func_ret_for_all_files = rdd.flatMap(lambda f : func(f)).collect()
for row in func_ret_for_all_files:
    print(row)


############ oooooorrrrrrrrrrr ... ###############

rdd = sc.textFile(path, use_unicode=False)
rdd = rdd.filter(lambda x : ('/getdata/' not in x))
rdd = rdd.map(lambda x : x.split('\t'))
rdd = rdd.filter(lambda x : len(x) == 7)

def func(line):
    [col1, col2, col3] = line
    return {
        'k1': 'v1',
        'k2': 'v2',
        'k3': 'v3'
    }
rdd = rdd.map(func)

df = rdd.toDF()

##################### oooooorrrr ... ############

https://towardsdatascience.com/production-data-processing-with-apache-spark-96a58dfd3fe7



######################## orrrrr ... ################

# if the cluster doesn't have the findspark python lib:
#       sudo pip install findspark
#       OR
#       sudo python3 -m pip install findspark

# access cluster via ssh with
# ssh -i ~/.ssh/bane-emr-bdd-key.pem hadoop@10.176.12.235



# example script a.py
# simple run it with python a.py

# import findspark
# findspark.init()

from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

# json_path = 's3://cmdt-user/ndicke/test_dir/people.json'
json_path = './test_dir/people.json'
df = spark.read.json(json_path)

df.show()




'''
