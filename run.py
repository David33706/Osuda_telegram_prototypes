import asyncio
from aiogram import Dispatcher
from aiogram import Bot
from dotenv import load_dotenv
import os

from handlers.handler import router
from handlers.mood_handler import mood_router

load_dotenv()
bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher()


async def main():
    dp.include_router(router)
    dp.include_router(mood_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:

        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exited Osuda AI Bot")
