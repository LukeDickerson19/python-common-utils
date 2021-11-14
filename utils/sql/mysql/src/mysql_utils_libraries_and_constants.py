
# LIBRARIES

# import standard libraries
import os
import sys
import pathlib

# import non-standard libraries
import numpy as np
import pandas as pd
MAX_ROWS = 1000
pd.set_option('display.max_rows', MAX_ROWS)
pd.set_option('display.max_columns', 20)
pd.set_option('display.max_colwidth', 200)
pd.set_option('display.width', 1000)
import mysql.connector
from datetime import datetime

# import common utils
COMMON_UTILS_REPO_PATH = str(pathlib.Path(__file__).resolve().parent.parent.parent.parent.parent)
LOG_UTIL_PATH          = os.path.join(COMMON_UTILS_REPO_PATH, 'utils', 'logging', 'src')
sys.path.append(LOG_UTIL_PATH)
import logging_utils
# print('COMMON_UTILS_REPO_PATH\t', COMMON_UTILS_REPO_PATH)
# print('LOG_UTIL_PATH\t', LOG_UTIL_PATH)
# sys.exit()



# CONSTANTS
# None


