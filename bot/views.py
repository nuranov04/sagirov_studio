from telebot import TeleBot
from decouple import config

from datetime import datetime
from bot.models import UserBid
from utils.class_redis import r
from utils.helper import user
from utils.fill_in_form import send_user_values

bot = TeleBot(config("TOKEN"))


@bot.message_handler(commands=['start'])
def get_start_message(message):
    if r.get_status_code():
        msg = bot.send_message(chat_id=message.from_user.id,
                               text=f"Hello, {message.from_user.first_name}!\nSend me your name)")
        bot.register_next_step_handler(msg, get_name)
    else:
        bot.reply_to(message, "sorry try after 10 minutes")


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
    if message.text[1:].isdigit():
        user.phone_number = message.text
        msg = bot.send_message(chat_id=message.from_user.id,
                               text="send me you date of birth. Format DD.MM.YYYY")
        bot.register_next_step_handler(msg, get_date_of_birth)
    else:
        msg = bot.reply_to(message, text="Not correct phone number")
        bot.register_next_step_handler(msg, get_phone_number)


def get_date_of_birth(message):
    try:
        date_of_birth = datetime.strptime(message.text, "%d.%m.%Y")
        user.date_of_birth = message.text
        UserBid.objects.create(name=user.name,
                               surname=user.surname,
                               email=user.email,
                               phone_number=user.phone_number,
                               date_of_birth=date_of_birth)
        bot.send_message(chat_id=message.from_user.id, text="Successfully! Please, wait :)")
        path = send_user_values(user_id=message.from_user.id, name=user.name, surname=user.surname, email=user.email,
                                phone_number=user.phone_number,
                                date=user.date_of_birth)
        if not isinstance(path, TypeError):
            bot.send_photo(chat_id=message.chat.id, photo=open(path, 'rb'))
        else:
            raise ValueError
    except ValueError:
        msg = bot.send_message(chat_id=message.from_user.id, text="Not correct format. Try again! Format DD.MM.YYYY")
        bot.register_next_step_handler(msg, get_date_of_birth)


@bot.message_handler(func=lambda message: True)
def main_handler(message):
    bot.send_message(chat_id=message.from_user.id, text="send me /start command")
