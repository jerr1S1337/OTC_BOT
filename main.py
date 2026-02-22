from aiogram import Bot, Dispatcher, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command, Text
import asyncio
import os

TOKEN = os.getenv("BOT_TOKEN")  # твой токен в переменных среды
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Главные кнопки
btn_create_deal = KeyboardButton("Создать сделку 💵")
btn_add_card = KeyboardButton("Добавить карту 💳")
keyboard_main = ReplyKeyboardMarkup(
    keyboard=[[btn_create_deal, btn_add_card]],
    resize_keyboard=True
)

# Кнопка подтверждения цены для продавца
btn_confirm_price = KeyboardButton("Подтвердить цену")
keyboard_confirm = ReplyKeyboardMarkup(
    keyboard=[[btn_confirm_price]],
    resize_keyboard=True
)

# Словарь для хранения информации о сделке
deals = {}  # пример: deals[buyer_id] = {"seller": seller_id, "item": None, "price_confirmed": False}

# Шаг 1: Покупатель нажимает "Создать сделку"
@dp.message(Text(text="Создать сделку 💵"))
async def start_deal(message: types.Message):
    await message.answer("Напиши юзернейм продавца (без @):")
    # сохраняем, что этот пользователь сейчас на шаге выбора продавца
    deals[message.from_user.id] = {"step": "waiting_seller"}

# Шаг 2: Получаем юзернейм продавца
@dp.message()
async def handle_seller_username(message: types.Message):
    buyer_id = message.from_user.id
    if buyer_id in deals and deals[buyer_id].get("step") == "waiting_seller":
        seller_username = message.text
        deals[buyer_id]["seller"] = seller_username
        deals[buyer_id]["step"] = "waiting_item"
        await message.answer(f"Продавец @{seller_username} добавлен в сделку.\nТеперь продавец должен написать, что он хочет продать.")

        # уведомление продавцу (если он написал боту)
        # здесь можно использовать find_user_id_by_username или попросить продавца начать чат с ботом
        # пока просто отправляем сообщение покупателю
        await message.answer(f"Продавцу будет показана кнопка 'Подтвердить цену' после описания товара.")

# Шаг 3: Продавец пишет товар и цену
@dp.message(Text(text="Подтвердить цену"))
async def confirm_price(message: types.Message):
    # Ищем сделку, где этот пользователь продавец
    for buyer_id, deal in deals.items():
        if deal.get("seller") == message.from_user.username:
            deal["price_confirmed"] = True
            await message.answer("Цена подтверждена! Сделка завершена.")
            # уведомляем покупателя
            await bot.send_message(buyer_id, f"Продавец @{message.from_user.username} подтвердил цену! Сделка завершена.")
            break

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
