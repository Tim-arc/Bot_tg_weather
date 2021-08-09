from bot__command import Command
import sqlite3

class Start(Command.Command):
    def execute(self, send_func, send_photo, message):
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

        send_func("Добро пожаловать, вам надо будет ввести город через команду "
                  "/add а затем, вы можете ввести команду "
                  "/weather для получения прогноза")

    def get_name(self):
        return "start"
