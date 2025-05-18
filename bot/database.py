import psycopg2
from config import database_settings
from re import match
from datetime import datetime

def datetime_transform(date: str):
    return f'{date[6:10]}-{date[3:5]}-{date[0:2]}T{date[11:13]}:{date[14:16]}:{date[17:19]}'

def date_transform(date: str):
    return f'{date[6:10]}-{date[3:5]}-{date[0:2]}'

def get_connection():
    return psycopg2.connect(**database_settings)

# Поиск

def search_by_id(table_name, record_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT * FROM {table_name} WHERE {table_name.lower()}_id = %s", (record_id,))
        rows = cur.fetchall()

        if not rows:
            return None
            
        colnames = [desc[0] for desc in cur.description]
        return colnames, rows
    finally:
        cur.close()
        conn.close()

def search_by_content(table_name, search_text):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(f"""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = %s 
            AND data_type IN ('character varying', 'text', 'varchar')
        """, (table_name.lower(),))
        text_columns = [row[0] for row in cur.fetchall()]
        if not text_columns:
            return None
        conditions = " OR ".join([f"{col} ILIKE %s" for col in text_columns])   
        cur.execute(f"""
            SELECT * FROM {table_name}
            WHERE {conditions}
            LIMIT 50
        """, [f"%{search_text}%"]*len(text_columns))
        rows = cur.fetchall()
        if not rows:
            return None
        colnames = [desc[0] for desc in cur.description]
        return colnames, rows
    finally:
        cur.close()
        conn.close()

# Удаление

def delete_from_database(table: str, id: int):
    conn = get_connection()
    cur = conn.cursor()
    if id <= 0:
        raise ValueError("ID должен быть положительным числом")
    cur.execute(f"""
        SELECT MAX({table}_id) FROM {table}
    """)
    max_id = cur.fetchone()[0]
    if id > max_id:
        raise ValueError(f"Максимальный ID в таблице {table} - {max_id}")
    cur.execute(f"""
        SELECT COUNT(*) FROM {table}
        WHERE {table}_id = %s
    """, (id,))
    if cur.fetchone()[0] == 0:
        raise ValueError(f"Запись с ID {id} не найдена в таблице {table}")
   
    cur.execute("""
        SELECT conrelid::regclass AS table_name, 
               a.attname AS column_name
        FROM pg_constraint c
        JOIN pg_attribute a ON a.attnum = ANY(c.conkey) AND a.attrelid = c.conrelid
        WHERE confrelid = %s::regclass
        AND c.contype = 'f'
    """, (table,))
    foreign_tables = cur.fetchall()
    for fk_table, fk_column in foreign_tables:
        cur.execute(f"""
            SELECT 1 FROM {fk_table} 
            WHERE {fk_column} = %s 
            LIMIT 1
        """, (id,))
        if cur.fetchone():
            raise ValueError(f"Нельзя удалить: есть связанные записи в таблице {fk_table}")
    cur.execute(f"""
        DELETE FROM {table}
        WHERE {table}_id = %s
    """, (id,))
    conn.commit()
    cur.close()
    conn.close()

#Вставки

def insert_into_employee(data: str):
    values = data.split("\n")
    if len(values) != 4:
        raise ValueError("Ошибка формата:\nФИО\nдолжность\nдата найма (ДД.ММ.ГГГГ)\nвозраст")
    name = values[0].split()
    values.pop(0)
    values.insert(0, name[2])
    values.insert(0, name[1])
    values.insert(0, name[0])
    conn = get_connection()
    cur = conn.cursor()
    values[4] = date_transform(values[4])
    cur.execute("""
        INSERT INTO employee (first_name, second_name, last_name, position, hire_date, age)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, values)
    conn.commit()
    cur.close()
    conn.close()
    print(values)

def insert_into_payment(data: str):
    values = data.split("\n")
    if len(values) != 4:
        raise ValueError("Ошибка формата:\nid накладной\nдата и время платежа (ДД.ММ.ГГГГ ЧЧ.ММ.СС\nсумма платежа\nтип оплаты (Наличный расчет, Безналичный расчет)")
    conn = get_connection()
    cur = conn.cursor()
    values[1] = datetime_transform(values[1])
    if datetime.strptime(values[1], "%Y-%m-%dT%H:%M:%S") > datetime.now():
        raise ValueError("Нельзя добавлять платежи в будущее")
    cur.execute("SELECT invoice_id FROM Invoice WHERE invoice_id = %s", (values[0],))
    if not cur.fetchone():
        raise ValueError(f"Накладная с ID {values[0]} не найдена")
    cur.execute("""
        INSERT INTO payment (invoice_id, payment_date, amount, payment_method)
        VALUES (%s, %s, %s, %s)
    """, values)
    conn.commit()
    cur.close()
    conn.close()
    print(values)    

def insert_into_invoice(data: str):
    values = data.split("\n")
    if len(values) != 4:
        raise ValueError("Ошибка формата:\nдата и время оформления(ДД.ММ.ГГГГ ЧЧ.ММ.СС)\nid покупателя\nid сотрудника\nстатус оплаты (Оплачено, Не оплачено, Частично оплачено)")
    conn = get_connection()
    cur = conn.cursor()
    values[0] = datetime_transform(values[0])
    cur.execute("SELECT customer_id FROM Customer WHERE customer_id = %s", (values[1],))
    if not cur.fetchone():
        raise ValueError(f"Покупатель с ID {values[1]} не найден")
    cur.execute("SELECT employee_id FROM Employee WHERE employee_id = %s", (values[2],))
    if not cur.fetchone():
        raise ValueError(f"Сотрудник с ID {values[2]} не найден")
    values.insert(1, 0)
    cur.execute("""
        INSERT INTO invoice (invoice_date, total_amount, customer_id, employee_id, payment_status)
        VALUES (%s, %s, %s, %s, %s)
    """, values)
    conn.commit()
    cur.close()
    conn.close()
    print(values)

def insert_into_invoiceline(data: str):
    values = data.split("\n")
    if len(values) != 3:
        raise ValueError("Ошибка формата:\nid накладной\nid детали\nколичество")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT invoice_id FROM invoice WHERE invoice_id = %s", (values[0],))
    if not cur.fetchone():
        raise ValueError(f"Накладная с ID {values[0]} не найдена")
    cur.execute("SELECT part_id FROM Part WHERE part_id = %s", (values[1],))
    if not cur.fetchone():
        raise ValueError(f"Деталь с ID {values[1]} не найдена")
    cur.execute("SELECT price FROM Part WHERE part_id = %s", (values[1],))
    result = cur.fetchone()
    values.append(result[0])
    values.append(float(values[3]) * int(values[2]))
    cur.execute("""
        INSERT INTO invoiceline (invoice_id, part_id, quantity, unit_price, line_total)
        VALUES (%s, %s, %s, %s, %s)
    """, values)
    conn.commit()
    cur.close()
    conn.close()
    print(values)

def insert_into_part(data: str):
    values = data.split("\n")
    if len(values) != 7:
        raise ValueError("Ошибка формата:\nматериал\nвес\nцена\nid типа\nколичество на складе\nid поставщика\nминимальный уровень запаса")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT parttype_id FROM PartType WHERE parttype_id = %s", (values[3],))
    if not cur.fetchone():
        raise ValueError(f"Тип детали с ID {values[3]} не найден")
    cur.execute("SELECT supplier_id FROM Supplier WHERE supplier_id = %s", (values[5],))
    if not cur.fetchone():
        raise ValueError(f"Поставщик с ID {values[5]} не найден")
    if values[4] < values[6]:
        values.append('true')
    else:
        values.append('false')
    cur.execute("""
        INSERT INTO part (material, weight, price, parttype_id, quantity_in_stock, supplier_id, min_stock_level, is_active)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, values)
    conn.commit()
    cur.close()
    conn.close()
    print(values)

def insert_into_partttype(data: str):
    values = data.split("\n")
    if len(values) != 2:
        raise ValueError("Ошибка формата:\nназвание\nописание")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO parttype (type_name, description)
        VALUES (%s, %s)
    """, values)
    conn.commit()
    cur.close()
    conn.close()
    print(values)

def insert_into_supplier(data: str):
    values = data.split("\n")
    if len(values) != 3:
        raise ValueError("Ошибка формата:\nназвание\nтелефон\nпочта")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO supplier (supplier_name, contact_phone, email)
        VALUES (%s, %s, %s)
    """, values)
    conn.commit()
    cur.close()
    conn.close()
    print(values)

