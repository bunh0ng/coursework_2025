import csv
import random
from datetime import datetime, timedelta
from faker import Faker
from natasha import MorphVocab

m = MorphVocab()
fake = Faker("ru_RU")

# Настройки
NUM_PARTS = 1_000_000 #
NUM_PART_TYPES = 100 #
NUM_SUPPLIERS = 114 #
NUM_CUSTOMERS = 222 #
NUM_EMPLOYEES = 200 #
NUM_INVOICES = 300_000
MAX_INVOICE_LINES = 1_000_000 


# Генерация данных для таблицы Customer (Покупатели)
def generate_customers():
    customers = []
    companies = ['Doosan Heavy Industries', 'Rolls-Royce Holdings', 'General Dynamics', 'Lockheed Martin', 'Boeing', 'Northrop Grumman', 'Raytheon Technologies', 'L3Harris Technologies', 'BAE Systems', 'Safran', 'United Technologies', 'PACCAR', 'Continental AG', 'Magna International', 'Dana Incorporated', 'Aisin Seiki', 'NSK Ltd.', 'Schaeffler Group', 'GKN Automotive', 'Mahle GmbH', 'Tenneco', 'Yazaki Corporation', 'Sumitomo Electric', 'Furukawa Electric', 'Nexans', 'Prysmian Group', 'Legrand', 'Hubbell Incorporated', 'nVent Electric', 'Amphenol', 'TE Connectivity', 'Molex', 'Aptiv', 'Lear Corporation', 'Adient', 'BASF', 'Dow Chemical', 'DuPont', 'LyondellBasell', 'Linde plc', 'Air Liquide', 'Praxair', 'Mitsubishi Chemical', 'Sumitomo Chemical', 'Toray Industries', 'LG Chem', 'Samsung SDI', 'SK Innovation', 'ThyssenKrupp Steel', 'Alcoa', 'Rio Tinto', 'BHP', 'Glencore', 'Freeport-McMoRan', 'Vale S.A.', 'Anglo American', 'Barrick Gold', 'Newmont Corporation', 'Fluor Corporation', 'Bechtel', 'Jacobs Engineering', 'AECOM', 'KBR', 'McDermott International', 'TechnipFMC', 'Saipem', 'Subsea 7', 'Weatherford International', 'NOV (National Oilwell Varco)', 'Mapal', 'Guhring', 'Mitsubishi Materials', 'Sumitomo Electric Hardmetal', 'Kyocera', 'Ceratizit', 'Plansee Group', 'Hitachi Metals', 'Daido Steel', 'Nippon Steel & Sumitomo Metal', 'JFE Steel', 'Kobe Steel', 'Aichi Steel', 'Sanyo Special Steel', 'Ovako', 'Uddeholm', 'Böhler', 'Carpenter Technology', 'Allegheny Technologies', 'Haynes International', 'Special Metals Corporation', 'VDM Metals', 'Outokumpu Stainless', 'Steel Dynamics', 'AK Steel', 'U.S. Steel', 'Cleveland-Cliffs', 'CSN (Companhia Siderúrgica Nacional)', 'Usiminas', 'Ternium', 'Techint Group', 'Tenova', 'Danieli', 'SMS Group', 'Primetals Technologies', 'Andritz', 'Loesche', 'Gebr. Pfeiffer', 'Polysius', 'Claudius Peters', 'Schenck Process', 'Bühler Group', 'GEA Group', 'ITT Inc.', 'Kaeser Kompressoren', 'Hitachi Construction Machinery', 'Kobelco', 'JCB', 'CASE Construction', 'New Holland', 'Terex', 'Manitowoc', 'Tadano', 'Sennebogen', 'Palfinger', 'Haulotte', 'JLG Industries', 'Genie (Terex)', 'Skyjack', 'Manitou Group', 'Doosan Infracore', 'Hyundai Construction Equipment', 'Sany Heavy Industry', 'Zoomlion', 'XCMG', 'Liugong', 'Lonking', 'Shantui', 'SDLG', 'Yutong Heavy Industries', 'Sinotruk', 'FAW', 'Dongfeng Motor', 'Shaanxi Heavy Duty Automobile', 'Beiben Trucks', 'Iveco', 'Volvo Trucks', 'DAF Trucks', 'Renault Trucks', 'Mercedes-Benz Trucks', 'Freightliner', 'Western Star', 'Kenworth', 'Peterbilt', 'Mack Trucks', 'Navistar International', 'Hino Motors', 'Isuzu Motors', 'UD Trucks', 'Fuso', 'Tata Motors', 'Ashok Leyland', 'Eicher Motors', 'Mahindra Truck and Bus', 'Kamaz', 'GAZ Group', 'KAMAZ', 'MAZ', 'KrAZ', 'BelAZ', 'Scania-Vabis', 'Van Hool', 'VDL Groep', 'Daimler Buses', 'Volvo Buses', 'Irizar', 'Solaris Bus & Coach', 'MAN Bus', 'Neoplan', 'Setra', 'Marcopolo', 'Caio Induscar', 'Comil', 'Agrale', 'Tatra', 'Avtotor', 'Sollers', 'UAZ', 'ZIL', 'KAMAZ', 'BAZ', 'ZiL', 'AMO ZIL', 'UralAZ', 'KAvZ', 'PAZ', 'LiAZ', 'NefAZ', 'MAZ', 'BelAZ', 'MoAZ', 'KrAZ', 'LAZ', 'Bogdan', 'Etalon', 'Volkswagen Commercial Vehicles', 'Ford Trucks', 'Iveco Defence Vehicles', 'Oshkosh Corporation', 'Navistar Defense', 'Rheinmetall MAN Military Vehicles', 'BAE Systems Land & Armaments', 'General Dynamics Land Systems', 'Textron Marine & Land Systems', 'Patria', 'Nexter Systems', 'Krauss-Maffei Wegmann', 'Hyundai Rotem', 'Doosan DST', 'Hanwha Defense', 'Norinco', 'Sinomach', 'China North Industries Group']
    cities = ['Чханвон', 'Лондон', 'Рестон', 'Бетесда', 'Чикаго', 'Фолс-Черч', 'Уолтем', 'Мельбурн', 'Лондон', 'Париж', 'Фармингтон', 'Белвью', 'Ганновер', 'Орора', 'Моми', 'Карья', 'Токио', 'Херцогенаурах', 'Реддич', 'Штутгарт', 'Лейк-Форест', 'Токио', 'Осака', 'Токио', 'Париж', 'Милан', 'Лимож', 'Шелтон', 'Лондон', 'Уоллингфорд', 'Шаффхаузен', 'Лайл', 'Дублин', 'Саутфилд', 'Плимут', 'Людвигсхафен', 'Мидленд', 'Уилмингтон', 'Хьюстон', 'Гилфорд', 'Париж', 'Данбери', 'Токио', 'Токио', 'Токио', 'Сеул', 'Сеул', 'Сеул', 'Дуйсбург', 'Питтсбург', 'Мельбурн', 'Мельбурн', 'Баар', 'Финикс', 'Рио-де-Жанейро', 'Лондон', 'Торонто', 'Денвер', 'Ирвинг', 'Рестон', 'Даллас', 'Лос-Анджелес', 'Хьюстон', 'Хьюстон', 'Лондон', 'Сан-Донато-Миланезе', 'Лондон', 'Хьюстон', 'Хьюстон', 'Аален', 'Альбштадт', 'Токио', 'Осака', 'Киото', 'Маммер', 'Ройтте', 'Токио', 'Нагоя', 'Токио', 'Токио', 'Кобе', 'Токай', 'Химэдзи', 'Стокгольм', 'Хагфорс', 'Капфенберг', 'Рединг', 'Питтсбург', 'Кокомо', 'Хантингтон', 'Вердоль', 'Эспоо', 'Форт-Уэйн', 'Уэст-Честер', 'Питтсбург', 'Кливленд', 'Сан-Паулу', 'Белу-Оризонти', 'Сан-Николас-де-лос-Гарса', 'Милан', 'Милан', 'Буттрио', 'Дюссельдорф', 'Лондон', 'Грац', 'Дюссельдорф', 'Кайзерслаутерн', 'Эссен', 'Гамбург', 'Дармштадт', 'Уцвиль', 'Дюссельдорф', 'Уайт-Плейнс', 'Кобург', 'Токио', 'Токио', 'Рочестер', 'Расин', 'Турин', 'Норуолк', 'Манитовок', 'Такамацу', 'Штраубинг', 'Зальцбург', 'Лорм', 'Хейгерстаун', 'Редмонд', 'Гвелф', 'Ансени', 'Сеул', 'Сеул', 'Чанша', 'Чанша', 'Сюйчжоу', 'Лючжоу', 'Шанхай', 'Цзинин', 'Линьи', 'Чжэнчжоу', 'Цзинань', 'Чанчунь', 'Ухань', 'Сиань', 'Чунцин', 'Турин', 'Гетеборг', 'Эйндховен', 'Сен-Приест', 'Штутгарт', 'Портленд', 'Портленд', 'Киркланд', 'Дентон', 'Гринсборо', 'Лайл', 'Токио', 'Токио', 'Агео', 'Кавасаки', 'Мумбаи', 'Ченнаи', 'Гургаон', 'Мумбаи', 'Набережные Челны', 'Нижний Новгород', 'Набережные Челны', 'Минск', 'Кременчуг', 'Жодино', 'Седертелье', 'Конингсхойкт', 'Эйндховен', 'Штутгарт', 'Гетеборг', 'Ормайстеги', 'Болехово', 'Мюнхен', 'Штутгарт', 'Ульм', 'Кашиас-ду-Сул', 'Сан-Паулу', 'Эрешин', 'Кашиас-ду-Сул', 'Копрживнице', 'Калининград', 'Москва', 'Ульяновск', 'Москва', 'Набережные Челны', 'Брянск', 'Москва', 'Москва', 'Миасс', 'Курган', 'Павлово', 'Ликино-Дулево', 'Нефтекамск', 'Минск', 'Жодино', 'Могилев', 'Кременчуг', 'Львов', 'Черкассы', 'Москва', 'Ганновер', 'Стамбул', 'Больцано', 'Ошкош', 'Уоррен', 'Мюнхен', 'Стерлинг-Хайтс', 'Лондон', 'Новый Орлеан', 'Хельсинки', 'Версаль', 'Мюнхен', 'Чханвон', 'Сеул', 'Сеул', 'Пекин', 'Пекин', 'Пекин']
    mailboxes = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'aol.com', 'mail.com', 'protonmail.com', 'zoho.com', 'yandex.ru', 'mail.ru', 'icloud.com', 'gmx.com', 'tutanota.com', 'fastmail.com', 'hushmail.com', 'qq.com', '163.com', 'rediffmail.com', 'sina.com', 'naver.com']
    for i in range(0, NUM_CUSTOMERS):
        customers.append({
            'customer_id': i + 1,
            'customer_name': companies[i],
            'city': cities[i],
            'contact_phone': fake.phone_number(),
            'discount_percent': round(random.uniform(0.0, 0.15), 2),
            'email': f'{companies[i].replace(' ', '').lower()}@{random.choice(mailboxes)}'
        })
    return customers

