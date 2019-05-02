import sqlite3

connection = sqlite3.connect("ecommerce.db")

crsr = connection.cursor()

crsr.execute("SELECT * FROM Item")

ans = crsr.fetchall()

for i in ans:
    print(i)

connection.commit()

connection.close()