from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from user import UserRegister

'''
	creating a professional REST API using flask_restful
	we no longer needs to use jsonify using flask_restful, since flask_restful returns json by default
'''


app = Flask(__name__)
app.secret_key = 'abc123xyz' # secret key for JWT authentication
api = Api(app) # allows us to add resources to the api

jwt = JWT(app, authenticate, identity) # JWT creates /auth endpoint that gets sent username and password, which gets sent to the authenticate function. We then get the correct user object and compare the user's password to the password given in the request. If it matches, we return the user and that becomes the identity. The /auth endpoint returns a JWT token if successful (not None when retrieving the user from authenticate). That JWT doesn't do anything, but we can send it to the next request we make. When we send a JWT, JWT calls the identity function and gets the correct user for that user id that the token represents. If it can do that, the user was authenticated and the JWT token was valid.



items = []


# Item Resource, which can only be accessed with a 'get' method
class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('price',
		type=float,
		required=True,
		help="price field cannot be empty!"
	)
	@jwt_required()
	def get(self, name):
		# for loop through items and returns the filter object in which the lambda predicate is true. Next returns the items in the order they appear (i.e. in this case it's getting the first item). Next throws an error if we reach the end; hence, we pass a None to its arguement which will give None if there is no next value
		item = next(filter(lambda x : x['name'] == name, items), None)
		return {"item" : item}, 200 if item else 404

	def post(self, name):
		if not next(filter(lambda x: x['name'] == name, items), None):
			data = Item.parser.parse_args()
			item = {'name': name,'price': data['price']}
			items.append(item)
			return item, 201
		# bad request, the client make a request with an invalid name (it's already in use)
		return {'message': 'item already exists'}, 400

	def delete(self, name):
		global items # specify the items variable in this block is not the local items we defined, but the global items list
		items = [item for item in items if item['name'] != name]
		return {'message': 'Item is deleted'}

	def put(self, name):
		data = Item.parser.parse_args()
		for item in items:
			if item['name'] == name:
				item['price'] = data['price']
				return {'item' : item}
		new_item = {
			"name": name,
			"price": data['price']
		}
		items.append(new_item)
		return {'item': new_item}

# ItemList Resource
class ItemList(Resource):
	def get(self):
		return {'items': items}


# tells our api that the Student Resource is accessible via our api.
api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:5000/student/some_name
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

app.run(port=5000, debug=True)