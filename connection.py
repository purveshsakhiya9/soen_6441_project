import mysql.connector as mysql


class connection:
    mydb = None
    def connect(self):
        host = "localhost"
        user = "root"
        password = "root"
        singleton = True
        if singleton == True:
            try:
                connection.mydb = mysql.connect(host=host, username=user, password=password)
                print("connected to mysql server.")
                try:
                    mycursor = connection.mydb.cursor()
                    mycursor.execute("CREATE DATABASE Car")
                    print("Database Created Successfully")

                except Exception as e:
                    print("Could not create database...database already exists")
                    print("connecting with database")
                connection.mydb = mysql.connect(
                    host="localhost",
                    user="root",
                    password="root",
                    database="Car"
                )
                print("Database connected Successfully.")
            except Exception as e:
                print(e)
            singleton = False
            return connection.mydb
        else:
            return connection.mydb