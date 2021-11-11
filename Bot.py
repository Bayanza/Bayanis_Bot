import telebot
from telebot import types
import db
import schedule
import time

bot = telebot.TeleBot("")


@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    items = db.get_menu(1)
    buttons = []
    for item in items:
        for i in item:
            buttons.append(i)
    markup.add(*buttons)
    bot.send_message(message.chat.id, "Привет, {0.first_name}!".format(message.from_user), reply_markup=markup)
    bot.send_message(message.chat.id, "Для навигации воспользуйся меню")


@bot.message_handler(content_types=['text'])
def bot_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = []
    if message.chat.type == 'private':

        # Раздел "Расходы"
        if message.text == "🤑 Расходы":
            items = db.get_menu(2)
            for item in items:
                for i in item:
                    buttons.append(i)
            markup.add(*buttons, '🔙 Назад')
            bot.send_message(message.chat.id, "Выбери категорию", reply_markup=markup)
        elif message.text in str(db.get_menu(2)) and message.text != '📊 Отчет' and message.text != '🔙 Назад':
            bot.send_message(message.chat.id, 'Сколько?')
            bot.register_next_step_handler(message, lambda m: db.add_row(m, str(message.text)))
        elif message.text == '📊 Отчет':
            report = db.draw_report(message.from_user.id)
            for i in report:
                bot.send_message(message.chat.id, str(i[0]) + ': ' + str(i[1]))

        # Раздел "Напоминания"
        elif message.text == '📮 Напоминания':
            items = db.get_menu(3)
            for item in items:
                for i in item:
                    buttons.append(i)
            markup.add(*buttons, '🔙 Назад')
            bot.send_message(message.chat.id, "Выбери категорию", reply_markup=markup)

        # Раздел "Качалка"
        elif message.text == '🏋 Качалка':
            items = db.get_menu(4)
            for item in items:
                for i in item:
                    buttons.append(i)
            markup.add(*buttons, '🔙 Назад')
            bot.send_message(message.chat.id, "Выбери категорию", reply_markup=markup)

        elif message.text == '🔙 Назад':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            items = db.get_menu(1)
            for item in items:
                for i in item:
                    buttons.append(i)
            markup.add(*buttons)
            bot.send_message(message.chat.id, "Для навигации воспользуйся меню", reply_markup=markup)


bot.infinity_polling()

# @bot.message_handler(content_types=['text'])
# def bot_message(message):
#     if message.chat.type == 'private':
#         if message.text == '🤑 Расходы':
#             markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#             item1 = types.KeyboardButton('🥖 Еда')
#             item2 = types.KeyboardButton('🍔 Кафе')
#             item3 = types.KeyboardButton('🍲 Столовка')
#             item4 = types.KeyboardButton('🧼 Быт')
#             item5 = types.KeyboardButton('🚎 Дорога')
#             item6 = types.KeyboardButton('🚘 Прокат')
#             item7 = types.KeyboardButton('🕺 Доп. расходы')
#             item8 = types.KeyboardButton('📊 Отчет')
#             back = types.KeyboardButton('🔙 Назад')
#             markup.add(item1, item2, item3, item4, item5, item6, item7, item8, back)
#             bot.send_message(message.chat.id, "Выбери категорию:", reply_markup=markup)
#         elif message.text == '🔙 Назад':
#             markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#             item1 = types.KeyboardButton('🤑 Расходы')
#             markup.add(item1)
#         elif message.text == '🥖 Еда':
#             bot.send_message(message.chat.id, 'Сколько?')
#             bot.register_next_step_handler(message, lambda m: db.add_row(m, 'Еда'))
#         elif message.text == '🍔 Кафе':
#             bot.send_message(message.chat.id, 'Сколько?')
#             bot.register_next_step_handler(message, lambda m: db.add_row(m, 'Кафе'))
#         elif message.text == '🍲 Столовка':
#             bot.send_message(message.chat.id, 'Сколько?')
#             bot.register_next_step_handler(message, lambda m: db.add_row(m, 'Столовка'))
#         elif message.text == '🧼 Быт':
#             bot.send_message(message.chat.id, 'Сколько?')
#             bot.register_next_step_handler(message, lambda m: db.add_row(m, 'Быт'))
#         elif message.text == '🚎 Дорога':
#             bot.send_message(message.chat.id, 'Сколько?')
#             bot.register_next_step_handler(message, lambda m: db.add_row(m, 'Дорога'))
#         elif message.text == '🚘 Прокат':
#             bot.send_message(message.chat.id, 'Сколько?')
#             bot.register_next_step_handler(message, lambda m: db.add_row(m, 'Прокат'))
#         elif message.text == '🕺 Развлечения':
#             bot.send_message(message.chat.id, 'Сколько?')
#             bot.register_next_step_handler(message, lambda m: db.add_row(m, 'Развлечения'))
#         elif message.text == '📊 Отчет':
#             report = db.draw_report(message.from_user.id)
#             for i in report:
#                 bot.send_message(message.chat.id, str(i[0]) + ': ' + str(i[1]))

# def remind():
#     bot.send_message(message.chat.id, 'hi')
# schedule.every().hour.do(remind())
# while True:
#     schedule.run_pending()
#     time.sleep(1)
