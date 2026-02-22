import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Получаем токен через переменную окружения
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- Клавиатуры ---
keyboard_main = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_main.add(KeyboardButton("Создать сделку"))
keyboard_main.add(KeyboardButton("Добавить или изменить кошелек"))

keyboard_wallet = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_wallet.add(KeyboardButton("Кошелек телеграмм"))
keyboard_wallet.add(KeyboardButton("Карта VISA"))

# --- Обработчики ---
@dp.message(commands=["start"])
async def start(message: types.Message):
    await message.reply(
        "Добро пожаловать в надежный OTC гарант-бот!\n\n"
        "В нашем боте:\n"
        "- Удобное управление сделкой\n"
        "- Добавление кошельков или карт\n\n"
        "Выберите нужный раздел ниже:",
        reply_markup=keyboard_main
    )

@dp.message(lambda message: message.text == "Добавить или изменить кошелек")
async def add_wallet(message: types.Message):
    await message.reply("Выберите способ получения:", reply_markup=keyboard_wallet)

@dp.message(lambda message: message.text in ["Кошелек телеграмм", "Карта VISA"])
async def wallet_input(message: types.Message):
    if message.text == "Кошелек телеграмм":
        await message.reply("Отправьте сюда свой адрес кошелька")
    else:
        await message.reply("Введите номер карты")
    await message.reply(f"{message.text} успешно добавлен ✅", reply_markup=keyboard_main)

# --- Основной запуск бота ---
async def main():
    try:
        print("Bot started")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
