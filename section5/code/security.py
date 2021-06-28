# security file
from user import User
from werkzeug.security import safe_str_cmp


def authenticate(username, password):
	user = User.find_by_username(username) # .get() is like [] except we can specify what the value will be if the key doesn't exist
	if user and safe_str_cmp(user.password, password):
		return user

# when user requests a endpoint where they need to be authenticated. We use the user_id and if it matches the JWT token, we assume its the correct user
def identity(payload):
	user_id = payload['identity']
	return User.find_by_id(user_id)