# Генерация данных для таблицы PartType (Типы деталей)
def generate_part_types():
    part_types = []
    types = [
    'Вал', 'Шестерня', 'Подшипник', 'Муфта', 
    'Крышка', 'Болт', 'Гайка', 'Шайба', 'Ось','Звездочка',
    'Цепь', 'Ролик', 'Сальник', 'Клапан', 'Фильтр',
    'Патрубок', 'Трубка', 'Штуцер', 'Кронштейн', 'Пластина',
    'Диск', 'Лента', 'Колодка', 'Рычаг', 'Вилка', 'Решетка'
    ]
    adjectives = [
        'упорн', 'радиальн', 'стопорн', 'переходн', 'соединительн',
        'защитн', 'крепежн', 'корончат', 'пружинн',
        'вращательн', 'клинов','уплотнительн',
        'армированн', 'обратн', 'маслян', 'быстроразъемн',
        'регулировочн', 'фрикционн',
        'вентиляционн', 'дренажн'
    ]
    part_functions = [
    'передачи вращательного момента', 'фиксации компонентов', 'уплотнения соединений',
    'снижения трения', 'передачи мощности', 'соединения валов', 'защиты механизмов',
    'крепления деталей', 'создания упора', 'регулировки зазоров', 'отвода жидкостей',
    'очистки рабочих сред', 'демпфирования вибраций', 'изменения передаточного отношения',
    'торможения системы', 'переключения скоростей', 'охлаждения узлов', 'фильтрации масел',
    'компенсации температурных расширений', 'перераспределения нагрузок'
    ]
    applications = [
        'в редукторах', 'в двигателях внутреннего сгорания', 'в коробках передач',
        'в насосном оборудовании', 'в компрессорах', 'в турбинных установках',
        'в станках ЧПУ', 'в гидравлических системах', 'в пневматических линиях',
        'в автомобильных трансмиссиях', 'в авиационных агрегатах', 'в железнодорожной технике',
        'в горнодобывающем оборудовании', 'в судовых механизмах', 'в энергетических установках'
    ]
    for i in range(0, NUM_PART_TYPES):
        type = random.choice(types)
        if m.parse(type)[0].feats['Gender'] == 'Masc':
            ending = 'ый'
        elif m.parse(type)[0].feats['Gender'] == 'Fem':
            ending = 'ая'
        part_types.append({
            'parttype_id': i + 1,
            'type_name': f'{random.choice(types)} {random.choice(adjectives) + ending}',
            'description': f'Используется для {random.choice(part_functions)} {random.choice(applications)}'
        })
    return part_types

