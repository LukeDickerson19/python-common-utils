import sys
import os
import pathlib
REPO_PATH = str(pathlib.Path(__file__).resolve().parent.parent)
SRC_PATH  = os.path.join(REPO_PATH, 'src')
sys.path.append(SRC_PATH)

from constants import *
import aws_utils
import snowflake_utils
import general_utils
from logging_utils import *

import boto3
import boto.rds
import moto
from moto import mock_secretsmanager, mock_rds, mock_sns_deprecated, mock_s3
from mock import Mock, MagicMock, patch
import unittest
from moto import core




YESTERDAY = datetime.now(tz=timezone.utc) - timedelta(days=1)
TEST_OUTPUT_FILE = './results.txt'


