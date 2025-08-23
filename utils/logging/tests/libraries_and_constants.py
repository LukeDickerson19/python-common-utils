
# LIBRARIES

# import standard libraries
import os
import sys
import time
import pathlib

# import non-standard libraries
# None

# import common utils
COMMON_UTILS_REPO_PATH = str(pathlib.Path(__file__).resolve().parent.parent.parent.parent)
LOG_UTIL_PATH          = os.path.join(COMMON_UTILS_REPO_PATH, 'utils', 'logging', 'src')
sys.path.append(LOG_UTIL_PATH)
import logging_utils
# print('COMMON_UTILS_REPO_PATH\t', COMMON_UTILS_REPO_PATH)
# print('LOG_UTIL_PATH\t', LOG_UTIL_PATH)



# CONSTANTS
LOG_FILENAME           = 'log.txt' # 'log_%s' % datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S.txt")
LOG_FILEPATH           = os.path.join(COMMON_UTILS_REPO_PATH, 'utils', 'logging', 'log', LOG_FILENAME)
# print('LOG_FILEPATH\t', LOG_FILEPATH)

