# db=__import__('db')

# db.cursor.execute("select * from a")

# myresult = db.cursor.fetchall()

# for i in myresult:
# 	print(i)

import bcrypt

org='admin2'.encode('utf-8')
tmp=bcrypt.hashpw(org,bcrypt.gensalt(12))
print(tmp.decode())

print(bcrypt.checkpw('user1'.encode('utf-8'),'$2b$12$TbHvUtoM1psc9LxbYDCc7OAgkAnMDioH.QXljlj9HgsIg42EnPVWS'.encode()))
from datetime import datetime
my_date = datetime.now()
print(my_date)