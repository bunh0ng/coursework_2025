import telebot
from telebot import types
import database
from config import bot_settings

bot = telebot.TeleBot(bot_settings['Token'])

def send_long_message(chat_id, text, bot, chunk_size=4096):
    for i in range(0, len(text), chunk_size):
        bot.send_message(chat_id, text[i:i+chunk_size])

@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Добавить запись", "Удалить запись")
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)

user_state = {}

@bot.message_handler(func=lambda msg: msg.text == "Добавить запись")
def handle_add_record(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Накладная", "Строка накладной", "Поставщик", "Покупатель")
    markup.row("Деталь", "Тип детали", "Сотрудник")
    bot.send_message(message.chat.id, "В какую таблицу добавить запись?", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text in ["Накладная", "Строка накладной", "Поставщик", "Покупатель", "Деталь", "Тип детали", "Сотрудник"])
def handle_table_selection(message):
    user_id = message.from_user.id
    user_state[user_id] = message.text  # Сохраняем выбранную таблицу
    bot.send_message(
        message.chat.id,
        f"Введите данные для таблицы «{message.text}» через запятую (без пробелов).",
        reply_markup=types.ReplyKeyboardRemove()
    )

@bot.message_handler(func=lambda msg: msg.from_user.id in user_state)
def handle_data_input(message):
    user_id = message.from_user.id
    table = user_state[user_id]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Добавить запись", "Удалить запись")
    print(table, message.text)
    try:
        if table == "Накладная":
            database.insert_into_invoice(message.text)
        # elif table == "Строка накладной":
        #     database.insert_into_invoiceline(message.text)
        # elif table == "Поставщик":
        #     database.insert_into_supplier(message.text)
        # elif table == "Покупатель":
        #     database.insert_into_customer(message.text)
        # elif table == "Деталь":
        #     database.insert_into_part(message.text)
        # elif table == "Тип детали":
        #     database.insert_into_parttype(message.text)
        elif table == "Сотрудник":
            database.insert_into_employee(message.text)
        bot.send_message(message.chat.id, f"✅ Запись добавлена в таблицу «{table}».", reply_markup=markup)
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка при добавлении:\n {e}", reply_markup=markup)
    finally:
        del user_state[user_id]


print("Бот запущен")
bot.polling(none_stop=True)
