import psycopg2
from config import database_settings

def get_connection():
    return psycopg2.connect(**database_settings)

#Удаление

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

#Вставки

def insert_into_employee(data: str):
    values = data.split(",")
    if len(values) != 6:
        raise ValueError("Формат: имя,фамилия,отчество,должность,дата найма,возраст\nФормат даты: ГГГГ-ММ-ДД")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO employee (first_name, second_name, last_name, position, hire_date, age)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, values)
    conn.commit()
    cur.close()
    conn.close()

def insert_into_invoice(data: str):
    values = data.split(",")
    if len(values) != 5:
        raise ValueError("Формат: дата,количесвто,id покупателя,id сотрудника,статус оплаты\nФормат даты: ГГГГ-ММ-ДД ЧЧ:ММ:СС")
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
        raise ValueError("Формат: id накладной,id детали,количество,цена за единицу,сумма")
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
        raise ValueError("Формат: материал,вес,цена,id типа,количество на складе,id поставщика,минимальный уровень запаса,в продаже")
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
        raise ValueError("Формат: название,описание")
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
    if len(values) != 4:
        raise ValueError("Формат: название,телефон,рейтинг надежности,почта")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO part (supplier_name, contact_phone, reliability_rating, email)
        VALUES (%s, %s, %s, %s)
    """, values)
    conn.commit()
    cur.close()
    conn.close()

def insert_into_customer(data: str):
    values = data.split(",")
    if len(values) != 5:
        raise ValueError("Формат: название,город,телефон,скидка,почта")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO part (customer_name, city, contact_phone, discount_percent, email)
        VALUES (%s, %s, %s, %s, %s)
    """, values)
    conn.commit()
    cur.close()
    conn.close()

# Запросы

def check_fill():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            part_id AS id_детали, 
            material AS материал, 
            quantity_in_stock AS запасы_на_складе,
            min_stock_level AS минимальный_уровень
        FROM Part
        WHERE quantity_in_stock < min_stock_level
        ORDER BY min_stock_level - quantity_in_stock DESC
        LIMIT 30
    """)
    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return colnames, rows

def most_valuable_customers():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT customer_id AS id_поставщика,
            (SELECT customer_name FROM Customer WHERE Customer.customer_id = Invoice.customer_id) AS название,
            COUNT(*) AS продажи
        FROM Invoice
        WHERE invoice_date >= current_date - INTERVAL '1 month'
        GROUP BY id_поставщика
        ORDER BY продажи DESC
        LIMIT 50
    """)
    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return colnames, rows

def most_sold_parts():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            l.part_id AS id_детали,
            (SELECT p.material FROM Part p WHERE p.part_id = l.part_id) AS материал,
            (SELECT type_name 
            FROM PartType pt 
            WHERE pt.parttype_id = (
                SELECT parttype_id FROM Part p WHERE p.part_id = l.part_id
            )) AS название_типа,
            SUM(l.line_total) AS сумма
        FROM InvoiceLine l
        GROUP BY l.part_id
        ORDER BY сумма DESC
        LIMIT 50
    """)
    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return colnames, rows

def most_valuable_employee():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            employee_id AS id_сотрудника,
            (SELECT second_name || ' ' || first_name || ' ' || last_name FROM Employee e WHERE e.employee_id = i.employee_id) AS полное_имя,
            COUNT(*) AS число_накладных
        FROM Invoice i
        WHERE invoice_date >= CURRENT_DATE - INTERVAL '1 month'
        GROUP BY id_сотрудника
        ORDER BY число_накладных DESC
        LIMIT 5
    """)
    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return colnames, rows

def most_active_suppliers():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            supplier_id AS id_поставщика,
            (SELECT supplier_name FROM Supplier s WHERE s.supplier_id = p.supplier_id) AS название,
            SUM(quantity_in_stock) AS всего_поставлено
        FROM Part p
        GROUP BY id_поставщика
        ORDER BY всего_поставлено ASC
        LIMIT 50
    """)
    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return colnames, rows

def invoices_for_period(data: str):
    values = data.split(",")
    if len(values) != 2:
        raise ValueError("Формат: дата начала,дата конца\nФормат даты: ГГГГ-ММ-ДД")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            i.invoice_id AS id_накладной,
            i.invoice_date AS дата_оформления,
            (SELECT customer_name || ', ' || city FROM Customer c WHERE c.customer_id = i.customer_id) AS компания_покупатель,
            i.total_amount AS общая_стоимость,
            i.payment_status AS статус_оплаты
        FROM Invoice i
        WHERE invoice_date BETWEEN %s AND %s
        ORDER BY invoice_date;
    """, values)
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