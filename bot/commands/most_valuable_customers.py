from format_table_ascii import format_table_ascii, format_table_for_md
from database import most_valuable_customers, all_most_valuable_customers
from os import remove

def mv_customers(bot, message, menu):
    try:
        clonames, rows = most_valuable_customers()
        table = format_table_ascii(clonames, rows)
        bot.send_message(message.chat.id, f"<pre>{table}</pre>", parse_mode="HTML", reply_markup=menu)
        clonames, rows = all_most_valuable_customers()
        table1 = format_table_ascii(clonames, rows)
        table2 = format_table_for_md(clonames, rows)
        with open('Самые_активные_покупатели.txt', 'w', encoding='utf-8') as f:
            f.write(table1)
        with open('Самые_активные_покупатели.txt', 'rb') as f:
            bot.send_document(message.chat.id, f, reply_markup=menu)
        remove(f'Самые_активные_покупатели.txt')
        with open('Самые_активные_покупатели.md', 'w', encoding='utf-8') as f:
            f.write(table2)
        with open('Самые_активные_покупатели.md', 'rb') as f:
            bot.send_document(message.chat.id, f, reply_markup=menu)
        remove('Самые_активные_покупатели.md')
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка:\n<pre>{e}</pre>', parse_mode="HTML", reply_markup=menu)