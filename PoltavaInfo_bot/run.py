import asyncio
import logging
from aiogram.filters import CommandStart, Command
from aiogram import Bot, Dispatcher
from handlers import router
from aiogram.types import Message
import keyboards as kb

TOKEN="7591772838:AAG4iw4v31dmgE685ynDS1O13PjIzrq0nMU"



bot = Bot(TOKEN)
dp = Dispatcher()




async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)
    try:
       asyncio.run(main())
    except KeyboardInterrupt:
       print('Exit')