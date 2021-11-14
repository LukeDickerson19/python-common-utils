from libraries_and_constants import *



def test_print(log):

	# test num_indents and multi line indentation
	log.print('a', num_indents=0)
	log.print('b', num_indents=1)
	log.print('c', num_indents=2)
	log.print('d', num_indents=3)
	log.print('e', num_indents=4)
	log.print('indented\nmulti\nline\nstring', num_indents=5)

	# test new_line_start
	console_str, logfile_str = log.print(
		'new_line_start=True, draw_line=False',
		num_indents=1, new_line_start=True)
	console_str, logfile_str = log.print(
		'new_line_start=True, draw_line=True',
		num_indents=1, new_line_start=True, draw_line=True)
	console_str, logfile_str = log.print(
		'new_line_start=False',
		num_indents=1, new_line_start=False)

	# test new_line_end
	console_str, logfile_str = log.print(
		'new_line_end=True, draw_line=False',
		num_indents=1, new_line_end=True)
	console_str, logfile_str = log.print(
		'new_line_end=True, draw_line=True',
		num_indents=1, new_line_end=True, draw_line=True)
	console_str, logfile_str = log.print(
		'new_line_end=False',
		num_indents=1, new_line_end=False)

	# test return value
	print('\nconsole_str:')
	print(console_str)
	print('\nlogfile_str:')
	print(logfile_str)	
	print()

def test_print_dct(log):
	dct0 = {'a' : 1, 'b' : 2, 'c' : 3}
	log.print_dct(dct0, num_indents=3)
	print()

def test_print_same_line(log):

	sleep_time = 0.5 # seconds
	num_indents = 3
	print('... starting test_print_same_line on this line ...')

	# new text has shorter lines
	log.print_same_line('aaaa', num_indents=num_indents)
	time.sleep(sleep_time)
	log.print_same_line('bbb', num_indents=num_indents)
	time.sleep(sleep_time)
	log.print_same_line('cc', num_indents=num_indents)
	time.sleep(sleep_time)
	log.print_same_line('d', num_indents=num_indents)
	time.sleep(sleep_time)
	log.print_same_line('', num_indents=0)
	time.sleep(sleep_time)

	# new text has longer lines
	log.print_same_line('a', num_indents=num_indents)
	time.sleep(sleep_time)
	log.print_same_line('bb', num_indents=num_indents)
	time.sleep(sleep_time)
	log.print_same_line('ccc', num_indents=num_indents)
	time.sleep(sleep_time)
	log.print_same_line('dddd', num_indents=num_indents)
	time.sleep(sleep_time)
	log.print_same_line('', num_indents=0)
	time.sleep(sleep_time)

	# new text has more lines
	log.print_same_line('a', num_indents=num_indents)
	time.sleep(sleep_time)
	log.print_same_line('b\nb', num_indents=num_indents)
	time.sleep(sleep_time)
	log.print_same_line('c\nc\nc', num_indents=num_indents)
	time.sleep(sleep_time)
	log.print_same_line('d\nd\nd\nd', num_indents=num_indents)
	time.sleep(sleep_time)
	log.print_same_line('', num_indents=0)
	time.sleep(sleep_time)

	# new text has less lines
	log.print_same_line('a\na\na\na', num_indents=num_indents)
	time.sleep(sleep_time)
	log.print_same_line('b\nb\nb', num_indents=num_indents)
	time.sleep(sleep_time)
	log.print_same_line('c\nc', num_indents=num_indents)
	time.sleep(sleep_time)
	log.print_same_line('d', num_indents=num_indents)
	time.sleep(sleep_time)
	log.print_same_line('', num_indents=0, end='')
	time.sleep(sleep_time)
	print('... ending test_print_same_line on this line ...')

	# verify regular log.print() works after print_same_line()
	log.print('a', num_indents=0)
	log.print('b', num_indents=1)
	log.print('c', num_indents=2)
	log.print('d', num_indents=3)
	log.print('e', num_indents=4)
	log.print('indented\nmulti\nline\nstring', num_indents=5)

	# verify print_same_line() works after regular log.print()
	log.print_same_line('testing', num_indents=num_indents)
	time.sleep(3*sleep_time)
	log.print_same_line('print_same_line()', num_indents=num_indents)
	time.sleep(3*sleep_time)
	log.print_same_line('after', num_indents=num_indents)
	time.sleep(3*sleep_time)
	log.print_same_line('regular print()', num_indents=num_indents)
	time.sleep(3*sleep_time)
	log.print_same_line('', num_indents=0, end='')
	time.sleep(3*sleep_time)

	log.print('testing regular print() after print_same_line() again',
		num_indents=num_indents)
	print()



if __name__ == '__main__':

	log = logging_utils.Log(LOG_FILEPATH)
	test_print(log)
	test_print_dct(log)
	test_print_same_line(log)
