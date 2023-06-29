from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

new_user = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text='Давай!')]
    ]
)