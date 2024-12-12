import asyncio
from aiogram import Dispatcher
from aiogram import Bot
from dotenv import load_dotenv
import os

from handler import router

from aiogram.client.session.aiohttp import AiohttpSession

# Setting up proxy
session = AiohttpSession(proxy="http://95.216.36.231:8889/")
load_dotenv()

# Adding proxy to bot
bot = Bot(os.getenv("TOKEN"), session=session)
dp = Dispatcher()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:

        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exited Osuda AI Bot")
