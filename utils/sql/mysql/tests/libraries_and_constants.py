
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
LOG_UTIL_PATH          = os.path.join(COMMON_UTILS_REPO_PATH, 'utils', 'logging', 'src')
MYSQL_UTIL_PATH        = os.path.join(COMMON_UTILS_REPO_PATH, 'utils', 'sql', 'mysql', 'src')
sys.path.append(LOG_UTIL_PATH)
sys.path.append(MYSQL_UTIL_PATH)
# print('COMMON_UTILS_REPO_PATH\t', COMMON_UTILS_REPO_PATH)
# print('LOG_UTIL_PATH\t\t', LOG_UTIL_PATH)
# print('MYSQL_UTIL_PATH\t\t', MYSQL_UTIL_PATH)
# sys.exit()
import logging_utils
import mysql_utils




# CONSTANTS

LOG_FILENAME = 'log.txt'
LOG_FILEPATH = os.path.join(COMMON_UTILS_REPO_PATH, 'utils', 'sql', 'mysql', 'log', LOG_FILENAME)
DATA_PATH    = os.path.join(COMMON_UTILS_REPO_PATH, 'utils', 'sql', 'mysql', 'data')
# print('LOG_FILEPATH\t', LOG_FILEPATH)
# print('DATA_PATH\t', DATA_PATH)
# sys.exit()

TEST_VERBOSE = False

# MySQL database credentials
TEST_HOSTNAME = ''
TEST_PORT     = ''
TEST_USERNAME = ''
TEST_PASSWORD = ''
TEST_DATABASE = ''


TEST_SELECT_QUERY = '''
select
	asset_id,
	provider_id,
	description
from eam_asset
limit 10
'''
