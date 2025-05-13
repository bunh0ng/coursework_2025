from database import check_fill, check_full_fill
from format_table_ascii import format_table_ascii, format_table_for_md
from os import remove

def checkfill(bot, message, menu):
    try:
        clonames, rows = check_fill()
        table = format_table_ascii(clonames, rows)
        bot.send_message(message.chat.id, f"<pre>{table}</pre>", parse_mode="HTML", reply_markup=menu)
        clonames, rows = check_full_fill()
        table1 = format_table_ascii(clonames, rows)
        table2 = format_table_for_md(clonames, rows)
        with open('Что_пополнить.txt', 'w', encoding='utf-8') as f:
            f.write(table1)
        with open('Что_пополнить.txt', 'rb') as f:
            bot.send_document(message.chat.id, f, reply_markup=menu)
        remove(f'Что_пополнить.txt')
        with open('Что_пополнить.md', 'w', encoding='utf-8') as f:
            f.write(table2)
        with open('Что_пополнить.md', 'rb') as f:
            bot.send_document(message.chat.id, f, reply_markup=menu)
        remove('Что_пополнить.md')
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка:\n<pre>{e}</pre>', parse_mode="HTML", reply_markup=menu)