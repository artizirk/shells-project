import threading, time
def threadfunc():
	while True:
		time.sleep(1)
th = threading.Thread(target=threadfunc)
#th.daemon = True
th.start()
print "Daemon running"
