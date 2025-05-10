def return_back(bot, message, menu, user_state):
    try:
        user_id = message.from_user.id
        del user_state[user_id]
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=menu)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка:\n<pre>{e}</pre>', parse_mode="HTML", reply_markup=menu)