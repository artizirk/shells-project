import dbapi
api = dbapi.DBApi()
#print api.flush_tables()
#print api.create_tables()
#print api.adduser('mark', 'lol', 'marks', 'mikroskeem@gmail.com')
print api.search_user('lol')
#print api.deluser('lol')
print api.search_user('mikroskeem')
print api.db_close()