def insert_into_customer(data: str):
    values = data.split("\n")
    if len(values) != 4:
        raise ValueError("Ошибка формата:\nназвание\nгород\nтелефон\nпочта")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO customer (customer_name, city, contact_phone, email)
        VALUES (%s, %s, %s, %s)
    """, values)
    conn.commit()
    cur.close()
    conn.close()
    print(values)

# Запросы

def check_fill():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            part_id, 
            material, 
            quantity_in_stock,
            min_stock_level
        FROM Part
        WHERE quantity_in_stock < min_stock_level
        ORDER BY min_stock_level - quantity_in_stock DESC
        LIMIT 10
    """)
    if not cur.fetchone():
        raise ValueError("Ничего пополнять не нужно")
    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return colnames, rows

def check_full_fill():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            part_id, 
            material, 
            quantity_in_stock,
            min_stock_level
        FROM Part
        WHERE quantity_in_stock < min_stock_level
        ORDER BY min_stock_level - quantity_in_stock DESC
    """)
    if not cur.fetchone():
        raise ValueError("Ничего пополнять не нужно")
    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return colnames, rows

def all_most_valuable_customers():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT customer_id,
            (SELECT customer_name FROM Customer c WHERE c.customer_id = Invoice.customer_id) AS customer,
            COUNT(*) AS sold
        FROM Invoice
        WHERE invoice_date >= current_date - INTERVAL '1 month'
        GROUP BY customer_id
        ORDER BY sold DESC
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
        SELECT customer_id,
            (SELECT customer_name FROM Customer c WHERE c.customer_id = Invoice.customer_id) AS customer,
            COUNT(*) AS sold
        FROM Invoice
        WHERE invoice_date >= current_date - INTERVAL '1 month'
        GROUP BY customer_id
        ORDER BY sold DESC
        LIMIT 10
    """)
    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return colnames, rows

