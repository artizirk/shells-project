import dbapi
api = dbapi.DBApi()
print api.flush_tables()
print api.create_tables()
print api.adduser('mikroskeem', 'jdjdueudjf84jfufj38dkt', 'Mark Vainomaa', 'mikroskeem@gmail.com')
print api.search_user('mikroskeem', 'server')
print api.change_password('mikroskeem', 'lul')
print api.deluser('mikroskeem')
print api.search_user('mikroskeem', 'server')
print api.db_close()
