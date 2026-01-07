import sys
import time
from smb.SMBConnection import SMBConnection

'''

	DESCRIPTION:

		This script shows how to programmatically interact with an SMB Server
			How to read (aka download) a file?
			How to write (aka upload) a new file?
				write to an existing file by downloading it, modifying it, and uploading it again
			How to delete a file?
			How to create a folder?
			How to delete a folder and all its contents?

		I'm running an SMB Server on my Android phone with this App
			App Name: LAN drive - SAMBA Server & Client
			It worked pretty well and this library can access it so I paid $3.99 for the full thing
				It was interesting psycologically. Normally I don't buy apps. I was trying many other apps
				and they didn't work. I was reading their comments and they weren't working for other people
				either. Some of them were paid for and I scoffed at them for even thinking I would pay for
				their app, along with other people in the comments. When this one JUST WORKED though I was
				like, sure. Paying for it removed a transfer limit of 0.5MB/s and some other stuff
			Type this into Nautilus File Explorer > Other Locations > Connect to Server
				smb://192.168.1.73:1445/InternalStorage
					U: luke
					P: same as this computer
		https://play.google.com/store/apps/details?id=fr.webrox.landrive&hl=en_US

			I needed to run the server on my phone instead of on the computer because I need the
			computer to be able to read/write the files on the phone 

				It would be cool if there was a way to read/write both from both ...
					I dont think the server can read/write data on the client though
					perhaps if both were servers and both were clients to each other

				Before I discovered this library and app I also tried a bunch of other stuff.
				If I ever want to see if I can make a server and client on both then the app
				I bought also can create SMB clients, and have run the client simultaniously
				with the server. See all these other notes for what else I did to run a SMB
				server on my computer with SAMBA (free software re-implementation of the SMB
				networking protocol).

					following these instructions:
					https://linuxize.com/post/how-to-install-and-configure-samba-on-ubuntu-18-04/

					used this to fix issue with:
						sudo systemctl restart nmbd
						Status: "nmbd: No local IPv4 non-loopback interfaces available, waiting for interface ..."
					https://askubuntu.com/questions/1125678/ubuntu-18-04-nmbd-service-will-not-start

					used "ifconfig" to find the samba server IP
					https://vitux.com/how-to-install-and-configure-samba-on-ubuntu/

					In Ubuntu Nautilus File explorer

					Tried to use this to connect my phone to the Samba server
						Phones "home" path: /storage/emulated/0
					https://www.techrepublic.com/article/how-to-connect-to-an-smb-share-from-your-android-device/

					https://discourse.ubuntu.com/t/the-default-file-sharing-and-media-sharing-experience-in-18-04/3834/3

	SOURCES:

		install
		https://pypi.org/project/pysmb/

		docs
		https://pysmb.readthedocs.io/en/latest/api/smb_SMBConnection.html

		example
		https://gist.github.com/joselitosn/e74dbc2812c6479d3678

	'''


userID = 'luke'
password = 'l'
client_machine_name = 'samsunggreatqlt'
server_name = 'samsunggreatqlt'
server_ip = '192.168.1.73'
port = 1445
domain_name = 'WORKGROUP'

print('\nconnecting to SMB Server')
conn = SMBConnection(
	userID,
	password,
	client_machine_name,
	server_name,
	domain=domain_name,
	use_ntlm_v2=True,
    is_direct_tcp=True)
conn.connect(server_ip, port)
print('connection established')

print('\nlisting directory contents')
shares = conn.listShares()
for share in shares:
	if share.name != 'InternalStorage': continue
	share_contents = conn.listPath(share.name, '/Download')
	print(share.name + '/Download')
	for sc in share_contents:
		# p.s. this lib calls everything files, both dirs and files
		print('\tisDirectory:', sc.isDirectory, sc.filename)
print()



# write new file to server
print('\nwrite file to server')
f = open('test_file_computer.txt', 'w')
f.write('Hello phone,\nsincerely computer.\n')
f.close()
f = open('test_file_computer.txt', 'rb') # must be in rb mode
num_bytes_uploaded = conn.storeFile(
	'InternalStorage',
	'/Download/test_file_phone.txt', f)
f.seek(0)
for line in f.readlines(): print(line)
f.close()

input('Press any key to continue ...')

# read file from server
print('\nread file from server')
f = open('test_file_from_phone.txt', 'wb') # must be in wb mode
_, _ = conn.retrieveFile('InternalStorage', '/Download/test_file_phone.txt', f)
f.close()
f = open('test_file_from_phone.txt', 'r')
for line in f.readlines():
	line = line if line[-1] != '\n' else line[:-1]
	print(line)
f.close()

# get file attributes from server
# ex. last_write_time
# for all attributes see: https://pysmb.readthedocs.io/en/latest/api/smb_SharedFile.html
print('\nget file attributes from server')
sharedFile = conn.getAttributes('InternalStorage', '/Download/test_file_phone.txt')
print('File: /Download/test_file_phone.txt')
print('last_write_time (unix timestamp):', sharedFile.last_write_time)

# delete a file on server
print('\ndelete file on server')
conn.deleteFiles('InternalStorage', '/Download/test_file_phone.txt')
print('deleted test_file_phone.txt at /Download/, see server for proof')

############ ERROR ############
# for some reason the SMB server can't copy over large files without disconnecting :(
# https://github.com/miketeo/pysmb/issues/23
# # write mp3 file to server
# print('\nwrite mp3 file to server')
# # local_mp3_path = '/home/luke/Music/Rap/Kendrick_Lamar/Good_Kid/Swimming_Pools.mp3'
# local_mp3_path = '/home/luke/Music/Rap/Eminem/8_Mile/test_file.txt'
# phone_mp3_path = '/Music/Rap/Kendrick_Lamar/Good_Kid/test_file.txt'
# # import io
# # f = io.BytesIO(open(local_mp3_path, 'rb').read()) # must be in rb mode
# print('conn.isUsingSMB2 =', conn.isUsingSMB2)
# f = open(local_mp3_path, 'rb')
# offset = 0
# position = conn.storeFileFromOffset(
# 	'InternalStorage',
# 	phone_mp3_path, f, offset)
# print(position)
# f.close()

# create directory on server
print('\ncreate directory on server')
conn.createDirectory('InternalStorage', '/Download/test_folder/')
print('created director InternalStorage/Download/test_folder/, see server for proof')

input('Press any key to continue ...')

# delete directory on server
print('\ndelete directory on server')
conn.deleteDirectory('InternalStorage', '/Download/test_folder/')
print('deleted director InternalStorage/Download/test_folder/, see server for proof')

print('\nclose connection to server')
conn.close()
print('connection terminated')



# clean up files from tests
import subprocess
subprocess.run(['rm', 'test_file_computer.txt'])
subprocess.run(['rm', 'test_file_from_phone.txt'])
