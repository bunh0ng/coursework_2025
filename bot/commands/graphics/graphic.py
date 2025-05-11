from database import get_sales_dynamics, get_payment_status_stats, get_payments_vs_debts
from telebot import types
from commands.graphics.plot import create_plot

def graphic_types(bot, message, user_state):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Динамика продаж за год', 'Статусы оплат')
    markup.row('Оплаты и долги компаний', 'Назад')
    bot.send_message(message.chat.id, 'Выберите график:', reply_markup=markup)
    user_state[message.chat.id] = {'action': 'analytics'}
def plot_selection(bot, message, menu, user_state):
    try:
        if message.text == 'Динамика продаж за год':
            data = get_sales_dynamics()
            plot = create_plot(data, 'bar', 'Динамика продаж по месяцам', 'Месяц', 'Сумма продаж')
        elif message.text == 'Статусы оплат':
            data = get_payment_status_stats()
            plot = create_plot(data, 'pie', 'Распределение статусов оплат')
        elif message.text == 'Оплаты и долги компаний':
            data = get_payments_vs_debts()
            plot = create_plot(data, '2bars', 'Соотношение оплат и долгов по компаниям', 'Компании', 'Долги/оплаты')
        bot.send_photo(message.chat.id, plot, reply_markup=menu)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка:\n<pre>{e}</pre>', parse_mode="HTML")
    finally:
        if message.chat.id in user_state:
            del user_state[message.chat.id]
