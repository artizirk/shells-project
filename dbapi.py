#!/usr/bin/python2
import MySQLdb
class DBApi():
	def __init__(self):
		try:
			global db
			global cursor
			db = MySQLdb.connect("localhost","root","root","shells_users")
			cursor = db.cursor()
		except:
			print "Couldn't connect to database"
			exit(1)
	def __call__(self):
		pass
	def flush_tables(self):
		sql = """DROP TABLE USERS;"""
		cursor.execute(sql)
		db.commit()
		return "[DBApi]: Tables flushed"

	def create_tables(self):
		sql = """CREATE TABLE USERS (
		USERNAME CHAR(20) NOT NULL,
		PASSWORD CHAR(100) NOT NULL,
		REALNAME CHAR(50),
		EMAIL CHAR(30) 
		);"""
		cursor.execute(sql)
		db.commit()
		return "[DBApi]: Users table created"

	def adduser(self, user, passw, realname, email):
		sql = """INSERT INTO USERS (USERNAME, PASSWORD, REALNAME, EMAIL)
		VALUES ('{}', '{}', '{}', '{}');""" .format(user, passw, realname, email)
		try:
			cursor.execute(sql)
			db.commit()
			return "[DBApi]: User {} created".format(user)
		except:
			return "[DBApi]: An error occured during user creation!"
		return "[DBApi]: User {} created!".format(user)
	def db_close(self):
		db.close()
		return "[DBApi]: Database closed"
	def search_user(self, keyword):
		sql = """SELECT * FROM USERS WHERE USERNAME LIKE '{0}' OR EMAIL LIKE '{0}' OR REALNAME LIKE '{0}';""".format(keyword)
		cursor.execute(sql)
		result = "[DBApi]: No result for {}".format(keyword)
		results = cursor.fetchall()
		for row in results:
			uname = row[0]
			rname = row[2]
			email = row[3]
			result = '[DBApi]: User: "{}", Realname: "{}", E-Mail: "{}"'.format(uname, rname, email)
		return result
	def deluser(self, user):
		sql = """DELETE FROM USERS WHERE USERNAME='{0}';""".format(user)
		cursor.execute(sql)
		db.commit()
		return "[DBApi]: User {} deleted".format(user)
