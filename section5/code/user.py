import sqlite3
from flask_restful import Resource, reqparse

class User:
	def __init__(self, _id, username, password):
		self.id = _id
		self.username = username
		self.password = password

	@classmethod
	def find_by_username(cls, username):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		# get user based on username
		user_query = "SELECT * FROM users WHERE username=?" # value must always be in the form of a tuple

		# get result
		result = cursor.execute(user_query, (username,)) # note (username) just means paranthesis around username.. similar to (5+3) * 10 = 80, but (username,) specifies this is a tuple

		# get the first row
		row = result.fetchone()
		if row:
			# user = User(row[0], row[1], row[2]) --> notice we are using the current class User and creating a User, but we don't want to hard code User in case the class name changes, so we add the @classmethod decorator, and change the self parameter to cls. We can then create the user via cls(x,y,z)
			#user = cls(row[0], row[1], row[2]) # use the current class 'cls' as opposed to 'User' so that we don't hard code User and if we ever change the class name, it'll still work
			user = cls(*row) # instead of passing each row element, we can just pass all the arguments by using *
		else:
			user = None

		connection.close()
		return user

	@classmethod
	def find_by_id(cls, _id):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		id_query = "SELECT * FROM users WHERE id=?"
		result = cursor.execute(id_query, (_id,))

		row = result.fetchone()
		if row:
			user = cls(*row)
		else:
			user = None

		connection.close()
		return user

# create a resource to register a user
class UserRegister(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('username',
			type=str,
			required=True,
			help="you must specify a username"
		)
	parser.add_argument('password',
			type=str,
			required=True,
			help="you must specify a password"
		)
	def post(self):
		data = UserRegister.parser.parse_args()
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "INSERT INTO users VALUES (NULL, ?, ?)" # by using NULL as the ID for the INTEGER PRIMARY KEY field, it will auto-incrememnt
		cursor.execute(query, (data['username'], data['password']))

		connection.commit()
		connection.close()

		return {"message": "User created successfully"}, 201