def most_sold_parts500():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            l.part_id,
            (SELECT p.material FROM Part p WHERE p.part_id = l.part_id),
            (SELECT type_name 
            FROM PartType pt 
            WHERE pt.parttype_id = (
                SELECT parttype_id FROM Part p WHERE p.part_id = l.part_id
            )),
            SUM(l.line_total) AS summ
        FROM InvoiceLine l
        GROUP BY l.part_id
        ORDER BY summ DESC
        LIMIT 500
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
            l.part_id,
            (SELECT p.material FROM Part p WHERE p.part_id = l.part_id),
            (SELECT type_name 
            FROM PartType pt 
            WHERE pt.parttype_id = (
                SELECT parttype_id FROM Part p WHERE p.part_id = l.part_id
            )),
            SUM(l.line_total) AS summ
        FROM InvoiceLine l
        GROUP BY l.part_id
        ORDER BY summ DESC
        LIMIT 10
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
        WITH EmployeeSales AS (
            SELECT
                e.second_name || ' ' || e.first_name || ' ' || e.last_name AS full_name,
                (SELECT COUNT(*) FROM Invoice WHERE employee_id = e.employee_id) AS invoices_total,
                ROUND((SELECT SUM(total_amount) FROM Invoice WHERE employee_id = e.employee_id), 2) AS total_amount 
            FROM Employee e
        )
        SELECT 
            full_name,
            invoices_total,
            ROUND(total_amount / NULLIF(invoices_total, 0), 2) AS average,
            total_amount
        FROM EmployeeSales
        ORDER BY total_amount DESC
        LIMIT 10
    """)
    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return colnames, rows

def all_most_valuable_employees():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        WITH EmployeeSales AS (
            SELECT
                e.second_name || ' ' || e.first_name || ' ' || e.last_name AS full_name,
                (SELECT COUNT(*) FROM Invoice WHERE employee_id = e.employee_id) AS invoices_total,
                ROUND((SELECT SUM(total_amount) FROM Invoice WHERE employee_id = e.employee_id), 2) AS total_amount
            FROM Employee e
        )
        SELECT 
            full_name,
            invoices_total,
            ROUND(total_amount / NULLIF(invoices_total, 0), 2) AS average,
            total_amount
        FROM EmployeeSales
        ORDER BY total_amount DESC
    """)
    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return colnames, rows

def all_most_due():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            i.customer_id,
            (SELECT customer_name || ', ' || city FROM Customer c WHERE c.customer_id = i.customer_id) AS customer_name,
            COUNT(*) AS invoice_count,
            SUM(i.total_amount) AS total_billed,
            SUM(COALESCE((
                SELECT SUM(p.amount)
                FROM Payment p
                WHERE p.invoice_id = i.invoice_id
            ), 0)) AS total_paid,
            SUM(i.total_amount - COALESCE((
                SELECT SUM(p.amount)
                FROM Payment p
                WHERE p.invoice_id = i.invoice_id
            ), 0)) AS total_due
        FROM Invoice i
        GROUP BY i.customer_id
        HAVING SUM(i.total_amount - COALESCE((
            SELECT SUM(p.amount)
            FROM Payment p
            WHERE p.invoice_id = i.invoice_id
        ), 0)) > 0
        ORDER BY total_due DESC
    """)
    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return colnames, rows

def most_due():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            i.customer_id,
            (SELECT customer_name || ', ' || city FROM Customer c WHERE c.customer_id = i.customer_id) AS customer_name,
            COUNT(*) AS invoice_count,
            SUM(i.total_amount) AS total_billed,
            SUM(COALESCE((
                SELECT SUM(p.amount)
                FROM Payment p
                WHERE p.invoice_id = i.invoice_id
            ), 0)) AS total_paid,
            SUM(i.total_amount - COALESCE((
                SELECT SUM(p.amount)
                FROM Payment p
                WHERE p.invoice_id = i.invoice_id
            ), 0)) AS total_due
        FROM Invoice i
        GROUP BY i.customer_id
        HAVING SUM(i.total_amount - COALESCE((
            SELECT SUM(p.amount)
            FROM Payment p
            WHERE p.invoice_id = i.invoice_id
        ), 0)) > 0
        ORDER BY total_due DESC
        LIMIT 10
    """)
    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return colnames, rows


