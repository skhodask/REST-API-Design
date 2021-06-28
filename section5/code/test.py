# demo

# 
import sqlite3

# init a connection
connection = sqlite3.connect('data.db') # data.db will be a file created in our current directory

# responsible for executing the query and access the result
cursor = connection.cursor()

# create a table query with users, which has 3 columns and the specified type
create_table = "CREATE TABLE users (id int, username text, password text)"

# run the query
cursor.execute(create_table)

# create user object
user = (1, 'neal', 'abc')

# insert many users into the database
users = [
	(1, 'neal', 'abc'),
	(2, 'tom', 'xyz'),
	(3, 'jerry', '123')
]

# insert query where the cursor is smart enough to know to replace the user's values with the "?"
insert_query = "INSERT INTO users VALUES (?, ?, ?)"

# pass both insert_query and the single object to the cursor
# cursor.execute(insert_query, user)

# pass the insert_query and multiple objects to the cursor
cursor.executemany(insert_query, users)


# retrieve data from query
select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
	print(row)


# whenever we insert data, we have to tell the database to save the changes to the disk
connection.commit()

# close the connection
connection.close()