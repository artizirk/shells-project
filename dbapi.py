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
		sql = """DROP TABLE USERS;"""
		cursor.execute(sql)
		self.db_commit()
		return "dbapi:table:flushed"

	def create_tables(self):
		sql = """CREATE TABLE USERS (
		USERNAME CHAR(20) NOT NULL,
		PASSWORD CHAR(100) NOT NULL,
		REALNAME CHAR(50),
		EMAIL CHAR(30) 
		);"""
		cursor.execute(sql)
		self.db_commit()
		return "dbapi:table:created"

	def adduser(self, user, passw, realname, email):
		sql = """INSERT INTO USERS (USERNAME, PASSWORD, REALNAME, EMAIL)
		VALUES ('{}', '{}', '{}', '{}');""" .format(user, passw, realname, email)
		try:
			cursor.execute(sql)
			self.db_commit()
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
	def search_user(self, keyword, type):
		sql = """SELECT * FROM USERS WHERE USERNAME LIKE '{0}' OR EMAIL LIKE '{0}' OR REALNAME LIKE '{0}';""".format(keyword)
		cursor.execute(sql)
		result = "dbapi:noresult:{}".format(keyword)
		results = cursor.fetchall()
		for row in results:
			uname = row[0]
			passw = row[1]
			rname = row[2]
			email = row[3]
			if type == "server":
				result = 'dbapi:result:server:{}:{}:{}:{}'.format(uname, passw, rname, email)
			elif type == "normal":
				result = 'dbapi:result:normal:{}:{}:{}'.format(uname, rname, email)
		return result
	def deluser(self, user):
		sql = """DELETE FROM USERS WHERE USERNAME='{0}';""".format(user)
		cursor.execute(sql)
		self.db_commit()
		userapi.deluser(user)
		return "dbapi:deluser:{}".format(user)
	def list(self):
		sql = """SELECT * FROM USERS;"""
		cursor.execute(sql)
		results = cursor.fetchall()		 
		for row in results:
			uname = row[0]
			passw = row[1]
			rname = row[2]
			email = row[3]
			print "dbapi:list:{}:{}:{}:{}".format(uname, passw, rname, email)
	def change_password(self, user, passw):
		sql = """UPDATE USERS SET PASSWORD="{1}" WHERE USERNAME="{0}";""".format(user, passw)
		cursor.execute(sql)
		self.db_commit()
		userapi.password(user, passw)
		return "dbapi:passwd:changed:{}".format(user)
