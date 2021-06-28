# security file
from user import User
from werkzeug.security import safe_str_cmp

users = [
	User(1,'neal','abc'),
	User(2, 'tom', 'xyz'),
	User(3, 'jerry', '123')
]

username_mapping = {user.username : user for user in users}

userID_mapping = {user.id : user for user in users}

def authenticate(username, password):
	user = username_mapping.get(username, None) # .get() is like [] except we can specify what the value will be if the key doesn't exist
	if user and safe_str_cmp(user.password, password):
		return user

def identity(payload):
	user_id = payload['identity']
	return userID_mapping.get(user_id, None)




