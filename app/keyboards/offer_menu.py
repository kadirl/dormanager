import types

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardBuilder

def reply_to_offer():
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(
        text="{ACCEPT}",
        callback_data="accept")
    )
    builder.add(InlineKeyboardButton(
        text="{COUNTER OFFER}",
        callback_data="counter_offer")
    )
    builder.add(InlineKeyboardButton(
        text="{DECLINE}",
        callback_data="decline")
    )

    builder.adjust(2)

    return builder.as_markup()
