import os
import re
import telebot
import time
from dotenv import load_dotenv
from pytube import YouTube
from telebot import types

load_dotenv()

BOT_TOKEN = os.getenv('TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)
url_regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$"

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Please enter a YouTube video URL to download.")

@bot.message_handler(func=lambda msg: re.match(url_regex, msg.text))
def ask_format(message):
    video_url = message.text
    markup = types.InlineKeyboardMarkup()
    video_button = types.InlineKeyboardButton("Video", callback_data=f"video|{video_url}")
    audio_button = types.InlineKeyboardButton("Audio", callback_data=f"audio|{video_url}")
    markup.add(video_button, audio_button)
    bot.reply_to(message, "Please choose the format you want to download:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def download(call):
    action, video_url = call.data.split('|')
    bot.send_message(call.message.chat.id, "Processing your request, please wait...")
    try:
        yt = YouTube(video_url)
        video_path = str(round(time.time() * 1000))
        if action == "video":
            stream = yt.streams.filter(progressive=True).order_by('resolution').desc().first()
            video_path += ".mp4"
            stream.download(filename=video_path)
            with open(video_path, 'rb') as video:
                bot.send_video(chat_id=call.message.chat.id, video=video)
            os.remove(video_path)
        elif action == "audio":
            stream = yt.streams.filter(only_audio=True).first()
            video_path = video_path + ".mp3"
            stream.download(filename=video_path)
            with open(video_path, 'rb') as audio:
                bot.send_audio(chat_id=call.message.chat.id, audio=audio)
            os.remove(video_path)
    except Exception as e:
        bot.reply_to(call.message, "An error occurred. Please try again. If you see this message again, please avoid trying to download this video. Error: " + str(e))
        if os.path.exists(video_path):
            os.remove(video_path)
@bot.message_handler(func=lambda msg: True)
def invalid_url(message):
    bot.reply_to(message, "Please enter a valid YouTube video URL.")

bot.infinity_polling()
