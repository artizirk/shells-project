import userapi
api = userapi.UserApi()
print api.createuser("foo", "tmp", "/tmp/foo", "/bin/bash")
print api.deluser("foo")
