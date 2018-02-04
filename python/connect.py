#!/usr/bin/python
import mysql.connector as mariadb

def init():
	global mariadb_connection
	global cursor
	mariadb_connection = mariadb.connect(user='root', password='root')
	mariadb_connection.database = 'tg'  
	cursor = mariadb_connection.cursor(buffered=True)

def first():
	DB_NAME = 'tg'

	TABLES = {}

	TABLES['users'] = (
	    "CREATE TABLE `users` ("
	    "  `id` int NOT NULL AUTO_INCREMENT,"
	    "  `name` varchar(14) NOT NULL,"
	    "  PRIMARY KEY (`id`))")

	try:
	    mariadb_connection.database = DB_NAME  
	except mariadb.Error as err:
	    if err.errno == errorcode.ER_BAD_DB_ERROR:
	        create_database(cursor)
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
	cursor.close()

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mariadb.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

def insert_user(name):
	try:
	    cursor.execute('INSERT INTO users (name) VALUES ("%s")'%format(name))
	except mariadb.Error as error:
	    print("Error: {}".format(error))

	mariadb_connection.commit()

def select_users():
	cursor.execute('SELECT * FROM users')
	for name, id in cursor:
	    print("Name: {}, id: {}").format(name,id)

def select_user(name):
	cursor.execute('SELECT * FROM users WHERE name = "%s"'%format(name))
	for name, id in cursor:
	    print("Name: {}, id: {}").format(name,id)

init()
name = 'maria'
# insert_user(name)
select_user(name)

quit()