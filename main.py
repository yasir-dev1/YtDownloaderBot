#!./venv/bin/python3
import os
import re
import telebot
import  time
import dotenv
from pytube import YouTube

dotenv.load_dotenv()


BOT_TOKEN = os.getenv('TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)
url_regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$"

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Please Enter YouTube Video URL to Download")

@bot.message_handler(func=lambda msg: True)
def Download(message) :
    if re.match(url_regex, message.text):
        try:
            video_url = message.text
            yt = YouTube(video_url)
            stream = yt.streams.filter(progressive=True,).order_by('resolution').desc().first()
            video_path = str(round(time.time() * 1000))+".mp4"
            stream.download(filename=video_path)
            video = open(video_path,'rb+')
            bot.send_video(chat_id=message.chat.id, video=video)
            video.close()
            os.remove(video_path)
        except:
            bot.reply_to(message, "Bazı Sıkıntılar var lütfen tekrar denyeiyiniz eğer 2. kere bu  uyarıyı görüyorsan birdaha bu videoyu deneme bir sorun var demeki")
            video.close()
            os.remove(video_path)
    else:
        bot.reply_to(message, "Please enter a valid YouTube video URL.")

bot.infinity_polling()
