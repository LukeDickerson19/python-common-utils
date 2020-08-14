from constants import *
import sys


''' init_log()

    Description:
        Set the LOG_FILEPATH to a global variable within this file for the pprint() function to use.
        Optionally set OUTPUT_TO_CONSOLE and OUTPUT_TO_LOGFILE differently than how they're set in constants.py

    Arguments:
        log_filepath ... string ... complete path to the log file

    Returns:
        Nothing

    '''
def init_log(
    log_filepath,
    output_to_console=OUTPUT_TO_CONSOLE,
    output_to_logfile=OUTPUT_TO_LOGFILE,
    clear_old_log=False):

    global LOGFILE_PATH
    LOGFILE_PATH = log_filepath

    global OUTPUT_TO_CONSOLE
    OUTPUT_TO_CONSOLE = output_to_console

    global OUTPUT_TO_LOGFILE
    OUTPUT_TO_LOGFILE = output_to_logfile

    if clear_old_log:
        open(log_filepath, 'w').close() # clear log


''' pprint()

    Description:
        Log 'string' argument to logfile and/or console.
        Set how indented the line should be with 'num_indents' int argument.
            ^^^ very useful for organizing log ^^^

    Arguments:
        string .... string ........... what will be printed
        string .... indent ........... what an indent looks like
        int ....... num_indents ...... number of indents to put in front of the string
        boolean ... new_line_start ... print a new line in before the string
        boolean ... new_line_end ..... print a new line in after the string
        boolean ... draw_line ........ draw a line on the blank line before or after the string

    Returns:
        Nothing

    '''
def pprint(
    string='',
    num_indents=0,
    new_line_start=False,
    new_line_end=False,
    draw_line=DRAW_LINE):

    def output(out_loc):
        indent = len(INDENT)*' ' if out_loc != sys.stdout else INDENT
        total_indent0 = ''.join([indent] * num_indents)
        total_indent1 = ''.join([indent] * (num_indents + 1))
        if new_line_start:
            print(total_indent1 if draw_line else total_indent0, file=out_loc)
        for s in string.split('\n'):
            print(total_indent0 + s, file=out_loc)
        if new_line_end:
            print(total_indent1 if draw_line else total_indent0, file=out_loc)

    if OUTPUT_TO_CONSOLE:
        output(sys.stdout)
    if OUTPUT_TO_LOGFILE:
        logfile = open(LOGFILE_PATH, 'a')
        output(logfile)
        logfile.close()


