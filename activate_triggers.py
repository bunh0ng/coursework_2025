import os
import psycopg2
from bot.config import database_settings

def get_connection():
    return psycopg2.connect(**database_settings)

# Путь к папке с SQL-файлами
sql_folder = './triggers'

# Получаем список файлов в алфавитном порядке
sql_files = sorted(f for f in os.listdir(sql_folder) if f.endswith('.sql'))

# Подключение и выполнение
conn = get_connection()
conn.autocommit = True  # или manage вручную с .commit()

with conn.cursor() as cursor:
    for file in sql_files:
        file_path = os.path.join(sql_folder, file)
        with open(file_path, 'r', encoding='utf-8') as f:
            sql = f.read()
            print(f'Выполняется: {file}')
            try:
                cursor.execute(sql)
            except Exception as e:
                print(e)

conn.close()
print('Все SQL-скрипты выполнены.')