# Генерация данных для таблицы Supplier (Поставщики)
def generate_suppliers():
    suppliers = []
    suppliers_names = ['Bosch', 'Siemens', 'General Electric', 'Caterpillar', 'Honeywell', '3M', 'ABB', 'Schneider Electric', 'Mitsubishi Heavy Industries', 'Hitachi', 'Toshiba', 'Hyundai Heavy Industries', 'Doosan', 'ThyssenKrupp', 'Rolls-Royce', 'Alstom', 'Emerson Electric', 'Rockwell Automation', 'Cummins', 'John Deere', 'Volvo Group', 'Daimler Truck', 'Parker Hannifin', 'Eaton', 'ZF Friedrichshafen', 'Continental', 'Magna', 'BorgWarner', 'Valeo', 'Faurecia', 'Mahle', 'Knorr-Bremse', 'Wabtec', 'SKF', 'Timken', 'NSK', 'NTN', 'JTEKT', 'Schaeffler', 'GKN', 'Sandvik', 'Kennametal', 'Walter AG', 'Iscar', 'Seco Tools', 'MAPAL', 'Dormer Pramet', 'Gühring', 'Liebherr', 'Komatsu', 'Wärtsilä', 'MAN Energy Solutions', 'Sulzer', 'Atlas Copco', 'Ingersoll Rand', 'Gardner Denver', 'Sullair', 'Kaeser', 'Grundfos', 'KSB', 'Wilo', 'Xylem', 'Flowserve', 'ITT Inc', 'Pentair', 'Alfa Laval', 'GEA', 'SPX Flow', 'SMC Corporation', 'Festo', 'Pall', 'Donaldson', 'Parker Hannifin', 'Swagelok', 'Camozzi', 'Norgren', 'Rotork', 'AUMA', 'Siemens Healthineers', 'Philips', 'GE Healthcare', 'Baker Hughes', 'Halliburton', 'Schlumberger', 'Weatherford', 'National Oilwell Varco', 'Tenaris', 'Vallourec', 'TMK', 'SSAB', 'Voestalpine', 'ArcelorMittal', 'Nippon Steel', 'POSCO', 'Tata Steel', 'Outokumpu', 'Aperam', 'Nucor', 'Gerdau', 'Severstal', 'Metso Outotec', 'FLSmidth', 'Weir Group', 'KHD Humboldt Wedag', 'Claas', 'CNH Industrial', 'AGCO', 'Kubota', 'Yanmar', 'Deutz', 'Perkins', 'MTU', 'Scania', 'MAN Truck & Bus']
    mailboxes = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'aol.com', 'mail.com', 'protonmail.com', 'zoho.com', 'yandex.ru', 'mail.ru', 'icloud.com', 'gmx.com', 'tutanota.com', 'fastmail.com', 'hushmail.com', 'qq.com', '163.com', 'rediffmail.com', 'sina.com', 'naver.com']
    
    for i in range(0, NUM_SUPPLIERS):
        suppliers.append({
            'supplier_id': i + 1,
            'supplier_name': suppliers_names[i],
            'contact_phone': fake.phone_number(),
            'reliability_rating': random.randint(1, 5),
            'email': f'{suppliers_names[i].replace(' ', '').lower()}@{random.choice(mailboxes)}'
        })
    return suppliers

