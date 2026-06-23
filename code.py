from dotenv import load_dotenv
import os
import telebot 
import random
import string
load_dotenv()
bot_token = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start'])
def welcomemessage(message):
    bot.reply_to(message, "Hello, enter the length of the password you want to generate.")

@bot.message_handler(func=lambda message: True)
def password(message):
    len = int(message.text)
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(len))
    bot.reply_to(message, password)


bot.infinity_polling() 