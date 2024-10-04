import asyncio
from aiogram import Dispatcher
from handler import router
from config import bot

dp = Dispatcher()

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:

        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exited Osuda AI Bot")
