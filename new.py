import threading
import SocketServer

class ThreadedEchoRequestHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		# Echo the back to the client
		data = self.request.recv(1024)
		cur_thread = threading.currentThread()
		response = '%s: %s' % (cur_thread.getName(), data)
		self.request.send(response)
		return

class ThreadedEchoServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass

if __name__ == '__main__':
	import socket
	import threading

	address = ('localhost', 1025) # let the kernel give us a port
	server = ThreadedEchoServer(address, ThreadedEchoRequestHandler)
	ip, port = server.server_address # find out what port we were given

	t = threading.Thread(target=server.serve_forever)
	t.setDaemon(True) # don't hang on exit
	t.start()
	print 'Server loop running in thread:', t.getName()

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((ip, port))

	message = 'Hello, world'
	print 'Sending : "%s"' % message
	len_sent = s.send(message)

	response = s.recv(1024)
	print 'Received: "%s"' % response

	s.close()
	server.socket.close()
