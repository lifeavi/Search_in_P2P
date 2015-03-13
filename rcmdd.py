import socket
import sys
import time
import os
from datetime import datetime

if __name__ == '__main__':
	UDP_IP = socket.gethostbyname(socket.gethostname())
	print "Server IP",UDP_IP
	if len(sys.argv) < 2:
		print "Usage : rcmdd port_no"
		sys.exit(1)

	UDP_PORT = int(sys.argv[1])
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
	sock.bind((UDP_IP, UDP_PORT))
		
	while True:
		data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
		CL_IP,CL_PORT = addr
		
		exe_count = data.split(':')[0]
		time_delay = data.split(':')[1]
		command = data.split(':')[2]
		
		for i in range(int(exe_count)):
			time.sleep(float(time_delay)) # delays for specified seconds
			output = os.popen(command).read()
			output = "Server Time  ---->  "+str(datetime.now())+"\n"+output
			print "Server IP",UDP_IP
			print "Current Time : ", str(datetime.now()), "\t"
			print "Source/Client IP : ", CL_IP, "\t"
			print "Command : ", command, "\t"
			if i != int(exe_count)-1:
				print "Status : ", "connected", "\n"
			else:
				print "Status : ", "Closed", "\n"
			sock.sendto(output, (CL_IP, 5822))
			
			
