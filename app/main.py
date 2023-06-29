import asyncio
import logging

from app import bot, dp
from app.routers import main_router, registration_router, notification_router

logging.basicConfig(level=logging.INFO)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    dp.include_router(main_router.router)
    dp.include_router(registration_router.router)
    dp.include_router(notification_router.router)
    asyncio.get_event_loop().run_until_complete(main())
