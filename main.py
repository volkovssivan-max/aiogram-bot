from os import getenv
import asyncio
import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers.router import router

load_dotenv()
TOKEN = getenv('BOT_TOKEN')

dp = Dispatcher()
dp.include_router(router)

async def main():
    bot = Bot(token=TOKEN)
    
    logging.basicConfig(level=logging.INFO)
    
    print('Start...')
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main())