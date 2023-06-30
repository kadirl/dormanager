import types

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardBuilder

def reply_to_offer():
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(
        text="Интересно",
        callback_data="interested")
    )

    return builder.as_markup()

def get_cancel():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Отменить')]
        ]
    )