# Генерация данных для таблицы Part (Детали)
def generate_parts():
    materials = ['Сталь', 'Чугун', 'Алюминий', 'Медь', 'Латунь', 'Бронза', 'Титан', 'Никель', 'Железо', 'Резина', 'Углепластик', 'Керамика', 'Графит']
    parts = []
    
    for i in range(0, NUM_PARTS):
        part = {
            'part_id': i + 1,
            'material': random.choice(materials),
            'weight_kg': round(random.uniform(0.01, 50.0), 3),
            'price_usd': round(random.uniform(0.1, 500.0), 2),
            'parttype_id': random.randint(1, NUM_PART_TYPES),
            'quantity_in_stock': random.randint(0, 1000),
            'supplier_id': random.randint(1, NUM_SUPPLIERS),
            'min_stock_level': random.randint(5, 50)
        }
        
        # 10% деталей неактивны
        if random.random() < 0.1:
            part['is_active'] = False
        else:
            part['is_active'] = True
        parts.append(part)

    return parts

# Генерация данных для таблицы Employee (Сотрудники)
def generate_employees():
    positions = ['Менеджер по продажам', 'Специалист по закупкам', 'Логист', 'Технический консультант', 'Маркетолог', 'Складской работник', 'Сервисный инженер']
    employees = []
    
    for i in range(0, NUM_EMPLOYEES):
        hire_date = fake.date_between(start_date='-10y', end_date='-1d')
        first_names = ['Александр', 'Дмитрий', 'Максим', 'Сергей', 'Андрей', 'Алексей', 'Артем', 'Илья', 'Петр', 'Михаил', 'Геннадий', 'Матвей', 'Роман', 'Егор', 'Арсений', 'Иван', 'Денис', 'Евгений', 'Даниил', 'Павел']
        last_names = ['Александрович', 'Дмитриевич', 'Максимович', 'Сергеевич', 'Андреевич', 'Алексеевич', 'Артемович', 'Ильич', 'Петрович', 'Михаилович', 'Геннадьевич', 'Матвеевич', 'Романович', 'Егорович', 'Арсениевич', 'Иванович', 'Денисович', 'Евгениевич', 'Даниилович', 'Павелович']
        employees.append({
            'employee_id': i + 1,
            'first_name': random.choice(first_names),
            'second_name': fake.last_name_male(),
            'last_name': random.choice(last_names),
            'position': random.choice(positions),
            'hire_date': hire_date.isoformat(),
            'age': random.randint(18, 65)
        })
    return employees

