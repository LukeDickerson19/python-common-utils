from constants import *
import aws_utils
import snowflake_utils
import general_utils
from logging_utils import *



if __name__ == '__main__':

    # mark start time and init log for this hour:
    # log filename structure: log_YEAR-MONTH-DAY_HOUR-AM/PM-TIMEZONE.txt
    start_time = datetime.now(pytz.timezone('US/Pacific'))
    log_filepath = os.path.join(REPO_PATH, 'logs',
        'log_' + start_time.strftime('%Y-%m-%d_%I-%p-%Z') + '.txt')
    init_log(log_filepath,
        output_to_console=False,
        output_to_logfile=False,
        clear_old_log=False)

    # Datetime Format Codes:
    # source: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
    # Ctrl+f: "strftime() and strptime() Format Codes"
    pprint('Starting program at: %s' % start_time.strftime('%Y/%m/%d %I:%M:%S %p %Z'),
        num_indents=0, new_line_start=True)

    # initialize AWS boto3 session and get region_name
    profile_name, _ = general_utils.get_property('AWS', 'profile_name')
    region_name, _  = general_utils.get_property('AWS', 'region_name')
    session = aws_utils.init_session(profile_name=profile_name,
        num_indents=1, new_line_start=True)
    if session == None: sys.exit()

    # connect to Aurora database (read privileges to all tables)
    secret_name1, _ = general_utils.get_property('AWS', 'secret_name1')
    secrets_dct1, successful = aws_utils.get_secret(
        session, secret_name1, region_name,
        num_indents=1, verbose=False,
        new_line_start=True)
    if not successful: sys.exit()
    aurora_db1, successful = aws_utils.connect_to_aurora(
        secrets_dct1, num_indents=1, new_line_start=True)
    if not successful: sys.exit()

    # initialize snowflake connection
    snowflake_conn = snowflake_utils.init_connection(
        secrets_dct1, verbose=True, num_indents=1, new_line_start=True)
    if snowflake_conn == None: sys.exit()

    # # query aws aurora
    # select_query = ?
    # response, successful = aws_utils.select_query_aurora(
    #     aurora_db1, select_query, verbose=False, num_indents=1)
    # if not successful: sys.exit()

    # # query snowflake
    # select_query = ?
    # response, successful = snowflake_utils.select_query_snowflake(
    # snowflake_conn, select_query, verbose=True, num_indents=1)
    # if not successful: sys.exit()







    # log start_time, end_time and duration of program
    end_time = datetime.now(pytz.timezone('US/Pacific'))
    pprint('Regression Test Complete.', num_indents=0, new_line_start=True, draw_line=True)
    pprint('Started Regression Test at: %s' % start_time.strftime(
        '%Y/%m/%d %I:%M:%S %p %Z'), num_indents=0, new_line_start=True)
    pprint('Ended Regression Test at:   %s' % end_time.strftime(
        '%Y/%m/%d %I:%M:%S %p %Z'), num_indents=0)
    pprint('Duration:                   %.2f minutes\n' % ((end_time - start_time).total_seconds() / 60.0), num_indents=0)

    # upload log to s3
    log_s3_bucket, _       = general_utils.get_property('AWS', 'log_s3_bucket')
    log_s3_key_filepath, _ = general_utils.get_property('AWS', 'log_s3_key_filepath')
    aws_utils.s3_file_upload(session, region_name,
        log_filepath, log_s3_bucket, log_s3_key_filepath)


