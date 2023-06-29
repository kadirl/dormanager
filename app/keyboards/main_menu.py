from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton

def get_new_user():
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text='Давай!')]
        ]
    )

def get_registered_user():
    builder = ReplyKeyboardBuilder()

    builder.button(text='{FEATURE 1}')
    builder.button(text='{FEATURE 2}')
    builder.button(text='{FEATURE 3}')
    builder.button(text='{FEATURE 4}')
    builder.button(text='{FEATURE 5}')
    builder.button(text='{FEATURE 6}')
    builder.button(text='{SETTINGS}')

    builder.adjust(2)

    return builder.as_markup()
