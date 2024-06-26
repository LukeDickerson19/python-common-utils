import sys
import os
import subprocess
from io import StringIO
import pathlib
import json
from jsondiff import diff
import numpy as np
import pandas as pd
pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 20)
pd.set_option('display.max_colwidth', 200)
pd.set_option('display.width', 1000)
from datetime import datetime, timedelta, timezone
import pytz
import requests



# local file paths
REPO_PATH  = str(pathlib.Path(__file__).resolve().parent.parent)
SRC_PATH   = os.path.join(REPO_PATH, 'src')
UTILS_PATH = os.path.join(REPO_PATH, 'common_utils')
sys.path.append(SRC_PATH)
sys.path.append(UTILS_PATH)
PROPERTY_FILEPATH       = os.path.join(SRC_PATH, 'config.properties')
ACCESS_REQUEST_TEMPLATE = os.path.join(SRC_PATH, 'access_request_template.json')
TEST_OUTPUT_TEMPLATE    = os.path.join(SRC_PATH, 'test_output_template_CCPA.json')

# # logging constants
# # log_filepath declared in driver.py
# OUTPUT_TO_CONSOLE = True
# OUTPUT_TO_LOGFILE = True
# INDENT            = '|   '
# DRAW_LINE         = False

# aws aurora constants
AURORA_HOST = 'ccpa_db_host'
AURORA_USER = 'ccpa_db_user'
AURORA_PSWD = 'ccpa_db_pw'
AURORA_DTBS = 'ccpa_db_name'

# SQL queries
GET_TABLE_CELL = '''
select {column}
from {table}
where {table_id_name} = {table_id_value}
'''

UPDATE_TABLE_CELL = '''
update {table}
set {column} = {new_value}
where {table_id_name} = {table_id_value}
'''

GET_TABLE_COLUMNS = '''
select {columns}
from {table}
'''
