import mysql.connector as mysql


mydb = mysql.connect(
  host="localhost",
  user="root",
  password="root"
)
mycursor = mydb.cursor()

try:
  mycursor.execute("CREATE DATABASE Car")
  print("Database Created Successfully")
except Exception as e:
  print("Could not connect with database...database already exists")
  print("connecting with database")
  mydb = mysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="Car"
  )


