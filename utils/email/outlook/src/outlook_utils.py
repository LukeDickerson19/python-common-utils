from outlook_libraries_and_constants import *



class Outlook:

	def __init__(
		self,
		log,
		connect_to_outlook=True,
		verbose=False,
		num_indents=0,
		new_line_start=False):

		if not isinstance(log, logging_utils.Log):
			print('Invalid type for argument "log" into Outlook object.')
			print('log must be of type logging_utils.Log')
			sys.exit()

		self.log = log
		if verbose:
			self.log.print('Initializing Outlook Email',
				num_indents=num_indents, new_line_start=new_line_start)
		if connect_to_outlook:
			try:
				self.connect_to_outlook(verbose=verbose, num_indents=num_indents+1)
			except Exception as e:
				session = None
				self.log.print('Exception:', num_indents=num_indents+1)
				self.log.print('%s' % e, num_indents=num_indents+2)
				self.log.print('Failed to connect to Outlook', num_indents=num_indents)
				sys.exit()
		if verbose:
			self.log.print('Initialization complete.', num_indents=num_indents)

	def connect_to_outlook(
		self,
		verbose=False,
		num_indents=0,
		new_line_start=False):

		self.outlook = win32.Dispatch('Outlook.Application')
		self.mapi = self.outlook.GetNamespace('MAPI')
		if verbose:
			self.log.print('Connected to Outlook successfully.',
				num_indents=num_indents, new_line_start=new_line_start)

	def get_all_messages_in_inbox(
		self,
		limit=None,
		download_attachments=False,
		attachments_download_location='',
		verbose=False,
		num_indents=0,
		new_line_start=False):

		return self.get_all_messages_in_folder(6,
			limit=limit, verbose=verbose, num_indents=num_indents, new_line_start=new_line_start)

	def get_all_messages_in_folder(
		self,
		folder_number,
		limit=None,
		download_attachments=False,
		attachments_download_location='',
		verbose=False,
		num_indents=0,
		new_line_start=False):

		# folder types
		# 3  Deleted Items
		# 4  Outbox
		# 5  Sent Items
		# 6  Inbox
		# 9  Calendar
		# 10 Contacts
		# 11 Journal
		# 12 Notes
		# 13 Tasks
		# 14 Drafts
		# https://docs.microsoft.com/en-us/office/vba/api/outlook.oldefaultfolders

		# https://stackoverflow.com/questions/22813814/clearly-documented-reading-of-emails-functionality-with-python-win32com-outlook/39911751
		folder = self.mapi.GetDefaultFolder(folder_number)
		messages = folder.Items

		# The Sort function will sort your messages by their ReceivedTime property,
		# from the most recently received to the oldest. If you use False instead
		# of True, it will sort in the opposite direction: ascending order, from the
		# oldest to the most recent.
		# source: https://stackoverflow.com/questions/42428770/how-to-go-through-outlook-emails-in-reverse-order-using-python
		messages.Sort("[ReceivedTime]", True)

		# ms = list of messages (sorted most to least recent) that will be returned
		# messages will be a dictionary with format specified in get_message()
		ms = []
		for i, msg in enumerate(messages):
			if limit != None and (i+1) > limit:
				break
			if verbose:
				self.log.print('Message %d of %d:' % (i+1, messages.Count))
			m = self.get_message(
				msg,
				download_attachments=False,
				attachments_download_location=os.path.join(DATA_PATH, 'downloaded_attachments'),
				verbose=verbose,
				num_indents=num_indents+1,
				new_line_start=True)
			msg.Close(0)
			ms.append(m)
		return ms

	def convert_pywin32_datetime_to_regular_datetime(
		self,
		pywin32_dt,
		convert_to_local_timezone=True):

		# # win32com seems to be inaccurately putting the UTC timezone on the
		# # local (PST) time, by default. This updates it to the local timezone
		# local_tz = datetime.now().astimezone().tzinfo
		# reg_dt = datetime(
		# 	pywin32_dt.year,
		# 	pywin32_dt.month,
		# 	pywin32_dt.day,
		# 	pywin32_dt.hour,
		# 	pywin32_dt.minute,
		# 	pywin32_dt.second,
		# 	tzinfo=local_tz)

		# # if you ever need to change a pywin32 timezone (thats accurate, unlike this senario)
		# # to a datetime timezone then use the code below. It took a long to time to get working
		# # so I didn't want to delete it.

		# set current timezone to UTC
		tz_utc_offset = pywin32_dt.tzinfo.utcoffset(pywin32_dt)
		reg_dt = datetime(
			pywin32_dt.year,
			pywin32_dt.month,
			pywin32_dt.day,
			pywin32_dt.hour,
			pywin32_dt.minute,
			pywin32_dt.second,
			tzinfo=tz.tzlocal())
			# tzinfo=timezone(tz_utc_offset))

		# print('BEFORE', reg_dt.strftime('%Y-%m-%d %I:%M:%S %p %Z %z'))

		# # convert to local timezone:
		# local_tz = datetime.now().astimezone().tzinfo
		# reg_dt = reg_dt.replace(tzinfo=reg_dt.tzinfo).astimezone(local_tz)

		# print('AFTER', reg_dt.strftime('%Y-%m-%d %I:%M:%S %p %Z %z'))

		# OTHER SOURCES:	
		# https://stackoverflow.com/questions/39028290/python-convert-pywintyptes-datetime-to-datetime-datetime
		# https://stackoverflow.com/questions/46296564/timezone-issue-in-outlook-emails-while-connected-using-python
		# docs: https://docs.microsoft.com/en-us/office/vba/api/outlook.mailitem

		return reg_dt

	def find_messages_in_inbox(
		self,
		subject=None,
		received_daterange_dts=None,
		sender_address=None,
		download_attachments=False,
		attachments_download_location='',
		verbose=False,
		num_indents=0,
		new_line_start=False):

		return self.find_messages_in_folder(
			6,
			subject=subject,
			received_daterange_dts=received_daterange_dts,
			sender_address=sender_address,
			download_attachments=download_attachments,
			attachments_download_location=attachments_download_location,
			verbose=verbose, num_indents=num_indents, new_line_start=new_line_start)

	''' find_messages_in_folder

		Description:

		Arguments:

		Returns:
			list of tuples (msg, msg_dct) if found multiple messages

		Sources:
			https://www.codeforests.com/2020/06/04/python-to-read-email-from-outlook/

		'''
	def find_messages_in_folder(
		self,
		folder_number,
		subject=None,
		received_daterange_dts=None,
		sender_address=None,
		download_attachments=False,
		attachments_download_location='',
		verbose=False,
		num_indents=0,
		new_line_start=False):
		
		# log output and verify program passes in valid arguments
		if verbose:
			self.log.print('Searching for messages with:',
				num_indents=num_indents, new_line_start=new_line_start)
		if received_daterange_dts == None and subject == None and sender_address == None:
			self.log.print('Invalid arguments. Must have at least one of the following arguments.',
				num_indents=num_indents+1)
			self.log.print('received_daterange_dts\nsubject\nsender_address',
				num_indents=num_indents+2)
			return None
		if verbose:
			if subject != None:
				self.log.print('Subject: \'%s\'' % subject,
					num_indents=num_indents+1)
			if received_daterange_dts != None:
				self.log.print('Received DateRange End DateTime:   %s' % received_daterange_dts[1].strftime('%m/%d/%Y %I:%M %p %Z'),
					num_indents=num_indents+1)
				self.log.print('Received DateRange Start DateTime: %s' % received_daterange_dts[0].strftime('%m/%d/%Y %I:%M %p %Z'),
					num_indents=num_indents+1)
			if sender_address != None:
				self.log.print('Sender:						 %s' % sender_address,
					num_indents=num_indents+1)

		# get all messages in folder
		folder = self.mapi.GetDefaultFolder(folder_number)
		messages = folder.Items
		if verbose:
			self.log.print('%d message(s) in folder.' % messages.Count,
				num_indents=num_indents+1, new_line_start=True)

		# filter in the received time
		if received_daterange_dts != None:
			received_dt_start_str = received_daterange_dts[0].strftime('%m/%d/%Y %H:%M %p')
			received_dt_end_str   = received_daterange_dts[1].strftime('%m/%d/%Y %H:%M %p')
			messages = messages.Restrict("[ReceivedTime] >= '" + received_dt_start_str + "'")
			messages = messages.Restrict("[ReceivedTime] <= '" + received_dt_end_str   + "'")
			if verbose:
				self.log.print('%d message(s) in time range:' % messages.Count,
					num_indents=num_indents+1, new_line_start=True)
				self.log.print('Start: %s' % received_dt_start_str, num_indents=num_indents+2)
				self.log.print('End:   %s' % received_dt_end_str,   num_indents=num_indents+2)

		# filter for the subject
		if subject != None:
			messages = messages.Restrict('[Subject] = "%s"' % subject)
			# messages = messages.Restrict('[Subject] = \'%s\'' % subject)
			if verbose:
				self.log.print('%d message(s) with subject:' % messages.Count,
					num_indents=num_indents+1, new_line_start=True)
				self.log.print('Subject: \'%s\'' % subject, num_indents=num_indents+2)

		# filter for the sender
		# NOTE:
		# 	filtering by sender_address doesn't work for a sender email
		#	that has SenderEmailType of 'EX' (aka EXCHANGE ADMINISTRATIVE GROUP)
		# uncomment this for loop to see
		# print('Sender Email Addresses:')
		# for msg in messages:
		# 	print(msg.SenderEmailAddress)
		if sender_address != None:
			# print('[SenderEmailAddress] = \'%s\'' % sender_address)
			messages = messages.Restrict('[SenderEmailAddress] = \'%s\'' % sender_address)
			if verbose:
				self.log.print('%d message(s) from sender:' % messages.Count,
					num_indents=num_indents+1, new_line_start=True)
				self.log.print('Sender: \'%s\'' % sender_address, num_indents=num_indents+2)

		# return a list of tuples of the message and its dictionary
		return [(msg, self.get_message(msg,
			download_attachments=download_attachments,
			attachments_download_location=attachments_download_location)) \
				for msg in messages]

	''' get_message
		
		Description:

		Arguments:

		Returns:
		
		'''
	def get_message(
		self,
		msg,
		download_attachments=False,
		attachments_download_location='',
		verbose=False,
		num_indents=0,
		new_line_start=False):

		# m = dictionary to be returned
		m = dict()

		# check for msg type
		# types: MailItem, ReportItem, MeetingItem
		# https://stackoverflow.com/questions/31619012/extract-senders-email-address-from-outlook-exchange-in-python-using-win32
		if msg.Class == 43:
			m['Class'] = 'MailItem'
			if verbose:
				self.log.print('%s Message:' % m['Class'],
					num_indents=num_indents,
					new_line_start=True)

			# get From name and email address
			from_name = msg.SenderName
			if msg.SenderEmailType == 'EX':
				if msg.Sender.GetExchangeUser() != None:
					from_address = msg.Sender.GetExchangeUser().PrimarySmtpAddress
				else:
					from_address = msg.Sender.GetExchangeDistributionList().PrimarySmtpAddress
			else:
				# https://social.msdn.microsoft.com/Forums/sqlserver/en-US/0cf3eed3-ba46-41ec-b2d3-7e201c69d2cc/the-quotfrom-addressquot-of-an-outlook-mail-is-not-returned-properly-in-outlook-addin?forum=vsto
				from_address = msg.SenderEmailAddress
			m['From'] = {'Name' : from_name, 'Email Address' : from_address}
			if verbose:
				self.log.print('From:', num_indents=num_indents+1, new_line_start=True)
				self.log.print(from_name, num_indents=num_indents+2, new_line_start=True)
				self.log.print(from_address, num_indents=num_indents+3)

			# get Recipients of email (To, CC, BCC, and Originator)
			# https://stackoverflow.com/questions/43380084/unable-to-extract-recipients-name-in-outlook-email-python
			# https://stackoverflow.com/questions/62658802/how-to-get-recipient-names-and-emails-address-from-outlook-using-python-mapi
			# https://www.javaer101.com/en/article/2906367.html
			recipients = {
				'To'		 : [],
				'CC'		 : [],
				'BCC'		: [],
				'Originator' : []
			}
			to_email_names  = msg.To.split('; ')
			cc_email_names  = msg.CC.split('; ')
			bcc_email_names = msg.BCC.split('; ')
			for r in msg.Recipients:
				name = r.Name
				if r.AddressEntry.Type == 'EX':
					if r.AddressEntry.GetExchangeUser() != None:
						email_address = r.AddressEntry.GetExchangeUser().PrimarySmtpAddress
					else:
						email_address = r.AddressEntry.GetExchangeDistributionList().PrimarySmtpAddress
				else:
					email_address = r.AddressEntry.Address # r.Address will also work

				# code mapping: https://docs.microsoft.com/en-us/office/vba/api/outlook.olmailrecipienttype
				# Originator, used for email receipts:
				# https://www.pcreview.co.uk/threads/what-is-the-purpose-of-a-particular-inbox-column.2479289/
				if r.Type == 0: recipients['Originator'].append({'Name' : name, 'Email Address' : email_address})
				if r.Type == 1: recipients['To'].append({'Name' : name, 'Email Address' : email_address})
				if r.Type == 2:	recipients['CC'].append({'Name' : name, 'Email Address' : email_address})
				if r.Type == 3:	recipients['BCC'].append({'Name' : name, 'Email Address' : email_address})

			m['Recipients'] = recipients
			if verbose:
				self.log.print('Recipients:', num_indents=num_indents+1, new_line_start=True)
				for r_type, lst in recipients.items():
					self.log.print('%s:' % r_type, num_indents=num_indents+2, new_line_start=True)
					if len(lst) == 0:
						self.log.print('None', num_indents=num_indents+3, new_line_start=True)
					else:
						for dct in lst:
							self.log.print(dct['Name'], num_indents=num_indents+3, new_line_start=True)
							self.log.print(dct['Email Address'], num_indents=num_indents+4)

			# get the time when the message was received
			try:
				m['Received Datetime'] = self.convert_pywin32_datetime_to_regular_datetime(msg.ReceivedTime)
				if verbose:
					self.log.print('Received Time (when current email was received):',
						num_indents=num_indents+1, new_line_start=True)
					self.log.print(m['Received Datetime'].strftime('%Y-%m-%d %I:%M:%S %p %Z %z UTC offset'),
						num_indents=num_indents+2)		
			except:
				# use try catch
				# https://stackoverflow.com/questions/62169709/python-valueerror-microsecond-must-be-in-0-999999-while-using-win32com
				m['Received Datetime'] = None

			# get the time when the message thread was created
			try:
				m['Created Datetime'] = self.convert_pywin32_datetime_to_regular_datetime(msg.CreationTime)
				if verbose:
					self.log.print('Creation Time (when 1st email in thread was received):',
						num_indents=num_indents+1, new_line_start=True)
					self.log.print(m['Created Datetime'].strftime('%Y-%m-%d %I:%M:%S %p %Z %z UTC offset'),
						num_indents=num_indents+2)
			except:
				# use try catch
				# https://stackoverflow.com/questions/62169709/python-valueerror-microsecond-must-be-in-0-999999-while-using-win32com
				m['Created Datetime'] = None


			# get the subject (aka title) of the message
			m['Subject'] = msg.Subject
			if verbose:
				self.log.print('Subject:', num_indents=num_indents+1, new_line_start=True)
				self.log.print(m['Subject'], num_indents=num_indents+2)


			# get the body (aka contents) of the message
			m['Body'] = msg.Body
			if verbose:
				self.log.print('Body:', num_indents=num_indents+1, new_line_start=True)
				self.log.print(m['Body'], num_indents=num_indents+2)


			# get the attachments' filename of the message (if any)
			# and save them to attachments_download_location if
			# download_attachments = True.
			m['Attachments'] = dict()
			for a in msg.Attachments:
				m['Attachments'][a.FileName] = 'Attachment not downloaded, no local filepath.'
				if download_attachments:
					filepath = self.download_attachment(
						a, attachments_download_location)
					m['Attachments'][a.FileName] = filepath
			if verbose:
				self.log.print('%d Attachment(s):' % msg.Attachments.Count,
					num_indents=num_indents+1, new_line_start=True)
				if m['Attachments'] == dict():
					self.log.print('None', num_indents=num_indents+2, new_line_start=True)
				else:
					for filename, filepath in m['Attachments'].items():
						self.log.print(filename, num_indents=num_indents+2, new_line_start=True)
						self.log.print('attachment saved to: %s' % filepath, num_indents=num_indents+3)
			# other useful info on pywin32 attachments objects
			# https://stackoverflow.com/questions/22813814/clearly-documented-reading-of-emails-functionality-with-python-win32com-outlook/35801030#35801030

		# return message
		if verbose:
			self.log.print('End of Message.', num_indents=num_indents, new_line_start=True, draw_line=True)
		return m

	''' download_attachment
		
		Description:

		Arguments:

		Returns:
		
		'''
	def download_attachment(
		self,
		attachment,
		attachments_download_location):

		filepath = os.path.join(attachments_download_location, attachment.FileName)
		if os.path.exists(filepath):
			os.remove(filepath)
		attachment.SaveAsFile(filepath)
		return filepath

	''' print_message
		
		Description:

		Arguments:

		Returns:
		
		'''
	def print_message(
		self,
		m,
		num_indents=0,
		new_line_start=False):

		# check for message type
		# types: MailItem, ReportItem, MeetingItem
		if m['Class'] == 'MailItem':
			self.log.print('%s Message:' % m['Class'], num_indents=num_indents, new_line_start=True)

			# print From name and email address
			self.log.print('From:', num_indents=num_indents+1, new_line_start=True)
			self.log.print(m['From']['Name'], num_indents=num_indents+2, new_line_start=True)
			self.log.print(m['From']['Email Address'], num_indents=num_indents+3)

			# print Recipients of email (To, CC, BCC, and Originator)
			self.log.print('Recipients:', num_indents=num_indents+1, new_line_start=True)
			for r_type, lst in m['Recipients'].items():
				self.log.print('%s:' % r_type, num_indents=num_indents+2, new_line_start=True)
				if len(lst) == 0:
					self.log.print('None', num_indents=num_indents+3, new_line_start=True)
				else:
					for dct in lst:
						self.log.print(dct['Name'], num_indents=num_indents+3, new_line_start=True)
						self.log.print(dct['Email Address'], num_indents=num_indents+4)

			# print the time when the message was received
			self.log.print('Received Time (when current email was received):',
				num_indents=num_indents+1, new_line_start=True)
			self.log.print(m['Received Datetime'].strftime('%Y-%m-%d %I:%M:%S %p %Z %z UTC offset'),
				num_indents=num_indents+2)

			# print the time when the message thread was created
			self.log.print('Creation Time (when 1st email in thread was received):',
				num_indents=num_indents+1, new_line_start=True)
			self.log.print(m['Created Datetime'].strftime('%Y-%m-%d %I:%M:%S %p %Z %z UTC offset'),
				num_indents=num_indents+2)

			# print the subject (aka title) of the message
			self.log.print('Subject:', num_indents=num_indents+1, new_line_start=True)
			self.log.print(m['Subject'], num_indents=num_indents+2)

			# print the body (aka contents) of the message
			self.log.print('Body:', num_indents=num_indents+1, new_line_start=True)
			self.log.print(m['Body'], num_indents=num_indents+2)

			# print the attachments' filename of the message (if any)
			# and local file path if downloaded.
			self.log.print('%d Attachment(s):' % len(m['Attachments'].keys()),
				num_indents=num_indents+1, new_line_start=True)
			if m['Attachments'] == dict():
				self.log.print('None', num_indents=num_indents+2, new_line_start=True)
			else:
				for filename, filepath in m['Attachments'].items():
					self.log.print(filename, num_indents=num_indents+2, new_line_start=True)
					self.log.print('attachment saved to: %s' % filepath, num_indents=num_indents+3)

		self.log.print('End of Message.', num_indents=num_indents, new_line_start=True, draw_line=True)

	''' send_message
		
		Description:

		Arguments:
			msg ... outlook message object ... message to send

		Returns:
			nothing

		Sources:
			https://win32com.goermezer.de/microsoft/ms-office/send-email-with-outlook-and-python.html
			https://www.excelcise.org/python-outlook-send-text-email-pywin32/

		'''
	def send_message(
		self,
		msg,
		verbose=False,
		num_indents=0,
		new_line_start=False):

		# send the email
		if verbose:
			self.log.print('Sending email', num_indents=num_indents, new_line_start=new_line_start)
		msg.Send()
		if verbose:
			self.log.print('Email sent.', num_indents=num_indents)

	''' save_message_as_draft
		
		Description:

		Arguments:
			msg ... win32com MailItem object ... message to save to a draft

		Returns:
			nothing

		Sources:
			https://win32com.goermezer.de/microsoft/ms-office/send-email-with-outlook-and-python.html
			https://www.excelcise.org/python-outlook-send-text-email-pywin32/

		'''
	def save_message_as_draft(
		self,
		msg,
		num_indents=0,
		new_line_start=False):

		# save the email as a draft
		if verbose:
			self.log.print('Saving email as draft', num_indents=num_indents, new_line_start=new_line_start)
		msg.Save()
		if verbose:
			self.log.print('Email saved to draft.', num_indents=num_indents)

	''' create_new_message
		
		Description:

		Arguments:
			to ... list of strings ... list of email addresses to send the email to
			subject ... string ... email subject
			body ... string ... email body
			cc ... list of strings ... list of email addresses to CC on the email
			bcc ... list of strings ... list of email addresses to BCC on the email
			attachments ... list of strings ... list of filepaths to files to attach to email

		Returns:
			msg ... win32com MailItem object ... message to save to a draft

		Sources:
			https://win32com.goermezer.de/microsoft/ms-office/send-email-with-outlook-and-python.html
			https://www.excelcise.org/python-outlook-send-text-email-pywin32/

		'''
	def create_new_message(
		self,
		to,
		subject,
		body,
		cc=None,
		bcc=None,
		attachments=None,
		verbose=False,
		num_indents=0,
		new_line_start=False):

		if verbose:
			self.log.print('Creating Email', num_indents=num_indents, new_line_start=new_line_start)

		# create new message object
		msg = self.outlook.CreateItem(0)

		# set the To field in the email
		msg.To = '; '.join(to)
		if isinstance(to, list) and all(isinstance(x, str) for x in to):
			msg.To = '; '.join(to)
		else:
			self.log.print('Invalid \'To\' value: %s' % to, num_indents=num_indents+1)
			self.log.print('To value must be a list of strings', num_indents=num_indents+1)
			self.log.print('Email not sent.', num_indents=num_indents)
			return

		# set the CC field in the email
		if cc != None:
			if isinstance(cc, list) and all(isinstance(x, str) for x in cc):
				msg.CC = '; '.join(cc)
			else:
				self.log.print('Invalid \'CC\' value: %s' % cc, num_indents=num_indents+1)
				self.log.print('CC value must be a list of strings', num_indents=num_indents+1)
				self.log.print('Email not sent.', num_indents=num_indents)
				return

		# set the BCC field in the email
		if bcc != None:
			if isinstance(bcc, list) and all(isinstance(x, str) for x in bcc):
				msg.BCC = '; '.join(bcc)
			else:
				self.log.print('Invalid \'BCC\' value: %s' % bcc, num_indents=num_indents+1)
				self.log.print('BCC value must be a list of strings', num_indents=num_indents+1)
				self.log.print('Email not sent.', num_indents=num_indents)
				return

		# set the Subject field in the email
		if isinstance(subject, str):
			msg.Subject = subject
		else:
			self.log.print('Invalid \'Subject\' value.', num_indents=num_indents+1)
			self.log.print('Subject value must be a string', num_indents=num_indents+1)
			self.log.print('Email not sent.', num_indents=num_indents)
			return

		# set the Body field in the email
		if isinstance(body, str):
			msg.Body = body
		else:
			self.log.print('Invalid \'Body\' value.', num_indents=num_indents+1)
			self.log.print('Body value must be a string', num_indents=num_indents+1)
			self.log.print('Email not sent.', num_indents=num_indents)
			return

		# set the attachments in the email
		if attachments != None:
			if isinstance(attachments, list) and all(isinstance(x, str) for x in attachments):
				for filepath in attachments:
					if os.path.exists(filepath):
						msg.Attachments.Add(filepath)
					else:
						self.log.print('Invalid \'Attachment\' filepath value: %s' % filepath, num_indents=num_indents+1)
						self.log.print('Filepath does not exist', num_indents=num_indents+1)
						self.log.print('Email not sent.', num_indents=num_indents)
						return
			else:
				self.log.print('Invalid \'Attachments\' value.', num_indents=num_indents+1)
				self.log.print('Attachments value must be a list of strings', num_indents=num_indents+1)
				self.log.print('Email not sent.', num_indents=num_indents)
				return

		# this has been commented out because it gave an error and i need to move on
		# output message details to log
		if verbose:
			self.get_message(msg,
				verbose=True, num_indents=num_indents+1)
			# get_message() is used instead of print_message()
			# because print_message() takes a dictionary, not
			# an outlook message object

		if verbose:
			self.log.print('Email created.', num_indents=num_indents, new_line_start=True, draw_line=True)
		return msg


