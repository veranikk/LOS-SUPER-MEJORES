import sqlite3

conn = sqlite3.connect('BBDD-SQLITE.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tablas = cursor.fetchall()

print("Tablas en la base de datos:")
for tabla in tablas:
    print(tabla[0])

conn.close()
