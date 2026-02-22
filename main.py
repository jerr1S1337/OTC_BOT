import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Берём токен из переменной окружения BOT_TOKEN
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Приветственное сообщение и кнопки
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Основная клавиатура
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("Создать сделку"))
keyboard.add(KeyboardButton("Добавить или изменить кошелек"))

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        "Добро пожаловать в надежный OTC гарант-бот!\n\n"
        "В нашем боте:\n"
        "- Удобное управление сделкой\n"
        "- Добавление кошельков или карт\n\n"
        "Выберите нужный раздел ниже:",
        reply_markup=keyboard
    )

# Обработка нажатий кнопок
@dp.message_handler(lambda message: message.text == "Добавить или изменить кошелек")
async def add_wallet(message: types.Message):
    sub_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    sub_keyboard.add(KeyboardButton("Кошелек телеграмм"))
    sub_keyboard.add(KeyboardButton("Карта VISA"))
    await message.answer("Выберите способ получения:", reply_markup=sub_keyboard)

@dp.message_handler(lambda message: message.text in ["Кошелек телеграмм", "Карта VISA"])
async def wallet_input(message: types.Message):
    if message.text == "Кошелек телеграмм":
        await message.answer("Отправьте сюда свой адрес кошелька")
    else:
        await message.answer("Введите номер карты")
    # После ввода можно добавить обработку для сохранения данных
    # Пока бот просто отправляет сообщение о успешном добавлении
    await message.answer(f"{message.text} успешно добавлен ✅", reply_markup=keyboard)

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
