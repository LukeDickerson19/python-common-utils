import socket

baddr = '94:8B:C1:E1:B8:15'
channel = 4
s = socket.socket(
	socket.AF_BLUETOOTH,
	socket.SOCK_STREAM, 
	socket.BTPROTO_RFCOMM)
s.connect((baddr, channel))
s_sock = server_sock.accept()
print ("Accepted connection from "+address)

data = s_sock.recv(1024)
print ("received [%s]" % data)

s.listen(1)


# import bluetooth


# address = '98:7A:14:9B:5D:46'

# server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

# port = 5
# server_sock.bind((address, port))
# server_sock.listen(1)

# client_sock = server_sock.accept()
# print("Accepted connection from " + address)

# data = client_sock.recv(1024)
# print("received [%s]" % data)





# from bluetooth.ble import DiscoveryService

# service = DiscoveryService()
# devices = service.discover(2)

# for address, name in devices.items():
#     print("name: {}, address: {}".format(name, address))
