#!/usr/bin/python2
#-.- encoding: utf-8 -.-
import dbapi, time
from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash, _app_ctx_stack

dbapi = dbapi.DBApi()

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
	return "Hello flask :)"

@app.route('/register', methods=['GET', 'POST'])
def register():
	return "Under construction"
	if request.method == 'POST':
		if not request.form['username']:
			error = "You need to insert username!"
		if not request.form['password']:
			error = "You need to insert password!" 
		if not request.form['password'] == request.form['passwordagain']:
			error = "Password's don't match"
		uname = check_output(request.form['username'])
		password = check_output(request.form['password'])
		rname = check_output(request.form['realname'])
		email = check_output(request.form['email'])
		if uname == 'invalid':
			error = 'Invalid username!'
		if password == 'invalid':
			error = 'Invalid password!'
		if rname == 'invalid':
			error = 'Invalid Real name!(Dude, you're drunk? :D)'
		if email == 'invalid':
			error = 'Invalid email!' 
		if not request.form['realname']:
			rname = "IDontHaveName"
		if not request.form['email']:
			email = "idonthave@email.yet"
		result = dbapi.adduser(uname, password, rname, email)
		result = result.split(':')
		if result[1] == "error":
			error = "An error occured! A load of monkeys investigate it"
		else:
			flash("User {} registred! You can log in now".format(uname))
	else:
		error = "Method GET not supoorted, it's insecure for this thing ;)"
app.run(host='0.0.0.0', port='7558')
