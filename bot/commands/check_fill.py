from database import check_fill
from format_table_ascii import format_table_ascii

def checkfill(bot, message, menu):
    try:
        clonames, rows = check_fill()
        table = format_table_ascii(clonames, rows)
        bot.send_message(message.chat.id, f"<pre>{table}</pre>", parse_mode="HTML", reply_markup=menu)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка:\n<pre>{e}</pre>', parse_mode="HTML", reply_markup=menu)