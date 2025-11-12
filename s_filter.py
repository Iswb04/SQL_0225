import sqlite3
from s_main import DB_FILE, TABLE_NAME

connection = sqlite3.connect(DB_FILE)
cursor = connection.cursor()

cursor.execute(
    f'''SELECT NAME,AGE FROM {TABLE_NAME} 
    WHERE AGE >= 18 AND AGE <= 50'''
) 


rows = cursor.fetchall() 
if not rows:
    print('Nenhum registro encontrado!')
else:
    for row in rows: # row = linha
        print(row)

cursor.close()
connection.close()


