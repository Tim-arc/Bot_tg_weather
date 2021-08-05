import json
import telebot
import requests
import yaml
import sqlite3
from sqlite3 import Error

with open("coonfig.yaml") as file:
    config = yaml.safe_load(file)

bot = telebot.TeleBot(config['token'])

@bot.message_handler(commands=['start'])
def start(message):
    print('%s (%s): %s' % (message.chat.first_name, message.chat.username, message.text))
    user_id = str(message.chat.id)
    city = "Moscow"

    connect = sqlite3.connect('server.db')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                            id TEXT,
                            cities TEXT
                        )""")
    connect.commit()

    cursor.execute(f'SELECT id FROM users WHERE id = {user_id}')
    if cursor.fetchone() is None:
        cursor.execute(f'INSERT INTO users VALUES(?, ?);', (user_id, city))
        connect.commit()

    bot.send_message(message.chat.id, "Добро пожаловать, вам надо будет ввести город через команду "
                                      "/add а затем, вы можете ввести команду "
                                      "/weather для получения прогноза")


@bot.message_handler(commands= ['add'])
def add(message):
    try:
        print('%s (%s): %s' % (message.chat.first_name, message.chat.username, message.text))
        user_id = str(message.chat.id)
        arr = str(message.text)
        arr = arr.split()
        city = arr[1]

        connect = sqlite3.connect('server.db')
        cursor = connect.cursor()
        cursor.execute(f'UPDATE users SET cities = (?) WHERE id = (?)', (city, user_id))
        connect.commit()

        for i in cursor.execute('SELECT * FROM users'):
            print(i)

        bot.send_message(message.chat.id, "Город успешно добавлен в список")
    except BaseException :
        print("Обнаружена ошибка(")
        bot.send_message(message.chat.id, "По какой-то причине бот обнаружил ошибку, не забудьте "
                                          "писать город через пробел, после команды")

@bot.message_handler(commands=['weather'])
def weather(message):
    try:
        print('%s (%s): %s' % (message.chat.first_name, message.chat.username, message.text))
        apikey = config["apikey"]
        user_id = str(message.chat.id)


        connect = sqlite3.connect('server.db')
        cursor = connect.cursor()
        cursor.execute(f'SELECT cities FROM users WHERE id = "{user_id}" ')
        city = cursor.fetchall()[0]
        city = city[0]
        connect.commit()

        r = requests.get('http://api.openweathermap.org/data/2.5/weather?q={},canada&APPID={}'.format(city, apikey))
        data = r.json()
        print(data)
        temp = int(data["main"]["temp"] - 273)
        temp_feel = str(int(data["main"]["feels_like"] - 273))
        hum = str(data["main"]["humidity"])
        icon = data["weather"]
        icon = icon[0]['main']
        pressure = str(data['main']['pressure'])
        bot.send_message(message.chat.id, "Температура в {}: {} C".format(city, temp)  +
                         "\n" + "Ощущается как: " + temp_feel + "C" +
                         "\n" + "Влажность: " + hum + "%" +
                         "\n" + "Давление: " + pressure + " миллиметров ртутного столба")
        if icon == "Clear":
            bot.send_photo(message.chat.id, open('./Photos/Sunn.png', 'rb'))
        elif icon == "Rain":
            bot.send_photo(message.chat.id, open('./Photos/Rain.png', 'rb'))
        elif icon == "Clouds":
            bot.send_photo(message.chat.id, open('./Photos/Cloudy.jpg', 'rb'))
    except BaseException:
        print("Обнаружена ошибка(")
        bot.send_message(message.chat.id,  "По какой-то причине бот обнаружил ошибку, попробуйте снова")


bot.polling(none_stop=True, interval=0, timeout=0)