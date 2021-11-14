
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
OUTLOOK_UTIL_PATH      = os.path.join(COMMON_UTILS_REPO_PATH, 'utils', 'email', 'outlook', 'src')
sys.path.append(LOG_UTIL_PATH)
sys.path.append(OUTLOOK_UTIL_PATH)
# print('COMMON_UTILS_REPO_PATH\t', COMMON_UTILS_REPO_PATH)
# print('LOG_UTIL_PATH\t\t', LOG_UTIL_PATH)
# print('OUTLOOK_UTIL_PATH\t', OUTLOOK_UTIL_PATH)
import logging_utils
import outlook_utils




# CONSTANTS
LOG_FILENAME           = 'log.txt'
LOG_FILEPATH           = os.path.join(
	COMMON_UTILS_REPO_PATH, 'utils', 'email', 'outlook', 'log', LOG_FILENAME)
# print('LOG_FILEPATH\t', LOG_FILEPATH)
DATA_PATH = os.path.join(
	COMMON_UTILS_REPO_PATH, 'utils', 'email', 'outlook', 'data')
# print('DATA_PATH\t', DATA_PATH)

TEST_VERBOSE       = False
TEST_EMAIL_FROM    = 'ld085a@att.com'
TEST_EMAIL_TO      = ['ld085a@att.com']
TEST_EMAIL_SUBJECT = 'Test Hello World'
TEST_EMAIL_BODY    = "Hello\nworld\nthis\nis\nLuke."
TEST_EMAIL_CC      = ['ld085a@att.com']
TEST_EMAIL_BCC     = ['ld085a@att.com']
TEST_EMAIL_ATTACHMENTS = [
	os.path.join(DATA_PATH, 'sent_attachments', 'test_csv_file.csv'),
	os.path.join(DATA_PATH, 'sent_attachments', 'test_word_doc.docx')
	# os.path.join(DATA_PATH, 'sent_attachments', 'test_python_script.py'), # Outlook doesn't trust .py files
]

