from time import sleep

import telebot
from telebot import types
import sqlite3


API_TOKEN = "7945048191:AAGUxi1LzJVQbC4s9JnaACUrGHp8mUSza7o"
bot = telebot.TeleBot(API_TOKEN)

id = 0


#@bot.message_handler(commands=['start'])
#def send_welcome(message):
#    # Отправка приветственного сообщения
#    msg = "Добро пожаловать! Выберите опцию:"
#    buttons = [
#        types.InlineKeyboardButton("✅ Статистика сайта ✅", callback_data="button1"),
#        types.InlineKeyboardButton("ℹ Информация о пользователе ℹ", callback_data="button2"),
#        types.InlineKeyboardButton("❌ Бан пользователя ❌", callback_data="button3"),
#        types.InlineKeyboardButton("☠ Drop table nahui ☠", callback_data="button4"),
#    ]
#    reply_markup = types.InlineKeyboardMarkup(row_width=2)
#    for button in buttons:
#        reply_markup.add(button)
#    id = message.chat.id
#    print(id)
#    bot.send_message(message.chat.id, msg, reply_markup=reply_markup)
#
#
##@bot.callback_query_handler(lambda c: c.data == 'button1')
##def send_button1(callback_query):
##    user_id = callback_query.from_user.id
##    conn = sqlite3.connect('..\\scratch_app.db', check_same_thread=False)
##    cursor = conn.cursor()
##    # Выполнение запроса для получения всех строк из таблицы users
##    query = "SELECT login, email FROM users"
##    cursor.execute(query)
##
##    # Вывод результатов запроса
##    results = cursor.fetchall()
##    message = f"Список всех пользователей: \n"
##    for result in results:
##        message += f"Логин - {result[0]} | Почта - {result[1]} \n"
##
##   # Отправка сообщения пользователю
##   bot.send_message(user_id, message)
#from typing import Annotated
#
#from sqlalchemy.ext.asyncio import AsyncSession
#from sqlalchemy import insert, select, update, and_
#from starlette.templating import _TemplateResponse
#from fastapi import Depends
#from app.backend.db_depends import get_db
#from app.models.scratch import User, Comment
#
#@bot.callback_query_handler(lambda c: c.data == 'button1')
#def send_button1(callback_query):
#    user_id = callback_query.from_user.id
#    # Выполнение запроса для получения всех строк из таблицы users
#    results = await db.scalars(select(User).where(User.id > 0))
#
#    # Вывод результатов запроса
#    message = f"Список всех пользователей: \n"
#    for result in results:
#        message += f"Логин - {result[0]} | Почта - {result[1]} \n"
#   # Отправка сообщения пользователю
#   bot.send_message(user_id, message)
#
## Функция для обработки нажатия кнопки 2
#@bot.callback_query_handler(lambda c: c.data == 'button2')
#def send_button2(callback_query):
#    user_id = callback_query.from_user.id
#    message = f"Напишите логин пользователя для просмотра более подробной информации"
#    bot.send_message(user_id, message)
#    bot.register_next_step_handler_by_chat_id(user_id, get_login_response)
#
#
#def get_login_response(message):
#    user_id = message.from_user.id
#    login = message.text.strip()
#
#    if login:
#        try:
#            # Подключение к базе данных
#            conn = sqlite3.connect('..\\scratch_app.db')  # Замените на вашу базу данных
#            cursor = conn.cursor()
#
#            # Выполнение запроса к базе данных
#            cursor.execute("SELECT * FROM users WHERE login = ?", (login,))
#            user_data = cursor.fetchone()
#
#            if user_data:
#                # Формируем сообщение с данными пользователя
#                user_info = (f"Информация о пользователе:\n"
#                             f" id: {user_data[0]} \n"
#                             f" login: {user_data[1]} \n"
#                             f" email: {user_data[3]} \n"
#                             f" partner: {user_data[4]} \n"
#                             f" user time: {user_data[5]} \n"
#                             f" partner time: {user_data[6]} \n"
#                             f" user sex: {user_data[8]} \n"
#                             f" partner sex: {user_data[9]} \n")
#                bot.send_message(user_id, user_info)
#            else:
#                bot.send_message(user_id, "Пользователь с таким логином не найден.")
#
#            # Закрываем соединение с базой данных
#            conn.close()
#        except sqlite3.Error as e:
#            bot.send_message(user_id, f"Ошибка при обращении к базе данных: {e}")
#    else:
#        bot.send_message(user_id, "Пожалуйста, введите логин корректно.")
#        bot.register_next_step_handler(message, get_login_response)
#
#
## Функция для обработки нажатия кнопки 3
#@bot.callback_query_handler(lambda c: c.data == 'button3')
#def send_button2(callback_query):
#    user_id = callback_query.from_user.id
#    message = f"Напишите логин пользователя для бана"
#    bot.send_message(user_id, message)
#    bot.register_next_step_handler_by_chat_id(user_id, get_login_banned)
#
#
#def get_login_banned(message):
#    user_id = message.from_user.id
#    login = message.text.strip()
#
#    if login:
#        try:
#            # Подключение к базе данных
#            conn = sqlite3.connect('..\\scratch_app.db')
#            cursor = conn.cursor()
#
#            # Выполнение запроса к базе данных
#            cursor.execute("SELECT * FROM users WHERE login = ?", (login,))
#            user_data = cursor.fetchone()
#
#            if user_data:
#                # Формируем сообщение с данными пользователя
#                user_info = f"Пользователь {login} забанен"
#                cursor.execute("DELETE FROM users WHERE login = ?", (login,))
#                conn.commit()
#                bot.send_message(user_id, user_info)
#            else:
#                bot.send_message(user_id, "Пользователь с таким логином не найден.")
#
#            # Закрываем соединение с базой данных
#            conn.close()
#        except sqlite3.Error as e:
#            bot.send_message(user_id, f"Ошибка при обращении к базе данных: {e}")
#    else:
#        bot.send_message(user_id, "Пожалуйста, введите логин корректно.")
#        bot.register_next_step_handler(message, get_login_response)
#
#
## Функция для обработки нажатия кнопки 4
#@bot.callback_query_handler(lambda c: c.data == 'button4')
#def send_button2(callback_query):
#    user_id = callback_query.from_user.id
#    message = f"Ебанулся? -- Y | N"
#    bot.send_message(user_id, message)
#    bot.register_next_step_handler_by_chat_id(user_id, drop_da_table)
#
#
#def drop_da_table(message):
#    user_id = message.from_user.id
#    if message.text == 'Y':
#        try:
#            # Подключение к базе данных
#            conn = sqlite3.connect('..\\scratch_app.db')
#            cursor = conn.cursor()
#
#            # Выполнение запроса к базе данных
#            user_data = cursor.execute("SELECT login FROM users").fetchall()
#            print(user_data)
#            if user_data:
#                for user in user_data:
#                    cursor.execute("DELETE FROM users WHERE login = ?", (user[0],))
#
#                # Формируем сообщение с данными пользователя
#                user_info = f"Ну молодец, что сказать..."
#                conn.commit()
#                bot.send_message(user_id, user_info)
#            else:
#                bot.send_message(user_id, "База данных пуста")
#
#            # Закрываем соединение с базой данных
#            conn.close()
#        except sqlite3.Error as e:
#            bot.send_message(user_id, f"Ошибка при обращении к базе данных: {e}")
#    else:
#        bot.send_message(user_id, 'Ну слава богу...')


#  Отправка сообщения при регистрации пользователя
#  @bot.send_message(content_types=['text'])
def send(message):
    chat_id = 884747686
    bot.send_message(chat_id, message)


# Регистрация функции
if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as _ex:
            print(f'Блядская ошибка {_ex}')
            sleep(6)
