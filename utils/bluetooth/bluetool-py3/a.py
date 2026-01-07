
import bluezutils
from bluetool import Bluetooth

phone_name = b'SAMSUNG-SM-N950U'
# phone_mac_address = '98:7A:14:9B:5D:46'

bluetooth = Bluetooth()
bluetooth.scan()
devices = bluetooth.get_available_devices()
for d in devices:
	if d['name'] == phone_name:
		phone_device = d
		print(phone_device)
		break

print(phone_device['mac_address'])
d0 = bluetooth.connect(str(phone_device['mac_address']))
# d0 = bluezutils.find_device(mac_address)
print(d0)