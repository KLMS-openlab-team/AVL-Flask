import mysql.connector
from configparser import ConfigParser
config = ConfigParser()


config.read('config.ini')
mydb = mysql.connector.connect(
  host=config.get('main','host'),
  user=config.get('main','user'),
  password=config.get('main','password'),
  database=config.get('main','database'),
  autocommit=True
)

cursor = mydb.cursor()

# mycursor.execute("select * from a")

# myresult = mycursor.fetchall()
