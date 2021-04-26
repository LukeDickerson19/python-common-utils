# common_utils



#### DESCRIPTION
```
	utility functions for automating microsoft outlook email capabilities

	NOTE: can't send .py files as an attachment
		Microsoft Outlook Security Software doesn't trust .py files
			https://social.technet.microsoft.com/Forums/office/en-US/94f10c8d-6c1e-4fce-a3c2-644da20d7b2a/this-item-contains-attachments-that-are-potentially-unsafe-recipients-using-microsoft-outlook-may?forum=outlook
```

#### TO DO
```
	useful functions to create

		reply to email
			calls function to find email based on subject
			how do I reply to a specific email?
				make the send function take an argument
				that is a boolean or string flagging if the email
				to be sent should be a new email or a reply to another
				email and if its a reply to another email, the send
				function will have optional arguments of which email
				message object to respond to and the send functions will then ... tbd

		it would also be cool if i figured out how to get all message in a specific inbox sub folder
			i think i'd just need to specify the subfolder in the get_all_messages_in_folder
			https://www.mathworks.com/matlabcentral/answers/44967-retrieve-a-specific-folder-in-outlook

	figure out
		the codes for the different msg.Class
			43 is for MailItem
			46 is for ReportItem
			and theres a bunch of codes for stuff related to MeetingItem
				see docs: https://docs.microsoft.com/en-us/dotnet/api/microsoft.office.interop.outlook.olobjectclass?view=outlook-pia

	figure out whats wrong with outlook desktop
		once i sent an email, the app started updating my inbox
		how do i "update outlook desktop inbox automatically?"
```

#### SOURCES
```
	pywin32 (aka win32com)
	https://www.excelcise.org/python-outlook-send-outlook-html-email-pywin32/
	https://pbpython.com/windows-com.html
```
