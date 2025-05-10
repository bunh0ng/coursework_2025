from format_table_ascii import format_table_ascii
from database import most_valuable_customers

def mv_customers(bot, message, menu):
    try:
        clonames, rows = most_valuable_customers()
        table = format_table_ascii(clonames, rows)
        bot.send_message(message.chat.id, f"<pre>{table}</pre>", parse_mode="HTML", reply_markup=menu)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка:\n<pre>{e}</pre>', parse_mode="HTML", reply_markup=menu)