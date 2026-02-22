import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import F
import asyncio

# Берём токен из переменной окружения или ставим прямо строкой
TOKEN = os.getenv("BOT_TOKEN")  # убедись, что в Docker установлена переменная BOT_TOKEN
# TOKEN = "ТВОЙ_ТОКЕН"  # если хочешь напрямую

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- Создаём клавиатуру ---
keyboard_main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Кнопка 1")],
        [KeyboardButton(text="Кнопка 2")]
    ],
    resize_keyboard=True
)

# --- Пример хэндлера команды /start ---
@dp.message(Command(commands=["start"]))
async def cmd_start(message: Message):
    await message.answer("Привет! Я работаю на Aiogram 3.x", reply_markup=keyboard_main)

# --- Основная функция запуска ---
async def main():
    try:
        print("Бот запускается...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
