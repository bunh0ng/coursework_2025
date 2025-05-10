def start(bot, message, menu):
    with open("hello.txt", "r", encoding='utf-8') as f:
            bot.send_message(message.chat.id, f.read())
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=menu)