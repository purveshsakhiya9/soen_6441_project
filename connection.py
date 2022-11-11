import mysql.connector as mysql

host="localhost"
user="root"
password="root"

try:
  mydb = mysql.connect(host=host,username=user,password=password)
  print("connected to mysql server.")
  try:
    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE Car")
    print("Database Created Successfully")
  except Exception as e:
    print("Could not connect with database...database already exists")
    print("connecting with database")
    mydb1 = mysql.connect(
      host="localhost",
      user="root",
      password="root",
      database="Car"
    )
except Exception as e:
  print(e)