def get_sales_dynamics():
    query = """
        SELECT 
            TO_CHAR(invoice_date, 'YYYY-MM') AS month,
            SUM(total_amount) AS total_sales
        FROM Invoice
        GROUP BY month
        ORDER BY month DESC
        LIMIT 12
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()

def get_payments_vs_debts():
    query = """
        SELECT 
            (SELECT customer_name FROM Customer c WHERE c.customer_id = i.customer_id) AS customer_name,
            SUM(COALESCE((
                SELECT SUM(p.amount)
                FROM Payment p
                WHERE p.invoice_id = i.invoice_id
            ), 0)) AS total_paid,
            SUM(i.total_amount - COALESCE((
                SELECT SUM(p.amount)
                FROM Payment p
                WHERE p.invoice_id = i.invoice_id
            ), 0)) AS total_due
        FROM Invoice i
        GROUP BY i.customer_id
        HAVING SUM(i.total_amount) > 0
        ORDER BY SUM(i.total_amount) DESC
        LIMIT 10
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()

def get_payment_status_stats():
    query = """
        SELECT 
            payment_status,
            COUNT(*) AS status_count,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Invoice), 2) AS percentage
        FROM Invoice
        GROUP BY payment_status
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()

def invoices_for_period(data: str):
    from datetime import datetime
    values = data.split("\n")
    if len(values) != 2 or not match(r"^\d{2}\.\d{2}\.\d{4}$", values[0]) or not match(r"^\d{2}\.\d{2}\.\d{4}$", values[1]):
        raise ValueError("Ошибка формата:\nдата начала (ДД.ММ.ГГГГ)\nдата конца (ДД.ММ.ГГГГ)")
    values = [date_transform(i) for i in values]
    if values[0] > values[1]:
        raise ValueError("Дата начала не может быть позже даты окончания")
    conn = get_connection()
    cur = conn.cursor()
    if datetime.strptime(values[0], "%Y-%m-%d") < datetime.strptime("2020-05-11", "%Y-%m-%d") or datetime.strptime(values[1], "%Y-%m-%d") < datetime.strptime("2020-05-11", "%Y-%m-%d"):
        raise ValueError("База содержит накладные только с 11.05.2020")
    if datetime.strptime(values[0], "%Y-%m-%d") > datetime.now() or datetime.strptime(values[1], "%Y-%m-%d") > datetime.now():
        raise ValueError("Нельзя посмотреть накладные из будущего")
    cur.execute("""
        SELECT 
            i.invoice_id,
            i.invoice_date,
            (SELECT customer_name || ', ' || city FROM Customer c WHERE c.customer_id = i.customer_id) AS company_name,
            i.total_amount,
            i.payment_status
        FROM Invoice i
        WHERE invoice_date BETWEEN %s AND %s
        ORDER BY invoice_date
        LIMIT 10
    """, values)
    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return colnames, rows

def all_invoices_for_period(data: str):
    from datetime import datetime
    values = data.split("\n")
    if len(values) != 2 or not match(r"^\d{2}\.\d{2}\.\d{4}$", values[0]) or not match(r"^\d{2}\.\d{2}\.\d{4}$", values[1]):
        raise ValueError("Ошибка формата:\nдата начала (ДД.ММ.ГГГГ)\nдата конца (ДД.ММ.ГГГГ)")
    values = [date_transform(i) for i in values]
    if values[0] > values[1]:
        raise ValueError("Дата начала не может быть позже даты окончания")
    conn = get_connection()
    cur = conn.cursor()
    if datetime.strptime(values[0], "%Y-%m-%d") < datetime.strptime("2020-05-11", "%Y-%m-%d") or datetime.strptime(values[1], "%Y-%m-%d") < datetime.strptime("2020-05-11", "%Y-%m-%d"):
        raise ValueError("База содержит накладные только с 11.05.2020")
    if datetime.strptime(values[0], "%Y-%m-%d") > datetime.now() or datetime.strptime(values[1], "%Y-%m-%d") > datetime.now():
        raise ValueError("Нельзя посмотреть накладные из будущего")
    cur.execute("""
        SELECT 
            i.invoice_id,
            i.invoice_date,
            (SELECT customer_name || ', ' || city FROM Customer c WHERE c.customer_id = i.customer_id) AS company_name,
            i.total_amount,
            i.payment_status
        FROM Invoice i
        WHERE invoice_date BETWEEN %s AND %s
        ORDER BY invoice_date;
    """, values)
    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return colnames, rows