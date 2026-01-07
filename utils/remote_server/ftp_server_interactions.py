import sys
import ftplib



'''

	Description:

	Sources:

		FTP Server App Article
			this source also shows how to access the server via Ubuntu's Nautilus file explorer
		https://www.linuxbabe.com/beginners/transfer-files-android-ubuntu

		FTP Server App on Google Play
			maybe I could download it on my computer too, and my phone could access data on my computer
		https://play.google.com/store/apps/details?id=com.medhaapps.wififtpserver&hl=en_US

		Was running into issues with the standard way of creating the ftplib.FTP() constructor
		this sources method worked though
		https://pythontic.com/ftplib/ftp/connect

		ftplib docs
		https://docs.python.org/3/library/ftplib.html

		How To Connect to FTP Server in KDE Dolphin
		https://askubuntu.com/questions/129794/connect-to-ftp-sftp-in-dolphin-or-transfer-nautilus-bookmarks

	'''

# connect to FTP server
print('\nconnecting to FTP server ...')
host = '192.168.1.211'
port = 2221
user = 'luke'
password = 'guitar93'
print('|   host ... %s' % host)
print('|   port ... %s' % port)
ftpObject = ftplib.FTP()
ftpResponseCode = ftpObject.connect(host=host, port=port)
ftpResponseCode = ftpObject.login(user=user, passwd=password)
print('connection established')

# view directory contents (aka "ls")
# default directory when is /storage/emulated/0 according to Ftp server App
# this is the same path as /InternalStorage/ on the SMB server
print('\nviewing contents of /Music directory ...')
# you can also use any of the below 3 options to do it
# ftpResponseCode = ftpObject.dir("/Music") # returns dir contents with metadata (same thing as "ll")
# ftpResponseCode = ftpObject.nlst("/Music") # returns a list of just the file names
# print(ftpResponseCode) # this print statement is unneccessary because the results are printed to stdout
# retrlines() HOWEVER can have its callback set to a variable instead of stdout though (which is the default)
# https://stackoverflow.com/questions/9969247/creating-list-from-retrlines-in-python
lines = []
ftpObject.retrlines("LIST /Music", callback=lines.append)
for l in lines: print(l)
sys.exit()

# view current working directory (aka "pwd")
print('\nviewing current working directory path ...')
ftpResponseCode = ftpObject.pwd()
print(ftpResponseCode)

# make directory on server
print('\nmaking directory /Download/a/b/c/ ...')
ftpResponseCode = ftpObject.mkd('/Download/a/')
ftpResponseCode = ftpObject.mkd('/Download/a/b/')
ftpResponseCode = ftpObject.mkd('/Download/a/b/c/')
print(ftpResponseCode)

# copy file to server
print('\ncopying file to server ...')
local_file_path = '/home/luke/Music/Rap/Kendrick_Lamar/Good_Kid_mAAd_City/Swimming_Pools.mp3'
phone_file_path = '/Download/a/b/c/Swimming_Pools.mp3' # '/Music/Rap/Kendrick_Lamar/Good_Kid_mAAd_City/Swimming_Pools.mp3'
print('|   local_file_path ... %s' % local_file_path)
print('|   phone_file_path ... %s' % phone_file_path)
f = open(local_file_path,'rb')
ftpResponseCode = ftpObject.storbinary('STOR %s' % phone_file_path, f)
print(ftpResponseCode)
f.close()

input('\npress any key to continue ...')

# delete file on server
print('\ndeleteing file on server ...')
print('|   phone_file_path ... %s' % phone_file_path)
ftpResponseCode = ftpObject.delete(phone_file_path)
print(ftpResponseCode)

# delete directory on server
# there does not seem to be a way to delete a directory recursively
# https://curl-library.cool.haxx.narkive.com/aGXsTJKL/removing-directory-from-ftp-server
print('\ndeleteing directory on server ...')
ftpResponseCode = ftpObject.rmd('/Download/a/b/c/')
ftpResponseCode = ftpObject.rmd('/Download/a/b/')
ftpResponseCode = ftpObject.rmd('/Download/a/')
print(ftpResponseCode)

# close connection to server 
print('\nclosing connection to server ...')
ftpResponseCode = ftpObject.quit()
print(ftpResponseCode)


