import psycopg2
from config import database_settings

def get_connection():
    return psycopg2.connect(**database_settings)

def delete_from_database(table: str, id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"""
        DELETE FROM {table}
        WHERE {table}_id = {id}
    """)
    conn.commit()
    cur.close()
    conn.close()

def insert_into_employee(data: str):
    values = data.split(",")
    if len(values) != 4:
        raise ValueError("Формат: имя, фамилия, должность, дата")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO employee (first_name, last_name, position, hire_date)
        VALUES (%s, %s, %s, %s)
    """, values)
    conn.commit()
    cur.close()
    conn.close()

def insert_into_invoice(data: str):
    values = data.split(",")
    if len(values) != 5:
        raise ValueError("Формат: дата, количесвто, id покупателя, id сотрудника, статус оплаты")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO invoice (invoice_date, total_amount, customer_id, employee_id, payment_status)
        VALUES (%s, %s, %s, %s, %s)
    """, values)
    conn.commit()
    cur.close()
    conn.close()

def insert_into_invoiceline(data: str):
    values = data.split(",")
    if len(values) != 5:
        raise ValueError("Формат: id накладной, id детали, количество, цена за единицу, сумма")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO invoiceline (invoice_id, part_id, quantity, unit_price, line_total)
        VALUES (%s, %s, %s, %s, %s)
    """, values)
    conn.commit()
    cur.close()
    conn.close()

def insert_into_part(data: str):
    values = data.split(",")
    if len(values) != 8:
        raise ValueError("Формат: материал, вес, цена, id типа, количество на складе, id поставщика, минимальный уровень запаса, в продаже")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO part (material, weight, price, parttype_id, quantity_in_stock, supplier_id, min_stock_level, is_active)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, values)
    conn.commit()
    cur.close()
    conn.close()

def insert_into_partttype(data: str):
    values = data.split(",")
    if len(values) != 2:
        raise ValueError("Формат: название, описание")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO part (type_name, description)
        VALUES (%s, %s)
    """, values)
    conn.commit()
    cur.close()
    conn.close()

def insert_into_supplier(data: str):
    values = data.split(",")
    if len(values) != 3:
        raise ValueError("Формат: название, телефон, рейтинг надежности")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO part (supplier_name, phone, reliability_rating)
        VALUES (%s, %s, %s)
    """, values)
    conn.commit()
    cur.close()
    conn.close()

def insert_into_customer(data: str):
    values = data.split(",")
    if len(values) != 4:
        raise ValueError("Формат: название, город, телефон, скидка")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO part (customer_name, city, contact_phone, discount_percent)
        VALUES (%s, %s, %s, %s)
    """, values)
    conn.commit()
    cur.close()
    conn.close()

def check_fill():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT part_id, material, quantity_in_stock, min_stock_level
        FROM Part
        WHERE quantity_in_stock < min_stock_level
        ORDER BY min_stock_level - quantity_in_stock DESC
        LIMIT 50
    """)
    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return colnames, rows













'''
DO $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN 
        SELECT t.relname AS table_name, 
               a.attname AS column_name,
               s.relname AS sequence_name
        FROM pg_class s
        JOIN pg_depend d ON d.objid = s.oid
        JOIN pg_class t ON d.refobjid = t.oid
        JOIN pg_attribute a ON (d.refobjid, d.refobjsubid) = (a.attrelid, a.attnum)
        WHERE s.relkind = 'S' AND t.relkind = 'r'
    LOOP
        EXECUTE format('SELECT setval(%L, COALESCE((SELECT MAX(%I) FROM %I), 1))', 
                      r.sequence_name, r.column_name, r.table_name);
    END LOOP;
END $$;
'''