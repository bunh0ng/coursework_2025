from telebot import types
from format_table_ascii import format_table_ascii
from database import search_by_content, search_by_id

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

def search_record(bot, message, menu, user_state):
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Поиск по ID', 'Поиск по содержимому')
        markup.row('Назад')
        bot.send_message(message.chat.id, 'Выберите тип поиска:', reply_markup=markup)
        user_state[message.chat.id] = {'action': 'search_type'}
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка:\n<pre>{e}</pre>', parse_mode="HTML", reply_markup=menu)

def search_type(bot, message, menu, user_state):
    try:
        search_type = 'id' if message.text == 'Поиск по ID' else 'content'
        user_state[message.chat.id] = {'action': 'search_table', 'search_type': search_type}
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Накладная', 'Строка накладной', 'Поставщик', 'Покупатель')
        markup.row('Деталь', 'Тип детали', 'Сотрудник', 'Платеж')
        markup.row('Назад')
        bot.send_message(message.chat.id, 'В какой таблице искать?', reply_markup=markup)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка:\n<pre>{e}</pre>', parse_mode="HTML", reply_markup=menu)\
        
def search_table(bot, message, menu, user_state):
    try:
        user_state[message.chat.id]['table'] = message.text
        search_type = user_state[message.chat.id]['search_type']
        
        if search_type == 'id':
            bot.send_message(message.chat.id, f'Введите ID для поиска в таблице "{message.text}":', reply_markup=types.ReplyKeyboardRemove())
        elif search_type == 'content':
            bot.send_message(message.chat.id, f'Введите ключевое слово для поиска в таблице "{message.text}":', reply_markup=types.ReplyKeyboardRemove())
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка:\n<pre>{e}</pre>', parse_mode="HTML", reply_markup=menu)

def search_query(bot, message, menu, user_state):
    try:
        user_id = message.from_user.id
        state = user_state[user_id]
        table = state['table']
        search_type = state['search_type']
        search_query = message.text
        db_table = table_map[table]
        
        if search_type == 'id':
            result = search_by_id(db_table, search_query)
        elif search_type == 'content':
            result = search_by_content(db_table, search_query)
        
        if result:
            colnames, rows = result
            table_text = format_table_ascii(colnames, rows)
            bot.send_message(message.chat.id, f"<pre>{table_text}</pre>", parse_mode="HTML", reply_markup=menu)
        else:
            bot.send_message(message.chat.id, "Ничего не найдено", reply_markup=menu)
            
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при поиске:\n<pre>{e}</pre>', parse_mode="HTML", reply_markup=menu)
    finally:
        if user_id in user_state:
            del user_state[user_id]