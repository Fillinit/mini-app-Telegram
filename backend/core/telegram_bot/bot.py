import telebot
import requests
import os
from telebot import types
from invoices import create_invoice_payload
from decouple import config

# Токен Telegram-бота
BOT_TOKEN = config("BOT_TOKEN")
API_BASE = config("API_BASE")
token_url = config("TOKEN_URL")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")


# Старт
@bot.message_handler(commands=["start"])
def send_welcome(message):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Открыть меню", web_app=types.WebAppInfo(url="http://127.0.0.1:3000/")))
    bot.send_message(
        message.chat.id,
        "Привет 👋\nЯ бот для заказа еды.\nНажми кнопку ниже, чтобы открыть меню:",
        reply_markup=kb
    )


# Обработка успешной оплаты
@bot.message_handler(content_types=["successful_payment"])
def successful_payment(message):
    payload = message.successful_payment.invoice_payload
    order_id = payload.split(":")[-1]

    try:
        requests.post(f"{API_BASE}/orders/{order_id}/mark_paid/")
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Ошибка при подтверждении оплаты: {e}")
        return

    bot.send_message(message.chat.id, f"✅ Оплата за заказ №{order_id} прошла успешно!")


# Создание счета (инвойса) для оплаты
def send_invoice(chat_id: int, order_id: int, title: str, description: str, amount: int):
    """
    Отправляет пользователю инвойс (Telegram Payments).
    amount указывается в копейках (например, 10000 = 100 руб.)
    """
    payload = create_invoice_payload(order_id)
    prices = [types.LabeledPrice(label=title, amount=amount)]

    bot.send_invoice(
        chat_id,
        title=title,
        description=description,
        provider_token=os.getenv("PAYMENT_PROVIDER_TOKEN"),
        currency="RUB",
        prices=prices,
        start_parameter=f"order-{order_id}",
        invoice_payload=payload
    )


# Запуск long polling
if __name__ == "__main__":
    print("🤖 Бот запущен (long polling)...")
    bot.infinity_polling(skip_pending=True)
