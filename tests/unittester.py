from test_constants import *



class Unittester(unittest.TestCase):



    ################### AWS Utils Tests ###################

    def test_init_aws_session_success(self):
        f = open(TEST_OUTPUT_FILE, 'a')
        f.write('test_init_aws_session_success .................... ')
        session = aws_utils.init_session(profile_name=VALID_PROFILE_NAME)
        assertion = session != None
        test_output = 'success\n' if assertion else 'FAILURE\n'
        f.write(test_output)
        f.close()
        assert(assertion)
    def test_init_aws_session_failure(self):
        f = open(TEST_OUTPUT_FILE, 'a')
        f.write('test_init_aws_session_failure .................... ')
        session = aws_utils.init_session(
            profile_name=INVALID_PROFILE_NAME)
        assertion = session == None
        test_output = 'success\n' if assertion else 'FAILURE\n'
        f.write(test_output)
        f.close()
        assert(assertion)

    @mock_secretsmanager
    def test_get_secret_success(self):
        f = open(TEST_OUTPUT_FILE, 'a')
        f.write('test_get_secret_success .................... ')

        secret_name = 'mock-secret-name'
        secret_values = {
            'ccpa_db_host'              : 'testccpadbhost',
            'ccpa_db_user'              : 'testccpadbuser',
            'ccpa_db_pw'                : 'testccpadbpw',
            'ccpa_db_name'              : 'testccpadbname',
        }
        region_name, _ = general_utils.get_property('AWS', 'region_name')
        conn = boto3.client("secretsmanager", region_name=region_name)
        create_secret = conn.create_secret(
            Name=secret_name,
            SecretString=json.dumps(
                secret_values, indent=4)
        )

        session = aws_utils.init_session(profile_name=VALID_PROFILE_NAME)
        secret_dct, successful = aws_utils.get_secret(session, secret_name, region_name)
        assertion = successful and secret_dct != None
        test_output = 'success\n' if assertion else 'FAILURE\n'
        f.write(test_output)
        f.close()
        assert(assertion)
    def test_get_secret_failure(self):
        f = open(TEST_OUTPUT_FILE, 'a')
        f.write('test_get_secret_failure .................... ')
        secret_name = 'invalid-secret-name'
        region_name, _ = general_utils.get_property('AWS', 'region_name')
        session = aws_utils.init_session(profile_name=VALID_PROFILE_NAME)
        secret_dct, successful = aws_utils.get_secret(session, secret_name, region_name)
        assertion = not successful and secret_dct == None
        test_output = 'success\n' if assertion else 'FAILURE\n'
        f.write(test_output)
        f.close()
        assert(assertion)

    @mock_secretsmanager
    @patch('aws_utils.mysql.connector')
    def test_connect_to_aurora_success(self, mock_mysql_connector):
        f = open(TEST_OUTPUT_FILE, 'a')
        f.write('test_connect_to_aurora_success .................... ')

        secret_name = 'mock-secret-name'
        secret_values = {
            'ccpa_db_host'              : 'testccpadbhost',
            'ccpa_db_user'              : 'testccpadbuser',
            'ccpa_db_pw'                : 'testccpadbpw',
            'ccpa_db_name'              : 'testccpadbname',
        }
        region_name, _ = general_utils.get_property('AWS', 'region_name')
        conn = boto3.client("secretsmanager", region_name=region_name)
        create_secret = conn.create_secret(
            Name=secret_name,
            SecretString=json.dumps(
                secret_values, indent=4)
        )

        session = aws_utils.init_session(profile_name=VALID_PROFILE_NAME)
        secret_dct, successful = aws_utils.get_secret(session, secret_name, region_name)

        aurora_db, successful = aws_utils.connect_to_aurora(
            secret_dct,
            ar_host='ccpa_db_host',
            ar_user='ccpa_db_user',
            ar_pswd='ccpa_db_pw',
            ar_dtbs='ccpa_db_name')
        assertion = successful and aurora_db != None
        test_output = 'success\n' if assertion else 'FAILURE\n'
        f.write(test_output)
        f.close()
        assert(assertion)
    @mock_secretsmanager
    @patch('aws_utils.mysql.connector')
    def test_connect_to_aurora_failure(self, mock_mysql_connector):
        f = open(TEST_OUTPUT_FILE, 'a')
        f.write('test_connect_to_aurora_failure .................... ')

        secret_name = 'mock-secret-name'
        secret_values = {
            'ccpa_db_host'              : 'testccpadbhost',
            'ccpa_db_user'              : 'testccpadbuser',
            'ccpa_db_pw'                : 'testccpadbpw',
            'ccpa_db_name'              : 'testccpadbname',
        }
        region_name, _ = general_utils.get_property('AWS', 'region_name')
        conn = boto3.client("secretsmanager", region_name=region_name)
        create_secret = conn.create_secret(
            Name=secret_name,
            SecretString=json.dumps(
                secret_values, indent=4)
        )

        session = aws_utils.init_session(profile_name=VALID_PROFILE_NAME)
        secret_dct, successful = aws_utils.get_secret(session, secret_name, region_name)

        aurora_db, successful = aws_utils.connect_to_aurora(
            secret_dct,
            ar_host='invalid_ccpa_db_host',
            ar_user='invalid_ccpa_db_user',
            ar_pswd='invalid_ccpa_db_pw',
            ar_dtbs='invalid_ccpa_db_name')
        assertion = not successful and aurora_db == None
        test_output = 'success\n' if assertion else 'FAILURE\n'
        f.write(test_output)
        f.close()
        assert(assertion)

    @mock_secretsmanager
    @patch('aws_utils.mysql.connector')
    def test_select_query_aurora_success(self, mock_mysql_connector):
        f = open(TEST_OUTPUT_FILE, 'a')
        f.write('test_select_query_aurora_success .................... ')

        secret_name = 'mock-secret-name'
        secret_values = {
            'ccpa_db_host'              : 'testccpadbhost',
            'ccpa_db_user'              : 'testccpadbuser',
            'ccpa_db_pw'                : 'testccpadbpw',
            'ccpa_db_name'              : 'testccpadbname',
        }
        region_name, _ = general_utils.get_property('AWS', 'region_name')
        conn = boto3.client("secretsmanager", region_name=region_name)
        create_secret = conn.create_secret(
            Name=secret_name,
            SecretString=json.dumps(
                secret_values, indent=4))

        session = aws_utils.init_session(profile_name=VALID_PROFILE_NAME)
        secret_dct, successful = aws_utils.get_secret(session, secret_name, region_name)

        # each object returned from the original call to something that is replaces with MagicMock
        # needs its own MagicMock and its own return value (thats either a MagicMock also or a value)
        cursor = MagicMock(name='cursor')
        cursor.fetchall.return_value = TEST_RUN_SUMMARY['rows']
        cursor.description = list(map(lambda col : (col, 0), TEST_RUN_SUMMARY['columns']))
        aurora_db = MagicMock(name='aurora_db')
        aurora_db.cursor.return_value = cursor
        aws_utils.connect_to_aurora = MagicMock(name='connect_to_aurora')
        aws_utils.connect_to_aurora.return_value = (aurora_db, True)

        select_query = 'mock select query'
        aurora_db, _ = aws_utils.connect_to_aurora(
            secret_dct,
            host='ccpa_db_host',
            user='ccpa_db_user',
            pswd='ccpa_db_pw',
            dtbs='ccpa_db_name')
        query_results, successful = aws_utils.select_query_aurora(aurora_db, select_query)

        correct_result = [dict(zip(TEST_RUN_SUMMARY['columns'], r)) for r in TEST_RUN_SUMMARY['rows']]
        assertion = successful and query_results == correct_result
        test_output = 'success\n' if assertion else 'FAILURE\n'
        f.write(test_output)
        f.close()
        assert(assertion)
    @mock_secretsmanager
    @patch('aws_utils.mysql.connector')
    def test_select_query_aurora_failure(self, mock_mysql_connector):
        f = open(TEST_OUTPUT_FILE, 'a')
        f.write('test_select_query_aurora_failure .................... ')

        secret_name = 'mock-secret-name'
        secret_values = {
            'ccpa_db_host'              : 'testccpadbhost',
            'ccpa_db_user'              : 'testccpadbuser',
            'ccpa_db_pw'                : 'testccpadbpw',
            'ccpa_db_name'              : 'testccpadbname',
        }
        region_name, _ = general_utils.get_property('AWS', 'region_name')
        conn = boto3.client("secretsmanager", region_name=region_name)
        create_secret = conn.create_secret(
            Name=secret_name,
            SecretString=json.dumps(
                secret_values, indent=4))

        session = aws_utils.init_session(profile_name=VALID_PROFILE_NAME)
        secret_dct, successful = aws_utils.get_secret(session, secret_name, region_name)

        # each object returned from the original call to something that is replaces with MagicMock
        # needs its own MagicMock and its own return value (thats either a MagicMock also or a value)
        cursor = MagicMock(name='cursor')
        cursor.fetchall.return_value = TEST_RUN_SUMMARY['rows']
        cursor.description = None
        aurora_db = MagicMock(name='aurora_db')
        aurora_db.cursor.return_value = cursor
        aws_utils.connect_to_aurora = MagicMock(name='connect_to_aurora')
        aws_utils.connect_to_aurora.return_value = (aurora_db, True)

        select_query = 'mock select query'
        aurora_db, _ = aws_utils.connect_to_aurora(
            secret_dct,
            host='ccpa_db_host',
            user='ccpa_db_user',
            pswd='ccpa_db_pw',
            dtbs='ccpa_db_name')
        query_results, successful = aws_utils.select_query_aurora(aurora_db, select_query)

        correct_result = [dict(zip(TEST_RUN_SUMMARY['columns'], r)) for r in TEST_RUN_SUMMARY['rows']]
        assertion = not successful and query_results != correct_result
        test_output = 'success\n' if assertion else 'FAILURE\n'
        f.write(test_output)
        f.close()
        assert(assertion)

    @mock_secretsmanager
    @patch('aws_utils.mysql.connector')
    def test_update_query_aurora_success(self, mock_mysql_connector):
        f = open(TEST_OUTPUT_FILE, 'a')
        f.write('test_update_query_aurora_success .................... ')

        secret_name = 'mock-secret-name'
        secret_values = {
            'ccpa_db_host'              : 'testccpadbhost',
            'ccpa_db_user'              : 'testccpadbuser',
            'ccpa_db_pw'                : 'testccpadbpw',
            'ccpa_db_name'              : 'testccpadbname',
        }
        region_name, _ = general_utils.get_property('AWS', 'region_name')
        conn = boto3.client("secretsmanager", region_name=region_name)
        create_secret = conn.create_secret(
            Name=secret_name,
            SecretString=json.dumps(
                secret_values, indent=4))

        session = aws_utils.init_session(profile_name=VALID_PROFILE_NAME)
        secret_dct, successful = aws_utils.get_secret(session, secret_name, region_name)

        # each object returned from the original call to something that is replaces with MagicMock
        # needs its own MagicMock and its own return value (thats either a MagicMock also or a value)
        cursor = MagicMock(name='cursor')
        cursor.execute.return_value = None
        cursor.commit.return_value = None
        aurora_db = MagicMock(name='aurora_db')
        aurora_db.cursor.return_value = cursor
        aws_utils.connect_to_aurora = MagicMock(name='connect_to_aurora')
        aws_utils.connect_to_aurora.return_value = (aurora_db, True)

        update_query = 'mock select query'
        aurora_db, _ = aws_utils.connect_to_aurora(
            secret_dct,
            host='ccpa_db_host',
            user='ccpa_db_user',
            pswd='ccpa_db_pw',
            dtbs='ccpa_db_name')
        successful = aws_utils.update_query_aurora(aurora_db, update_query)
        assertion = successful
        test_output = 'success\n' if assertion else 'FAILURE\n'
        f.write(test_output)
        f.close()
        assert(assertion)
    @mock_secretsmanager
    @patch('aws_utils.mysql.connector')
    def test_update_query_aurora_failure(self, mock_mysql_connector):
        f = open(TEST_OUTPUT_FILE, 'a')
        f.write('test_update_query_aurora_failure .................... ')

        secret_name = 'mock-secret-name'
        secret_values = {
            'ccpa_db_host'              : 'testccpadbhost',
            'ccpa_db_user'              : 'testccpadbuser',
            'ccpa_db_pw'                : 'testccpadbpw',
            'ccpa_db_name'              : 'testccpadbname',
        }
        region_name, _ = general_utils.get_property('AWS', 'region_name')
        conn = boto3.client("secretsmanager", region_name=region_name)
        create_secret = conn.create_secret(
            Name=secret_name,
            SecretString=json.dumps(
                secret_values, indent=4))

        session = aws_utils.init_session(profile_name=VALID_PROFILE_NAME)
        secret_dct, successful = aws_utils.get_secret(session, secret_name, region_name)

        aurora_db = MagicMock(name='aurora_db')
        aurora_db.cursor.return_value = Exception
        aws_utils.connect_to_aurora = MagicMock(name='connect_to_aurora')
        aws_utils.connect_to_aurora.return_value = (aurora_db, True)

        update_query = 'mock select query'
        aurora_db, _ = aws_utils.connect_to_aurora(
            secret_dct,
            host='ccpa_db_host',
            user='ccpa_db_user',
            pswd='ccpa_db_pw',
            dtbs='ccpa_db_name')
        successful = aws_utils.update_query_aurora(aurora_db, update_query)
        assertion = not successful
        test_output = 'success\n' if assertion else 'FAILURE\n'
        f.write(test_output)
        f.close()
        assert(assertion)

    @mock_s3
    def test_s3_file_upload_success(self):
        f = open(TEST_OUTPUT_FILE, 'a')
        f.write('test_s3_file_upload_success .................... ')

        region_name, _ = general_utils.get_property('AWS', 'region_name')
        session = aws_utils.init_session(profile_name=VALID_PROFILE_NAME)
        s3_bucket = 'mock_s3_bucket'
        conn = boto3.resource('s3', region_name='us-west-2')
        conn.create_bucket(Bucket=s3_bucket)
        local_filepath  = './results.txt'
        s3_key_filepath = 'mock s3 key filepath'
        successful = aws_utils.s3_file_upload(session, region_name,
            local_filepath, s3_bucket, s3_key_filepath)

        assertion = successful
        test_output = 'success\n' if assertion else 'FAILURE\n'
        f.write(test_output)
        f.close()
        assert(assertion)
    @mock_s3
    def test_s3_file_upload_failure(self):
        f = open(TEST_OUTPUT_FILE, 'a')
        f.write('test_s3_file_upload_failure .................... ')

        region_name, _ = general_utils.get_property('AWS', 'region_name')
        session = aws_utils.init_session(profile_name=VALID_PROFILE_NAME)
        s3_bucket = 'mock_s3_bucket'
        conn = boto3.resource('s3', region_name='us-west-2')
        conn.create_bucket(Bucket=s3_bucket)
        local_filepath  = './results.txt'
        s3_key_filepath = 'mock s3 key filepath'
        successful = aws_utils.s3_file_upload(session, region_name,
            local_filepath, 'invalid bucket name', s3_key_filepath)

        assertion = not successful
        test_output = 'success\n' if assertion else 'FAILURE\n'
        f.write(test_output)
        f.close()
        assert(assertion)

    ################### General Util Tests ###################

    def test_get_property_success(self):
        f = open(TEST_OUTPUT_FILE, 'a')
        f.write('test_get_property_success .................... ')
        valid_value, successful = general_utils.get_property('AWS', 'profile_name')
        assertion = successful
        test_output = 'success\n' if assertion else 'FAILURE\n'
        f.write(test_output)
        f.close()
        assert(assertion)
    def test_get_property_failure(self):
        f = open(TEST_OUTPUT_FILE, 'a')
        f.write('test_get_property_failure .................... ')
        invalid_value, successful = general_utils.get_property('AWS', 'nonexistant_variable')
        assertion = not successful
        test_output = 'success\n' if assertion else 'FAILURE\n'
        f.write(test_output)
        f.close()
        assert(assertion)

    ################### Logging Util Tests ###################

    def test_init_log_success(self):
        f = open(TEST_OUTPUT_FILE, 'a')
        f.write('test_init_log_success .................... ')
        valid_path = os.path.join(REPO_PATH, 'tests', 'mock_logfile.txt')
        try:
            init_log(
                valid_path,
                output_to_console=False,
                output_to_logfile=False,
                clear_old_log=False)
            successful = True
        except Exception as e:
            successful = False
        assertion = successful
        test_output = 'success\n' if assertion else 'FAILURE\n'
        f.write(test_output)
        f.close()
        init_log(LOG_FILEPATH, clear_old_log=False) # reset path to original log file
        assert(assertion)
    def test_init_log_failure(self):
        f = open(TEST_OUTPUT_FILE, 'a')
        f.write('test_init_log_failure .................... ')
        invalid_path = '.'
        try:
            init_log(
                invalid_path,
                output_to_console=False,
                output_to_logfile=False,
                clear_old_log=True)
            successful = True
        except:
            successful = False
        assertion = not successful
        test_output = 'success\n' if assertion else 'FAILURE\n'
        f.write(test_output)
        f.close()
        assert(assertion)

    ################### Snowflake Utils Tests ################

    @mock_secretsmanager
    @patch('snowflake_utils.snowflake.connector')
    def test_init_sf_connection_success(self, mock_snowflake_connector):
        f = open(TEST_OUTPUT_FILE, 'a')
        f.write('test_init_sf_connection_success .................... ')

        secret_name = 'mock-secret-name'
        secret_values = {
            'ccpa_db_user' : 'testccpadbuser',
            'ccpa_db_pswd' : 'testccpadbpswd',
            'ccpa_db_acct' : 'testccpadbacct',
            'ccpa_db_dtbs' : 'testccpadbdtbs',
        }
        region_name, _ = general_utils.get_property('AWS', 'region_name')
        conn = boto3.client("secretsmanager", region_name=region_name)
        create_secret = conn.create_secret(
            Name=secret_name,
            SecretString=json.dumps(
                secret_values, indent=4)
        )

        session = aws_utils.init_session(profile_name=VALID_PROFILE_NAME)
        secret_dct, successful = aws_utils.get_secret(session, secret_name, region_name)

        sf_conn = snowflake_utils.init_connection(
            secret_dct,
            sf_user='ccpa_db_user',
            sf_pswd='ccpa_db_pswd',
            sf_acct='ccpa_db_acct',
            sf_dtbs='ccpa_db_dtbs')
        assertion = sf_conn != None
        test_output = 'success\n' if assertion else 'FAILURE\n'
        f.write(test_output)
        f.close()
        assert(assertion)
    @mock_secretsmanager
    @patch('snowflake_utils.snowflake.connector')
    def test_init_sf_connection_failure(self, mock_snowflake_connector):
        f = open(TEST_OUTPUT_FILE, 'a')
        f.write('test_init_sf_connection_failure .................... ')

        secret_name = 'mock-secret-name'
        secret_values = {
            'ccpa_db_user' : 'testccpadbuser',
            'ccpa_db_pswd' : 'testccpadbpswd',
            'ccpa_db_acct' : 'testccpadbacct',
            'ccpa_db_dtbs' : 'testccpadbdtbs',
        }
        region_name, _ = general_utils.get_property('AWS', 'region_name')
        conn = boto3.client("secretsmanager", region_name=region_name)
        create_secret = conn.create_secret(
            Name=secret_name,
            SecretString=json.dumps(
                secret_values, indent=4)
        )

        session = aws_utils.init_session(profile_name=VALID_PROFILE_NAME)
        secret_dct, successful = aws_utils.get_secret(session, secret_name, region_name)

        sf_conn = snowflake_utils.init_connection(
            secret_dct,
            sf_user='invalid_ccpa_db_user',
            sf_pswd='invalid_ccpa_db_pswd',
            sf_acct='invalid_ccpa_db_acct',
            sf_dtbs='invalid_ccpa_db_dtbs')
        assertion = sf_conn == None
        test_output = 'success\n' if assertion else 'FAILURE\n'
        f.write(test_output)
        f.close()
        assert(assertion)

    @mock_secretsmanager
    @patch('snowflake_utils.snowflake.connector')
    def test_select_query_snowflake_success(self, mock_snowflake_connector):
        f = open(TEST_OUTPUT_FILE, 'a')
        f.write('test_select_query_snowflake_success .................... ')

        secret_name = 'mock-secret-name'
        secret_values = {
            'ccpa_db_user' : 'testccpadbuser',
            'ccpa_db_pswd' : 'testccpadbpswd',
            'ccpa_db_acct' : 'testccpadbacct',
            'ccpa_db_dtbs' : 'testccpadbdtbs',
        }
        region_name, _ = general_utils.get_property('AWS', 'region_name')
        conn = boto3.client("secretsmanager", region_name=region_name)
        create_secret = conn.create_secret(
            Name=secret_name,
            SecretString=json.dumps(
                secret_values, indent=4)
        )
        session = aws_utils.init_session(profile_name=VALID_PROFILE_NAME)
        secret_dct, successful = aws_utils.get_secret(session, secret_name, region_name)

        select_query = 'mock select query'

        # each object returned from the original call to something that is replaces with MagicMock
        # needs its own MagicMock and its own return value (thats either a MagicMock also or a value)
        cursor = MagicMock(name='cursor')
        cursor.fetchall.return_value = TEST_RUN_SUMMARY['rows']
        cursor.description = list(map(lambda col : (col, 0), TEST_RUN_SUMMARY['columns']))
        sf_conn = MagicMock(name='sf_conn')
        sf_conn.cursor.return_value = cursor
        snowflake_utils.init_connection = MagicMock(name='sf_init_conn')
        snowflake_utils.init_connection.return_value = (sf_conn, True)

        sf_conn, _ = snowflake_utils.init_connection(
            secret_dct,
            sf_user='ccpa_db_user',
            sf_pswd='ccpa_db_pswd',
            sf_acct='ccpa_db_acct',
            sf_dtbs='ccpa_db_dtbs')

        query_results, successful = snowflake_utils.select_query_snowflake(
            sf_conn, select_query)

        correct_result = [dict(zip(TEST_RUN_SUMMARY['columns'], r)) for r in TEST_RUN_SUMMARY['rows']]
        assertion = successful and query_results == correct_result
        test_output = 'success\n' if assertion else 'FAILURE\n'
        f.write(test_output)
        f.close()
        assert(assertion)
    @mock_secretsmanager
    @patch('snowflake_utils.snowflake.connector')
    def test_select_query_snowflake_failure(self, mock_snowflake_connector):
        f = open(TEST_OUTPUT_FILE, 'a')
        f.write('test_select_query_snowflake_failure .................... ')

        secret_name = 'mock-secret-name'
        secret_values = {
            'ccpa_db_user' : 'testccpadbuser',
            'ccpa_db_pswd' : 'testccpadbpswd',
            'ccpa_db_acct' : 'testccpadbacct',
            'ccpa_db_dtbs' : 'testccpadbdtbs',
        }
        region_name, _ = general_utils.get_property('AWS', 'region_name')
        conn = boto3.client("secretsmanager", region_name=region_name)
        create_secret = conn.create_secret(
            Name=secret_name,
            SecretString=json.dumps(
                secret_values, indent=4)
        )
        session = aws_utils.init_session(profile_name=VALID_PROFILE_NAME)
        secret_dct, successful = aws_utils.get_secret(session, secret_name, region_name)

        select_query = 'mock select query'

        # each object returned from the original call to something that is replaces with MagicMock
        # needs its own MagicMock and its own return value (thats either a MagicMock also or a value)
        cursor = MagicMock(name='cursor')
        cursor.fetchall.return_value = TEST_RUN_SUMMARY['rows']
        cursor.description = None#list(map(lambda col : (col, 0), TEST_RUN_SUMMARY['columns']))
        sf_conn = MagicMock(name='sf_conn')
        sf_conn.cursor.return_value = cursor
        snowflake_utils.init_connection = MagicMock(name='sf_init_conn')
        snowflake_utils.init_connection.return_value = (sf_conn, True)

        sf_conn, _ = snowflake_utils.init_connection(
            secret_dct,
            sf_user='ccpa_db_user',
            sf_pswd='ccpa_db_pswd',
            sf_acct='ccpa_db_acct',
            sf_dtbs='ccpa_db_dtbs')

        query_results, successful = snowflake_utils.select_query_snowflake(
            sf_conn, select_query)

        correct_result = [dict(zip(TEST_RUN_SUMMARY['columns'], r)) for r in TEST_RUN_SUMMARY['rows']]
        assertion = not successful and query_results != correct_result
        test_output = 'success\n' if assertion else 'FAILURE\n'
        f.write(test_output)
        f.close()
        assert(assertion)


def suite():
    suite = unittest.TestSuite()
    open(TEST_OUTPUT_FILE, 'w').close() # clear TEST_OUTPUT_FILE
    suite.addTests(
       unittest.TestLoader().loadTestsFromTestCase(Unittester)
    )
    return suite

# Testing and Code coverage with Python
# run with:
#   coverage run unittester.py
#   coverage report -m --include=/path/to/repo/src/*,/path/to/repo/common_utils/*
#   coverage report -m --include=../src/*,../common_utils/*
# source: https://developer.ibm.com/recipes/tutorials/testing-and-code-coverage-with-python/
if __name__ == '__main__':

    # init test log
    global LOG_FILEPATH
    log_filepath = os.path.join(REPO_PATH, 'logs', 'test_log.txt')
    LOG_FILEPATH = log_filepath
    init_log(log_filepath,
        output_to_console=False,
        clear_old_log=True)

    # run tests
    unittest.TextTestRunner(verbosity=1).run(suite())

