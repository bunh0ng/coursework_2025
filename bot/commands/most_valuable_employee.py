from database import most_valuable_employee, all_most_valuable_employees
from format_table_ascii import format_table_ascii, format_table_for_md
from os import remove

def mv_employee(bot, message, menu):
    try:
        clonames, rows = most_valuable_employee()
        table = format_table_ascii(clonames, rows)
        bot.send_message(message.chat.id, f"<pre>{table}</pre>", parse_mode="HTML", reply_markup=menu)
        clonames, rows = all_most_valuable_employees()
        table1 = format_table_ascii(clonames, rows)
        table2 = format_table_for_md(clonames, rows)
        with open('Самые_ценные_сотрудники.txt', 'w', encoding='utf-8') as f:
            f.write(table1)
        with open('Самые_ценные_сотрудники.txt', 'rb') as f:
            bot.send_document(message.chat.id, f, reply_markup=menu)
        remove(f'Самые_ценные_сотрудники.txt')
        with open('Самые_ценные_сотрудники.md', 'w', encoding='utf-8') as f:
            f.write(table2)
        with open('Самые_ценные_сотрудники.md', 'rb') as f:
            bot.send_document(message.chat.id, f, reply_markup=menu)
        remove('Самые_ценные_сотрудники.md')
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка:\n<pre>{e}</pre>', parse_mode="HTML", reply_markup=menu)