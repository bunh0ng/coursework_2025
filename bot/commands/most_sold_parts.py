from database import most_sold_parts, most_sold_parts500
from format_table_ascii import format_table_ascii, format_table_for_md
from os import remove

def ms_parts(bot, message, menu):
    try:
        clonames, rows = most_sold_parts()
        table = format_table_ascii(clonames, rows)
        bot.send_message(message.chat.id, f"<pre>{table}</pre>", parse_mode="HTML", reply_markup=menu)
        clonames, rows = most_sold_parts500()
        table1 = format_table_ascii(clonames, rows)
        table2 = format_table_for_md(clonames, rows)
        with open('Самые_продаваемые_детали.txt', 'w', encoding='utf-8') as f:
            f.write(table1)
        with open('Самые_продаваемые_детали.txt', 'rb') as f:
            bot.send_document(message.chat.id, f, reply_markup=menu)
        remove(f'Самые_продаваемые_детали.txt')
        with open('Самые_продаваемые_детали.md', 'w', encoding='utf-8') as f:
            f.write(table2)
        with open('Самые_продаваемые_детали.md', 'rb') as f:
            bot.send_document(message.chat.id, f, reply_markup=menu)
        remove('Самые_продаваемые_детали.md')
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка:\n<pre>{e}</pre>', parse_mode="HTML", reply_markup=menu)