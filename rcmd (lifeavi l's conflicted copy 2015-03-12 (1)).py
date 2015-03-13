import socket
import sys
import threading
import time
from fileSystem import *

class Assign4(threading.Thread):
	
	ipOfNeighbors = {}
	whichThread = 0
	listOfSearches = []
	
	
	def __init__(self, whichThread, ip_address, port_no, ipOfNeighbors):
		threading.Thread.__init__(self)
		self.whichThread = whichThread
		self.ipOfNeighbors = ipOfNeighbors
		self.ip_address = ip_address
		self.port_no = port_no
		print "class Assign4 Initialized"
		
	def bind_ip(self,port_no):
		while 1:
			print " I am listening on ",port_no
			data, addr = self.sockr.recvfrom(1024)
			if not data: 
				print "no data"
			else:
				print "the data recieved from server is :",data
				retVal = self.parsedata(data)
				self.sockr.sendto(retVal,addr)

	def listenForArgs(self):
		time.sleep(2)
		while 1:
			try:
				action= raw_input("Type the command: ")
				self.parseAction(action)
			except KeyboardInterrupt:
				sys.exit(0)
				
				
	def parseAction(self,action):
		UDP_IP = "turnip.cs.colostate.edu"
		UDP_PORT = 5000
		
			
		actions = action.split()

		if len(actions) > 1:	
			self.ip_address = actions[1]
			self.port_no    = actions[2]
		
		if actions[0] == "REG" or actions[0] == "UNREG":
			self.command_to_send_bs(UDP_IP,UDP_PORT,actions[0])
		elif actions[0] == "JOIN" or actions[0] == "LEAVE":
			self.command_to_send_nodes(actions[0])
		elif actions[0] == "NEIGHBOURS":
			print self.ipOfNeighbors.keys()
		elif actions[0] == 'time':
			print time.time()
		else:
			print "This command is invalid "
			
	def command_to_send_bs(self,UDP_IP,UDP_PORT,command_to_send):
		username = "apor"
		if command_to_send == "JOIN":
			x = command_to_send+" "+str(self.ip_address)+" "+str(int(self.port_no))
		else:
			x = command_to_send+" "+str(self.ip_address)+" "+str(int(self.port_no))+" "+username
		
		if len(x) < 100:
			leng = '00'+str(len(x)+5)
		elif len(x) > 99:
			leng = '0'+str(len(x)+5)
			
		send_data = leng+' '+x
		self.socks.sendto(send_data, (UDP_IP, UDP_PORT))
		print "The data to send is", send_data 
		data, addr = self.socks.recvfrom(1024)
		print "rec",data
		self.parsedata(data)
		
	def command_to_send_nodes(self,command_to_send):
		x = command_to_send+" "+str(self.ip_address)+" "+str(int(self.port_no))
		if len(x) < 100:
			leng = '00'+str(len(x)+5)
		elif len(x) > 99:
			leng = '0'+str(len(x)+5)
			
		send_data = leng+' '+x
		
		for neighbor in self.ipOfNeighbors.keys():
			try:
				self.socks.sendto(send_data, (neighbor, int(ipOfNeighbors[neighbor]['port'])))
				data, addr = self.socks.recvfrom(1024)
				print data
			except KeyError:
				print "Key doesn't exist"	
	
	def parsedata(self, data):
		d = data.split()

		if d[1] == "REGOK" and d[2] == "0":
			print "First Node in System"
			
		if d[1] == "REGOK" and d[2] == "1":
			self.ipOfNeighbors[d[3]] = {'port':d[4]}
			
		if d[1] == "REGOK" and d[2] == "2":
			self.ipOfNeighbors[d[3]] = {'port':d[4]}
			self.ipOfNeighbors[d[5]] = {'port':d[6]}

			
		if len(self.ipOfNeighbors) > 0 and d[1] == "REGOK":
			self.command_to_send_nodes("JOIN")
			
		if d[1] == "JOIN":
			try:
				if d[2] in self.ipOfNeighbors.keys() and self.ipOfNeighbors[d[2]]['port'] == d[3]:
					return "0014 JOINOK 9999"
				else:
					self.ipOfNeighbors[d[2]] = {'port':d[3]}
					return "0014 JOINOK 0"
			except KeyError:
				print "Key doesn't exist"
		
		if d[1] == "UNROK":
			self.command_to_send_nodes("LEAVE")
			
		if d[1] == "LEAVE":
			try:
				del self.ipOfNeighbors[d[2]]
				return "0015 LEAVEOK 0"
			except KeyError:
				print "Key doesn't exist"
					
		print self.ipOfNeighbors
		return "Okay"		
	
	def run(self):
		if self.whichThread == 0:
			self.sockr = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
			self.sockr.bind((ip_address, port_no))
			self.bind_ip(port_no)
		else:
			self.socks = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
			self.socks.bind((ip_address, port_no+1))
			self.listenForArgs()
		
		

if __name__ == '__main__':		
	ipOfNeighbors ={}
	ip_address = socket.gethostbyname(socket.gethostname())
	port_no = 0
	
	f = FileSystem()
	thread0 = Assign4(0, ip_address, port_no, ipOfNeighbors)
	thread1 = Assign4(1, ip_address, port_no, ipOfNeighbors)
	
	
	#start the threads
	thread0.start()
	thread1.start()








