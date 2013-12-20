#!/usr/bin/python2
import subprocess, dbapi
"""
I'm only called by DBApi!
"""
blacklist = [";", "$", "`", "(", ")"]
class UserApi():
	def __init__(self):
		pass
	def __call__(self):
		pass
	def createuser(self, name, passw, home, shell):
		for i in blacklist:
			if i in name:
				return "userapi:error:newuser:invalid"
			if i in passw:
				return "userapi:error:newuser:invalid"
			if i in home:
				return "userapi:error:newuser:invalid"
			if i in shell:
				return "userapi:error:newuser:invalid"
		data = "sudo useradd -m -d {} -s {} {}".format(home, shell, name)
		subprocess.call(["bash", "-c", data], stderr=None, stdout=None)
		return "userapi:newuser:{}:{}".format(name, home)
		self.password(name, passw)
	def deluser(self, user):
		for i in blacklist:
			if i in user:
				return "userapi:error:deluser:invalid"
		subprocess.call(["sudo", "userdel", "-r", user], stdout=None, stderr=None)
		return "userapi:deluser:{}".format(user)
	
	def password(self, user, passw):
		for i in blacklist:
			if i in user:
				return "userapi:error:passwd:invalid"
			if i in passw:
				return "userapi:error:passwd:invalid"
		
		cmd="sudo passwd {} <<EOF\n{}\n{}\nEOF".format(user, passw, passw)
		subprocess.call(cmd, shell=True, stdout=None, stderr=None)
		return "userapi:password:{}:{}".format(user, passw)
