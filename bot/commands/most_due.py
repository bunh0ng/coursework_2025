from database import most_due, all_most_due
from format_table_ascii import format_table_ascii, format_table_for_md
from os import remove

def mst_due(bot, message, menu):
    try:
        clonames, rows = most_due()
        table = format_table_ascii(clonames, rows)
        bot.send_message(message.chat.id, f"<pre>{table}</pre>", parse_mode="HTML", reply_markup=menu)
        clonames, rows = all_most_due()
        table1 = format_table_ascii(clonames, rows)
        table2 = format_table_for_md(clonames, rows)
        with open(f'Задолженности.txt', 'w', encoding='utf-8') as f:
            f.write(table1)
        with open(f'Задолженности.txt', 'rb') as f:
            bot.send_document(message.chat.id, f, reply_markup=menu)
        remove(f'Задолженности.txt')
        with open(f'Задолженности.md', 'w', encoding='utf-8') as f:
            f.write(table2)
        with open(f'Задолженности.md', 'rb') as f:
            bot.send_document(message.chat.id, f, reply_markup=menu)
        remove(f'Задолженности.md')
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка:\n<pre>{e}</pre>', parse_mode="HTML", reply_markup=menu)