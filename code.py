from dotenv import load_dotenv
import os
import telebot 
import random
import string
load_dotenv()
bot_token = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(bot_token)
user_state = {}

@bot.message_handler(commands=['start'])
def welcomemessage(message):
    bot.reply_to(message, "Hello, this bot can generate or check the stregth of your passwords. Choose /check or /generate to continue.")

@bot.message_handler(commands=['generate'])
def ask_length(message):
    user_state[message.chat.id] = 'asking_length'
    bot.reply_to(message, "Enter the length of the password you want to generate.")

@bot.message_handler(commands=['check'])
def ask_password(message):
    user_state[message.chat.id] = 'asking_password'
    bot.reply_to(message, "Enter the password you want to check.")

@bot.message_handler(func=lambda message: True)
def reply(message):
    chat_id = message.chat.id
    state = user_state.get(chat_id)
    if state == "asking_length":
        generate(message)
        user_state[chat_id] = None
    elif state == "asking_password":
        check(message)
        user_state[chat_id] = None
    else:
        bot.reply_to(message, "try again")

def generate(message):
    bot.reply_to(message, "In process.")

def check(message):
    bot.reply_to(message, "In process...")

bot.infinity_polling() 