import os

import youtube_dl
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.types import Message
from aiogram.utils import executor
from pytube import YouTube

from settings import TOKEN

bot = Bot(TOKEN)
dp = Dispatcher(bot)

# DOWNLOAD_FOLDER = "../tmp"
DOWNLOAD_FOLDER = "~/tmp"


@dp.message_handler()
async def command_start(message: Message):
    await message.answer("One moment, please...")
    url = message.text
    try:
        if url.find('https://youtu.be/') == 0 or url.find('https://youtube.com/') == 0:
            video_obj = YouTube(url)
            stream = video_obj.streams.get_highest_resolution()
            file_path = stream.download(DOWNLOAD_FOLDER)

        elif url.find('https://vk.com/') == 0:
            file_path = 'tmp_video.mp4'  # '%(id)s.%(ext)s'
            file_path = file_path.replace('-', '')
            opt = {
                'nooverwrites': True,
                'outtmpl': file_path,
                'format': 'worst',
                # 'progress_hooks': [handle_video],
                'quiet': True  # ,
                # 'postprocessors': [
                #      {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
                #  ]
            }
            with youtube_dl.YoutubeDL(opt) as ydl:
                ydl.download([url])

        with open(file_path, 'rb') as video:
            await message.answer_video(video)

    except Exception:
        await message.answer("Alas, I failed...")

    if os.path.isfile(file_path):
        os.remove(file_path)


executor.start_polling(dp, skip_updates=True)
