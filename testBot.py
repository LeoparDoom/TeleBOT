import config
import telebot
import sqlite3
from telebot import types
from distutils.core import setup

Tbot=telebot.TeleBot(config.TOKEN)

#Работа с БД /пока не работает и вряд ли будет:(

@Tbot.message_handler(commands=['bd'])
def bd (message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id (id INTEGER)""")
    connect.commit()

    #Проверка на имеющийся id
    user_id=message.chat.id
    cursor.execute(f"SELECT id FROM login_id WHERE id={user_id}")
    data=cursor.fetchone()
    if data == None:

        users_list = [message.chat.id]
        cursor.execute("INSERT INTO login_id VALUES(?);", users_list)
        connect.commit()
    else:
        Tbot.send_message(message.chat.id, 'Такой пользователь уже сущетвует!')

@Tbot.message_handler(commands=['delete'])
def delete (message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    user_id=message.chat.id
    cursor.execute(f"DELETE FROM login_id WHERE id={user_id}")
    connect.commit()
    Tbot.send_message(message.chat.id, 'Пользователь удалён!')

#Управление

@Tbot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
 #   itembtn1 = types.KeyboardButton('👋Hello')
 #   itembtn2 = types.KeyboardButton('🆔id')
 #   itembtn3 = types.KeyboardButton('❓Ну чё там с блоком?')
    itembtn4 = types.KeyboardButton('ℹ️ Информация')
    markup.add(#itembtn1, itembtn2, itembtn3, 
            itembtn4)
    Tbot.send_message(message.chat.id, "Выберите из меню:", reply_markup=markup)

@Tbot.message_handler(content_types=['text'])
def bot_message(message):
    if message.text == '👋Hello':
        mess = f'Привет, <b>{message.from_user.first_name}</b>'
        Tbot.send_message(message.chat.id, mess,parse_mode='html')
    elif message.text == '🆔id':
        Tbot.send_message(message.chat.id, f"Твой ID: {message.from_user.id}" ,parse_mode='html')
    elif message.text == '❓Ну чё там с блоком?':
        Tbot.send_message(message.chat.id, f"'Смотри обвязку'" ,parse_mode='html')
    elif message.text == 'ℹ️ Информация':
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        itembtn1 = types.KeyboardButton('📄Прайс-лист')
        itembtn2 = types.KeyboardButton('📆 Наши часы работы')
        itembtn3 = types.KeyboardButton('☎️ Наши контакты')
        itembtn4 = types.KeyboardButton('🏢 Наш адрес')
        back = types.KeyboardButton('Назад')
        markup.add(itembtn1,itembtn2,itembtn4,itembtn3, back)
        Tbot.send_message(message.chat.id, "ℹ️ Информация:", reply_markup=markup)
    elif message.text== '📄Прайс-лист':
        doc = open("Prise.pdf", "rb")
        Tbot.send_message(message.chat.id, f'Прайс на наши услуги:', parse_mode='html')
        Tbot.send_document(message.chat_id, doc)
    elif message.text== '📆 Наши часы работы':
        Tbot.send_message(message.chat.id, f"<b>Пн-Пт</b>:с 10:00 до 20:00 \n<b>Сб-Вс</b>: Выходные" ,parse_mode='html')
    elif message.text== '☎️ Наши контакты':
        Tbot.send_message(message.chat.id, f"<b>Кирилл:</b> 8-9**-***-**-** \n<b>Александр:</b> 8-9**-***-**-**\n<b>Илья:</b> 8-9**-***-**-**" ,parse_mode='html')
    elif message.text== '🏢 Наш адрес':
        Tbot.send_message(message.chat.id, f"г.Иркутск, микрорайон Крылатый, дом 6" ,parse_mode='html')
    elif message.text =='Назад':
        return start(message)

@Tbot.message_handler(commands=['admin']) 
def admin_panel(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Клиенты')
    itembtn2 = types.KeyboardButton('Склад')
    itembtn3 = types.KeyboardButton('Смотри обвязку =)')
    markup.add(itembtn1, itembtn2, itembtn3)
    Tbot.send_message(message.chat.id, "Меню адмна:", reply_markup=markup)

Tbot.polling(non_stop=True)