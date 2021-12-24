import socket

robot = '172.16.8.101'
port = 50001

class UDP_Send():
	def __init__(self,addr,port):
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.addr = addr
		self.port = port
	def send(self,lis):
		strig = ''
		num = len(lis)
		i = 0
		while i<num:
			strig = strig + str("%12.8f"%lis[i])
			if i != num-1:
				strig = strig+','
			i = i+1
		self.sock.sendto(strig.encode('utf-8'),(self.addr,self.port))
		return 0
		
class UDP_Recv():
	def __init__(self,addr,port):
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.sock.bind((addr,port))
		self.sock.setblocking(0)
	def recv(self):
		message = self.sock.recv(18000).decode('utf-8')
		slist = message.split(',')
		a = [float(s) for s in slist]
		return a
