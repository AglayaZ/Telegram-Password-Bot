from dotenv import load_dotenv
from zxcvbn import zxcvbn
from xkcdpass import xkcd_password as xp 
import os
import telebot 
import random
import string
import hashlib
import requests
load_dotenv()
bot_token = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(bot_token)
user_state = {}
words = xp.generate_wordlist(wordfile=xp.locate_wordfile(), min_length=4, max_length=8)

@bot.message_handler(commands=['start'])
def welcomemessage(message):
    bot.reply_to(message, "Hello, this bot can generate a password(random or memorable) or check he stregth of your pastswords. Choose /check or /generaterandom or /generatememorable to continue.")

@bot.message_handler(commands=['generaterandom'])
def ask_length(message):
    user_state[message.chat.id] = 'asking_length'
    bot.reply_to(message, "Enter the length of the password you want to generate.")

@bot.message_handler(commands=['generatememorable'])
def ask_words(message):
    user_state[message.chat.id] = 'asking_wordcount'
    bot.reply_to(message, "Enter the number of words in the password you want to generate.")

@bot.message_handler(commands=['check'])
def ask_password(message):
    user_state[message.chat.id] = 'asking_password'
    bot.reply_to(message, "Enter the password you want to check.")

@bot.message_handler(func=lambda message: True)
def reply(message):
    chat_id = message.chat.id
    state = user_state.get(chat_id)
    if state == "asking_length":
        generaterandom(message)
        user_state[chat_id] = None
    elif state == "asking_wordcount":
        generatememorable(message)
        user_state[chat_id] = None
    elif state == "asking_password":
        check(message)
        user_state[chat_id] = None
    else:
        bot.reply_to(message, "try again")

def generaterandom(message):
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

def generatememorable(message):
    try:
        length = int(message.text)
    except ValueError:
        bot.reply_to(message, "This is not a number, try agin")
        return
    if length > 8 or length < 4:
        bot.reply_to(message, "Please enter a number between 4 and 8")
        return
    
    password = xp.generate_xkcdpassword(words, numwords=4, delimiter='-')
    bot.reply_to(message, f"Here's your password:\n`{password}`", parse_mode="Markdown")

def check(message):
    password = message.text
    result = zxcvbn(password)
    hashed = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = hashed[:5]
    suffix = hashed[5:]
    response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
    found = 0
    for line in response.text.splitlines():
        hashedsuffix, count = line.split(":")
        if hashedsuffix == suffix:
           found = count 
           break
    if result["score"] == 0:
        strength = "very weak"
    elif result["score"] == 1:
        strength = "weak"
    elif result["score"] == 2:
        strength = "fair"
    elif result["score"] == 3:
        strength = "strong"
    else:
        strength = "very strong"
    
    cracktime = result["crack_times_display"]["offline_fast_hashing_1e10_per_second"]
    bot.reply_to(message, f"Your password is {strength} with crack time {cracktime}")
   
    if found != 0:
        bot.reply_to(message, f"This password has appeared in {found} known data breaches. Avoid using it.")
    else:
        bot.reply_to(message, "This password did not appear in known data breaches")

bot.infinity_polling() 