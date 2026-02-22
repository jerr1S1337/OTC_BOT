from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import asyncio

API_TOKEN = "8033758820:AAGNh1NOXcV8j2tPoFEVBARSiU98cAvgtdE"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Клавиатуры
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Создать сделку 💵")],
        [KeyboardButton(text="Добавить карту 💳")]
    ],
    resize_keyboard=True
)

confirm_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Подтвердить цену")],
        [KeyboardButton(text="Отмена")]
    ],
    resize_keyboard=True
)

# Старт
@dp.message(lambda message: message.text == "/start")
async def start(message: types.Message):
    await message.answer("Привет! Выбери действие:", reply_markup=main_kb)

# Создать сделку
@dp.message(lambda message: message.text == "Создать сделку 💵")
async def create_deal(message: types.Message):
    await message.answer("Введите сумму сделки:", reply_markup=confirm_kb)

# Добавить карту
@dp.message(lambda message: message.text == "Добавить карту 💳")
async def add_card(message: types.Message):
    await message.answer("Введите данные карты:", reply_markup=main_kb)

# Подтвердить цену
@dp.message(lambda message: message.text == "Подтвердить цену")
async def confirm_price(message: types.Message):
    await message.answer("Цена подтверждена!", reply_markup=main_kb)

# Отмена
@dp.message(lambda message: message.text == "Отмена")
async def cancel(message: types.Message):
    await message.answer("Действие отменено.", reply_markup=main_kb)

async def main():
    try:
        print("Бот запущен...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
