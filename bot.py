import asyncio

from aiogram import Dispatcher
from app.handlers import router

from app.handlers import *


dp = Dispatcher()

async def main():
    dp.include_routers(router)
    await dp.start_polling(bot)
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("выход")