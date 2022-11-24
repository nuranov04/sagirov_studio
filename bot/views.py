from telebot import TeleBot

import re

from datetime import datetime
from time import sleep

from bot.models import UserBid
from con_file import TOKEN
from utils.helper import user

bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def get_start_message(message):
    msg = bot.send_message(chat_id=message.from_user.id,
                           text=f"Hello, {message.from_user.first_name}!\nSend me your name)")
    bot.register_next_step_handler(msg, get_name)


def get_name(message):
    user.name = message.text
    msg = bot.send_message(chat_id=message.from_user.id,
                           text='send me your surname')
    bot.register_next_step_handler(msg, get_surname)


def get_surname(message):
    user.surname = message.text
    msg = bot.send_message(chat_id=message.from_user.id,
                           text='send me your email')
    bot.register_next_step_handler(msg, get_email)


def get_email(message):
    if message.text.endswith("@gmail.com"):
        user.email = message.text
        msg = bot.send_message(chat_id=message.from_user.id, text='send me your phone number')
        bot.register_next_step_handler(msg, get_phone_number)
    else:
        msg = bot.send_message(chat_id=message.from_user.id,
                               text="send me correct email, please)")
        bot.register_next_step_handler(msg, get_email)


def get_phone_number(message):
    user.phone_number = message.text
    msg = bot.send_message(chat_id=message.from_user.id,
                           text="send me you date of birth. Format DD.MM.YYYY")
    bot.register_next_step_handler(msg, get_date_of_birth)


def get_date_of_birth(message):
    try:
        user.date_of_birth = message.text
        UserBid.objects.create(name=user.name,
                               surname=user.surname,
                               email=user.email,
                               phone_number=user.phone_number,
                               date_of_birth=datetime.strptime(user.date_of_birth, "%d.%m.%Y"))
        bot.send_message(chat_id=message.from_user.id, text="Done! Send /start for send again")
    except ValueError:
        msg = bot.send_message(chat_id=message.from_user.id, text="Not correct format. Try again! Format DD.MM.YYYY")
        bot.register_next_step_handler(msg, get_date_of_birth)


@bot.message_handler()
def main_handler(message):
    bot.send_message(chat_id=message.from_user.id, text="send me /start command")
