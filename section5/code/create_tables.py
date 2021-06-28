import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# it doesn't make sense to increment the id manually everytime there is a new user, so we should make it auto increment, which requires type INTEGER and PRIMARY KEY 
create_table_query = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)'
cursor.execute(create_table_query)

connection.commit()
connection.close()
