import psycopg2
from config import database_settings

def get_connection():
    return psycopg2.connect(**database_settings)

def insert_into_employee(data: str):
    values = data.split(",")
    if len(values) != 4:
        raise ValueError("Формат: имя,фамилия,должность,дата")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO employee (first_name, last_name, position, hire_date)
        VALUES (%s, %s, %s, %s)
    """, values)

    conn.commit()
    cur.close()
    conn.close()