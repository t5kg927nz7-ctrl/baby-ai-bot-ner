import os
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from openai import AsyncOpenAI

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👶 Запитати AI")],
        [KeyboardButton(text="🌡 Температура"), KeyboardButton(text="💉 Вакцинація")],
        [KeyboardButton(text="💤 Сон"), KeyboardButton(text="🍎 Харчування")],
    ],
    resize_keyboard=True
)

SYSTEM_PROMPT = """
Ти AI-помічник для батьків дітей від 0 до 3 років.

Правила:
- Не ставиш діагнози.
- Не призначаєш лікування.
- Не замінюєш лікаря.
- Пояснюєш інформацію зрозумілою українською мовою.
- При небезпечних симптомах рекомендуєш звернутися до лікаря.
"""

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Вітаю 👋\nЯ AI-помічник для батьків дітей 0–3 років.",
        reply_markup=keyboard
    )

@dp.message(F.text == "🌡 Температура")
async def temp(message: Message):
    await message.answer(
        "Напишіть вік дитини та температуру, і я поясню загальну інформацію."
    )

@dp.message(F.text == "💉 Вакцинація")
async def vaccine(message: Message):
    await message.answer(
        "Напишіть вік дитини, і я розповім про загальні рекомендації щодо вакцинації."
    )

@dp.message(F.text == "💤 Сон")
async def sleep(message: Message):
    await message.answer(
        "Опишіть проблему зі сном дитини."
    )

@dp.message(F.text == "🍎 Харчування")
async def food(message: Message):
    await message.answer(
        "Напишіть вік дитини та ваше питання щодо харчування."
    )

@dp.message()
async def ai_chat(message: Message):
    try:
        response = await client.responses.create(
            model="gpt-5-mini",
            input=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": message.text
                }
            ]
        )

        answer = response.output_text

        await message.answer(answer)

    except Exception as e:
        await message.answer(
            "Сталася помилка. Спробуйте пізніше."
        )
        print(e)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())