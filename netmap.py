import os
from pprint import pprint
devices = []
dynamicdevices=[]
formatted_devices=[]
def map():
	formatted_devices=[]
	for device in os.popen('arp -a'): 
		devices.append(device)

	for n in range(0,len(devices)):
		devices[n]=devices[n].replace('\n','')

	for device in devices:
		if 'dynamic' in device:
			dynamicdevices.append(device)

	for device in dynamicdevices:
		formatted_devices.append(device[0:16].replace(' ',''))
	return(formatted_devices)

def get_ipv4():
	for line in os.popen('ipconfig'):
		if 'IPv4' in line:
			IPv4=line[-17:].replace('.','',-3)
	return(IPv4)
if __name__=='__main__':
	pprint(map())
	print(get_ipv4())