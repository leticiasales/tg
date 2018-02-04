#!/usr/bin/python
import json
import mysql.connector as mariadb
from mysql.connector import errorcode

def init():
	global mariadb_connection
	global cursor
	mariadb_connection = mariadb.connect(user='root', password='root')
	cursor = mariadb_connection.cursor(buffered=True)

	DB_NAME = 'tg'

	TABLES = {}

	TABLES['users'] = (
	    "CREATE TABLE `users` ("
	    " `user_id` int PRIMARY KEY AUTO_INCREMENT,"
	    " `name` varchar(255) NOT NULL)")

	TABLES['data'] = (
	    "CREATE TABLE `data` ("
	    "  `data_id` int PRIMARY KEY AUTO_INCREMENT,"
	    "  `user_id` int NOT NULL,"
	    "  `dict` varchar(255) NOT NULL,"
	    "  `value` varchar(255) NOT NULL)")

	try:
	    mariadb_connection.database = DB_NAME  
	except mariadb.Error as err:
	    if err.errno == errorcode.ER_BAD_DB_ERROR:
	        create_database(DB_NAME)
	        mariadb_connection.database = DB_NAME
	    else:
	        print(err)
	        exit(1)

	for name, ddl in TABLES.iteritems():
	    try:
	        print("Creating table {}: " . format(name))
	        cursor.execute(ddl)
	    except mariadb.Error as err:
	            print(err.msg)
	    else:
	        print("OK")

def quit():
	mariadb_connection.commit()
	cursor.close()

def create_database(DB_NAME):
    try:
        cursor.execute(
            "CREATE DATABASE %s DEFAULT CHARACTER SET 'utf8'"%format(DB_NAME))
    except mariadb.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

def insert_user(name):
	try:
	    cursor.execute('INSERT INTO users (name) VALUES ("%s")'%format(name))
	except mariadb.Error as error:
	    print("Error: {}".format(error))

def insert_data(userid, node):
	for key in node:
		print key
		try:
		    cursor.execute('INSERT INTO data (user_id, dict, value) VALUES (%s,%s,%s)',(userid, key, node[key]))
		except mariadb.Error as error:
		    print("Error: {}".format(error))

def select_users():
	cursor.execute('SELECT * FROM users')

def select_user(name):
	return cursor.execute('SELECT * FROM users WHERE name = "%s"'%format(name))

init()
with open('test.json') as json_data:
    d = json.load(json_data)
    # print(d)

for node in d:
	select_user(node['name'])
	if(cursor.rowcount == 0):
		insert_user(node['name'])
		userid = cursor.lastrowid
	else:
		for user_id, name in cursor:
			userid = id
	insert_data(userid, node)

select_users()
for user_id, name in cursor:
    print("Name: {}, id: {}").format(name, user_id)

quit()