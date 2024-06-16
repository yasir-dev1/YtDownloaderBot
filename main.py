#!./venv/bin/python3
import os
import re
import telebot
import time
from dotenv import load_dotenv
from pytube import YouTube

load_dotenv()

BOT_TOKEN = os.getenv('TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)
url_regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$"

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Please enter a YouTube video URL to download.")

@bot.message_handler(func=lambda msg: True)
def download(message):
    if re.match(url_regex, message.text):
        try:
            video_url = message.text
            yt = YouTube(video_url)
            stream = yt.streams.filter(progressive=True).order_by('resolution').desc().first()
            video_path = str(round(time.time() * 1000)) + ".mp4"
            stream.download(filename=video_path)
            with open(video_path, 'rb') as video:
                bot.send_video(chat_id=message.chat.id, video=video)
            os.remove(video_path)
        except Exception as e:
            bot.reply_to(message, "An error occurred. Please try again. If you see this message again, please avoid trying to download this video. Error: " + str(e))
            if os.path.exists(video_path):
                os.remove(video_path)
    else:
        bot.reply_to(message, "Please enter a valid YouTube video URL.")

bot.infinity_polling()
