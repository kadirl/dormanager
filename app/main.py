import asyncio
import logging

from aiogram import Bot

from app import bot, dp
from app.routers import (
    main_router,
    registration_router,
    notification_router,
    offer_router
)

logging.basicConfig(level=logging.INFO)


async def start_bot(bot: Bot):
    await bot.send_message(406340756, 'BOT STARTED')
    await bot.send_message(529158582, 'BOT STARTED')


async def stop_bot(bot: Bot):
    await bot.send_message(406340756, 'BOT STOPED')
    await bot.send_message(529158582, 'BOT STOPED')


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.include_router(main_router.router)
    dp.include_router(registration_router.router)
    dp.include_router(notification_router.router)
    dp.include_router(offer_router.router)
    asyncio.get_event_loop().run_until_complete(main())
