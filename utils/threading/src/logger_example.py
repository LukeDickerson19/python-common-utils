



'''

  Description:
    Good explaination of logger.
    
  Example Usage:
  
    We can use this logger object now to write entries to the log file:
      logger.error('We have a problem')
      logger.info('While this is just chatty')
    
    If we look in the file that was created, we'll see something like this:
      2003-07-08 16:49:45,896 ERROR We have a problem

    The info message was not written to the file - we called the setLevel method
    to say we only wanted WARNING or worse, so the info message is discarded.

  Logging Levels:

          Level       	Numeric value
          CRITICAL	    50
          ERROR	        40
          WARNING	      30
          INFO	        20
          DEBUG	        10
          NOTSET	      0

  Sources:
    https://docs.python.org/2.3/lib/node304.html
    https://www.loggly.com/ultimate-guide/python-logging-basics/

  '''

import logging

logger = logging.getLogger('myapp') # create a Logger instance
hdlr = logging.FileHandler('/var/tmp/myapp.log') # create a FileHandler
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s') # create a Formatter
hdlr.setFormatter(formatter) # attach the Formatter to the FileHandler
logger.addHandler(hdlr) # attach the FileHandler to the Logger
logger.setLevel(logging.WARNING) # sets a debug level for the logger


