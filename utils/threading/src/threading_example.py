
'''

    Description:

        Example of how to do basic threading and logging in python


    Sample Terminal Output:

        2020-01-27 13:59:30.144 MainThread	function[<module>]	    a.py:69	Main right before starting thread t1
        2020-01-27 13:59:30.145 Thread-1	function[thread_fn1]	a.py:41	Thread 1: starting
        2020-01-27 13:59:30.145 MainThread	function[<module>]	    a.py:71	Main right after  starting thread t1
        2020-01-27 13:59:30.145 Thread-2	function[thread_fn2]	a.py:46	Thread 2: starting
        2020-01-27 13:59:30.145 MainThread	function[<module>]	    a.py:78	hi 0
        2020-01-27 13:59:31.149 MainThread	function[<module>]  	a.py:78	hi 1
        2020-01-27 13:59:32.151 MainThread	function[<module>]  	a.py:78	hi 2
        2020-01-27 13:59:33.146 Thread-1	function[thread_fn1]	a.py:43	Thread 1: finishing
        2020-01-27 13:59:33.153 MainThread	function[<module>]  	a.py:78	hi 3
        2020-01-27 13:59:34.156 MainThread	function[<module>]  	a.py:78	hi 4
        2020-01-27 13:59:35.162 MainThread	function[<module>]  	a.py:78	hi 5
        2020-01-27 13:59:36.146 Thread-2	function[thread_fn2]	a.py:48	Thread 2: finishing
        2020-01-27 13:59:36.165 MainThread	function[<module>]  	a.py:82	Main all done

    Other things to Research:

        Google:
            python threading lock vs semaphore
            python threading mutex

        python multiprocessing - completely different library that could be better than (or use in tandem with) threading
        https://docs.python.org/3.4/library/multiprocessing.html?highlight=process


    Source:

        Where I originally got the example below
        https://realpython.com/intro-to-python-threading/

        format python logger lib to use milliseconds:
        https://stackoverflow.com/questions/31328300/python-logging-module-logging-timestamp-to-include-microsecond/31335874

        Threading Docs
        https://docs.python.org/3/library/threading.html

        Get thread id in logger
        https://javawithravi.com/how-to-display-thread-id-in-python-logs/

    '''

import logging
import threading
import time
# import datetime as dt

def thread_fn1(name):
    logging.info("Thread %s: starting", name)
    time.sleep(3)
    logging.info("Thread %s: finishing", name)

def thread_fn2(name):
    logging.info("Thread %s: starting", name)
    time.sleep(6)
    logging.info("Thread %s: finishing", name)


if __name__ == "__main__":

    format = "%(asctime)s: %(message)s"
    # logging.basicConfig(
    #     format='%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s] %(message)s',
    #     level=logging.INFO,
    #     datefmt='%Y-%m-%d %H:%M:%S')

    # formatter = logging.Formatter('[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s','%m-%d %H:%M:%S')
    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(threadName)s\tfunction[%(funcName)s]\t%(pathname)s:%(lineno)d\t%(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')



    t1 = threading.Thread(target=thread_fn1, args=('1',))

    logging.info("Main right before starting thread t1")
    t1.start()
    logging.info("Main right after  starting thread t1")

    t2 = threading.Thread(target=thread_fn2, args=('2',))
    t2.start()

    i = 0
    while t1.is_alive() or t2.is_alive():
        logging.info('hi %d' % i)
        i += 1
        time.sleep(1)

    logging.info("Main all done")

    
