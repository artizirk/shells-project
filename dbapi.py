#!/usr/bin/python2
import MySQLdb, userapi
userapi = userapi.UserApi()
class DBApi():
	def __init__(self):
		try:
			global db
			global cursor
			db = MySQLdb.connect("localhost","root","root","shells_users")
			cursor = db.cursor()
		except:
			print "dbapi:error:connect"
			exit(1)
	def __call__(self):
		pass
	def flush_tables(self):
		sql = """DROP TABLE users;"""
		cursor.execute(sql)
		self.db_commit()
		return "dbapi:table:flushed"

	def create_tables(self):
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
		return "dbapi:table:created"

	def adduser(self, user, passw, realname, email, isadmin, hasshell):
		check_user = self.match_user(user)
		check_user = check_user.split(':')
		if not check_user[1] == 'nomatch':
			return "dbapi:newuser:exsists:{}".format(user) 
		isadmin = 'no'
		hasshell = 'no'
		sql = """INSERT INTO users (username, password, realname, email, isadmin, hasshell)
		VALUES ('{}', '{}', '{}', '{}', '{}', '{}');""" .format(user, passw, realname, email, isadmin, hasshell)
		try:
			cursor.execute(sql)
			self.db_commit()
			if hasshell is 'yes':
				print userapi.createuser(user, passw, '/home/{}'.format(user), '/bin/bash')
			return "dbapi:newuser:{}".format(user)
		except:
			return "dbapi:error:newuser"
	def db_close(self):
		db.close()
		return "dbapi:closed"
	def db_commit(self):
		try:
			db.commit()
			return "dbapi:commited"
		except:
			return "dbapi:error:commit"
	def match_user(self, keyword):
		sql = """SELECT * FROM users WHERE username='{0}'""".format(keyword)
		cursor.execute(sql)
		result = "dbapi:nomatch:{}".format(keyword)
		results = cursor.fetchall()
		for row in results:
			uname = row[0]
			passw = row[1]
			rname = row[2]
			email = row[3]
			isadmin = row[4]
			hasshell = row[5]
			result = 'dbapi:{}:{}:{}:{}:{}:{}'.format(uname, passw, rname, email, isadmin, hasshell)
		return result
	def raw_command(self, query):
		cursor.execute(query)
		result = cursor.fetchall()
		return result if result else None
	def search_user(self, keyword, type):
		sql = """SELECT * FROM users WHERE username LIKE '{0}' OR email LIKE '{0}' OR realname LIKE '{0}';""".format(keyword)
		cursor.execute(sql)
		result = "dbapi:noresult:{}".format(keyword)
		results = cursor.fetchall()
		for row in results:
			uname = row[0]
			passw = row[1]
			rname = row[2]
			email = row[3]
			isadmin = row[4]
			hasshell = row[5]
			if type == "server":
				result = 'dbapi:result:server:{}:{}:{}:{}:{}:{}'.format(uname, passw, rname, email, isadmin, hasshell)
			elif type == "normal":
				result = 'dbapi:result:normal:{}:{}:{}:{}:{}'.format(uname, rname, email, isadmin, hasshell)
		return result
	def deluser(self, user):
		check_user = self.match_user(user)
		check_user = check_user.split(':')
		if check_user[1] == 'nomatch':
			return "dbapi:deluser:nosuchuser:{}".format(user)
		sql = """DELETE FROM users WHERE username='{0}';""".format(user)
		cursor.execute(sql)
		self.db_commit()
		if check_user[6] == 'yes':
			print userapi.deluser(user)
		return "dbapi:deluser:{}".format(user)
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
			print "dbapi:list:{}:{}:{}:{}:{}:{}".format(uname, passw, rname, email, isadmin, hasshell)
	def change_password(self, user, passw):
		check_user = self.match_user(user)
		check_user = check_user.split(':')
		if check_user[1] == 'nomatch':
			return "dbapi:passwd:nosuchuser:{}".format(user)
		sql = """UPDATE users SET password="{1}" WHERE username="{0}";""".format(user, passw)
		cursor.execute(sql)
		self.db_commit()
		if check_user[6] is 'yes':
			print userapi.password(user, passw)
		return "dbapi:passwd:changed:{}".format(user)
