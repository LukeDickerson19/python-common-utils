
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
LOG_FILENAME = 'log.txt' # 'log_%s' % datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S.txt")
LOG_FILEPATH = os.path.join(COMMON_UTILS_REPO_PATH, 'utils', 'logging', 'log', LOG_FILENAME)
# print('LOG_FILEPATH\t', LOG_FILEPATH)


log = logging_utils.Log(
	LOG_FILEPATH,
	output_to_console=True,
	output_to_logfile=True,
	clear_old_log=True,
)

def test_print():
	log.print('\ntest_print():')

	# test num_indents and multi line indentation
	log.print('a', i=0)
	log.print('b', i=1)
	log.print('c', i=2)
	log.print('d', i=3)
	log.print('e', i=4)
	log.print('indented\nmulti\nline\nstring', i=5)

	# test new line start
	log.print('new line start = True, draw line = False', i=1, ns=True)
	log.print('new line start = True, draw line = True', i=1, ns=True, d=True)
	log.print('new line start = False', i=1, ns=False)

	# test new line end
	log.print('new line end = True, draw line = False', i=1, ne=True)
	log.print('new line end = True, draw line = True', i=1, ne=True, d=True)
	console_str, logfile_str = log.print('new line end = False', i=1, ne=False)

	# test return value
	print('\n    console_str: "%s"' % console_str)
	print('\n    logfile_str: "%s"' % logfile_str)
	print()

	# test prepend datetime
	log2 = logging_utils.Log(
		output_to_console=True,
		output_to_logfile=False,
		prepend_datetime_fmt='%y-%m-%d %H:%M:%S.%f %Z')
	log2.print('testing single line prepend_datetime_fmt', ns=True)
	log2.print('testing\nmulti\nline\nprepend_datetime_fmt', i=1)
	log2.print('testing single line indented prepend_datetime_fmt', i=2)

	# test prepend memory usage
	log3 = logging_utils.Log(
		output_to_console=True,
		output_to_logfile=False,
		prepend_memory_usage=True)
	log3.print('testing single line prepend_memory_usage', ns=True)
	log3.print('testing\nmulti\nline\nprepend_memory_usage', i=1)
	log3.print('testing single line indented prepend_memory_usage', i=2)

	# test both prepend datetime and memory usage
	log4 = logging_utils.Log(
		output_to_console=True,
		output_to_logfile=False,
		prepend_datetime_fmt='%y-%m-%d %H:%M:%S.%f %Z',
		prepend_memory_usage=True)
	log4.print('testing single line prepend_datetime_fmt and prepend_memory_usage', ns=True)
	log4.print('testing\nmulti\nline\nprepend_datetime_fmt\nand\nprepend_memory_usage', i=1)
	log4.print('testing single line indented prepend_datetime_fmt and prepend_memory_usage', i=2)

def test_print_dct():
	log.print('\ntest_print_dct():')
	dct0 = {'a' : 1, 'b' : 2, 'c' : 3}
	log.print_dct(dct0, i=1, ne=True)

def test_overwrite_prev_print():
	log.print('\ntest_overwrite_prev_print():')

	sleep_time = 0.5 # seconds
	i = 1

	# new text has shorter lines
	log.print('aaaa', i=i, overwrite_prev_print=False)
	time.sleep(sleep_time)
	log.print('bbb', i=i, overwrite_prev_print=True)
	time.sleep(sleep_time)
	log.print('cc', i=i, overwrite_prev_print=True)
	time.sleep(sleep_time)
	log.print('d', i=i, overwrite_prev_print=True)
	time.sleep(sleep_time)
	log.print('', i=0, overwrite_prev_print=True)
	time.sleep(sleep_time)

	# new text has longer lines
	log.print('a', i=i, overwrite_prev_print=True)
	time.sleep(sleep_time)
	log.print('bb', i=i, overwrite_prev_print=True)
	time.sleep(sleep_time)
	log.print('ccc', i=i, overwrite_prev_print=True)
	time.sleep(sleep_time)
	log.print('dddd', i=i, overwrite_prev_print=True)
	time.sleep(sleep_time)
	log.print('', i=0, overwrite_prev_print=True)
	time.sleep(sleep_time)

	# new text has more lines
	log.print('a', i=i, overwrite_prev_print=True)
	time.sleep(sleep_time)
	log.print('b\nb', i=i, overwrite_prev_print=True)
	time.sleep(sleep_time)
	log.print('c\nc\nc', i=i, overwrite_prev_print=True)
	time.sleep(sleep_time)
	log.print('d\nd\nd\nd', i=i, overwrite_prev_print=True)
	time.sleep(sleep_time)
	log.print('', i=0, overwrite_prev_print=True)
	time.sleep(sleep_time)

	# new text has less lines
	log.print('a\na\na\na', i=i, overwrite_prev_print=True)
	time.sleep(sleep_time)
	log.print('b\nb\nb', i=i, overwrite_prev_print=True)
	time.sleep(sleep_time)
	log.print('c\nc', i=i, overwrite_prev_print=True)
	time.sleep(sleep_time)
	log.print('d', i=i, overwrite_prev_print=True)
	time.sleep(sleep_time)
	log.print('', i=0, end='', overwrite_prev_print=True)
	time.sleep(sleep_time)

	# verify regular log.print() works after overwrite_prev_print
	log.print('a', i=0)
	log.print('b', i=1)
	log.print('c', i=2)
	log.print('d', i=3)
	log.print('e', i=4)
	log.print('indented\nmulti\nline\nstring', i=5)

	# verify overwrite_prev_print works after regular log.print()
	log.print('test', i=i, overwrite_prev_print=True)
	time.sleep(3*sleep_time)
	log.print('overwrite_prev_print', i=i, overwrite_prev_print=True)
	time.sleep(3*sleep_time)
	log.print('after', i=i, overwrite_prev_print=True)
	time.sleep(3*sleep_time)
	log.print('regular print()', i=i, overwrite_prev_print=True)
	time.sleep(3*sleep_time)
	log.print('', i=0, end='', overwrite_prev_print=True)
	time.sleep(3*sleep_time)

	log.print('test regular print() after overwrite_prev_print', i=i, ne=True)



if __name__ == '__main__':

	test_print()
	test_print_dct()
	# test_overwrite_prev_print()

	log.close()