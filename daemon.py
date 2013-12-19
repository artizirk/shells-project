#!/usr/bin/python2
import threading, time, socket, dbapi, userapi, base64

dbapi = dbapi.DBApi()
userapi = userapi.UserApi()

class MainDaemon():
	def __init__(self):
		print "[MainDaemon]: Starting..."
		global sock
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_address = ('127.0.0.1', 1025)
		host = sock.getsockname()
		try:
			sock.bind(server_address)
			print "[MainDaemon]: Sucessfully started on {}!".format(server_address)
		except:
			print "[MainDaemon]: Failed to bind on {}! Exiting...".format(server_addr)
			exit(1)
	def __call__(self):
		self.__init__(self)
	def run(self):
		while True:
			sock.listen(1)
			while True:
				connection, client_address = sock.accept()
				print '[MainDaemon]: Client ', client_address
				data = connection.recv(1000)
				if data:
					self.messageaction(client_address, connection, data)
	def messageaction(self, client, connection, data):
		msg = base64.b64decode(data)
		print "{} {}".format(client, msg)
		cmd = msg.split(':')
		print "DEBUG: {}".format(cmd)
		if cmd[0] == "reg":
			print "[MainDaemon]: Calling register for {}".format(client)
			print dbapi.adduser(cmd[1], cmd[2], cmd[3], cmd[4])
		elif cmd[0] == "del":
			print "[MainDaemon]: Deleting user {}".format(cmd[1])
			print dbapi.deluser(cmd[1])
		elif cmd[0] == "search":
			print "[MainDaemon]: {} searches for {}".format(client, cmd[1])
			connection.send("Not implemented")
app = MainDaemon()
try:
	app.run()
except KeyboardInterrupt:
	sock.close()
	exit(1)
