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
    try:
        length = int(message.text)
    except ValueError:
        bot.reply_to(message, "This is not a number, try agin")
        return
    if length > 128 or length < 4:
        bot.reply_to(message, "Please enter a number between 4 and 128")
        return
    
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    bot.reply_to(message, f"Here's your password:\n`{password}`", parse_mode="Markdown")

def check(message):
    bot.reply_to(message, "This function is in process")

bot.infinity_polling() 