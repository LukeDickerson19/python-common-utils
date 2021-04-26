from libraries_and_constants import *




def test_connect_to_outlook(
	log,
	verbose=False,
	num_indents=0,
	new_line_start=False):

	if verbose:
		log.print('test_connect_to_outlook', num_indents=num_indents, new_line_start=new_line_start)
	outlook = outlook_utils.Outlook(
		log,
		connect_to_outlook=True,
		verbose=verbose,
		num_indents=num_indents+1,
		new_line_start=True)
	test_result = 'SUCCEEDED' if isinstance(outlook, outlook_utils.Outlook) else 'FAILED'
	log.print('Test Function: connect_to_outlook ............................ %s' % test_result,
		num_indents=num_indents, new_line_start=new_line_start)
	if test_result == 'FAILED':
		sys.exit()
	return outlook

def test_get_all_messages_in_inbox(
	outlook,
	verbose=False,
	num_indents=0,
	new_line_start=False):

	if verbose:
		outlook.log.print('test_get_all_messages_in_inbox', num_indents=num_indents, new_line_start=new_line_start)

	limit = 5

	messages = outlook.get_all_messages_in_inbox(
		limit=limit,
		num_indents=num_indents+1,
		new_line_start=True)

	test_result = 'SUCCEEDED' if len(messages) == limit else 'FAILED'
	outlook.log.print('Test Function: test_get_all_messages_in_inbox ................ %s' % test_result,
		num_indents=num_indents, new_line_start=new_line_start)

def test_send_message(
	outlook,
	verbose=False,
	num_indents=0,
	new_line_start=False):

	if verbose:
		outlook.log.print('test_send_message', num_indents=num_indents, new_line_start=new_line_start)

	# test create_new_message(), save_message_as_draft(), and send_message()
	msg = outlook.create_new_message(
		TEST_EMAIL_TO,
		TEST_EMAIL_SUBJECT,
		TEST_EMAIL_BODY,
		cc=TEST_EMAIL_CC,
		bcc=TEST_EMAIL_BCC,
		attachments=TEST_EMAIL_ATTACHMENTS,
		verbose=verbose,
		num_indents=0,
		new_line_start=True)
	# save_message_as_draft(
	outlook.send_message(
		msg,
		verbose=verbose,
		num_indents=0,
		new_line_start=True)

def test_find_message_in_inbox(
	outlook,
	verbose=False,
	num_indents=0,
	new_line_start=False):

	if verbose:
		outlook.log.print('test_find_message_in_inbox', num_indents=num_indents, new_line_start=new_line_start)

	# remove attachment files from previous test
	filepaths = [f for f in os.listdir(
		os.path.join(DATA_PATH, 'downloaded_attachments')) \
		if os.path.isfile(os.path.join(DATA_PATH, 'download_attachments', f))]
	for filepath in filepaths:
		os.remove(filepath)

	# pause to give time for sent message to appear in inbox
	time.sleep(10)

	# test find message in inbox
	received_dt = datetime.now()
	message = outlook.find_message_in_inbox(
		subject=TEST_EMAIL_SUBJECT,
		received_dt=received_dt,
		download_attachments=True,
		attachments_download_location=os.path.join(DATA_PATH, 'downloaded_attachments'),
		verbose=verbose,
		num_indents=num_indents+1,
		new_line_start=True)
	# NOTE:
	# 	filtering by sender_address doesn't work for a sender email
	#	that has SenderEmailType of 'EX' (aka EXCHANGE ADMINISTRATIVE GROUP)

	# the test results of the test before for the function test_send_message
	# are printed here because the function for this test find_message_in_inbox
	# is used to verify if the message was sent successfully
	test_result = 'SUCCEEDED' if \
		isinstance(message, tuple) and \
		message[1]['Subject'] == TEST_EMAIL_SUBJECT \
		else 'FAILED'
	outlook.log.print('Test Function: test_send_message ............................. %s' % test_result,
		num_indents=num_indents, new_line_start=new_line_start)
	if test_result == 'FAILED':
		sys.exit()

	test_result = 'SUCCEEDED' if isinstance(message, tuple) else 'FAILED'
	log.print('Test Function: test_find_message_in_inbox .................... %s' % test_result,
		num_indents=num_indents, new_line_start=new_line_start)


if __name__ == '__main__':

	log = logging_utils.Log(LOG_FILEPATH)
	log.print('Running Outlook Utils Tests:',
		num_indents=0, new_line_start=True)

	outlook = test_connect_to_outlook(
		log, verbose=TEST_VERBOSE, num_indents=1, new_line_start=False)

	test_get_all_messages_in_inbox(
		outlook, verbose=TEST_VERBOSE, num_indents=1, new_line_start=False)

	test_send_message(
		outlook, verbose=TEST_VERBOSE, num_indents=1, new_line_start=False)

	test_find_message_in_inbox(
		outlook, verbose=TEST_VERBOSE, num_indents=1, new_line_start=False)


	# OLD TESTS
	
	# outlook, mapi = connect_to_outlook(
	# 	log, num_indents=0, new_line_start=True)

	# # this lists accounts
	# for folder in mapi.Folders:
	# 	print(folder.Name)

	# this gets the current account
	# from_outlook_account = mapi.Session.CurrentUser.AddressEntry.GetExchangeUser()
	# print(from_outlook_account.Name)
	# print(from_outlook_account.PrimarySmtpAddress)
	# from_outlook_address = mapi.Session.CurrentUser.AddressEntry.GetExchangeUser().PrimarySmtpAddress
	# print(from_outlook_address)

