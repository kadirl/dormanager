import re

from aiogram.filters import BaseFilter
from aiogram.types import Message

from datetime import datetime


class DateFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        try:
            date = datetime.strptime(message.text, "%d.%m.%y")
            return True
        except ValueError:
            return False

