import telebot
from telebot import types
import database
from config import bot_settings
from format_table_ascii import format_table_ascii
import os


bot = telebot.TeleBot(bot_settings['Token'])

user_state = {}
markup_page_1 = types.ReplyKeyboardMarkup(resize_keyboard=True).row('Добавить запись', 'Удалить запись').row('Самые активные покупатели', 'Самые продаваемые детали').row('Следующая страница')
markup_page_2 = types.ReplyKeyboardMarkup(resize_keyboard=True).row('Посмотреть накладные за период', 'Самые ценные сотрудники').row('Самые активные поставщики', 'Какие детали пополнить').row('Предыдущая страница')

@bot.message_handler(commands=['start'])
def handle_start(message):
    with open("hello.txt", "r", encoding='utf-8') as f:
            bot.send_message(message.chat.id, f.read())
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup_page_1)

@bot.message_handler(commands=['documents'])
def handle_docs(message):
    bot.send_message(message.chat.id, 'Скоро здесь будут документы :)', reply_markup=markup_page_1)

@bot.message_handler(func=lambda msg: msg.text == 'Предыдущая страница')
def handle_page_1(message):
    try:
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup_page_1)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка:\n{e}', reply_markup=markup_page_1)

@bot.message_handler(func=lambda msg: msg.text == 'Следующая страница')
def handle_page_1(message):
    try:
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup_page_2)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка:\n{e}', reply_markup=markup_page_1)

@bot.message_handler(func=lambda msg: msg.text == 'Добавить запись')
def handle_add_record(message):
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Накладная', 'Строка накладной', 'Поставщик', 'Покупатель')
        markup.row('Деталь', 'Тип детали', 'Сотрудник')
        bot.send_message(message.chat.id, 'В какую таблицу добавить запись?', reply_markup=markup)
        user_state[message.chat.id] = {'action': 'add'}
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при добавлении:\n{e}', reply_markup=markup_page_1)

@bot.message_handler(func=lambda msg: msg.text == 'Удалить запись')
def handle_add_record(message):
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Накладная', 'Строка накладной', 'Поставщик', 'Покупатель')
        markup.row('Деталь', 'Тип детали', 'Сотрудник')
        bot.send_message(message.chat.id, 'Из какой таблицы удалить запись?', reply_markup=markup)
        user_state[message.chat.id] = {'action': 'delete'}
    except Exception as e:
            bot.send_message(message.chat.id, f'Ошибка при добавлении:\n{e}', reply_markup=markup_page_1)

@bot.message_handler(func=lambda msg: msg.text in ['Накладная', 'Строка накладной', 'Поставщик', 'Покупатель', 'Деталь', 'Тип детали', 'Сотрудник'])
def handle_table_selection(message):
    try:
        state = user_state.get(message.chat.id)
        if state and state['action'] == 'delete':
            user_state[message.chat.id]['table'] = message.text
            bot.send_message(message.chat.id, f'Введите ID записи, которую нужно удалить из таблицы "{message.text}"', reply_markup=types.ReplyKeyboardRemove())
        elif state and state['action'] == 'add':
            user_state[message.chat.id]['table'] = message.text
            bot.send_message(message.chat.id, f'Введите данные для таблицы "{message.text}" через запятую без пробелов', reply_markup=types.ReplyKeyboardRemove())
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при добавлении:\n{e}', reply_markup=markup_page_1)

@bot.message_handler(func=lambda msg: msg.chat.id in user_state and user_state[msg.chat.id]['action'] == 'add' and 'table' in user_state[msg.chat.id])
def handle_data_input(message):
    user_id = message.from_user.id
    table = user_state[user_id]['table']
    try:
        if table == 'Накладная':
            database.insert_into_invoice(message.text)
        elif table == 'Строка накладной':
            database.insert_into_invoiceline(message.text)
        elif table == 'Поставщик':
            database.insert_into_supplier(message.text)
        elif table == 'Покупатель':
            database.insert_into_customer(message.text)
        elif table == 'Деталь':
            database.insert_into_part(message.text)
        elif table == 'Тип детали':
            database.insert_into_parttype(message.text)
        elif table == 'Сотрудник':
            database.insert_into_employee(message.text)
        bot.send_message(message.chat.id, f'Запись добавлена в таблицу "{table}"', reply_markup=markup_page_1)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при добавлении:\n{e}', reply_markup=markup_page_1)
    finally:
        del user_state[user_id]

