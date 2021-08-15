from bot__command import Command
import sqlite3
import requests
import yaml

class WeatherPro(Command.Command):
    def execute(self, send_func, send_photo,message):
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
            hum = str(data["main"]["humidity"])
            icon = data["weather"]
            icon = icon[0]['main']
            pressure = str(int(data['main']['pressure'] / 1.333))
            wind = str(data['wind']['speed'])
            visibility = str(data['visibility'])
            sea_level = str(data['main']['sea_level'])
            send_func("Температура в {}: {} C".format(city, temp)  +
                             "\n" + "Ощущается как: " + temp_feel + "C" +
                             "\n" + "Влажность: " + hum + "%" +
                             "\n" + "Давление: " + pressure + " миллиметров ртутного столба" +
                             "\n" + "Скорость ветра: " + wind + " м/с" +
                             "\n" + "Видимость: " + visibility + " м" +
                             "\n" + "Уровень над морем: " + sea_level  + " м")

            if icon == "Clear":
                send_photo(open('./Photos/Sunn.png', 'rb'))
            elif icon == "Rain":
                send_photo(open('./Photos/Rain.png', 'rb'))
            elif icon == "Clouds":
                send_photo(open('./Photos/Cloudy.jpg', 'rb'))

        except BaseException:
            print("Обнаружена ошибка(")
            send_func("По какой-то причине бот обнаружил ошибку, попробуйте снова")

    def get_name(self):
        return "weatherpro"