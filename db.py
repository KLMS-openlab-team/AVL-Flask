import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="12345678",
  database="avl_flask",
  autocommit=True
)

cursor = mydb.cursor()

# mycursor.execute("select * from a")

# myresult = mycursor.fetchall()
