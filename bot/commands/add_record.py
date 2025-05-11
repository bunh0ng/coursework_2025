from telebot import types
import database

def add_record(bot, message, menu, user_state):
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Накладная', 'Строка накладной', 'Поставщик', 'Покупатель')
        markup.row('Деталь', 'Тип детали', 'Сотрудник', 'Платеж')
        markup.row('Назад')
        bot.send_message(message.chat.id, 'В какую таблицу добавить запись?', reply_markup=markup)
        user_state[message.chat.id] = {'action': 'add'}
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при добавлении:\n<pre>{e}</pre>', parse_mode="HTML", reply_markup=menu)

def table_selection(bot, message, menu, user_state):
    try:
        state = user_state.get(message.chat.id)
        if state and state['action'] == 'delete':
            user_state[message.chat.id]['table'] = message.text
            bot.send_message(message.chat.id, f'Введите ID записи, которую нужно удалить из таблицы "{message.text}"', reply_markup=types.ReplyKeyboardRemove())
        elif state and state['action'] == 'add':
            user_state[message.chat.id]['table'] = message.text
            bot.send_message(message.chat.id, f'Введите данные для таблицы "{message.text}" через строку', reply_markup=types.ReplyKeyboardRemove())
            if message.text == 'Накладная':
                bot.send_message(message.chat.id, 'Формат:\n<pre>дата и время оформления (ДД.ММ.ГГГГ ЧЧ.ММ.СС)\nid покупателя\nid сотрудника\nстатус оплаты (Оплачено, Не оплачено, Частично оплачено)</pre>', parse_mode="HTML")
            elif message.text == 'Строка накладной':
                bot.send_message(message.chat.id, 'Формат:\n<pre>id накладной\nid детали\nколичество</pre>', parse_mode="HTML")
            elif message.text == 'Поставщик':
                bot.send_message(message.chat.id, 'Формат:\n<pre>название\nтелефон\nпочта</pre>', parse_mode="HTML")
            elif message.text == 'Покупатель':
                bot.send_message(message.chat.id, 'Формат:\n<pre>название\nгород\nтелефон\nпочта</pre>', parse_mode="HTML")
            elif message.text == 'Деталь':
                bot.send_message(message.chat.id, 'Формат:\n<pre>материал\nвес\nцена\nid типа\nколичество на складе\nid поставщика\nминимальный уровень запаса</pre>', parse_mode="HTML")
            elif message.text == 'Тип детали':
                bot.send_message(message.chat.id, 'Формат:\n<pre>название\nописание</pre>', parse_mode="HTML")
            elif message.text == 'Сотрудник':
                bot.send_message(message.chat.id, 'Формат:\n<pre>ФИО\nдолжность\nдата найма (ДД.ММ.ГГГГ)\nвозраст</pre>', parse_mode="HTML")
            elif message.text == 'Платеж':
                bot.send_message(message.chat.id, 'Формат:\n<pre>id накладной\nдата и время платежа (ДД.ММ.ГГГГ ЧЧ.ММ.СС\nсумма платежа\nтип оплаты (Наличный расчет, Безналичный расчет)</pre>', parse_mode="HTML")
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка:\n<pre>{e}</pre>', parse_mode="HTML", reply_markup=menu)

def data_input(bot, message, menu, user_state):
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
        elif table == 'Платеж':
            database.insert_into_payment(message.text)
        bot.send_message(message.chat.id, f'Запись добавлена в таблицу "{table}"', reply_markup=menu)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при добавлении:\n<pre>{e}</pre>', parse_mode="HTML", reply_markup=menu)
    finally:
        del user_state[user_id]