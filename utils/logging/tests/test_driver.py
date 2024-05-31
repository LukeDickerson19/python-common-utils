from libraries_and_constants import *



def test_print(log):

	# test num_indents and multi line indentation
	log.print('a', i=0)
	log.print('b', i=1)
	log.print('c', i=2)
	log.print('d', i=3)
	log.print('e', i=4)
	log.print('indented\nmulti\nline\nstring', i=5)

	# test new_line_start
	console_str, logfile_str = log.print(
		'new_line_start=True, draw_line=False',
		i=1, ns=True)
	console_str, logfile_str = log.print(
		'new_line_start=True, draw_line=True',
		i=1, ns=True, d=True)
	console_str, logfile_str = log.print(
		'new_line_start=False',
		i=1, ns=False)

	# test new_line_end
	console_str, logfile_str = log.print(
		'new_line_end=True, draw_line=False',
		i=1, ne=True)
	console_str, logfile_str = log.print(
		'new_line_end=True, draw_line=True',
		i=1, ne=True, d=True)
	console_str, logfile_str = log.print(
		'new_line_end=False',
		i=1, ne=False)

	# test prepend date
	log2 = logging_utils.Log(prepend_datetime_fmt='%y-%m-%d %H:%M:%S.%f %Z')
	log2.print('testing single line prepend_datetime_fmt', ns=True)
	log2.print('testing\nmulti\nline\nprepend_datetime_fmt')

	# test prepend memory usage
	log3 = logging_utils.Log(prepend_memory_usage=True)
	log3.print('testing single line prepend_memory_usage', ns=True)
	log3.print('testing\nmulti\nline\nprepend_memory_usage')

	# test return value
	print('\nconsole_str:')
	print(console_str)
	print('\nlogfile_str:')
	print(logfile_str)	
	print()

def test_print_dct(log):
	dct0 = {'a' : 1, 'b' : 2, 'c' : 3}
	log.print_dct(dct0, i=3)
	print()

def test_print_same_line(log):

	sleep_time = 0.5 # seconds
	num_indents = 3
	print('... starting test_print_same_line on this line ...')

	# new text has shorter lines
	log.print_same_line('aaaa', i=num_indents)
	time.sleep(sleep_time)
	log.print_same_line('bbb', i=num_indents)
	time.sleep(sleep_time)
	log.print_same_line('cc', i=num_indents)
	time.sleep(sleep_time)
	log.print_same_line('d', i=num_indents)
	time.sleep(sleep_time)
	log.print_same_line('', i=0)
	time.sleep(sleep_time)

	# new text has longer lines
	log.print_same_line('a', i=num_indents)
	time.sleep(sleep_time)
	log.print_same_line('bb', i=num_indents)
	time.sleep(sleep_time)
	log.print_same_line('ccc', i=num_indents)
	time.sleep(sleep_time)
	log.print_same_line('dddd', i=num_indents)
	time.sleep(sleep_time)
	log.print_same_line('', i=0)
	time.sleep(sleep_time)

	# new text has more lines
	log.print_same_line('a', i=num_indents)
	time.sleep(sleep_time)
	log.print_same_line('b\nb', i=num_indents)
	time.sleep(sleep_time)
	log.print_same_line('c\nc\nc', i=num_indents)
	time.sleep(sleep_time)
	log.print_same_line('d\nd\nd\nd', i=num_indents)
	time.sleep(sleep_time)
	log.print_same_line('', i=0)
	time.sleep(sleep_time)

	# new text has less lines
	log.print_same_line('a\na\na\na', i=num_indents)
	time.sleep(sleep_time)
	log.print_same_line('b\nb\nb', i=num_indents)
	time.sleep(sleep_time)
	log.print_same_line('c\nc', i=num_indents)
	time.sleep(sleep_time)
	log.print_same_line('d', i=num_indents)
	time.sleep(sleep_time)
	log.print_same_line('', i=0, end='')
	time.sleep(sleep_time)
	print('... ending test_print_same_line on this line ...')

	# verify regular log.print() works after print_same_line()
	log.print('a', i=0)
	log.print('b', i=1)
	log.print('c', i=2)
	log.print('d', i=3)
	log.print('e', i=4)
	log.print('indented\nmulti\nline\nstring', i=5)

	# verify print_same_line() works after regular log.print()
	log.print_same_line('testing', i=num_indents)
	time.sleep(3*sleep_time)
	log.print_same_line('print_same_line()', i=num_indents)
	time.sleep(3*sleep_time)
	log.print_same_line('after', i=num_indents)
	time.sleep(3*sleep_time)
	log.print_same_line('regular print()', i=num_indents)
	time.sleep(3*sleep_time)
	log.print_same_line('', i=0, end='')
	time.sleep(3*sleep_time)

	log.print('testing regular print() after print_same_line() again', i=num_indents)
	print()



if __name__ == '__main__':

	log = logging_utils.Log(LOG_FILEPATH)
	test_print(log)
	# test_print_dct(log)
	# test_print_same_line(log)
