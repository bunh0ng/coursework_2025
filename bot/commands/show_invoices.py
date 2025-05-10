from database import invoices_for_period
from format_table_ascii import format_table_ascii
from os import remove
from telebot import types

def show_invoices(bot, message, menu, user_state):
    user_id = message.from_user.id
    try:
        clonames, rows = invoices_for_period(message.text)
        table = format_table_ascii(clonames, rows)
        with open(f'{message.text.replace('\n', '-')}.txt', 'w', encoding='utf-8') as f:
            f.write(table)
        with open(f'{message.text.replace('\n', '-')}.txt', 'rb') as f:
            bot.send_document(message.chat.id, f, reply_markup=menu)
        remove(f'{message.text.replace('\n', '-')}.txt')
        print(f'{message.from_user.username} посмотрел накладные с {message.text.replace('\n', ' по ')}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка:\n<pre>{e}</pre>', parse_mode="HTML", reply_markup=menu)
    finally:
        del user_state[user_id]

def ask_period(bot, message, menu, user_state):
    try:
        bot.send_message(message.chat.id, 'Введите период, за который хотите посмотреть накладные в формате\n<pre>ДД.ММ.ГГГГ\nДД.ММ.ГГГГ</pre>', parse_mode="HTML", reply_markup=types.ReplyKeyboardRemove())
        user_state[message.chat.id] = {'action': 'watch'}
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка:\n<pre>{e}</pre>', parse_mode="HTML", reply_markup=menu)