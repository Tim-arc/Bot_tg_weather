from bot__command import Command
import sqlite3

class Add(Command.Command):
    def execute(self, send_func, send_photo, message):
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

            send_func("Город успешно добавлен в список")
        except BaseException:
            print("Обнаружена ошибка(")
            send_func("По какой-то причине бот обнаружил ошибку, не забудьте "
                      "писать город через пробел, после команды")

    def get_name(self):
        return "add"
