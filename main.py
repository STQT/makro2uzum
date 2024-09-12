import os
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.ERROR,  # Установите нужный уровень логирования: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),  # Логирование в файл
        logging.StreamHandler()  # Логирование в консоль
    ]
)

logger = logging.getLogger(__name__)

# Замените на свой токен бота
API_TOKEN = os.getenv("BOT_TOKEN")

# Путь к папке, куда будут сохраняться изображения
SAVE_PATH = os.getenv("SAVE_PATH")

# Идентификатор канала, который бот будет прослушивать (начинается с -100)
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.channel_post_handler(content_types=[ContentType.DOCUMENT], chat_id=CHANNEL_ID)
async def save_photo(message: types.Message):
    try:
        file_name = message.document.file_name
        file_info = await bot.get_file(message.document.file_id)
        save_path = os.path.join(SAVE_PATH, file_name)
        await bot.download_file(file_info.file_path, save_path)
    except Exception as e:
        await bot.send_message(CHANNEL_ID, f"Ошибка отправки файла: {file_name}\nОшибка:{e}")


@dp.message_handler()
async def echo(message):
    await message.answer("Бот работает")


# Запуск бота
if __name__ == '__main__':
    # Создаем папку, если ее нет
    os.makedirs(SAVE_PATH, exist_ok=True)
    executor.start_polling(dp, skip_updates=True)
