import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from yt_dlp import YoutubeDL
import os
API_TOKEN = os.getenv("API_TOKEN")

# Токен твоего бота

# Правильная инициализация бота и диспетчера
bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Папка для временного хранения
SAVE_DIR = "downloads"
os.makedirs(SAVE_DIR, exist_ok=True)
def download_mp3(url: str) -> str:
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(SAVE_DIR, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = os.path.join(SAVE_DIR, f"{info['title']}.mp3")
        return filename

# Команда /start
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет! Отправь мне ссылку на YouTube, и я скачаю MP3.")

# Обработка ссылок
@dp.message(F.text.contains("youtube.com") | F.text.contains("youtu.be"))
async def handle_youtube_link(message: Message):
    url = message.text.strip()
    wait_msg = await message.answer("⏳ Скачиваю...")

    try:
        mp3_path = download_mp3(url)
        await message.answer_document(FSInputFile(mp3_path))
        os.remove(mp3_path)
        await wait_msg.delete()
    except Exception as e:
        await wait_msg.edit_text(f"⚠️ Ошибка: {e}")

# Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
