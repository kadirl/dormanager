import re

from aiogram.filters import BaseFilter
from aiogram.types import Message


class RoomFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        # Integer [1, 999]

        input_string = message.text

        return (
            input_string.isdigit()
            and 1 <= int(input_string) <= 999
        )


class RateFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        # Integer [1, 999]

        input_string = message.text

        return (
            input_string.isdigit()
            and 1 <= int(input_string) <= 5
        )

