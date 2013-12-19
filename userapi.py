#!/usr/bin/python2
import subprocess

blacklist = [";", "$", "`", "(", ")"]
DEBUG = False
class UserApi():
	def __init__(self):
		pass
	def __call__(self):
		pass
	def createuser(self, name, passw, home, shell):
		for i in blacklist:
			if i in name:
				return "Invalid characters"
			if i in passw:
				return "Invalid characters"
			if i in home:
				return "Invalid characters"
			if i in shell:
				return "Invalid characters"
		data = "useradd -m -d {} -s {} {}".format(home, shell, name)
		print "[UserApi]: Running cmd: {}".format(data)
		if not DEBUG:
			subprocess.call(["bash", "-c", data])
		return "[UserApi]: User {} created with home in {}".format(name, home)
		self.password(name, passw)
	def deluser(self, user):
		for i in blacklist:
			if i in user:
				return "Invalid characters"
		#TODO: Check user from database
		if not DEBUG:
			subprocess.call(["userdel", "-r", user])
		return "[UserApi]: User {} deleted".format(user)
	
	def password(self, user, passw):
		for i in blacklist:
			if i in user:
				return "Invalid characters"
			if i in passw:
				return "Invalid characters"
		
		cmd="passwd {} <<EOF\n{}\n{}\nEOF".format(user, passw, passw)
		print "[UserApi]: Running command '{}'".format(cmd)
		if not DEBUG:
			subprocess.call(cmd)
		return "[UserApi]: User '{}' password changed to {}".format(user, passw)

