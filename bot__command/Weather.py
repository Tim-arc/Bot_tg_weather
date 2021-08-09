from bot__command import Command
import sqlite3
import requests
import yaml

class Weather(Command.Command):
    def execute(self, send_func, send_photo, message):
        try:
            print('%s (%s): %s' % (message.chat.first_name, message.chat.username, message.text))
            with open("coonfig.yaml") as file:
                config = yaml.safe_load(file)
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
            send_func("Температура в {}: {} C".format(city, temp)  +
                             "\n" + "Ощущается как: " + temp_feel + "C")
        except BaseException:
            print("Обнаружена ошибка(")
            send_func("По какой-то причине бот обнаружил ошибку, попробуйте снова")

    def get_name(self):
        return "weather"