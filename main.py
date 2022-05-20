from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import Message
from settings import TOKEN
from pytube import YouTube
import os

bot = Bot(TOKEN)
dp = Dispatcher(bot)

# DOWNLOAD_FOLDER = "../tmp"
DOWNLOAD_FOLDER = "~/tmp"


@dp.message_handler()
async def command_start(message: Message):
    await message.answer("One moment, please...")
    video_obj = YouTube(message.text)
    stream = video_obj.streams.get_highest_resolution()
    file_path = stream.download(DOWNLOAD_FOLDER)
    with open(file_path, 'rb') as video:
        await message.answer_video(video)
    if os.path.isfile(file_path):
        os.remove(file_path)


executor.start_polling(dp, skip_updates=True)
