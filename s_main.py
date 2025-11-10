import sqlite3
from pathlib import Path

ROOT_DIR = Path(__file__).parent
DB_NAME = 'db.sqlite3'
DB_FILE = ROOT_DIR / DB_NAME
TABLE_NAME = 'customers'

if __name__ == '__main__': 
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()


    cursor.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER
        )
        '''
    )
    connection.commit()


    sql_costumers = (    
        f'''
        INSERT INTO {TABLE_NAME} (name, age)
        VALUES
            (?,?)''' #binding para previnir sql injection
    )

    dados =[
        ("Jorge", 15),
        ("Elson", 45),
        ("Deyvidson", 24),
        ("Chica", 78)
    ]

    cursor.executemany(sql_costumers, dados)
    connection.commit()


    cursor.close()
    connection.close()


