import re

from aiogram.filters import BaseFilter
from aiogram.types import Message


class FirstLastNameFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        # Single word
        # Cyrillic only
        # No numbers
        # No special symbols

        input_string = message.text

        return (
                len(input_string.split()) == 1 and
                bool(re.match(r'^[а-яәіңғүұқөһА-ЯӘІҢҒҮҰҚӨҺёЁ]+$', input_string)) and
                not any(char.isdigit() for char in input_string) and
                input_string.isalpha()
        )


class EmailFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        # Regular expression pattern for email validation

        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        # Check if the email matches the pattern
        return bool(re.match(pattern, message.text))