from logging_libraries_and_constants import *



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
            prepend_memory_usage ... boolean ... 

        Returns:
            Nothing

        '''
    def __init__(
        self,
        log_filepath=None,
        output_to_console=True,
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
            open(self.path, 'a+').close()

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
            string ........... string .... what will be printed
            i ................ int ....... number of indents to put in front of the string
            ns ............... boolean ... print a new line in before the string
            ne ............... boolean ... print a new line in after the string
            d ................ boolean ... draw a line on the blank line before or after the string
            end .............. string .... last character(s) to print at the end of the string

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
        d=False, # d = draw line
        end='\n'):

        self.same_line_string = False # used for print_same_line(), disregard

        # only accept 'string' as a string type
        string = str(string)
        # if not isinstance(string, str):
        #     t = str(type(string)).split('\'')[1]
        #     raise TypeError("first argument of Log.print() must be of type \'string\', not type \'%s\'" % t)

        console_str, logfile_str = None, None
        if self.output_to_console:
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
        if self.output_to_logfile:
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
            d=d,
            end=end)

    ''' print_same_line()

        Description:
            print over the same line as the previous time print_same_line() was called.
            NOTE:
                It only seems to work on linux. On windows it prints
                to the next line instead of the same line

        Arguments:
            string ........... string .... what will be printed
            i ................ int ....... number of indents to put in front of the string
            ns ............... boolean ... print a new line in before the string
            ne ............... boolean ... print a new line in after the string
            d ................ boolean ... draw a line on the blank line before or after the string
            end .............. string .... last character(s) to print at the end of the string

        Returns:
            tuple:
                console_str ... string ... string that was output to the console
                logfile_str ... string ... string that was output to the logfile

        '''
    def print_same_line(
        self,
        string,
        i=0, # i = number of indents
        ns=False, # ns = newline start
        ne=False, # ne = newline end
        d=False, # d = draw line
        end='\n'):

        # clear previous text by overwriting non-spaces with spaces
        if self.same_line_string:
            # last_line_index = len(self.blanked_out_previous_string) - 1 # this variable isn't used anywhere
            for line in self.blanked_out_previous_string:
                print(line, end='')

        # print the string
        console_str, logfile_str = self.print(
            string,
            i=i,
            ns=ns,
            ne=ne,
            d=d,
            end=end)

        # update blanked_out_previous_string
        self.same_line_string = True
        self.blanked_out_previous_string = \
            ['\x1b[A' + '\r' + ' '*len(line) + '\r' \
                for line in console_str.split('\n')]

        return console_str, logfile_str

    ''' get_formatted_string()

        Description:
            create a string with string0, indent0, and other optional arguments that is concatenated properly for printing.
            it also prepends the datetime and the memory usage if the user requested it

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
        if ns:
            string += (total_indent1 if d else total_indent0) + '\n'
        for s in string0.split('\n'):
            p = ''
            if self.prepend_memory_usage:
                bytes_used, bytes_allocated = tracemalloc.get_traced_memory()
                p += f'({Log.convert_bytes(bytes_used)} used {Log.convert_bytes(bytes_allocated)} allocated)'.ljust(45, ' ') # pad w/ spaces
            if self.prepend_datetime_fmt != '':
                now = datetime.now(ZoneInfo(self.timezone))
                p += now.strftime(self.prepend_datetime_fmt) + ' '
            string += p + total_indent0 + s + '\n'
        if ne:
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

