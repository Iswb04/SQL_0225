import sqlite3
from pathlib import Path

ROOT_DIR = Path(__file__).parent
DB_NAME = 'db.sqlite3'
DB_FILE = ROOT_DIR / DB_NAME
TABLE_NAME = 'customers'

connection = sqlite3.connect(DB_FILE)
cursor = connection.cursor()

cursor.execute(
    f'CREATE TABLE IF NOT EXISTS {TABLE_NAME}'
    '('
    'id INTEGER PRIMARY KEY AUTOINCREMENT,'
    'name TEXT,'
    'age INTEGER'
    ')'
)
connection.commit()


cursor.execute(
    f'INSERT INTO {TABLE_NAME} (id, name, age)'
    'VALUES'
    '(NULL, "Jhonny Emici", 45)'
    '(NULL, "Xamuel Silva", 12)'
)
connection.commit()

cursor.close()
connection.close()


