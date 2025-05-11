from imports import *
from datetime import datetime as dt

bot = telebot.TeleBot(bot_settings['Token'])

user_state = {}
actions = ['Поиск записи', 'Добавить запись', 'Удалить запись', 
           'Посмотреть накладные за период', 'Графики аналитики', 
           'Самые активные покупатели', 'Самые продаваемые детали',
            'Самые ценные сотрудники', 'Самые активные поставщики', 
            'Какие детали пополнить']
menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
for i in actions:
    menu.add(i)

@bot.message_handler(commands=['start'])
def handle_start(message):
    start(bot, message, menu)

@bot.message_handler(commands=['documents'])
def handle_docs(message):
    bot.send_message(message.chat.id, 'Скоро здесь будут документы :)', reply_markup=menu)

@bot.message_handler(func=lambda msg: msg.text == 'Поиск записи')
def handle_search_record(message):
    search_record(bot, message, menu, user_state)

@bot.message_handler(func=lambda msg: msg.chat.id in user_state and user_state[msg.chat.id]['action'] == 'search_type' and msg.text in ['Поиск по ID', 'Поиск по содержимому'])
def handle_search_type(message):
    search_type(bot, message, menu, user_state)

@bot.message_handler(func=lambda msg: msg.chat.id in user_state and user_state[msg.chat.id]['action'] == 'search_table' and msg.text in ['Накладная', 'Строка накладной', 'Поставщик', 'Покупатель', 'Деталь', 'Тип детали', 'Сотрудник'])
def handle_search_table(message):
    search_table(bot, message, menu, user_state)

@bot.message_handler(func=lambda msg: msg.chat.id in user_state and user_state[msg.chat.id].get('action') in ['search_table'] and 'table' in user_state[msg.chat.id])
def handle_search_query(message):
    search_query(bot, message, menu, user_state)

@bot.message_handler(func=lambda msg: msg.text == 'Добавить запись')
def handle_add_record(message):
    add_record(bot, message, menu, user_state)

@bot.message_handler(func=lambda msg: msg.text == 'Удалить запись')
def handle_delete_record(message):
    delete_record(bot, message, menu, user_state)

@bot.message_handler(func=lambda msg: msg.text == 'Назад')
def handle_return_back(message):
    return_back(bot, message, menu, user_state)

@bot.message_handler(func=lambda msg: msg.text in ['Накладная', 'Строка накладной', 'Поставщик', 'Покупатель', 'Деталь', 'Тип детали', 'Сотрудник'])
def handle_table_selection(message):
    table_selection(bot, message, menu, user_state)

@bot.message_handler(func=lambda msg: msg.chat.id in user_state and user_state[msg.chat.id]['action'] == 'add' and 'table' in user_state[msg.chat.id])
def handle_data_input(message):
    data_input(bot, message, menu, user_state)

@bot.message_handler(func=lambda msg: msg.chat.id in user_state and user_state[msg.chat.id]['action'] == 'delete' and 'table' in user_state[msg.chat.id])
def handle_delete_data(message):
    delete_data(bot, message, menu, user_state)

@bot.message_handler(func=lambda msg: msg.text == 'Посмотреть накладные за период')
def handle_ask_period(message):
    ask_period(bot, message, menu, user_state)

@bot.message_handler(func=lambda msg: msg.chat.id in user_state and user_state[msg.chat.id]['action'] == 'watch')
def handle_show_invoices(message):
    show_invoices(bot, message, menu, user_state)

@bot.message_handler(func=lambda msg: msg.text == 'Какие детали пополнить')
def handle_check_fill(message):
    checkfill(bot, message, menu)

@bot.message_handler(func=lambda msg: msg.text == 'Самые активные покупатели')
def handle_mv_customers(message):
    mv_customers(bot, message, menu)

@bot.message_handler(func=lambda msg: msg.text == 'Самые продаваемые детали')
def handle_ms_parts(message):
    ms_parts(bot, message, menu)

@bot.message_handler(func=lambda msg: msg.text == 'Самые ценные сотрудники')
def handle_mv_employees(message):
    mv_employee(bot, message, menu)

@bot.message_handler(func=lambda msg: msg.text == 'Самые активные поставщики')
def handle_ma_suppliers(message):
    ma_suppliers(bot, message, menu)

@bot.message_handler(func=lambda msg: msg.text == 'Графики аналитики')
def handle_graphic_types(message):
    graphic_types(bot, message, user_state)

@bot.message_handler(func=lambda msg: msg.chat.id in user_state and user_state[msg.chat.id]['action'] == 'analytics' and msg.text in ['Динамика продаж за год', 'Статусы оплат'])
def handle_plot_selection(message):
    plot_selection(bot, message, menu, user_state)

@bot.message_handler(content_types=['text', 'audio', 'photo', 'video', 'sticker', 'location', 'voice', 'document', 'contact'])
def on_flood(message):
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=menu)

print(f'Бот запущен {dt.now()}')
bot.polling(none_stop=True)
