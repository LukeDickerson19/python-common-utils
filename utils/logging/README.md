# Logging Utilities



#### DESCRIPTION
> logging class with the following features:
> - set indendation of string being printed
> - print on the same line (overwritting previous line)
> - print time of when string was printed
> - print memory usage of code when string was printed
> - print to console and to file individually or simultaniously


#### USAGE
```
see tests folder for how to import properly
	driver.py and libraries_and_constants.py

log = logging_utils.Log(LOG_FILEPATH) # then create a log object with
log.print('hello world', num_indents=0) # print to the log and/or console with

the optional argument num_indents makes it really easy to
indent text you write to the log.

When you open the log file in any text editor that has code folding (such a Sublime Text or VS Code) you can fold individual blocks of text by clicking the arrow to the left of the first line, or multiple blocks with keyboard short cuts (in Sublime its Ctrl+K, Ctrl+<indentation_level_number>).

Example Log:

	Getting All ID Types:
	    Successfully read input file: C:\Users\luke\Desktop\people_to_keep_in_touch_with.csv
	        Data Type: title_asset_id
	        1 duplicate(s) in the list
	        	REID2342346546754032
	    
	    Connecting to MySQL database ...
	        Connection Details:
	            hostname = 111.222.333.444
	            port     = 3306
	            database = dbadmin
	    Successfully connected to MySQL database.
	        
	    Running Select Query on MySQL DB ...
	        Query:
	            
	            select
	            	*
	            from- table_1
	            where birthday like '%-03-26'
	            
	    Successfully queried MySQL DB.
	    Results:
	                       person_id   name    birthday
	        1   REID3912398459404844  Alice  1989-03-26
	        0   REID0923419871984595    Bob  1997-03-26
	        2   REID1988776766637378  Larry  1982-03-26
	    
	    Do you want to save this table as an excel file? Y/N
	        
	        You selected Yes.
	        Table saved to: C:\Users\luke\Desktop\person_ids_to_email_happy_birthday.xlsx
	    
	Successfully aquired all IDs from title_asset_id.
```


