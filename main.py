import os

import telebot

BOT_TOKEN = os.environ.get('TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Please Enter Youtube Video URL to Downlad")


bot.infinity_polling()