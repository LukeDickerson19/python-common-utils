# logging_utils



#### DESCRIPTION
```
tool that makes it easy to organize log files and console output
```

#### USAGE
```
see tests folder for how to import properly
	driver.py and libraries_and_constants.py

then create a log object with:
log = logging_utils.Log(LOG_FILEPATH)

then print to the log and/or console with:
log.print('hello world', num_indents=0)

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


#### TO DO
```
New Features:

	none

Bug Fixes:

	the print_same_line function does not print to the same line
	in the actual log file. It should convert the contents of the
	log equal to lenght of blanked_out_previous_string to blank
	space character, then replace them with the new text

	also, why doesn't the print_same_line functino print to the same
	line in the console when on windows, but it works on linux?
```

