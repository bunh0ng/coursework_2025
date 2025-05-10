import psycopg2
from config import database_settings



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
            
        # Получаем названия столбцов
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
    cur.execute(f"""
        DELETE FROM {table}
        WHERE {table}_id = {id}
    """)
    conn.commit()
    cur.close()
    conn.close()

#Вставки

def insert_into_employee(data: str):
    values = data.split("\n")
    if len(values) != 4:
        raise ValueError("Формат:\nФИО\nдолжность\nдата найма (ДД.ММ.ГГГГ)\nвозраст")
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

def insert_into_invoice(data: str):
    values = data.split("\n")
    if len(values) != 4:
        raise ValueError("Формат:\nдата (ДД.ММ.ГГГГ ЧЧ.ММ.СС)\nid покупателя\nid сотрудника\nстатус оплаты")
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
        raise ValueError("Формат:\nid накладной\nid детали\nколичество")
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
        raise ValueError("Формат:\nматериал\nвес\nцена\nid типа\nколичество на складе\nid поставщика\nминимальный уровень запаса")
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
        raise ValueError("Формат:\nназвание\nописание")
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
        raise ValueError("Формат:\nназвание\nтелефон\nпочта")
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
        raise ValueError("Формат:\nназвание\nгород\nтелефон\nпочта")
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
        WITH EmployeeSales AS (
            SELECT
                e.second_name || ' ' || e.first_name || ' ' || e.last_name AS полное_имя,
                (SELECT COUNT(*) FROM Invoice WHERE employee_id = e.employee_id) AS всего_накладных,
                ROUND((SELECT SUM(total_amount) FROM Invoice WHERE employee_id = e.employee_id), 2) AS всего_заработано
            FROM Employee e
        )
        SELECT 
            полное_имя,
            всего_накладных,
            ROUND(всего_заработано / NULLIF(всего_накладных, 0), 2) AS средний_чек,
            всего_заработано
        FROM EmployeeSales
        ORDER BY всего_заработано DESC
        LIMIT 10
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

def most_useless_employees():
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
        ORDER BY число_накладных ASC
        LIMIT 10
    """)
    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return colnames, rows

def get_sales_dynamics():
    """Возвращает данные для графика продаж по месяцам"""
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


def get_payment_status_stats():
    """Возвращает статистику по статусам оплат"""
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
    if len(values) != 2:
        raise ValueError("Формат: дата начала\nдата конца\nФормат даты: ДД.ММ.ГГГГ")
    values = [date_transform(i) for i in values]
    if values[0] > values[1]:
        raise ValueError("Дата начала не может быть позже даты окончания")
    conn = get_connection()
    cur = conn.cursor()
    if values[0] < "2020-05-11" or values[1] < "2020-05-11":
        raise ValueError("База содержит накладные только с 11.05.2020")
    if values[0] > str(datetime.now()).split()[0] or values[1] > str(datetime.now()).split()[0]:
        raise ValueError("Нельзя посмотреть накладные из будущего")
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

