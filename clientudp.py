import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(('',0))

while 1:
	data = input("write message : ")
	sock.sendto(data.encode(),('localhost',1234))

	data, addr = sock.recvfrom(1024)
	print( data.decode() )
