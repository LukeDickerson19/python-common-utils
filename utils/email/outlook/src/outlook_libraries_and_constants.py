
# LIBRARIES

# import standard libraries
import os
import sys
import json
import pathlib

# import non-standard libraries
import pytz
from datetime import datetime, timezone, timedelta
import win32com.client as win32
from dateutil import tz
# source: https://stackoverflow.com/questions/4770297/convert-utc-datetime-string-to-local-datetime

# import common utils
COMMON_UTILS_REPO_PATH = str(pathlib.Path(__file__).resolve().parent.parent.parent.parent.parent)
LOG_UTIL_PATH          = os.path.join(COMMON_UTILS_REPO_PATH, 'utils', 'logging', 'src')
sys.path.append(LOG_UTIL_PATH)
import logging_utils
# print('COMMON_UTILS_REPO_PATH\t', COMMON_UTILS_REPO_PATH)
# print('LOG_UTIL_PATH\t', LOG_UTIL_PATH)




# CONSTANTS
DATA_PATH = os.path.join(COMMON_UTILS_REPO_PATH, 'utils', 'email', 'outlook', 'data')