@bot.message_handler(func=lambda msg: msg.chat.id in user_state and user_state[msg.chat.id]['action'] == 'delete' and 'table' in user_state[msg.chat.id])
def handle_delete_data(message):
    user_id = message.from_user.id
    try:
        table = user_state[message.chat.id]['table']
        record_id = int(message.text)
        if table == 'Накладная':
            table = 'Invoice'
        elif table == 'Строка накладной':
            table = 'Invoiceline'
        elif table == 'Поставщик':
            table = 'Supplier'
        elif table == 'Покупатель':
            table = 'Customer'
        elif table == 'Деталь':
            table = 'Part'
        elif table == 'Тип детали':
            table = 'Parttype'
        elif table == 'Сотрудник':
            table = 'Employee'
        database.delete_from_database(table, record_id)
        bot.send_message(message.chat.id, f'Запись с ID {record_id} удалена из таблицы "{table}".', reply_markup=markup_page_1)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при удалении:\n{e}', reply_markup=markup_page_1)
    finally:
        del user_state[user_id]

@bot.message_handler(func=lambda msg: msg.text == 'Посмотреть накладные за период')
def handle_ask_period(message):
    try:
        bot.send_message(message.chat.id, 'Введите период, за который хотите посмотреть накладные в формате "ГГГГ-ММ-ДД,ГГГГ-ММ-ДД"', reply_markup=types.ReplyKeyboardRemove())
        user_state[message.chat.id] = {'action': 'watch'}
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при добавлении:\n{e}', reply_markup=markup_page_1)

@bot.message_handler(func=lambda msg: msg.chat.id in user_state and user_state[msg.chat.id]['action'] == 'watch')
def handle_show_invoices(message):
    user_id = message.from_user.id
    try:
        clonames, rows = database.invoices_for_period(message.text)
        table = format_table_ascii(clonames, rows)
        with open(f'{message.text}.txt', 'w', encoding='utf-8') as f:
            f.write(table)
        with open(f'{message.text}.txt', 'rb') as f:
            bot.send_document(message.chat.id, f, reply_markup=markup_page_1)
        os.remove(f'{message.text}.txt')
        print(f'{message.from_user.username} посмотрел накладные с {message.text.replace(',', ' по ')}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при просмотре:\n{e}', reply_markup=markup_page_1)
    finally:
        del user_state[user_id]

@bot.message_handler(func=lambda msg: msg.text == 'Какие детали пополнить')
def handle_check_fill(message):
    try:
        clonames, rows = database.check_fill()
        table = format_table_ascii(clonames, rows)
        bot.send_message(message.chat.id, f"<pre>{table}</pre>", parse_mode="HTML", reply_markup=markup_page_1)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при добавлении:\n{e}', reply_markup=markup_page_1)

@bot.message_handler(func=lambda msg: msg.text == 'Самые активные покупатели')
def handle_mv_customers(message):
    try:
        clonames, rows = database.most_valuable_customers()
        table = format_table_ascii(clonames, rows)
        bot.send_message(message.chat.id, f"<pre>{table}</pre>", parse_mode="HTML", reply_markup=markup_page_1)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при добавлении:\n{e}', reply_markup=markup_page_1)

@bot.message_handler(func=lambda msg: msg.text == 'Самые продаваемые детали')
def handle_ms_parts(message):
    try:
        clonames, rows = database.most_sold_parts()
        table = format_table_ascii(clonames, rows)
        bot.send_message(message.chat.id, f"<pre>{table}</pre>", parse_mode="HTML", reply_markup=markup_page_1)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при добавлении:\n{e}', reply_markup=markup_page_1)

@bot.message_handler(func=lambda msg: msg.text == 'Самые ценные сотрудники')
def handle_mv_employees(message):
    try:
        clonames, rows = database.most_valuable_employee()
        table = format_table_ascii(clonames, rows)
        bot.send_message(message.chat.id, f"<pre>{table}</pre>", parse_mode="HTML", reply_markup=markup_page_1)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при добавлении:\n{e}', reply_markup=markup_page_1)

@bot.message_handler(func=lambda msg: msg.text == 'Самые активные поставщики')
def handle_ma_suppliers(message):
    try:
        clonames, rows = database.most_active_suppliers()
        table = format_table_ascii(clonames, rows)
        bot.send_message(message.chat.id, f"<pre>{table}</pre>", parse_mode="HTML", reply_markup=markup_page_1)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при добавлении:\n{e}', reply_markup=markup_page_1)

print('Бот запущен')
bot.polling(none_stop=True)
