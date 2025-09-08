
# LIBRARIES

# import standard libraries
import os
import sys
import json
from datetime import datetime
from zoneinfo import ZoneInfo
import tracemalloc # used to get memory usage of code using logging

# import non-standard libraries
import pandas as pd

# import common utils
# None



# CONSTANTS
# None




class Log:

    ''' __init__()

        Description:
            Initialize a log to print to the console and/or a log file.

        Arguments:
            log_filepath ........... string .... complete path to the log file
            output_to_console ...... boolean ... flag to print to the console or not
            output_to_logfile ...... boolean ... flag to print to the log file or not
            clear_old_log .......... boolean ... flag to clear the log file or not
            indent ................. string .... what an indent looks like in the log
            prepend_datetime_fmt ... string .... format specifying datetime to prepend to each line printed
            timezone ............... string .... timezone to use if prepend_datetime_fmt is not an empty string
            prepend_memory_usage ... boolean ... prepend the memory used and allocated to the python program

        Returns:
            Nothing

        '''
    def __init__(
        self,
        log_filepath=None,
        output_to_console=False,
        output_to_logfile=True,
        clear_old_log=True,
        indent='|   ',
        prepend_datetime_fmt='',
        timezone='UTC',
        prepend_memory_usage=False):

        self.path = log_filepath
        self.output_to_console = output_to_console
        self.output_to_logfile = output_to_logfile if log_filepath != None else False
        self.indent = indent
        self.prepend_datetime_fmt = prepend_datetime_fmt
        self.timezone = timezone
        self.prepend_memory_usage = prepend_memory_usage
        if self.prepend_memory_usage:
            tracemalloc.start()

        if log_filepath != None:

            # create logfile if it doesn't exist
            # https://appdividend.com/2021/06/03/how-to-create-file-if-not-exists-in-python/
            if not os.path.exists(self.path):
                open(self.path, 'w').close()

            # clear log
            if clear_old_log:
                open(self.path, 'w').close()

        # variables used for print_same_line()
        self.blanked_out_previous_string = []
        self.same_line_string = False

        # variables used for print_prev_line
        self.prev_string = ''

    ''' print()

        Description:
            Log 'string' argument to logfile and/or console.
            Set how indented the line should be with 'num_indents' int argument.
                ^^^ very useful for organizing log ^^^

        Arguments:
            string ................. string .... what will be printed
            i ...................... int ....... number of indents to put in front of the string
            ns ..................... boolean ... print a new line in before the string
            ne ..................... boolean ... print a new line in after the string
            oc ..................... boolean ... default to self.output_to_console bool if oc == None else oc
            of ..................... boolean ... default to self.output_to_logfile bool if of == None else of
            d ...................... boolean ... draw a line on the blank line before or after the string
            overwrite_prev_print ... boolean ... overwrite previous print statement in console, does nothing in logfile
            end .................... string .... last character(s) to print at the end of the string

        Returns:
            tuple:
                console_str ... string ... string that was output to the console
                logfile_str ... string ... string that was output to the logfile

        '''
    def print(
        self,
        string='',
        i=0, # i = number of indents
        ns=False, # ns = newline start
        ne=False, # ne = newline end
        oc=None, # oc = output to console
        of=None, # of = output to file
        d=False, # d = draw line
        overwrite_prev_print=False,
        end='\n'):

        # only accept 'string' as a string type
        string = str(string)
        # if not isinstance(string, str):
        #     t = str(type(string)).split('\'')[1]
        #     raise TypeError("first argument of Log.print() must be of type \'string\', not type \'%s\'" % t)

        console_str, logfile_str = None, None
        output_to_console = self.output_to_console if oc == None else oc
        if output_to_console:
            if overwrite_prev_print and self.prev_string != '':
                sys.stdout.flush()
                # Move cursor up for each line and clear it
                for _ in self.prev_string.split('\n'):
                    # Move cursor up one line
                    sys.stdout.write("\033[F")   # Cursor up 1 line
                    sys.stdout.write("\033[K")   # Clear line
            console_str = \
                self.get_formatted_string(
                    string,
                    self.indent,
                    i=i,
                    ns=ns,
                    ne=ne,
                    d=d)
            print(
                console_str,
                end=end,
                file=sys.stdout)
            self.prev_string = console_str # used from print_prev_line(), disregard
        output_to_logfile = self.output_to_logfile if of == None else of
        if output_to_logfile:
            logfile_str = \
                self.get_formatted_string(
                    string,
                    len(self.indent)*' ',
                    i=i,
                    ns=ns,
                    ne=ne,
                    d=d)
            logfile = open(self.path, 'a')
            print(
                logfile_str,
                end=end,
                file=logfile)
            logfile.close()
        return console_str, logfile_str

    ''' print_dct()

        Description:
            print a dictionary using json library's indentation

        Arguments:
            dct0 ............. dict ...... dictionary to print
            sort_keys ........ boolean ... whether or not to sort the dict by keys when printed
            truncate_str ..... int ....... max number of characters a string can have
            i ................ int ....... number of indents to put in front of the string
            ns ............... boolean ... print a new line in before the string
            ne ............... boolean ... print a new line in after the string
            oc ............... boolean ... default to self.output_to_console bool if oc == None else oc
            of ............... boolean ... default to self.output_to_logfile bool if of == None else of
            d ................ boolean ... draw a line on the blank line before or after the string
            end .............. string .... last character(s) to print at the end of the string

        Returns:
            tuple:
                console_str ... string ... string that was output to the console
                logfile_str ... string ... string that was output to the logfile

        '''
    def print_dct(
        self,
        dct0,
        sort_keys=False,
        truncate_str=None,
        i=0, # i = number of indents
        ns=False, # ns = newline start
        ne=False, # ne = newline end
        oc=None, # oc = output to console
        of=None, # of = output to file
        d=False, # d = draw line
        end='\n'):

        def convert_pandas_to_string(d):
            d2 = {}
            for k, v in d.items():
                if isinstance(v, pd.DataFrame):
                    v2 = 'pd.DataFrame, shape=(%d, %d), columns=%s' % (
                        v.shape[0], v.shape[1], v.columns.values)
                elif isinstance(v, pd.Series):
                    v2 = 'pd.Series, length=%d' % (v.size)
                elif isinstance(v, dict):
                    v2 = convert_pandas_to_string(v)
                elif isinstance(v, str) and \
                    truncate_str != None and \
                    len(v) > truncate_str:
                    v2 = v[:truncate_str] + '...'
                else:
                    v2 = v
                d2[k] = v2
            return d2
        dct1 = convert_pandas_to_string(dct0)

        return self.print(
            json.dumps(
                dct1,
                indent=4,
                sort_keys=sort_keys),
            i=i,
            ns=ns,
            ne=ne,
            oc=oc,
            of=of,
            d=d,
            end=end)

    ''' get_formatted_string()

        Description:
            create a string with string0, indent0, and other optional arguments that is concatenated properly for printing.
            it also prepends the datetime and the memory usage if the user requested it

            WARNING: this function is honestly some of the worst spagetti I've ever written, but the log is gorgeous!

        Arguments:
            string0 .......... string .... what will be printed
            indent0 .......... string .... what an indent looks like
            i ................ int ....... number of indents to put in front of the string
            ns ............... boolean ... print a new line in before the string
            ne ............... boolean ... print a new line in after the string
            d ................ boolean ... draw a line on the blank line before or after the string

        Returns:
            string ... string ... string0 with indent0 and other optional arguments concatenated properly

        '''
    def get_formatted_string(
        self,
        string0,
        indent0,
        i=0, # i = number of indents
        ns=False, # ns = newline start
        ne=False, # ne = newline end
        d=False): # d = draw line

        total_indent0 = ''.join([indent0] * i)
        total_indent1 = ''.join([indent0] * (i + 1))
        string = ''
        div_mark = '-'
        mock_indent = ' '
        max_estimated_indents = 10
        assert i <= max_estimated_indents
        prepend_sep = ' ' * (max_estimated_indents + 1) # set it to a number larger than the estimated max number of indents you'll ever use while logging
        p0 = '' # p0 = mock indents
        p = '' # p = prepended info after mock indents
        prepend_stuff = self.prepend_datetime_fmt != '' or self.prepend_memory_usage
        if prepend_stuff:
            if self.prepend_datetime_fmt != '':
                now = datetime.now(ZoneInfo(self.timezone))
                p += now.strftime(self.prepend_datetime_fmt) + '  '
            if self.prepend_memory_usage:
                bytes_used, bytes_allocated = tracemalloc.get_traced_memory()
                if self.prepend_datetime_fmt != '':
                    p += f'{div_mark}  '
                p += f'{Log.convert_bytes(bytes_used)} used {Log.convert_bytes(bytes_allocated)} allocated'.ljust(45, ' ') # pad w/ spaces
            p0 = mock_indent*i + div_mark
            p = prepend_sep[:len(prepend_sep) - len(mock_indent*i)] + p + f'{div_mark}  ' # put small 1 space indents before everything so VS Code's code folding features continues to work when there's prepended info such as memory or datetime
        blank_p = p0 + ' ' * (len(p) - (len(div_mark) + 2)) + f'{div_mark}  ' # blank_p = p but w/ prepend info removed, only marks remain
        if ns:
            # print(1, string, 1)
            string += blank_p if prepend_stuff else ''
            # print(2, string, 2)
            string += (total_indent1 if d else total_indent0) + '\n'
            # print(3, string, 3)
        for s in string0.split('\n'):
            if prepend_stuff:
                if s == '':
                    string += blank_p
                else:
                    string += p0 + p
            else:
                string += ''
            if s == '':
                total_indent = total_indent1 if d else total_indent0
            else:
                total_indent = total_indent0
            string += total_indent + s + '\n'
        if ne:
            string += blank_p if prepend_stuff else ''
            string += (total_indent1 if d else total_indent0) + '\n'
        string = string[:-1] # remove final newline character
        return string

    ''' convert_bytes(b)

        Description:
            converts the int number of bytes to a string with appropriate units

        Arguments:
            b ... int ... number of bytes

        Returns:
            string with format "{num} {unit}"

        '''
    @staticmethod
    def convert_bytes(b):
        units = ['bytes', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']
        index = 0
        while b >= 1024 and index < len(units) - 1:
            b /= 1024
            index += 1
        if index == 0:
            if b == 1:
                return f"{b} byte"
            else:
                return f"{b} bytes"
        else:
            return f"{b:.4f} {units[index]}"

