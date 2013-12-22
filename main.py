#!/usr/bin/python2
#-.- encoding: utf-8 -.-
import dbapi, time
from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash, _app_ctx_stack

dbapi = dbapi.DBApi()
Debug = True
app = Flask(__name__)
app.config.from_object(__name__)

blacklist = ['`', '$', '(', ')', ';', ',', '.', ':', '[', ']', '{', '}', '\\', '/', '=']
def check_output(input):
	for list in blacklist:
		if not list in input:
			return input
		else:
			return "invalid"
@app.route('/')
def home():
	return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
	print 'reached register()'
	if request.method == 'POST':
		print 'request method right'
		####FIXME!!! Data won't go forward at here
		if not request.form['username']:
			error = "You need to insert username!"
		print 'username checked'
		if not request.form['password']:
			error = "You need to insert password!" 
		print 'passwd checked' 
		if not request.form['password'] == request.form['passwordagain']:
			error = "Password's don't match"
		print 'all forms validated'
		uname = request.form['username']
		password = request.form['password']
		rname = request.form['realname']
		email = request.form['email']
		print 'variables set'
		result = dbapi.adduser(uname, password, rname, email)
		print 'user created'
		result = result.split(':')
		print 'result splitted'
		if result[1] == "error":
			error = "An error occured! A load of monkeys investigate it"
		else:
			flash("User {} registred! You can log in now".format(uname))
		return redirect('/', error=error)
	else:
		return render_template('register.html')
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=7558)
