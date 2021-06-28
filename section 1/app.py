from flask import Flask, jsonify, request

app = Flask(__name__)

# need to store our stores, normally this is in a database but we will store here for simplification purposes:
stores = [
	{
		'name': 'my store',
		'items': [
			{
				'name': 'my item',
				'price': 15.99
			}	
		]
	},
		{
		'name': 'other store',
		'items': [
			{
				'name': 'other item',
				'price': 10.00
			}	
		]
	}	
]

# define the requests our apps will understand
# define an endpoint via a decorator that has to always act on a function, forward slash is the home page of the application
@app.route('/')
def home():
	return "Hello, world!"

# /store endpoint is only accessible via a POST request
# POST /store data: {name:}
@app.route('/store', methods=['POST'])
def create_store():
	# request.get_json() --> request is the request sent to this end point; .get_json() converts the JSON string to a dictionary object
	request_data = request.get_json()
	new_store = {
		'name': request_data['name'],
		'items': []
	}
	stores.append(new_store)
	return jsonify(new_store)

@app.route('/store/<string:name>') # http://127.0.0.1:5000/store/some_name ; some_name will be name in the function parameter
def get_store(name):
	# iterate over stores, if the store name matches, return it. If none match, return an error message
	for store in stores:
		if store['name'] == name:
			return jsonify(store)
	return jsonify({'message': 'store not found'})

@app.route('/store')
def get_stores():
	# note, we need to do the inner dictionary because JSON cannot be a list, it must be a dictionary.
	return jsonify({'stores': stores})

# POST /store/<string:name>/item {name:, price:}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
	request_data = request.get_json()
	for store in stores:
		if store['name'] == name:
			new_item = {
				"name": request_data['name'],
				"price": request_data['price']
			}
			store['items'].append(new_item)
			return jsonify(store)
	return jsonify({'message':'store not found'})

# GET /store/<string:name>/items
@app.route('/store/<string:name>/item')
def get_item_in_store(name):
	for store in stores:
		if store['name'] == name:
			return jsonify({'items': store['items']})
	return jsonify({'message': 'store not found'})




# run the application and define the port, which is an area on your computer which can handle requests; if an error, some other application is using this port
# 127.0.0.1 is a special ip address that is reserved for your computer. When you access this in the browser, it's accessing your computer.
app.run(port=5000, debug=True)