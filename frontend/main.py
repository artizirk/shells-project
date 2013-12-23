#!/usr/bin/env python3
#
#  main.py
#  
#  Copyright 2013 Arti Zirk <arti.zirk@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  



from flask import Flask, request, session, g, redirect, url_for, \
                abort, render_template, flash
from pymongo import MongoClient
import requests
import json

# configuration
DEBUG = True
SECRET_KEY = 'ChangeME!!!!'
USERNAME = 'admin'
PASSWORD = 'default'

# create application
app = Flask(__name__)
app.config.from_object(__name__)

app.config.from_envvar('LEARNX_SETTINGS', silent=True)

@app.before_request
def before_request():
    g.db_con = MongoClient()
    g.db = g.db_con["LearnX"]

@app.teardown_request
def teardown_request(exception):
    db_con = getattr(g, 'db_con', None)
    if db_con is not None:
        db_con.close()

@app.route("/")
def index():
    return redirect(url_for('show_tasks'))
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_tasks'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        if request.form['username'] == "":
            error = 'not good username'
        elif request.form['password'] == "":
            error = 'not good password'
        else:
            session['logged_in'] = True
            flash('User {} added'.format(request.form['username']))
            return redirect(url_for('show_tasks'))
    return render_template('register.html', error=error)

@app.route('/tasks')
def show_tasks():
    if not session.get('logged_in'):
        flash('You need to login first')
        return redirect(url_for('login'))
    tasks = []
    return render_template('tasks.html', tasks=tasks)
    
@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run()
