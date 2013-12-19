import socket, base64
from time import sleep
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('127.0.0.1', 1025)
print "connecting to %s port %s" % server_address
sock.connect(server_address)
#sock.sendall(base64.b64encode('reg:mikroskeem:mvainomaa:Mark Vainomaa:mikroskeem@gmail.com'))
while True:
	try:
		opt = raw_input('> ')
		if opt == 'help':
			print "Funcs: adduser deluser search exit(ctrl-c)"
		elif opt == 'adduser':
			user = raw_input("username: ")
			passw = raw_input("pass: ")
			realn = raw_input("realname: ")
			email = raw_input("email: ")
			sock.send(base64.b64encode('reg:{}:{}:{}:{}'.format(user,passw,realn, email)))
		elif opt == 'deluser':
			user = raw_input("username: ")
			sock.send(base64.b64encode('del:{}'.format(user)))
		elif opt == 'search':
			keyword = raw_input("search for: ")
			sock.send(base64.b64encode('search:{}'.format(keyword)))
			print "search result: ", sock.recv(100)
	except KeyboardInterrupt:
		sock.close()
		exit(1)
