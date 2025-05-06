import telebot
from telebot import types
import database
from config import bot_settings
from format_table_ascii import format_table_ascii

bot = telebot.TeleBot(bot_settings['Token'])

default_markup = types.ReplyKeyboardMarkup(resize_keyboard=True).row('Добавить запись', 'Удалить запись', 'Какие детали пополнить')

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=default_markup)

user_state = {}

@bot.message_handler(func=lambda msg: msg.text == 'Добавить запись')
def handle_add_record(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Накладная', 'Строка накладной', 'Поставщик', 'Покупатель')
    markup.row('Деталь', 'Тип детали', 'Сотрудник')
    bot.send_message(message.chat.id, 'В какую таблицу добавить запись?', reply_markup=markup)
    user_state[message.chat.id] = {'action': 'add'}

@bot.message_handler(func=lambda msg: msg.text == 'Удалить запись')
def handle_add_record(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Накладная', 'Строка накладной', 'Поставщик', 'Покупатель')
    markup.row('Деталь', 'Тип детали', 'Сотрудник')
    bot.send_message(message.chat.id, 'Из какой таблицы удалить запись?', reply_markup=markup)
    user_state[message.chat.id] = {'action': 'delete'}

@bot.message_handler(func=lambda msg: msg.text in ['Накладная', 'Строка накладной', 'Поставщик', 'Покупатель', 'Деталь', 'Тип детали', 'Сотрудник'])
def handle_table_selection(message):
    state = user_state.get(message.chat.id)
    if state and state['action'] == 'delete':
        user_state[message.chat.id]['table'] = message.text
        bot.send_message(message.chat.id, f'Введите ID записи, которую нужно удалить из таблицы «{message.text}»', reply_markup=types.ReplyKeyboardRemove())
    elif state and state['action'] == 'add':
        user_state[message.chat.id]['table'] = message.text
        bot.send_message(message.chat.id, f'Введите данные для таблицы «{message.text}» через запятую без пробелов', reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(func=lambda msg: msg.chat.id in user_state and user_state[msg.chat.id]['action'] == 'add' and 'table' in user_state[msg.chat.id])
def handle_data_input(message):
    user_id = message.from_user.id
    table = user_state[user_id]['table']
    print(table, message.text)
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
        bot.send_message(message.chat.id, f'Запись добавлена в таблицу "{table}"', reply_markup=default_markup)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при добавлении:\n {e}', reply_markup=default_markup)
    finally:
        del user_state[user_id]

@bot.message_handler(func=lambda msg: msg.chat.id in user_state and user_state[msg.chat.id]['action'] == 'delete' and 'table' in user_state[msg.chat.id])
def handle_delete_data(message):
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
        bot.send_message(message.chat.id, f'Запись с ID {record_id} удалена из таблицы «{table}».', reply_markup=default_markup)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при удалении:\n {e}', reply_markup=default_markup)
    finally:
        user_state.pop(message.chat.id, None)


@bot.message_handler(func=lambda msg: msg.text == 'Какие детали пополнить')
def check_fill(message):
    clonames, rows = database.check_fill()
    table = format_table_ascii(clonames, rows)
    bot.send_message(message.chat.id, f"<pre>{table}</pre>", parse_mode="HTML", reply_markup=default_markup)




print('Бот запущен')
bot.polling(none_stop=True)