# Генерация данных для таблицы Invoice (Накладные)
def generate_invoices(customers, employees):
    invoices = []
    start_date = datetime.now() - timedelta(days=365*3)  
    
    for i in range(1, NUM_INVOICES + 1):
        invoice_date = fake.date_time_between(start_date=start_date, end_date='now')
        
        invoices.append({
            'invoice_id': i,
            'invoice_date': invoice_date.isoformat(),
            'total_amount': 0, 
            'customer_id': random.randint(1, NUM_CUSTOMERS),
            'employee_id': random.randint(1, NUM_EMPLOYEES),
            'payment_status': random.choices(
                ['Оплачено', 'Частично оплачено', 'Неоплачено'], 
                weights=[85, 10, 5]
            )[0]
        })
    return invoices

# Генерация данных для таблицы InvoiceLine (Строки накладных)
def generate_invoice_lines(invoices, parts):
    invoice_lines = []
    line_id = 1
    active_parts = [p for p in parts if p['is_active']]
    
    for invoice in invoices:
        num_lines = random.randint(1, 8) 
        invoice_total = 0
        
        for _ in range(num_lines):
            part = random.choice(active_parts)
            quantity = random.randint(1, 100)
            unit_price = part['price_usd'] * (1 - random.uniform(0.0, 0.1)) 
            line_total = round(quantity * unit_price, 2)
            
            invoice_lines.append({
                'invoiceline_id': line_id,
                'invoice_id': invoice['invoice_id'],
                'part_id': part['part_id'],
                'quantity': quantity,
                'unit_price': unit_price,
                'line_total': line_total
            })
            
            invoice_total += line_total
            line_id += 1

        invoice['total_amount'] = round(invoice_total, 2)

    
    return invoice_lines

