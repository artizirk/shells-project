#!/usr/bin/python2
import MySQLdb
from subprocess import call
class API():
	def __init__(self):
		try:
			global db
			global cursor
			db = MySQLdb.connect("localhost","root","root","shells_users")
			cursor = db.cursor()
		except:
			print "api:error:connect"
			exit(1)
	def __call__(self):
		pass
	def flush_tables(self):
		#USE WITH CAUTION!
		sql = """DROP TABLE users;"""
		cursor.execute(sql)
		self.db_commit()
		return "api:table:flushed"

	def create_tables(self):
		#USE WITH CAUTION
		sql = """CREATE TABLE users (
		username CHAR(20) NOT NULL,
		password CHAR(100) NOT NULL,
		realname CHAR(50),
		email CHAR(30),
		isadmin CHAR(3),
		hasshell CHAR(3) 
		);"""
		cursor.execute(sql)
		self.db_commit()
		return "api:table:created"

	def adduser(self, user, passw, realname, email, home, shell, isadmin, hasshell):
		check_user = self.match_user(user)
		check_user = check_user.split(':')
		if not check_user[1] == 'nomatch':
			return "api:newuser:exsists:{}".format(user) 
		isadmin = 'no'
		hasshell = 'no'
		sql = """INSERT INTO users (username, password, realname, email, isadmin, hasshell)
		VALUES ('{}', '{}', '{}', '{}', '{}', '{}');""" .format(user, passw, realname, email, isadmin, hasshell)
		try:
			cursor.execute(sql)
			self.db_commit()
			if hasshell is 'yes':
				cmd = "sudo useradd -m -d {} -s {} {}".format(home, shell, user)
				call(["bash", "-c"], cmd)
				self._shell_change_password(user, passw)
			return "api:newuser:{}".format(user)
		except:
			return "api:error:newuser"
	def db_close(self):
		db.close()
		return "api:closed"
	def db_commit(self):
		try:
			db.commit()
			return "api:commited"
		except:
			return "api:error:commit"
	def match_user(self, keyword):
		sql = """SELECT * FROM users WHERE username='{0}'""".format(keyword)
		cursor.execute(sql)
		result = "api:nomatch:{}".format(keyword)
		results = cursor.fetchall()
		for row in results:
			uname = row[0]
			passw = row[1]
			rname = row[2]
			email = row[3]
			isadmin = row[4]
			hasshell = row[5]
			result = 'api:{}:{}:{}:{}:{}:{}'.format(uname, passw, rname, email, isadmin, hasshell)
		return result
	def raw_command(self, query):
		cursor.execute(query)
		result = cursor.fetchall()
		return result if result else None
	def search_user(self, keyword, type):
		sql = """SELECT * FROM users WHERE username LIKE '{0}' OR email LIKE '{0}' OR realname LIKE '{0}';""".format(keyword)
		cursor.execute(sql)
		result = "api:noresult:{}".format(keyword)
		results = cursor.fetchall()
		for row in results:
			uname = row[0]
			passw = row[1]
			rname = row[2]
			email = row[3]
			isadmin = row[4]
			hasshell = row[5]
			if type == "server":
				result = 'api:result:server:{}:{}:{}:{}:{}:{}'.format(uname, passw, rname, email, isadmin, hasshell)
			elif type == "normal":
				result = 'api:result:normal:{}:{}:{}:{}:{}'.format(uname, rname, email, isadmin, hasshell)
		return result
	def deluser(self, user):
		check_user = self.match_user(user)
		check_user = check_user.split(':')
		if check_user[1] == 'nomatch':
			return "api:deluser:nosuchuser:{}".format(user)
		sql = """DELETE FROM users WHERE username='{0}';""".format(user)
		cursor.execute(sql)
		self.db_commit()
		if check_user[6] == 'yes':
			cmd = 'sudo userdel -r {}'.format(user)
			call(["bash", "-c"], cmd)
		return "api:deluser:{}".format(user)
	def list(self):
		sql = """SELECT * FROM users;"""
		cursor.execute(sql)
		results = cursor.fetchall()
		for row in results:
			uname = row[0]
			passw = row[1]
			rname = row[2]
			email = row[3]
			isadmin = row[4]
			hasshell = row[5]
			print "api:list:{}:{}:{}:{}:{}:{}".format(uname, passw, rname, email, isadmin, hasshell)
	def _shell_change_password(self, user, passw):
		cmd="sudo passwd {0} <<EOF\n{1}\n{1}\nEOF".format(user, passw)
		call(cmd, shell=True, stdout=None, stderr=None)
	def change_password(self, user, passw):
		check_user = self.match_user(user)
		check_user = check_user.split(':')
		if check_user[1] == 'nomatch':
			return "api:passwd:nosuchuser:{}".format(user)
		sql = """UPDATE users SET password="{1}" WHERE username="{0}";""".format(user, passw)
		cursor.execute(sql)
		self.db_commit()
		if check_user[6] is 'yes':
			self._shell_change_password(user, passw)
		return "api:passwd:changed:{}".format(user)
