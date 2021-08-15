from bot__command import Add
from bot__command import Start
from bot__command import Weather
from bot__command import WeatherPro
from bot__command import Command
from telebot import TeleBot


class TelegramBot(TeleBot):
    def __init__(self, token):
        super().__init__(token=token)
        self.commands = {}
        self.register_command(Start.Start())
        self.register_command(Add.Add())
        self.register_command(Weather.Weather())
        self.register_command(WeatherPro.WeatherPro())

    def register_command(self, command: Command):
        self.commands[command.get_name()] = command
    
    def other(self, send_func, message):
        print('%s (%s): %s' % (message.chat.first_name, message.chat.username, message.text))
        send_func(
                         "Это явно не моя команда( \n " + str(message.chat.first_name) + " введи start")