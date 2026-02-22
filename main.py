import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.filters.text import Text

# =======================
# 1️⃣ Токен бота
# =======================
TOKEN = os.getenv("BOT_TOKEN")  # или просто "твой_токен_бота"
if not TOKEN:
    raise ValueError("Токен бота не задан!")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# =======================
# 2️⃣ Клавиатура
# =======================
keyboard_main = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="Создать сделку 💵")],
        [types.KeyboardButton(text="Добавить карту 💳")]
    ],
    resize_keyboard=True
)

confirm_price_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="Подтвердить цену")]
    ],
    resize_keyboard=True
)

# =======================
# 3️⃣ Состояния для сделки
# =======================
users_in_deal = {}  # {user_id: {"stage": "waiting_for_seller", "seller_id": None}}

# =======================
# 4️⃣ Хендлеры
# =======================
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Выберите действие:",
        reply_markup=keyboard_main
    )

@dp.message(Text("Создать сделку 💵"))
async def create_deal(message: types.Message):
    users_in_deal[message.from_user.id] = {"stage": "waiting_for_seller", "seller_id": None}
    await message.answer("Напиши юзернейм продавца:")

@dp.message(lambda message: users_in_deal.get(message.from_user.id, {}).get("stage") == "waiting_for_seller")
async def add_seller(message: types.Message):
    users_in_deal[message.from_user.id]["seller_id"] = message.text
    users_in_deal[message.from_user.id]["stage"] = "waiting_for_item"
    await message.answer(f"Продавец @{message.text} добавлен. Теперь продавец должен написать, что он хочет продать.")

@dp.message(lambda message: users_in_deal.get(message.from_user.id, {}).get("stage") == "waiting_for_item")
async def wait_item(message: types.Message):
    users_in_deal[message.from_user.id]["item"] = message.text
    users_in_deal[message.from_user.id]["stage"] = "waiting_for_confirmation"
    await message.answer(f"Товар '{message.text}' добавлен.", reply_markup=confirm_price_keyboard)

@dp.message(Text("Подтвердить цену"))
async def confirm_price(message: types.Message):
    deal = users_in_deal.get(message.from_user.id)
    if deal and deal.get("stage") == "waiting_for_confirmation":
        deal["stage"] = "done"
        await message.answer(f"Сделка с @{deal['seller_id']} подтверждена! ✅", reply_markup=keyboard_main)
    else:
        await message.answer("Нет активной сделки для подтверждения.", reply_markup=keyboard_main)

@dp.message(Text("Добавить карту 💳"))
async def add_card(message: types.Message):
    await message.answer("Введите данные карты (только тест):")

# =======================
# 5️⃣ Асинхронный запуск
# =======================
async def main():
    print("Бот запускается...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