# Функция для сохранения данных в CSV
def save_to_csv(data, filename, fieldnames):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f'Saved {len(data)} records to {filename}')

# Основной процесс генерации данных
def main():
    print('Generating customers...')
    customers = generate_customers()
    save_to_csv(customers, 'tables/customers.csv', ['customer_id', 'customer_name', 'city', 'contact_phone', 'discount_percent', 'email'])

    print('Generating part types...')
    part_types = generate_part_types()
    save_to_csv(part_types, 'tables/part_types.csv', ['parttype_id', 'type_name', 'description'])
    
    print('Generating suppliers...')
    suppliers = generate_suppliers()
    save_to_csv(suppliers, 'tables/suppliers.csv', ['supplier_id', 'supplier_name', 'contact_phone', 'reliability_rating', 'email'])
    
    print('Generating parts...')
    parts = generate_parts()
    save_to_csv(parts, 'tables/parts.csv', ['part_id', 'material', 'weight_kg', 'price_usd', 'parttype_id', 'quantity_in_stock', 'supplier_id', 'min_stock_level', 'is_active'])
    
    print('Generating employees...')
    employees = generate_employees()
    save_to_csv(employees, 'tables/employees.csv', ['employee_id', 'first_name', 'second_name', 'last_name', 'position', 'hire_date', 'age'])
    
    print('Generating invoices...')
    invoices = generate_invoices(customers, employees)
    print('Generating invoice lines...')
    invoice_lines = generate_invoice_lines(invoices, parts)
    save_to_csv(invoice_lines, 'tables/invoice_lines.csv', ['invoiceline_id', 'invoice_id', 'part_id', 'quantity', 'unit_price', 'line_total'])
    save_to_csv(invoices, 'tables/invoices.csv', ['invoice_id', 'invoice_date', 'total_amount', 'customer_id', 'employee_id', 'payment_status'])

if __name__ == '__main__':
    main()