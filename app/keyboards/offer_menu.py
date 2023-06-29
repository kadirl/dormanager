import types

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
def reply_to_offer():
    builder = InlineKeyboardButton()

    builder.add(types.InlineKeyboardButton(
        text="{ACCEPT}",
        callback_data="accept")
    )
    builder.add(types.InlineKeyboardButton(
        text="{COUNTER OFFER}",
        callback_data="counter_offer")
    )
    builder.add(types.InlineKeyboardButton(
        text="{DECLINE}",
        callback_data="decline")
    )

    builder.adjust(3)

    return builder.as_markup()
