
# LIBRARIES

# import standard libraries
import os
import sys
import time
import pathlib
from datetime import datetime, timezone, timedelta

# import non-standard libraries
# None

# import common utils
COMMON_UTILS_REPO_PATH = str(pathlib.Path(__file__).resolve().parent.parent.parent.parent.parent)
LOG_UTIL_PATH          = os.path.join(COMMON_UTILS_REPO_PATH, 'common_utils', 'logging_utils', 'src')
ORACLE_SQL_UTIL_PATH   = os.path.join(COMMON_UTILS_REPO_PATH, 'common_utils', 'sql_utils', 'oracle_sql_utils', 'src')
sys.path.append(LOG_UTIL_PATH)
sys.path.append(ORACLE_SQL_UTIL_PATH)
# print('COMMON_UTILS_REPO_PATH\t', COMMON_UTILS_REPO_PATH)
# print('LOG_UTIL_PATH\t\t', LOG_UTIL_PATH)
# print('ORACLE_SQL_UTIL_PATH\t\t', ORACLE_SQL_UTIL_PATH)
# sys.exit()
import logging_utils
import oracle_sql_utils




# CONSTANTS

LOG_FILENAME = 'log.txt'
LOG_FILEPATH = os.path.join(
	COMMON_UTILS_REPO_PATH, 'common_utils', 'sql_utils', 'oracle_sql_utils', 'log', LOG_FILENAME)
DATA_PATH = os.path.join(
	COMMON_UTILS_REPO_PATH, 'common_utils', 'sql_utils', 'oracle_sql_utils', 'data')
# print('LOG_FILEPATH\t', LOG_FILEPATH)
# print('DATA_PATH\t', DATA_PATH)
# sys.exit()

TEST_VERBOSE = False

# Oracle SQL database credentials
TEST_HOSTNAME = ''
TEST_PORT     = ''
TEST_USERNAME = ''
TEST_PASSWORD = ''
TEST_DATABASE = ''




TEST_SELECT_QUERY = '''
select
	material_id,
	title_asset_id,
	title
from bbv_title
where material_id like 'B00114370%'
'''
