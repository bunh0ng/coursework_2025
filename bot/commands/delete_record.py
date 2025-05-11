from telebot import types
from database import delete_from_database

table_map = {
            'Накладная': 'Invoice',
            'Строка накладной': 'InvoiceLine',
            'Поставщик': 'Supplier',
            'Покупатель': 'Customer',
            'Деталь': 'Part',
            'Тип детали': 'PartType',
            'Сотрудник': 'Employee',
            'Платеж': 'Payment'
        }

def delete_record(bot, message, menu, user_state):
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Накладная', 'Строка накладной', 'Поставщик', 'Покупатель')
        markup.row('Деталь', 'Тип детали', 'Сотрудник', 'Платеж')
        markup.row('Назад')
        bot.send_message(message.chat.id, 'Из какой таблицы удалить запись?', reply_markup=markup)
        user_state[message.chat.id] = {'action': 'delete'}
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при удалении:\n<pre>{e}</pre>', parse_mode="HTML", reply_markup=menu)

def delete_data(bot, message, menu, user_state):
    user_id = message.from_user.id
    try:
        table = user_state[message.chat.id]['table']
        record_id = int(message.text)
        delete_from_database(table_map[table], record_id)
        bot.send_message(message.chat.id, f'Запись с ID {record_id} удалена из таблицы "{table}".', reply_markup=menu)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при удалении:\n<pre>{e}</pre>', parse_mode="HTML", reply_markup=menu)
    finally:
        del user_state[user_id]