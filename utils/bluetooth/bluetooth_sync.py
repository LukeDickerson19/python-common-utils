import sys
import bluetooth

# devices = bluetooth.discover_devices()
# for d in devices:
# 	print(d)

phone_bluetooth_address = '94:8B:C1:E1:B8:15'
# phone_bluetooth_name    = 'SAMSUMG-SMN950U'


# # result = bluetooth.lookup_name(phone_bluetooth_address)
# # print(result)

# sys.exit()


"""
A simple Python script to receive messages from a client over
Bluetooth using PyBluez (with Python 2).
"""

port = 3
backlog = 1
size = 1024
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((phone_bluetooth_address, port))
print('asdf')
s.listen(backlog)
print('888')
try:
	# print('143')
    client, clientInfo = s.accept()
    # print('56')
    while 1:
        data = client.recv(size)
        if data:
            print(data)
            client.send(data) # Echo back to client
except:	
    print("Closing socket")
    client.close()
    s.close()

