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



from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

from jsonrpc import JSONRPCResponseManager, dispatcher


@dispatcher.add_method
def version():
    """Returns the version"""
    return {"version":"0.1"}

@dispatcher.add_method
def add_unix_user(user, password):
    """Adds a new unix user to the system"""
    return {"uid":1001, "gid":500, "user":user}

@dispatcher.add_method
def remove_unix_user(user):
    """Removes a unix user to the system"""
    return {"uid":1001, "gid":500, "user":user}

@Request.application
def application(request):
    """Main application"""
    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


if __name__ == '__main__':
    run_simple('localhost', 4000, application)
